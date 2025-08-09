from app import app, db, User, Student, Teacher, SchoolClass, Subject, TeacherSubject, Attendance, Grade, Fee, Book, BookIssue, Timetable
from werkzeug.security import generate_password_hash
from datetime import date, datetime, time
from decimal import Decimal
import random

def init_database():
    """Initialize the database with sample data"""
    with app.app_context():
        # Drop all tables and recreate them
        db.drop_all()
        db.create_all()
        
        print("Creating sample data...")
        
        # Create admin user
        admin_user = User(
            username='admin',
            email='admin@school.com',
            password_hash=generate_password_hash('admin123'),
            role='admin',
            first_name='System',
            last_name='Administrator',
            phone='+1-555-0001',
            address='School Administration Office'
        )
        db.session.add(admin_user)
        
        # Create sample teachers
        teachers_data = [
            {
                'username': 'teacher1',
                'email': 'john.johnson@school.com',
                'password': 'teacher123',
                'first_name': 'John',
                'last_name': 'Johnson',
                'phone': '+1-555-0101',
                'teacher_id': 'TCH001',
                'subject_specialization': 'Mathematics',
                'qualification': 'M.Sc. Mathematics',
                'experience_years': 8,
                'salary': Decimal('45000.00')
            },
            {
                'username': 'teacher2',
                'email': 'sarah.davis@school.com',
                'password': 'teacher123',
                'first_name': 'Sarah',
                'last_name': 'Davis',
                'phone': '+1-555-0102',
                'teacher_id': 'TCH002',
                'subject_specialization': 'Science',
                'qualification': 'M.Sc. Physics',
                'experience_years': 6,
                'salary': Decimal('42000.00')
            },
            {
                'username': 'teacher3',
                'email': 'mike.wilson@school.com',
                'password': 'teacher123',
                'first_name': 'Mike',
                'last_name': 'Wilson',
                'phone': '+1-555-0103',
                'teacher_id': 'TCH003',
                'subject_specialization': 'English',
                'qualification': 'M.A. English Literature',
                'experience_years': 10,
                'salary': Decimal('48000.00')
            }
        ]
        
        teacher_objects = []
        for teacher_data in teachers_data:
            user = User(
                username=teacher_data['username'],
                email=teacher_data['email'],
                password_hash=generate_password_hash(teacher_data['password']),
                role='teacher',
                first_name=teacher_data['first_name'],
                last_name=teacher_data['last_name'],
                phone=teacher_data['phone'],
                address=f"{teacher_data['first_name']}'s Address"
            )
            db.session.add(user)
            db.session.flush()  # Get the user ID
            
            teacher = Teacher(
                user_id=user.id,
                teacher_id=teacher_data['teacher_id'],
                subject_specialization=teacher_data['subject_specialization'],
                qualification=teacher_data['qualification'],
                experience_years=teacher_data['experience_years'],
                salary=teacher_data['salary']
            )
            db.session.add(teacher)
            teacher_objects.append(teacher)
        
        # Create sample parents
        parents_data = [
            {
                'username': 'parent1',
                'email': 'robert.doe@email.com',
                'password': 'parent123',
                'first_name': 'Robert',
                'last_name': 'Doe',
                'phone': '+1-555-0201'
            },
            {
                'username': 'parent2',
                'email': 'mary.smith@email.com',
                'password': 'parent123',
                'first_name': 'Mary',
                'last_name': 'Smith',
                'phone': '+1-555-0202'
            }
        ]
        
        parent_objects = []
        for parent_data in parents_data:
            user = User(
                username=parent_data['username'],
                email=parent_data['email'],
                password_hash=generate_password_hash(parent_data['password']),
                role='parent',
                first_name=parent_data['first_name'],
                last_name=parent_data['last_name'],
                phone=parent_data['phone'],
                address=f"{parent_data['first_name']}'s Home Address"
            )
            db.session.add(user)
            parent_objects.append(user)
        
        # Create sample classes
        classes_data = [
            {'name': 'Grade 1-A', 'grade_level': 1, 'section': 'A', 'academic_year': '2023-2024'},
            {'name': 'Grade 2-A', 'grade_level': 2, 'section': 'A', 'academic_year': '2023-2024'},
            {'name': 'Grade 3-A', 'grade_level': 3, 'section': 'A', 'academic_year': '2023-2024'},
            {'name': 'Grade 4-A', 'grade_level': 4, 'section': 'A', 'academic_year': '2023-2024'},
            {'name': 'Grade 5-A', 'grade_level': 5, 'section': 'A', 'academic_year': '2023-2024'},
        ]
        
        class_objects = []
        for class_data in classes_data:
            school_class = SchoolClass(
                name=class_data['name'],
                grade_level=class_data['grade_level'],
                section=class_data['section'],
                academic_year=class_data['academic_year'],
                max_students=30
            )
            db.session.add(school_class)
            class_objects.append(school_class)
        
        # Create subjects
        subjects_data = [
            {'name': 'Mathematics', 'code': 'MATH', 'credits': 4},
            {'name': 'Science', 'code': 'SCI', 'credits': 4},
            {'name': 'English', 'code': 'ENG', 'credits': 3},
            {'name': 'History', 'code': 'HIST', 'credits': 2},
            {'name': 'Art', 'code': 'ART', 'credits': 2},
            {'name': 'Physical Education', 'code': 'PE', 'credits': 1},
        ]
        
        subject_objects = []
        for subject_data in subjects_data:
            subject = Subject(
                name=subject_data['name'],
                code=subject_data['code'],
                credits=subject_data['credits']
            )
            db.session.add(subject)
            subject_objects.append(subject)
        
        db.session.flush()  # Ensure all objects have IDs
        
        # Create sample students
        students_data = [
            {
                'username': 'student1',
                'email': 'john.doe@student.school.com',
                'password': 'student123',
                'first_name': 'John',
                'last_name': 'Doe',
                'phone': '+1-555-0301',
                'student_id': 'STU001',
                'date_of_birth': date(2010, 1, 15),
                'gender': 'Male',
                'class_id': class_objects[4].id,  # Grade 5-A
                'parent_id': parent_objects[0].id
            },
            {
                'username': 'student2',
                'email': 'jane.smith@student.school.com',
                'password': 'student123',
                'first_name': 'Jane',
                'last_name': 'Smith',
                'phone': '+1-555-0302',
                'student_id': 'STU002',
                'date_of_birth': date(2011, 3, 22),
                'gender': 'Female',
                'class_id': class_objects[3].id,  # Grade 4-A
                'parent_id': parent_objects[1].id
            },
            {
                'username': 'student3',
                'email': 'emma.johnson@student.school.com',
                'password': 'student123',
                'first_name': 'Emma',
                'last_name': 'Johnson',
                'phone': '+1-555-0303',
                'student_id': 'STU003',
                'date_of_birth': date(2010, 7, 8),
                'gender': 'Female',
                'class_id': class_objects[4].id,  # Grade 5-A
                'parent_id': parent_objects[0].id
            }
        ]
        
        student_objects = []
        for student_data in students_data:
            user = User(
                username=student_data['username'],
                email=student_data['email'],
                password_hash=generate_password_hash(student_data['password']),
                role='student',
                first_name=student_data['first_name'],
                last_name=student_data['last_name'],
                phone=student_data['phone'],
                address=f"{student_data['first_name']}'s Home Address"
            )
            db.session.add(user)
            db.session.flush()
            
            student = Student(
                user_id=user.id,
                student_id=student_data['student_id'],
                class_id=student_data['class_id'],
                date_of_birth=student_data['date_of_birth'],
                gender=student_data['gender'],
                parent_id=student_data['parent_id']
            )
            db.session.add(student)
            student_objects.append(student)
        
        # Create teacher-subject assignments
        db.session.flush()
        
        # Assign teachers to subjects and classes
        teacher_assignments = [
            {'teacher_id': teacher_objects[0].id, 'subject_id': subject_objects[0].id, 'class_id': class_objects[4].id},  # Math teacher to Grade 5-A
            {'teacher_id': teacher_objects[1].id, 'subject_id': subject_objects[1].id, 'class_id': class_objects[4].id},  # Science teacher to Grade 5-A
            {'teacher_id': teacher_objects[2].id, 'subject_id': subject_objects[2].id, 'class_id': class_objects[4].id},  # English teacher to Grade 5-A
        ]
        
        for assignment in teacher_assignments:
            teacher_subject = TeacherSubject(
                teacher_id=assignment['teacher_id'],
                subject_id=assignment['subject_id'],
                class_id=assignment['class_id']
            )
            db.session.add(teacher_subject)
        
        # Create sample grades
        for student in student_objects:
            for subject in subject_objects[:3]:  # First 3 subjects
                grade = Grade(
                    student_id=student.id,
                    subject_id=subject.id,
                    exam_type='Midterm',
                    marks_obtained=Decimal(str(random.randint(75, 98))),
                    total_marks=Decimal('100.00'),
                    grade_letter='A' if random.randint(75, 98) >= 90 else 'B',
                    exam_date=date(2023, 10, 15),
                    teacher_id=teacher_objects[0].id
                )
                db.session.add(grade)
        
        # Create sample fees
        for student in student_objects:
            fee = Fee(
                student_id=student.id,
                fee_type='Tuition',
                amount=Decimal('500.00'),
                due_date=date(2023, 11, 30),
                status='pending',
                academic_year='2023-2024'
            )
            db.session.add(fee)
        
        # Create sample books
        books_data = [
            {'title': 'Mathematics Grade 5', 'author': 'John Smith', 'isbn': '978-1234567890', 'category': 'Textbook', 'total_copies': 50},
            {'title': 'Science Experiments', 'author': 'Jane Doe', 'isbn': '978-1234567891', 'category': 'Reference', 'total_copies': 25},
            {'title': 'English Literature', 'author': 'Mike Johnson', 'isbn': '978-1234567892', 'category': 'Literature', 'total_copies': 30},
            {'title': 'The Great Gatsby', 'author': 'F. Scott Fitzgerald', 'isbn': '978-0743273565', 'category': 'Fiction', 'total_copies': 15},
            {'title': 'To Kill a Mockingbird', 'author': 'Harper Lee', 'isbn': '978-0061120084', 'category': 'Fiction', 'total_copies': 20},
        ]
        
        book_objects = []
        for book_data in books_data:
            book = Book(
                title=book_data['title'],
                author=book_data['author'],
                isbn=book_data['isbn'],
                category=book_data['category'],
                total_copies=book_data['total_copies'],
                available_copies=book_data['total_copies'] - random.randint(0, 5),
                publication_year=2023,
                publisher='Educational Publishers'
            )
            db.session.add(book)
            book_objects.append(book)
        
        # Create sample book issues
        db.session.flush()
        
        for i, student in enumerate(student_objects[:2]):  # First 2 students
            book_issue = BookIssue(
                book_id=book_objects[i + 3].id,  # Fiction books
                student_id=student.id,
                issue_date=date(2023, 10, 15),
                due_date=date(2023, 11, 15),
                status='issued'
            )
            db.session.add(book_issue)
        
        # Create sample timetable
        timetable_data = [
            {'class_id': class_objects[4].id, 'subject_id': subject_objects[0].id, 'teacher_id': teacher_objects[0].id, 'day_of_week': 'monday', 'start_time': time(9, 0), 'end_time': time(9, 45), 'room_number': '101'},
            {'class_id': class_objects[4].id, 'subject_id': subject_objects[1].id, 'teacher_id': teacher_objects[1].id, 'day_of_week': 'monday', 'start_time': time(10, 0), 'end_time': time(10, 45), 'room_number': 'Lab1'},
            {'class_id': class_objects[4].id, 'subject_id': subject_objects[2].id, 'teacher_id': teacher_objects[2].id, 'day_of_week': 'monday', 'start_time': time(11, 15), 'end_time': time(12, 0), 'room_number': '203'},
        ]
        
        for timetable_entry in timetable_data:
            timetable = Timetable(
                class_id=timetable_entry['class_id'],
                subject_id=timetable_entry['subject_id'],
                teacher_id=timetable_entry['teacher_id'],
                day_of_week=timetable_entry['day_of_week'],
                start_time=timetable_entry['start_time'],
                end_time=timetable_entry['end_time'],
                room_number=timetable_entry['room_number']
            )
            db.session.add(timetable)
        
        # Create sample attendance records
        for student in student_objects:
            for i in range(10):  # 10 attendance records per student
                attendance = Attendance(
                    student_id=student.id,
                    date=date(2023, 10, i + 1),
                    status=random.choice(['present', 'present', 'present', 'present', 'absent']),  # 80% present
                    subject_id=subject_objects[0].id,
                    marked_by=teacher_objects[0].id
                )
                db.session.add(attendance)
        
        # Commit all changes
        db.session.commit()
        print("Database initialized successfully!")
        print("\nDemo Login Credentials:")
        print("Admin: admin / admin123")
        print("Teacher: teacher1 / teacher123")
        print("Student: student1 / student123")
        print("Parent: parent1 / parent123")

if __name__ == '__main__':
    init_database()