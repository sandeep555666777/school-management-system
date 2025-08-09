#!/usr/bin/env python3
"""
Railway production initialization script
This runs automatically when deployed to Railway
"""

from app import app, db
from init_sample_data import create_sample_data
import os

def initialize_production():
    """Initialize the production database with sample data"""
    with app.app_context():
        print("🚀 Initializing Railway production database...")
        
        # Create all tables
        db.create_all()
        print("✅ Database tables created")
        
        # Add sample data
        create_sample_data()
        print("✅ Sample data added")
        
        print("🎉 Railway initialization complete!")

if __name__ == "__main__":
    initialize_production()