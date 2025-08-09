#!/usr/bin/env python3
"""
School Management System - Run Script
"""

import os
from app import app

if __name__ == '__main__':
    # Set environment variables if not already set
    if not os.environ.get('FLASK_CONFIG'):
        os.environ['FLASK_CONFIG'] = 'development'
    
    # Run the application
    app.run(
        host='0.0.0.0',  # Allow external connections
        port=5000,
        debug=True
    )