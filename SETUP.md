# UnityCare Healthcare Management System - Setup Guide

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)
- Git (for cloning the repository)

### Installation Options

#### Option 1: Full Installation (Recommended)
```bash
# Clone the repository
git clone <repository-url>
cd unitycareD

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install all dependencies
pip install -r requirements.txt
```

#### Option 2: Minimal Installation
```bash
# For a lighter installation with only essential dependencies
pip install -r requirements-minimal.txt
```

#### Option 3: Development Installation
```bash
# For developers who want testing and code quality tools
pip install -r requirements-dev.txt
```

### Database Setup
```bash
# Navigate to the Django project directory
cd unitycare

# Create database migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create a superuser (optional)
python manage.py createsuperuser
```

### Running the Application
```bash
# Start the development server
python manage.py runserver

# The application will be available at:
# http://127.0.0.1:8000/
```

## 📋 Features

### Core Functionality
- **User Management**: Patient, Doctor, and Hospital registration
- **Authentication**: Secure login/logout system
- **Dashboard**: Role-based dashboards for different user types
- **Appointments**: Booking and management system
- **Teleconferencing**: WebRTC-based video calls
- **REST API**: RESTful API for mobile/external integrations

### User Roles
1. **Patients**: Book appointments, join video calls, manage profile
2. **Doctors**: Manage appointments, conduct video consultations
3. **Hospitals**: Manage doctor listings, facility information

## 🔧 Configuration

### Environment Variables (Optional)
Create a `.env` file in the project root for production settings:
```env
DEBUG=False
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DATABASE_URL=your-database-url
```

### Static Files (Production)
```bash
# Collect static files for production
python manage.py collectstatic
```

## 🧪 Testing

### Run Tests
```bash
# If you installed development requirements
pytest

# Or using Django's test runner
python manage.py test
```

### Code Quality
```bash
# Format code
black .

# Check code style
flake8

# Sort imports
isort .
```

## 📱 API Endpoints

### Authentication
- `POST /accounts/login/` - User login
- `POST /accounts/logout/` - User logout
- `POST /accounts/signup/patient/` - Patient registration
- `POST /accounts/signup/doctor/` - Doctor registration
- `POST /accounts/signup/hospital/` - Hospital registration

### Appointments
- `GET /api/appointments/` - List appointments
- `POST /api/appointments/` - Create appointment
- `PUT /api/appointments/{id}/` - Update appointment
- `DELETE /api/appointments/{id}/` - Cancel appointment

### Users
- `GET /api/doctors/` - List doctors
- `GET /accounts/hospitals/` - List hospitals

## 🌐 WebSocket Endpoints

### Teleconferencing
- `ws://127.0.0.1:8000/ws/telecon/{room_name}/?role={doctor|patient}` - Video call room

## 🔒 Security Features

- CSRF protection enabled
- User authentication required for sensitive operations
- Role-based access control
- Secure password validation
- Session management

## 📦 Dependencies Overview

### Core Dependencies
- **Django 4.2.7**: Web framework
- **Django REST Framework**: API functionality
- **Django Channels**: WebSocket support
- **Pillow**: Image processing

### Optional Dependencies
- **Celery**: Background task processing
- **Redis**: Caching and message broker
- **Twilio**: SMS/Voice communication
- **Google Maps**: Location services

## 🚀 Deployment

### Production Checklist
1. Set `DEBUG = False` in settings
2. Configure proper `ALLOWED_HOSTS`
3. Set up a production database (PostgreSQL recommended)
4. Configure static file serving
5. Set up HTTPS
6. Configure email backend
7. Set up monitoring and logging

### Recommended Production Stack
- **Web Server**: Nginx
- **WSGI Server**: Gunicorn
- **Database**: PostgreSQL
- **Cache**: Redis
- **Task Queue**: Celery with Redis broker

## 🆘 Troubleshooting

### Common Issues

#### Import Errors
```bash
# Make sure you're in the correct directory and virtual environment is activated
cd unitycare
python manage.py check
```

#### Database Issues
```bash
# Reset database (WARNING: This will delete all data)
rm db.sqlite3
python manage.py migrate
```

#### Static Files Not Loading
```bash
# Collect static files
python manage.py collectstatic --clear
```

#### WebSocket Connection Issues
- Ensure channels is properly installed
- Check that ASGI application is configured
- Verify WebSocket URL patterns

### Getting Help
1. Check the Django documentation: https://docs.djangoproject.com/
2. Review Django Channels documentation: https://channels.readthedocs.io/
3. Check the project's issue tracker
4. Ensure all dependencies are properly installed

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Run the test suite
6. Submit a pull request

## 📞 Support

For support and questions, please contact the development team or create an issue in the project repository.