@echo off
echo UnityCare Healthcare Management System - Installation Script
echo ============================================================

echo.
echo Checking Python installation...
python --version
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher from https://python.org
    pause
    exit /b 1
)

echo.
echo Creating virtual environment...
python -m venv venv
if %errorlevel% neq 0 (
    echo ERROR: Failed to create virtual environment
    pause
    exit /b 1
)

echo.
echo Activating virtual environment...
call venv\Scripts\activate.bat

echo.
echo Installing dependencies...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo Setting up database...
cd unitycare
python manage.py makemigrations
python manage.py migrate

echo.
echo Installation completed successfully!
echo.
echo To start the application:
echo 1. Activate virtual environment: venv\Scripts\activate.bat
echo 2. Navigate to project: cd unitycare
echo 3. Start server: python manage.py runserver
echo 4. Open browser: http://127.0.0.1:8000/
echo.
pause