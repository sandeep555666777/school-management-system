@echo off
echo ============================================================
echo     SCHOOL MANAGEMENT SYSTEM - WINDOWS INSTALLATION
echo ============================================================
echo.

echo Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher from https://python.org
    pause
    exit /b 1
)

echo Python found. Starting installation...
echo.

python install.py

echo.
echo Installation script completed.
echo.
echo To start the application, run: python run.py
echo Then open http://localhost:5000 in your browser
echo.
pause