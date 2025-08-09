#!/usr/bin/env python3
"""
School Management System - Installation Script
This script helps set up the application for first-time use.
"""

import os
import sys
import subprocess
import platform

def print_header():
    print("=" * 60)
    print("    SCHOOL MANAGEMENT SYSTEM - INSTALLATION")
    print("=" * 60)
    print()

def check_python_version():
    """Check if Python version is compatible"""
    print("Checking Python version...")
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8 or higher is required!")
        print(f"   Current version: {version.major}.{version.minor}.{version.micro}")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} - Compatible")
    return True

def install_requirements():
    """Install required packages"""
    print("\nInstalling required packages...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ All packages installed successfully")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install packages")
        return False

def initialize_database():
    """Initialize the database with sample data"""
    print("\nInitializing database...")
    try:
        subprocess.check_call([sys.executable, "init_db.py"])
        print("✅ Database initialized successfully")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to initialize database")
        return False

def create_directories():
    """Create necessary directories"""
    print("\nCreating necessary directories...")
    directories = ['uploads', 'logs', 'static/uploads']
    
    for directory in directories:
        if not os.path.exists(directory):
            try:
                os.makedirs(directory)
                print(f"✅ Created directory: {directory}")
            except OSError as e:
                print(f"❌ Failed to create directory {directory}: {e}")
                return False
        else:
            print(f"✅ Directory already exists: {directory}")
    
    return True

def print_demo_credentials():
    """Print demo login credentials"""
    print("\n" + "=" * 60)
    print("    DEMO LOGIN CREDENTIALS")
    print("=" * 60)
    print("| Role    | Username | Password   |")
    print("|---------|----------|------------|")
    print("| Admin   | admin    | admin123   |")
    print("| Teacher | teacher1 | teacher123 |")
    print("| Student | student1 | student123 |")
    print("| Parent  | parent1  | parent123  |")
    print("=" * 60)

def print_next_steps():
    """Print next steps for the user"""
    print("\n" + "=" * 60)
    print("    NEXT STEPS")
    print("=" * 60)
    print("1. Start the application:")
    print("   python run.py")
    print()
    print("2. Open your web browser and go to:")
    print("   http://localhost:5000")
    print()
    print("3. Login using the demo credentials above")
    print()
    print("4. Explore the different user roles and features")
    print("=" * 60)

def main():
    """Main installation process"""
    print_header()
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Install requirements
    if not install_requirements():
        print("\n❌ Installation failed at package installation step")
        sys.exit(1)
    
    # Create directories
    if not create_directories():
        print("\n❌ Installation failed at directory creation step")
        sys.exit(1)
    
    # Initialize database
    if not initialize_database():
        print("\n❌ Installation failed at database initialization step")
        sys.exit(1)
    
    # Success message
    print("\n" + "=" * 60)
    print("    INSTALLATION COMPLETED SUCCESSFULLY! 🎉")
    print("=" * 60)
    
    # Print demo credentials
    print_demo_credentials()
    
    # Print next steps
    print_next_steps()

if __name__ == '__main__':
    main()