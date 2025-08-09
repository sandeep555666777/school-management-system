@echo off
echo ============================================================
echo     SCHOOL MANAGEMENT SYSTEM - STARTING APPLICATION
echo ============================================================
echo.

echo Checking if database exists...
if not exist "school_management_dev.db" (
    echo Database not found. Running initialization...
    python init_db.py
    echo.
)

echo Starting the School Management System...
echo.
echo The application will be available at: http://localhost:5000
echo.
echo Demo Credentials:
echo Admin:   admin / admin123
echo Teacher: teacher1 / teacher123
echo Student: student1 / student123
echo Parent:  parent1 / parent123
echo.
echo Press Ctrl+C to stop the server
echo.

python run.py