#!/usr/bin/env python3
"""
Simple parent user fix
"""

from app import app, db, User

def fix_parent():
    with app.app_context():
        # Check if parent user exists
        parent_user = User.query.filter_by(username='parent1@school.com').first()
        
        if parent_user:
            # Make sure password is correct
            parent_user.set_password('parent123')
            db.session.commit()
            print("✅ Parent user password fixed: parent1@school.com / parent123")
        else:
            print("❌ Parent user not found")

if __name__ == "__main__":
    fix_parent()