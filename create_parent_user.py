#!/usr/bin/env python3
"""
Create parent user for testing
"""

from app import app, db, User, Student
from datetime import date

def create_parent_user():
    with app.app_context():
        # Check if parent user already exists
        parent_user = User.query.filter_by(username='parent1@school.com').first()
        
        if not parent_user:
            # Create parent user
            parent_user = User(
                username='parent1@school.com',
                email='parent1@school.com',
                first_name='Mary',
                last_name='Johnson',
                role='parent',
                phone='+1-555-9999'
            )
            parent_user.set_password('parent123')
            db.session.add(parent_user)
            db.session.commit()
            
            print("✅ Created parent user: parent1@school.com / parent123")
            
            # Link parent to a student (Alice Johnson)
            student = Student.query.join(User).filter(User.first_name == 'Alice', User.last_name == 'Johnson').first()
            if student:
                student.parent_id = parent_user.id
                db.session.commit()
                print(f"✅ Linked parent to student: {student.student_id}")
            
        else:
            print("✅ Parent user already exists")
            # Make sure password is correct
            parent_user.set_password('parent123')
            db.session.commit()
            print("✅ Updated parent password")

if __name__ == "__main__":
    create_parent_user()