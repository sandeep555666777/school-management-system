from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Numeric
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, date
import os
from functools import wraps
app = Flask(__name__)

# Production configuration for Railway
if os.environ.get('DATABASE_URL'):
    # Production environment (Railway)
    database_url = os.environ.get('DATABASE_URL')
    if database_url.startswith('postgres://'):
        database_url = database_url.replace('postgres://', 'postgresql://', 1)
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'railway-production-key-2024')
else:
    # Development environment
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///school.db'
    app.config['SECRET_KEY'] = 'dev-secret-key'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# User Models
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # admin, teacher, student, parent
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(20))
    address = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    student_id = db.Column(db.String(20), unique=True, nullable=False)
    class_id = db.Column(db.Integer, db.ForeignKey('school_class.id'))
    date_of_birth = db.Column(db.Date)
    gender = db.Column(db.String(10))
    admission_date = db.Column(db.Date, default=date.today)
    parent_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    user = db.relationship('User', foreign_keys=[user_id], backref='student_profile')
    parent = db.relationship('User', foreign_keys=[parent_id], backref='children')
    school_class = db.relationship('SchoolClass', backref='students')

class Teacher(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    teacher_id = db.Column(db.String(20), unique=True, nullable=False)
    specialization = db.Column(db.String(100))
    qualification = db.Column(db.String(200))
    experience_years = db.Column(db.Integer)
    salary = db.Column(Numeric(10, 2))
    hire_date = db.Column(db.Date, default=date.today)
    date_of_birth = db.Column(db.Date)
    phone = db.Column(db.String(20))
    address = db.Column(db.Text)
    
    user = db.relationship('User', backref='teacher_profile')

class SchoolClass(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    grade_level = db.Column(db.Integer, nullable=False)
    section = db.Column(db.String(10))
    class_teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id'))
    academic_year = db.Column(db.String(10), nullable=False)
    max_students = db.Column(db.Integer, default=30)
    
    class_teacher = db.relationship('Teacher', backref='assigned_classes')

class Subject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    code = db.Column(db.String(20), unique=True, nullable=False)
    description = db.Column(db.Text)
    credits = db.Column(db.Integer, default=1)
    grade_level = db.Column(db.Integer)

class TeacherSubject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id'), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'), nullable=False)
    class_id = db.Column(db.Integer, db.ForeignKey('school_class.id'), nullable=False)
    
    teacher = db.relationship('Teacher', backref='teaching_assignments')
    subject = db.relationship('Subject', backref='teacher_assignments')
    school_class = db.relationship('SchoolClass', backref='subject_assignments')

class Attendance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(10), nullable=False)  # present, absent, late
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'))
    time_in = db.Column(db.Time)
    time_out = db.Column(db.Time)
    remarks = db.Column(db.Text)
    marked_by = db.Column(db.Integer, db.ForeignKey('teacher.id'))
    
    student = db.relationship('Student', backref='attendance_records')
    subject = db.relationship('Subject', backref='attendance_records')
    teacher = db.relationship('Teacher', backref='attendance_marked')

