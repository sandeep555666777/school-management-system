#!/usr/bin/env python3
"""
Sample data initialization script for School Management System
"""

from app import app, db, User, Student, Teacher, SchoolClass, Subject, Fee, Book, BookIssue, Attendance, Grade, TeacherSubject, Timetable
from datetime import date, datetime, timedelta
import random

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

def create_sample_data():
    with app.app_context():
        # Create tables
        db.create_all()
        
        # Check if admin user exists
        admin_user = User.query.filter_by(username='admin').first()
        if not admin_user:
            # Create admin user
            admin_user = User(
                username='admin',
                email='admin@school.com',
                first_name='System',
                last_name='Administrator',
                role='admin'
            )
            admin_user.set_password('admin123')
            db.session.add(admin_user)
            
        # Create sample classes
        if SchoolClass.query.count() == 0:
            classes = [
                SchoolClass(name='Grade 1-A', grade_level=1, section='A', academic_year='2023-2024', max_students=30),
                SchoolClass(name='Grade 1-B', grade_level=1, section='B', academic_year='2023-2024', max_students=30),
                SchoolClass(name='Grade 2-A', grade_level=2, section='A', academic_year='2023-2024', max_students=30),
                SchoolClass(name='Grade 3-A', grade_level=3, section='A', academic_year='2023-2024', max_students=30),
                SchoolClass(name='Grade 4-A', grade_level=4, section='A', academic_year='2023-2024', max_students=30),
                SchoolClass(name='Grade 5-A', grade_level=5, section='A', academic_year='2023-2024', max_students=30),
            ]
            for cls in classes:
                db.session.add(cls)
        
        # Create sample subjects
        if Subject.query.count() == 0:
            subjects = [
                Subject(name='Mathematics', code='MATH101', description='Basic Mathematics', credits=3, grade_level=1),
                Subject(name='English', code='ENG101', description='English Language', credits=3, grade_level=1),
                Subject(name='Science', code='SCI101', description='General Science', credits=3, grade_level=1),
                Subject(name='Social Studies', code='SS101', description='Social Studies', credits=2, grade_level=1),
                Subject(name='Art', code='ART101', description='Creative Arts', credits=1, grade_level=1),
                Subject(name='Physical Education', code='PE101', description='Physical Education', credits=1, grade_level=1),
            ]
            for subject in subjects:
                db.session.add(subject)
        
        # Create sample teachers
        if Teacher.query.count() == 0:
            teacher_data = [
                ('teacher1@school.com', 'John', 'Smith', 'T001', 'Mathematics', 'M.Ed Mathematics', 5, 50000),
                ('teacher2@school.com', 'Sarah', 'Johnson', 'T002', 'English', 'M.A English Literature', 8, 52000),
                ('teacher3@school.com', 'Michael', 'Brown', 'T003', 'Science', 'M.Sc Physics', 6, 51000),
                ('teacher4@school.com', 'Emily', 'Davis', 'T004', 'Social Studies', 'M.A History', 4, 48000),
                ('teacher5@school.com', 'David', 'Wilson', 'T005', 'Art', 'BFA Fine Arts', 3, 45000),
            ]
            
            for email, first_name, last_name, teacher_id, specialization, qualification, experience, salary in teacher_data:
                # Create user account
                user = User(
                    username=email,
                    email=email,
                    first_name=first_name,
                    last_name=last_name,
                    role='teacher',
                    phone=f'+1-555-{random.randint(1000, 9999)}'
                )
                user.set_password('teacher123')
                db.session.add(user)
                db.session.flush()
                
                # Create teacher record
                teacher = Teacher(
                    user_id=user.id,
                    teacher_id=teacher_id,
                    specialization=specialization,
                    qualification=qualification,
                    experience_years=experience,
                    salary=salary,
                    hire_date=date.today() - timedelta(days=random.randint(30, 365))
                )
                db.session.add(teacher)
        
        # Create sample students
        if Student.query.count() == 0:
            student_data = [
                ('student1@school.com', 'Alice', 'Johnson', 'S001', 'female', '2015-03-15'),
                ('student2@school.com', 'Bob', 'Smith', 'S002', 'male', '2015-07-22'),
                ('student3@school.com', 'Charlie', 'Brown', 'S003', 'male', '2015-01-10'),
                ('student4@school.com', 'Diana', 'Wilson', 'S004', 'female', '2015-09-05'),
                ('student5@school.com', 'Eva', 'Davis', 'S005', 'female', '2015-11-18'),
                ('student6@school.com', 'Frank', 'Miller', 'S006', 'male', '2015-04-30'),
                ('student7@school.com', 'Grace', 'Taylor', 'S007', 'female', '2015-08-12'),
                ('student8@school.com', 'Henry', 'Anderson', 'S008', 'male', '2015-02-28'),
            ]
            
            classes = SchoolClass.query.all()
            
            for email, first_name, last_name, student_id, gender, dob in student_data:
                # Create user account
                user = User(
                    username=email,
                    email=email,
                    first_name=first_name,
                    last_name=last_name,
                    role='student',
                    phone=f'+1-555-{random.randint(1000, 9999)}'
                )
                user.set_password('student123')
                db.session.add(user)
                db.session.flush()
                
                # Create student record
                student = Student(
                    user_id=user.id,
                    student_id=student_id,
                    date_of_birth=datetime.strptime(dob, '%Y-%m-%d').date(),
                    gender=gender,
                    class_id=random.choice(classes).id,
                    admission_date=date.today() - timedelta(days=random.randint(30, 200))
                )
                db.session.add(student)
        
        # Create sample books
        if Book.query.count() == 0:
            books = [
                ('The Great Gatsby', 'F. Scott Fitzgerald', '978-0-7432-7356-5', 'Fiction', 5, 5),
                ('To Kill a Mockingbird', 'Harper Lee', '978-0-06-112008-4', 'Fiction', 3, 3),
                ('1984', 'George Orwell', '978-0-452-28423-4', 'Fiction', 4, 4),
                ('Pride and Prejudice', 'Jane Austen', '978-0-14-143951-8', 'Fiction', 2, 2),
                ('The Catcher in the Rye', 'J.D. Salinger', '978-0-316-76948-0', 'Fiction', 3, 3),
                ('Mathematics Grade 1', 'Education Board', '978-1-234-56789-0', 'Textbook', 10, 10),
                ('English Grade 1', 'Education Board', '978-1-234-56789-1', 'Textbook', 10, 10),
                ('Science Grade 1', 'Education Board', '978-1-234-56789-2', 'Textbook', 10, 10),
            ]
            
            for title, author, isbn, category, total, available in books:
                book = Book(
                    title=title,
                    author=author,
                    isbn=isbn,
                    category=category,
                    total_copies=total,
                    available_copies=available,
                    publication_year=random.randint(2000, 2023),
                    language='English'
                )
                db.session.add(book)
        
        # Create sample fees
        if Fee.query.count() == 0:
            students = Student.query.all()
            fee_types = ['tuition', 'library', 'transport', 'exam', 'sports', 'lab']
            
            for student in students:
                for i, fee_type in enumerate(fee_types[:3]):  # Create 3 fees per student
                    amount = random.uniform(100, 500)
                    due_date = date.today() + timedelta(days=random.randint(10, 60))
                    status = random.choice(['pending', 'paid', 'overdue'])
                    
                    fee = Fee(
                        student_id=student.id,
                        fee_type=fee_type,
                        amount=amount,
                        due_date=due_date,
                        status=status,
                        academic_year='2023-2024',
                        payment_date=date.today() - timedelta(days=random.randint(1, 30)) if status == 'paid' else None,
                        payment_method='online' if status == 'paid' else None
                    )
                    db.session.add(fee)
        
        # Create sample book issues
        if BookIssue.query.count() == 0:
            students = Student.query.all()
            books = Book.query.all()
            
            for i in range(min(10, len(students), len(books))):  # Create 10 book issues
                student = random.choice(students)
                book = random.choice(books)
                
                # Check if book is available
                if book.available_copies > 0:
                    issue_date = date.today() - timedelta(days=random.randint(1, 30))
                    due_date = issue_date + timedelta(days=14)  # 2 weeks loan period
                    status = 'issued' if due_date >= date.today() else random.choice(['issued', 'returned'])
                    
                    book_issue = BookIssue(
                        book_id=book.id,
                        student_id=student.id,
                        issue_date=issue_date,
                        due_date=due_date,
                        status=status,
                        return_date=date.today() - timedelta(days=random.randint(1, 5)) if status == 'returned' else None
                    )
                    db.session.add(book_issue)
                    
                    # Update book availability
                    if status == 'issued':
                        book.available_copies -= 1
        
        # Create sample attendance records
        if Attendance.query.count() == 0:
            students = Student.query.all()
            subjects = Subject.query.all()
            
            for student in students[:5]:  # Create attendance for first 5 students
                for i in range(10):  # 10 days of attendance
                    attendance_date = date.today() - timedelta(days=i)
                    subject = random.choice(subjects)
                    
                    attendance = Attendance(
                        student_id=student.id,
                        subject_id=subject.id,
                        date=attendance_date,
                        status=random.choice(['present', 'absent', 'late']),
                        marked_by=1  # Assuming first teacher
                    )
                    db.session.add(attendance)
        
        # Create sample grades
        if Grade.query.count() == 0:
            students = Student.query.all()
            subjects = Subject.query.all()
            
            for student in students[:5]:  # Create grades for first 5 students
                for subject in subjects[:3]:  # 3 subjects per student
                    for exam_type in ['quiz', 'midterm', 'final']:
                        marks = random.randint(60, 100)
                        total_marks = 100
                        percentage = (marks / total_marks) * 100
                        
                        grade = Grade(
                            student_id=student.id,
                            subject_id=subject.id,
                            exam_type=exam_type,
                            marks_obtained=marks,
                            total_marks=total_marks,
                            grade_letter=calculate_letter_grade(percentage),
                            teacher_id=1,  # Assuming first teacher
                            exam_date=date.today() - timedelta(days=random.randint(1, 60))
                        )
                        db.session.add(grade)
        
        # Commit all changes
        db.session.commit()
        print("Sample data created successfully!")
        print("Admin login: admin / admin123")
        print("Teacher login: teacher1@school.com / teacher123")
        print("Student login: student1@school.com / student123")

if __name__ == '__main__':
    create_sample_data()