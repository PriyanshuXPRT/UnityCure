#!/bin/bash

echo "UnityCare Healthcare Management System - Installation Script"
echo "============================================================"

# Check if Python is installed
echo ""
echo "Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python 3.8 or higher"
    exit 1
fi

python3 --version

# Create virtual environment
echo ""
echo "Creating virtual environment..."
python3 -m venv venv
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to create virtual environment"
    exit 1
fi

# Activate virtual environment
echo ""
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo ""
echo "Installing dependencies..."
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install dependencies"
    exit 1
fi

# Setup database
echo ""
echo "Setting up database..."
cd unitycare
python manage.py makemigrations
python manage.py migrate

echo ""
echo "Installation completed successfully!"
echo ""
echo "To start the application:"
echo "1. Activate virtual environment: source venv/bin/activate"
echo "2. Navigate to project: cd unitycare"
echo "3. Start server: python manage.py runserver"
echo "4. Open browser: http://127.0.0.1:8000/"
echo ""