class Grade(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'), nullable=False)
    exam_type = db.Column(db.String(50), nullable=False)  # midterm, final, quiz, assignment
    marks_obtained = db.Column(Numeric(5, 2), nullable=False)
    total_marks = db.Column(Numeric(5, 2), nullable=False)
    grade_letter = db.Column(db.String(5))
    exam_date = db.Column(db.Date, nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id'))
    
    student = db.relationship('Student', backref='grades')
    subject = db.relationship('Subject', backref='grades')
    teacher = db.relationship('Teacher', backref='grades_assigned')

class Fee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    fee_type = db.Column(db.String(50), nullable=False)  # tuition, library, transport, etc.
    amount = db.Column(Numeric(10, 2), nullable=False)
    due_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(20), default='pending')  # pending, paid, overdue
    payment_date = db.Column(db.Date)
    payment_method = db.Column(db.String(50))
    academic_year = db.Column(db.String(10), nullable=False)
    
    student = db.relationship('Student', backref='fees')

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    subtitle = db.Column(db.String(200))
    author = db.Column(db.String(100), nullable=False)
    isbn = db.Column(db.String(20), unique=True)
    category = db.Column(db.String(50))
    total_copies = db.Column(db.Integer, default=1)
    available_copies = db.Column(db.Integer, default=1)
    publication_year = db.Column(db.Integer)
    publisher = db.Column(db.String(100))
    language = db.Column(db.String(50), default='English')

class BookIssue(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    issue_date = db.Column(db.Date, default=date.today)
    due_date = db.Column(db.Date, nullable=False)
    return_date = db.Column(db.Date)
    status = db.Column(db.String(20), default='issued')  # issued, returned, overdue
    fine_amount = db.Column(Numeric(10, 2), default=0)
    
    book = db.relationship('Book', backref='issues')
    student = db.relationship('Student', backref='book_issues')

class Timetable(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    class_id = db.Column(db.Integer, db.ForeignKey('school_class.id'), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'), nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id'), nullable=False)
    day_of_week = db.Column(db.String(10), nullable=False)  # monday, tuesday, etc.
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    room_number = db.Column(db.String(20))
    
    school_class = db.relationship('SchoolClass', backref='timetable')
    subject = db.relationship('Subject', backref='timetable')
    teacher = db.relationship('Teacher', backref='timetable')

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def role_required(role):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated or current_user.role != role:
                flash('Access denied. Insufficient permissions.', 'error')
                return redirect(url_for('login'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator

# Routes
@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password_hash, password) and user.is_active:
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password', 'error')
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    if current_user.role == 'admin':
        # Get statistics for admin dashboard
        total_students = Student.query.count()
        total_teachers = Teacher.query.count()
        total_classes = SchoolClass.query.count()
        total_subjects = Subject.query.count()
        
        # Get recent activities (you can expand this)
        recent_students = db.session.query(Student, User).join(User, Student.user_id == User.id).order_by(Student.id.desc()).limit(5).all()
        
        # Get overdue fees
        overdue_fees = Fee.query.filter(Fee.status == 'overdue').count()
        
        # Get overdue books
        overdue_books = BookIssue.query.filter(BookIssue.status == 'issued', BookIssue.due_date < date.today()).count()
        
        return render_template('admin_dashboard.html', 
                             total_students=total_students,
                             total_teachers=total_teachers,
                             total_classes=total_classes,
                             total_subjects=total_subjects,
                             recent_students=recent_students,
                             overdue_fees=overdue_fees,
                             overdue_books=overdue_books)
    elif current_user.role == 'teacher':
        teacher = Teacher.query.filter_by(user_id=current_user.id).first()
        assignments = TeacherSubject.query.filter_by(teacher_id=teacher.id).all() if teacher else []
        return render_template('teacher_dashboard.html', teacher=teacher, assignments=assignments)
    elif current_user.role == 'student':
        student = Student.query.filter_by(user_id=current_user.id).first()
        recent_grades = Grade.query.filter_by(student_id=student.id).order_by(Grade.id.desc()).limit(5).all() if student else []
        recent_attendance = Attendance.query.filter_by(student_id=student.id).order_by(Attendance.date.desc()).limit(5).all() if student else []
        pending_fees = Fee.query.filter_by(student_id=student.id, status='pending').all() if student else []
        return render_template('student_dashboard.html', 
                             student=student, 
                             recent_grades=recent_grades,
                             recent_attendance=recent_attendance,
                             pending_fees=pending_fees)
    elif current_user.role == 'parent':
        children = Student.query.filter_by(parent_id=current_user.id).all()
        return render_template('parent_dashboard.html', children=children)

# Specific dashboard routes for each role
@app.route('/admin/dashboard')
@login_required
@role_required('admin')
def admin_dashboard():
    return dashboard()

@app.route('/teacher/dashboard')
@login_required
@role_required('teacher')
def teacher_dashboard():
    return dashboard()

@app.route('/student/dashboard')
@login_required
@role_required('student')
def student_dashboard():
    return dashboard()

@app.route('/parent/dashboard')
@login_required
@role_required('parent')
def parent_dashboard():
    return dashboard()

# Admin Routes
@app.route('/admin/students')
@login_required
@role_required('admin')
def admin_students():
    students = db.session.query(Student, User).join(User, Student.user_id == User.id).all()
    classes = SchoolClass.query.all()
    return render_template('admin/students.html', students=students, classes=classes)

@app.route('/admin/students/add', methods=['POST'])
@login_required
@role_required('admin')
def add_student():
    try:
        # Create user account first
        user = User(
            username=request.form['email'],
            email=request.form['email'],
            first_name=request.form['first_name'],
            last_name=request.form['last_name'],
            role='student'
        )
        user.set_password('student123')  # Default password
        db.session.add(user)
        db.session.flush()  # Get the user ID
        
        # Create student record
        student = Student(
            user_id=user.id,
            student_id=request.form['student_id'],
            date_of_birth=datetime.strptime(request.form['date_of_birth'], '%Y-%m-%d').date(),
            gender=request.form['gender'],
            class_id=request.form['class_id'] if request.form['class_id'] else None,
            parent_id=request.form.get('parent_id') if request.form.get('parent_id') else None
        )
        
        # Update user with additional info
        user.phone = request.form.get('phone')
        user.address = request.form.get('address')
        db.session.add(student)
        db.session.commit()
        
        flash('Student added successfully!', 'success')
        return redirect(url_for('admin_students'))
    except Exception as e:
        db.session.rollback()
        flash(f'Error adding student: {str(e)}', 'error')
        return redirect(url_for('admin_students'))

@app.route('/admin/students/<int:student_id>/delete', methods=['POST'])
@login_required
@role_required('admin')
def delete_student(student_id):
    try:
        student = Student.query.get_or_404(student_id)
        user = User.query.get(student.user_id)
        
        # Delete related records first
        Attendance.query.filter_by(student_id=student.id).delete()
        Grade.query.filter_by(student_id=student.id).delete()
        Fee.query.filter_by(student_id=student.id).delete()
        BookIssue.query.filter_by(student_id=student.id).delete()
        
        # Delete student and user
        db.session.delete(student)
        db.session.delete(user)
        db.session.commit()
        
        flash('Student deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting student: {str(e)}', 'error')
    
    return redirect(url_for('admin_students'))

@app.route('/admin/students/<int:student_id>/edit', methods=['POST'])
@login_required
@role_required('admin')
def edit_student(student_id):
    try:
        student = Student.query.get_or_404(student_id)
        user = User.query.get(student.user_id)
        
        # Update user information
        user.first_name = request.form['first_name']
        user.last_name = request.form['last_name']
        user.email = request.form['email']
        user.phone = request.form.get('phone')
        user.address = request.form.get('address')
        
        # Update student information
        student.date_of_birth = datetime.strptime(request.form['date_of_birth'], '%Y-%m-%d').date()
        student.gender = request.form['gender']
        student.class_id = request.form['class_id'] if request.form['class_id'] else None
        student.parent_id = request.form.get('parent_id') if request.form.get('parent_id') else None
        
        db.session.commit()
        flash('Student updated successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error updating student: {str(e)}', 'error')
    
    return redirect(url_for('admin_students'))

@app.route('/admin/teachers')
@login_required
@role_required('admin')
def admin_teachers():
    teachers = db.session.query(Teacher, User).join(User, Teacher.user_id == User.id).all()
    return render_template('admin/teachers.html', teachers=teachers)

@app.route('/admin/teachers/add', methods=['POST'])
@login_required
@role_required('admin')
def add_teacher():
    try:
        # Create user account first
        user = User(
            username=request.form['email'],
            email=request.form['email'],
            first_name=request.form['first_name'],
            last_name=request.form['last_name'],
            role='teacher'
        )
        user.set_password('teacher123')  # Default password
        db.session.add(user)
        db.session.flush()  # Get the user ID
        
        # Create teacher record
        teacher = Teacher(
            user_id=user.id,
            teacher_id=request.form['teacher_id'],
            specialization=request.form['specialization'],
            qualification=request.form['qualification'],
            experience_years=int(request.form['experience_years']),
            salary=float(request.form['salary']) if request.form.get('salary') else None,
            hire_date=datetime.strptime(request.form['hire_date'], '%Y-%m-%d').date(),
            date_of_birth=datetime.strptime(request.form['date_of_birth'], '%Y-%m-%d').date() if request.form.get('date_of_birth') else None
        )
        
        # Update user with additional info
        user.phone = request.form.get('phone')
        user.address = request.form.get('address')
        db.session.add(teacher)
        db.session.commit()
        
        flash('Teacher added successfully!', 'success')
        return redirect(url_for('admin_teachers'))
    except Exception as e:
        db.session.rollback()
        flash(f'Error adding teacher: {str(e)}', 'error')
        return redirect(url_for('admin_teachers'))

@app.route('/admin/teachers/<int:teacher_id>/edit', methods=['POST'])
@login_required
@role_required('admin')
def edit_teacher(teacher_id):
    try:
        teacher = Teacher.query.get_or_404(teacher_id)
        user = User.query.get(teacher.user_id)
        
        # Update user information
        user.first_name = request.form['first_name']
        user.last_name = request.form['last_name']
        user.email = request.form['email']
        user.phone = request.form.get('phone')
        user.address = request.form.get('address')
        
        # Update teacher information
        teacher.specialization = request.form['specialization']
        teacher.qualification = request.form['qualification']
        teacher.experience_years = int(request.form['experience_years'])
        teacher.salary = float(request.form['salary']) if request.form.get('salary') else None
        teacher.hire_date = datetime.strptime(request.form['hire_date'], '%Y-%m-%d').date()
        teacher.date_of_birth = datetime.strptime(request.form['date_of_birth'], '%Y-%m-%d').date() if request.form.get('date_of_birth') else None
        
        db.session.commit()
        flash('Teacher updated successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error updating teacher: {str(e)}', 'error')
    
    return redirect(url_for('admin_teachers'))

@app.route('/admin/teachers/<int:teacher_id>/delete', methods=['POST'])
@login_required
@role_required('admin')
def delete_teacher(teacher_id):
    try:
        teacher = Teacher.query.get_or_404(teacher_id)
        user = User.query.get(teacher.user_id)
        
        # Delete related records first
        TeacherSubject.query.filter_by(teacher_id=teacher.id).delete()
        Attendance.query.filter_by(marked_by=teacher.id).delete()
        Grade.query.filter_by(teacher_id=teacher.id).delete()
        
        # Delete teacher and user
        db.session.delete(teacher)
        db.session.delete(user)
        db.session.commit()
        
        flash('Teacher deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting teacher: {str(e)}', 'error')
    
    return redirect(url_for('admin_teachers'))

@app.route('/admin/classes')
@login_required
@role_required('admin')
def admin_classes():
    classes = SchoolClass.query.all()
    teachers = db.session.query(Teacher, User).join(User, Teacher.user_id == User.id).all()
    return render_template('admin/classes.html', classes=classes, teachers=teachers)

@app.route('/admin/classes/add', methods=['POST'])
@login_required
@role_required('admin')
def add_class():
    try:
        school_class = SchoolClass(
            name=request.form['name'],
            grade_level=int(request.form['grade_level']),
            section=request.form.get('section'),
            academic_year=request.form['academic_year'],
            class_teacher_id=int(request.form['class_teacher_id']) if request.form.get('class_teacher_id') else None,
            max_students=int(request.form['max_students'])
        )
        db.session.add(school_class)
        db.session.commit()
        
        flash('Class added successfully!', 'success')
        return redirect(url_for('admin_classes'))
    except Exception as e:
        db.session.rollback()
        flash(f'Error adding class: {str(e)}', 'error')
        return redirect(url_for('admin_classes'))

@app.route('/admin/classes/<int:class_id>/edit', methods=['POST'])
@login_required
@role_required('admin')
def edit_class(class_id):
    try:
        school_class = SchoolClass.query.get_or_404(class_id)
        
        school_class.name = request.form['name']
        school_class.grade_level = int(request.form['grade_level'])
        school_class.section = request.form.get('section')
        school_class.academic_year = request.form['academic_year']
        school_class.class_teacher_id = int(request.form['class_teacher_id']) if request.form.get('class_teacher_id') else None
        school_class.max_students = int(request.form['max_students'])
        
        db.session.commit()
        flash('Class updated successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error updating class: {str(e)}', 'error')
    
    return redirect(url_for('admin_classes'))

@app.route('/admin/classes/<int:class_id>/delete', methods=['POST'])
@login_required
@role_required('admin')
def delete_class(class_id):
    try:
        school_class = SchoolClass.query.get_or_404(class_id)
        
        # Check if class has students
        student_count = Student.query.filter_by(class_id=class_id).count()
        if student_count > 0:
            flash(f'Cannot delete class. It has {student_count} students enrolled.', 'error')
            return redirect(url_for('admin_classes'))
        
        # Delete related records
        TeacherSubject.query.filter_by(class_id=class_id).delete()
        Timetable.query.filter_by(class_id=class_id).delete()
        
        db.session.delete(school_class)
        db.session.commit()
        
        flash('Class deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting class: {str(e)}', 'error')
    
    return redirect(url_for('admin_classes'))

@app.route('/admin/subjects')
@login_required
@role_required('admin')
def admin_subjects():
    subjects = Subject.query.all()
    return render_template('admin/subjects.html', subjects=subjects)

@app.route('/admin/subjects/add', methods=['POST'])
@login_required
@role_required('admin')
def add_subject():
    try:
        subject = Subject(
            name=request.form['name'],
            code=request.form['code'],
            description=request.form.get('description'),
            grade_level=int(request.form['grade_level']) if request.form.get('grade_level') else None,
            credits=int(request.form['credits']) if request.form.get('credits') else 1
        )
        db.session.add(subject)
        db.session.commit()
        
        flash('Subject added successfully!', 'success')
        return redirect(url_for('admin_subjects'))
    except Exception as e:
        db.session.rollback()
        flash(f'Error adding subject: {str(e)}', 'error')
        return redirect(url_for('admin_subjects'))

@app.route('/admin/subjects/<int:subject_id>/edit', methods=['POST'])
@login_required
@role_required('admin')
def edit_subject(subject_id):
    try:
        subject = Subject.query.get_or_404(subject_id)
        
        subject.name = request.form['name']
        subject.code = request.form['code']
        subject.description = request.form.get('description')
        subject.grade_level = int(request.form['grade_level']) if request.form.get('grade_level') else None
        subject.credits = int(request.form['credits']) if request.form.get('credits') else 1
        
        db.session.commit()
        flash('Subject updated successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error updating subject: {str(e)}', 'error')
    
    return redirect(url_for('admin_subjects'))

@app.route('/admin/subjects/<int:subject_id>/delete', methods=['POST'])
@login_required
@role_required('admin')
def delete_subject(subject_id):
    try:
        subject = Subject.query.get_or_404(subject_id)
        
        # Delete related records
        TeacherSubject.query.filter_by(subject_id=subject_id).delete()
        Attendance.query.filter_by(subject_id=subject_id).delete()
        Grade.query.filter_by(subject_id=subject_id).delete()
        Timetable.query.filter_by(subject_id=subject_id).delete()
        
        db.session.delete(subject)
        db.session.commit()
        
        flash('Subject deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting subject: {str(e)}', 'error')
    
    return redirect(url_for('admin_subjects'))

@app.route('/admin/fees')
@login_required
@role_required('admin')
def admin_fees():
    fees = db.session.query(Fee, Student, User).join(Student, Fee.student_id == Student.id).join(User, Student.user_id == User.id).all()
    students = db.session.query(Student, User).join(User, Student.user_id == User.id).all()
    return render_template('admin/fees.html', fees=fees, students=students)

@app.route('/admin/fees/add', methods=['POST'])
@login_required
@role_required('admin')
def add_fee():
    try:
        fee = Fee(
            student_id=int(request.form['student_id']),
            fee_type=request.form['fee_type'],
            amount=float(request.form['amount']),
            due_date=datetime.strptime(request.form['due_date'], '%Y-%m-%d').date(),
            status=request.form['status'],
            payment_method=request.form.get('payment_method'),
            academic_year=request.form.get('academic_year', '2023-2024')
        )
        
        # If status is paid, set payment date
        if fee.status == 'paid':
            fee.payment_date = date.today()
            
        db.session.add(fee)
        db.session.commit()
        
        flash('Fee record added successfully!', 'success')
        return redirect(url_for('admin_fees'))
    except Exception as e:
        db.session.rollback()
        flash(f'Error adding fee record: {str(e)}', 'error')
        return redirect(url_for('admin_fees'))

@app.route('/admin/fees/<int:fee_id>/edit', methods=['POST'])
@login_required
@role_required('admin')
def edit_fee(fee_id):
    try:
        fee = Fee.query.get_or_404(fee_id)
        
        fee.fee_type = request.form['fee_type']
        fee.amount = float(request.form['amount'])
        fee.due_date = datetime.strptime(request.form['due_date'], '%Y-%m-%d').date()
        fee.status = request.form['status']
        fee.payment_method = request.form.get('payment_method')
        fee.academic_year = request.form.get('academic_year', '2023-2024')
        
        # If status is paid, set payment date
        if fee.status == 'paid' and not fee.payment_date:
            fee.payment_date = date.today()
        elif fee.status != 'paid':
            fee.payment_date = None
            
        db.session.commit()
        flash('Fee record updated successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error updating fee record: {str(e)}', 'error')
    
    return redirect(url_for('admin_fees'))

@app.route('/admin/fees/<int:fee_id>/delete', methods=['POST'])
@login_required
@role_required('admin')
def delete_fee(fee_id):
    try:
        fee = Fee.query.get_or_404(fee_id)
        db.session.delete(fee)
        db.session.commit()
        
        flash('Fee record deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting fee record: {str(e)}', 'error')
    
    return redirect(url_for('admin_fees'))

@app.route('/admin/library')
@login_required
@role_required('admin')
def admin_library():
    books = Book.query.all()
    students = db.session.query(Student, User).join(User, Student.user_id == User.id).all()
    book_issues = BookIssue.query.filter_by(status='issued').all()
    overdue_books = BookIssue.query.filter(BookIssue.status == 'issued', BookIssue.due_date < date.today()).all()
    
    return render_template('admin/library.html', 
                         books=books, 
                         students=students,
                         book_issues=book_issues,
                         overdue_books=overdue_books)

@app.route('/admin/library/add', methods=['POST'])
@login_required
@role_required('admin')
def add_book():
    try:
        book = Book(
            title=request.form['title'],
            author=request.form['author'],
            isbn=request.form.get('isbn'),
            publisher=request.form.get('publisher'),
            category=request.form['category'],
            total_copies=int(request.form['total_copies']),
            available_copies=int(request.form['available_copies']),
            publication_year=int(request.form['publication_year']) if request.form.get('publication_year') else None,
            language=request.form.get('language', 'English')
        )
        db.session.add(book)
        db.session.commit()
        
        flash('Book added successfully!', 'success')
        return redirect(url_for('admin_library'))
    except Exception as e:
        db.session.rollback()
        flash(f'Error adding book: {str(e)}', 'error')
        return redirect(url_for('admin_library'))

@app.route('/admin/library/<int:book_id>/edit', methods=['POST'])
@login_required
@role_required('admin')
def edit_book(book_id):
    try:
        book = Book.query.get_or_404(book_id)
        
        book.title = request.form['title']
        book.author = request.form['author']
        book.isbn = request.form.get('isbn')
        book.publisher = request.form.get('publisher')
        book.category = request.form['category']
        book.total_copies = int(request.form['total_copies'])
        book.available_copies = int(request.form['available_copies'])
        book.publication_year = int(request.form['publication_year']) if request.form.get('publication_year') else None
        book.language = request.form.get('language', 'English')
        
        db.session.commit()
        flash('Book updated successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error updating book: {str(e)}', 'error')
    
    return redirect(url_for('admin_library'))

@app.route('/admin/library/<int:book_id>/delete', methods=['POST'])
@login_required
@role_required('admin')
def delete_book(book_id):
    try:
        book = Book.query.get_or_404(book_id)
        
        # Check if book has active issues
        active_issues = BookIssue.query.filter_by(book_id=book_id, status='issued').count()
        if active_issues > 0:
            flash(f'Cannot delete book. It has {active_issues} active issues.', 'error')
            return redirect(url_for('admin_library'))
        
        # Delete all book issues first
        BookIssue.query.filter_by(book_id=book_id).delete()
        
        db.session.delete(book)
        db.session.commit()
        
        flash('Book deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting book: {str(e)}', 'error')
    
    return redirect(url_for('admin_library'))

@app.route('/admin/library/issue', methods=['POST'])
@login_required
@role_required('admin')
def issue_book():
    try:
        book = Book.query.get_or_404(int(request.form['book_id']))
        
        if book.available_copies <= 0:
            flash('No copies available for this book!', 'error')
            return redirect(url_for('admin_library'))
        
        book_issue = BookIssue(
            book_id=book.id,
            student_id=int(request.form['student_id']),
            issue_date=datetime.strptime(request.form['issue_date'], '%Y-%m-%d').date(),
            due_date=datetime.strptime(request.form['due_date'], '%Y-%m-%d').date(),
            status='issued'
        )
        
        # Decrease available copies
        book.available_copies -= 1
        
        db.session.add(book_issue)
        db.session.commit()
        
        flash('Book issued successfully!', 'success')
        return redirect(url_for('admin_library'))
    except Exception as e:
        db.session.rollback()
        flash(f'Error issuing book: {str(e)}', 'error')
        return redirect(url_for('admin_library'))

@app.route('/admin/library/return/<int:issue_id>', methods=['POST'])
@login_required
@role_required('admin')
def return_book(issue_id):
    try:
        book_issue = BookIssue.query.get_or_404(issue_id)
        book = Book.query.get(book_issue.book_id)
        
        # Update book issue
        book_issue.return_date = date.today()
        book_issue.status = 'returned'
        
        # Calculate fine if overdue
        if date.today() > book_issue.due_date:
            days_overdue = (date.today() - book_issue.due_date).days
            book_issue.fine_amount = days_overdue * 1.0  # $1 per day fine
        
        # Increase available copies
        book.available_copies += 1
        
        db.session.commit()
        flash('Book returned successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error returning book: {str(e)}', 'error')
    
    return redirect(url_for('admin_library'))

# Teacher Routes
@app.route('/teacher/attendance')
@login_required
@role_required('teacher')
def teacher_attendance():
    teacher = Teacher.query.filter_by(user_id=current_user.id).first()
    assignments = TeacherSubject.query.filter_by(teacher_id=teacher.id).all()
    return render_template('teacher/attendance.html', assignments=assignments)

@app.route('/teacher/grades')
@login_required
@role_required('teacher')
def teacher_grades():
    teacher = Teacher.query.filter_by(user_id=current_user.id).first()
    assignments = TeacherSubject.query.filter_by(teacher_id=teacher.id).all()
    return render_template('teacher/grades.html', assignments=assignments)

# Student Routes
@app.route('/student/grades')
@login_required
@role_required('student')
def student_grades():
    student = Student.query.filter_by(user_id=current_user.id).first()
    grades = Grade.query.filter_by(student_id=student.id).all()
    return render_template('student/grades.html', grades=grades)

@app.route('/student/attendance')
@login_required
@role_required('student')
def student_attendance():
    student = Student.query.filter_by(user_id=current_user.id).first()
    attendance = Attendance.query.filter_by(student_id=student.id).all()
    return render_template('student/attendance.html', attendance=attendance)

# Parent Routes
@app.route('/parent/children')
@login_required
@role_required('parent')
def parent_children():
    children = Student.query.filter_by(parent_id=current_user.id).all()
    return render_template('parent/children.html', children=children)

# Additional Student Routes
@app.route('/student/fees')
@login_required
@role_required('student')
def student_fees():
    student = Student.query.filter_by(user_id=current_user.id).first()
    fees = Fee.query.filter_by(student_id=student.id).all() if student else []
    return render_template('student/fees.html', fees=fees, student=student)

@app.route('/student/timetable')
@login_required
@role_required('student')
def student_timetable():
    student = Student.query.filter_by(user_id=current_user.id).first()
    if student and student.school_class:
        timetable = Timetable.query.filter_by(class_id=student.class_id).all()
    else:
        timetable = []
    return render_template('student/timetable.html', timetable=timetable)

@app.route('/student/library')
@login_required
@role_required('student')
def student_library():
    student = Student.query.filter_by(user_id=current_user.id).first()
    if not student:
        flash('Student profile not found', 'error')
        return redirect(url_for('dashboard'))
    
    # Get books issued to this student
    issued_books = db.session.query(BookIssue, Book).join(Book, BookIssue.book_id == Book.id).filter(
        BookIssue.student_id == student.id,
        BookIssue.status == 'issued'
    ).all()
    
    # Get all available books
    available_books = Book.query.filter(Book.available_copies > 0).all()
    
    return render_template('student/library.html', 
                         issued_books=issued_books,
                         available_books=available_books,
                         student=student)

@app.route('/student/pay-fee/<int:fee_id>', methods=['POST'])
@login_required
@role_required('student')
def pay_fee(fee_id):
    try:
        student = Student.query.filter_by(user_id=current_user.id).first()
        if not student:
            return jsonify({'error': 'Student not found'}), 404
        
        fee = Fee.query.filter_by(id=fee_id, student_id=student.id).first()
        if not fee:
            return jsonify({'error': 'Fee record not found'}), 404
        
        # Simulate payment processing
        fee.status = 'paid'
        fee.payment_date = date.today()
        fee.payment_method = request.json.get('payment_method', 'online')
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Payment processed successfully',
            'receipt_url': f'/student/receipt/{fee_id}'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/student/receipt/<int:fee_id>')
@login_required
@role_required('student')
def download_receipt(fee_id):
    student = Student.query.filter_by(user_id=current_user.id).first()
    if not student:
        flash('Student not found', 'error')
        return redirect(url_for('student_fees'))
    
    fee = Fee.query.filter_by(id=fee_id, student_id=student.id).first()
    if not fee:
        flash('Fee record not found', 'error')
        return redirect(url_for('student_fees'))
    
    # Generate a simple receipt (in a real app, you'd generate a PDF)
    receipt_content = f"""
    SCHOOL MANAGEMENT SYSTEM
    PAYMENT RECEIPT
    
    Receipt ID: RCP-{fee_id:06d}
    Date: {fee.payment_date}
    
    Student: {current_user.first_name} {current_user.last_name}
    Student ID: {student.student_id}
    
    Fee Type: {fee.fee_type}
    Amount: ${fee.amount:.2f}
    Payment Method: {fee.payment_method}
    Status: {fee.status.upper()}
    
    Thank you for your payment!
    """
    
    from flask import Response
    return Response(
        receipt_content,
        mimetype='text/plain',
        headers={'Content-Disposition': f'attachment; filename=receipt_{fee_id}.txt'}
    )

# API Routes for AJAX calls
@app.route('/api/students/<int:class_id>')
@login_required
@role_required('teacher')
def api_students_by_class(class_id):
    students = db.session.query(Student, User).join(User, Student.user_id == User.id).filter(Student.class_id == class_id).all()
    return jsonify([{
        'id': student.id,
        'student_id': student.student_id,
        'name': f"{user.first_name} {user.last_name}"
    } for student, user in students])

@app.route('/api/attendance', methods=['POST'])
@login_required
@role_required('teacher')
def api_mark_attendance():
    data = request.get_json()
    teacher = Teacher.query.filter_by(user_id=current_user.id).first()
    
    for record in data.get('attendance', []):
        attendance = Attendance(
            student_id=record['student_id'],
            date=datetime.strptime(record['date'], '%Y-%m-%d').date(),
            status=record['status'],
            subject_id=record.get('subject_id'),
            remarks=record.get('remarks'),
            marked_by=teacher.id
        )
        db.session.add(attendance)
    
    try:
        db.session.commit()
        return jsonify({'success': True, 'message': 'Attendance marked successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 400

@app.route('/api/grades', methods=['POST'])
@login_required
@role_required('teacher')
def api_add_grades():
    data = request.get_json()
    teacher = Teacher.query.filter_by(user_id=current_user.id).first()
    
    for record in data.get('grades', []):
        grade = Grade(
            student_id=record['student_id'],
            subject_id=record['subject_id'],
            exam_type=record['exam_type'],
            marks_obtained=record['marks_obtained'],
            total_marks=record['total_marks'],
            exam_date=datetime.strptime(record['exam_date'], '%Y-%m-%d').date(),
            teacher_id=teacher.id
        )
        db.session.add(grade)
    
    try:
        db.session.commit()
        return jsonify({'success': True, 'message': 'Grades added successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 400

# API Routes
@app.route('/api/students/<int:class_id>')
@login_required
def get_students_by_class(class_id):
    try:
        students = db.session.query(Student, User).join(User, Student.user_id == User.id).filter(Student.class_id == class_id).all()
        student_list = []
        for student, user in students:
            student_list.append({
                'id': student.id,
                'student_id': student.student_id,
                'name': f"{user.first_name} {user.last_name}",
                'email': user.email
            })
        return jsonify({'students': student_list})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/attendance', methods=['POST'])
@login_required
@role_required('teacher')
def submit_attendance():
    try:
        data = request.get_json()
        teacher = Teacher.query.filter_by(user_id=current_user.id).first()
        
        if not teacher:
            return jsonify({'error': 'Teacher not found'}), 404
        
        attendance_date = datetime.strptime(data['date'], '%Y-%m-%d').date()
        
        for student_attendance in data['attendance']:
            # Check if attendance already exists for this date
            existing = Attendance.query.filter_by(
                student_id=student_attendance['student_id'],
                date=attendance_date,
                subject_id=data['subject_id']
            ).first()
            
            if existing:
                # Update existing record
                existing.status = student_attendance['status']
                existing.remarks = student_attendance.get('remarks', '')
            else:
                # Create new record
                attendance = Attendance(
                    student_id=student_attendance['student_id'],
                    subject_id=data['subject_id'],
                    date=attendance_date,
                    status=student_attendance['status'],
                    remarks=student_attendance.get('remarks', ''),
                    marked_by=teacher.id
                )
                db.session.add(attendance)
        
        db.session.commit()
        return jsonify({'message': 'Attendance submitted successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/api/grades', methods=['POST'])
@login_required
@role_required('teacher')
def submit_grades():
    try:
        data = request.get_json()
        teacher = Teacher.query.filter_by(user_id=current_user.id).first()
        
        if not teacher:
            return jsonify({'error': 'Teacher not found'}), 404
        
        for student_grade in data['grades']:
            # Check if grade already exists
            existing = Grade.query.filter_by(
                student_id=student_grade['student_id'],
                subject_id=data['subject_id'],
                exam_type=data['exam_type']
            ).first()
            
            if existing:
                # Update existing record
                existing.marks_obtained = student_grade['marks']
                existing.total_marks = data['total_marks']
                existing.percentage = (student_grade['marks'] / data['total_marks']) * 100
                existing.grade = calculate_letter_grade(existing.percentage)
            else:
                # Create new record
                percentage = (student_grade['marks'] / data['total_marks']) * 100
                grade = Grade(
                    student_id=student_grade['student_id'],
                    subject_id=data['subject_id'],
                    exam_type=data['exam_type'],
                    marks_obtained=student_grade['marks'],
                    total_marks=data['total_marks'],
                    percentage=percentage,
                    grade=calculate_letter_grade(percentage),
                    teacher_id=teacher.id,
                    exam_date=datetime.strptime(data['exam_date'], '%Y-%m-%d').date()
                )
                db.session.add(grade)
        
        db.session.commit()
        return jsonify({'message': 'Grades submitted successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

def calculate_letter_grade(percentage):
    if percentage >= 90:
        return 'A+'
    elif percentage >= 80:
        return 'A'
    elif percentage >= 70:
        return 'B+'
    elif percentage >= 60:
        return 'B'
    elif percentage >= 50:
        return 'C+'
    elif percentage >= 40:
        return 'C'
    else:
        return 'F'

# PWA Routes
@app.route('/static/sw.js')
def service_worker():
    return app.send_static_file('sw.js'), 200, {'Content-Type': 'application/javascript'}

@app.route('/static/sw-simple.js')
def service_worker_simple():
    return app.send_static_file('sw-simple.js'), 200, {'Content-Type': 'application/javascript'}

@app.route('/static/sw-minimal.js')
def service_worker_minimal():
    return app.send_static_file('sw-minimal.js'), 200, {'Content-Type': 'application/javascript'}

@app.route('/static/manifest.json')
def manifest():
    return app.send_static_file('manifest.json'), 200, {'Content-Type': 'application/json'}

@app.route('/share', methods=['GET', 'POST'])
def share_target():
    """Handle PWA share target"""
    if request.method == 'POST':
        # Handle shared content
        title = request.form.get('title', '')
        text = request.form.get('text', '')
        url = request.form.get('url', '')
        files = request.files.getlist('files')
        
        # For now, redirect to dashboard with shared content
        if title or text or url:
            flash(f'Shared content received: {title} {text} {url}', 'info')
        
        if files:
            flash(f'Received {len(files)} shared files', 'info')
        
        return redirect(url_for('dashboard'))
    
    # GET request - show share form
    return render_template('share.html')

@app.route('/api/widget-data')
def widget_data():
    """Provide data for PWA widgets"""
    try:
        # Get basic stats for widget
        total_students = Student.query.count()
        total_teachers = Teacher.query.count()
        total_classes = Class.query.count()
        
        widget_data = {
            "students": total_students,
            "teachers": total_teachers,
            "classes": total_classes,
            "last_updated": datetime.now().isoformat()
        }
        
        return jsonify(widget_data)
    except Exception as e:
        return jsonify({"error": "Widget data unavailable"}), 500

@app.route('/test-pwa')
def test_pwa():
    """PWA validation test page"""
    return send_from_directory('.', 'test_pwa.html')

@app.route('/offline')
def offline():
    """Offline fallback page"""
    return render_template('offline.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        
        # Initialize sample data if no users exist (first run)
        if User.query.count() == 0:
            print("🔧 First run detected - initializing sample data...")
            from init_sample_data import create_sample_data
            create_sample_data()
            print("✅ Sample data initialized!")
    
    # Run in development mode
    app.run(debug=True)

# Production WSGI entry point for Railway
def create_app():
    with app.app_context():
        db.create_all()
        
        # Initialize sample data if no users exist (first run)
        if User.query.count() == 0:
            print("🔧 Production first run - initializing sample data...")
            from init_sample_data import create_sample_data
            create_sample_data()
            print("✅ Production sample data initialized!")
    
    return app