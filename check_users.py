#!/usr/bin/env python3
"""
Check users in the database and their passwords
"""

from app import app, db, User
from werkzeug.security import check_password_hash

def check_all_users():
    with app.app_context():
        print("=== CHECKING ALL USERS IN DATABASE ===\n")
        
        users = User.query.all()
        
        if not users:
            print("❌ No users found in database!")
            print("Please run: python init_sample_data.py")
            return
        
        print(f"Found {len(users)} users in database:\n")
        
        # Test credentials
        test_credentials = [
            ('admin', 'admin123'),
            ('teacher1@school.com', 'teacher123'),
            ('student1@school.com', 'student123'),
            ('parent1@school.com', 'parent123')
        ]
        
        for user in users:
            print(f"👤 User: {user.username}")
            print(f"   Email: {user.email}")
            print(f"   Name: {user.first_name} {user.last_name}")
            print(f"   Role: {user.role}")
            print(f"   Password Hash: {user.password_hash[:50]}...")
            
            # Test password
            for test_username, test_password in test_credentials:
                if user.username == test_username:
                    if user.check_password(test_password):
                        print(f"   ✅ Password '{test_password}' is CORRECT")
                    else:
                        print(f"   ❌ Password '{test_password}' is INCORRECT")
                        # Try to fix the password
                        print(f"   🔧 Fixing password for {user.username}...")
                        user.set_password(test_password)
                        db.session.commit()
                        print(f"   ✅ Password fixed!")
            print()

def fix_user_passwords():
    """Fix passwords for all users"""
    with app.app_context():
        print("=== FIXING USER PASSWORDS ===\n")
        
        # Fix admin password
        admin = User.query.filter_by(username='admin').first()
        if admin:
            admin.set_password('admin123')
            print("✅ Fixed admin password")
        
        # Fix teacher passwords
        teachers = User.query.filter_by(role='teacher').all()
        for teacher in teachers:
            teacher.set_password('teacher123')
            print(f"✅ Fixed password for teacher: {teacher.username}")
        
        # Fix student passwords
        students = User.query.filter_by(role='student').all()
        for student in students:
            student.set_password('student123')
            print(f"✅ Fixed password for student: {student.username}")
        
        # Fix parent passwords
        parents = User.query.filter_by(role='parent').all()
        for parent in parents:
            parent.set_password('parent123')
            print(f"✅ Fixed password for parent: {parent.username}")
        
        db.session.commit()
        print("\n🎉 All passwords have been fixed!")
        
        print("\n=== UPDATED LOGIN CREDENTIALS ===")
        print("Admin: admin / admin123")
        print("Teacher: teacher1@school.com / teacher123")
        print("Student: student1@school.com / student123")
        print("Parent: parent1@school.com / parent123")

if __name__ == "__main__":
    print("1. Checking current users...")
    check_all_users()
    
    print("\n" + "="*50)
    print("2. Fixing passwords...")
    fix_user_passwords()
    
    print("\n" + "="*50)
    print("3. Verifying fixes...")
    check_all_users()