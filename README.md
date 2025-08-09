# School Management System

A comprehensive, fully functional web-based school management system built with Flask, featuring complete student management, teacher portals, parent access, fee management, library system, and mobile-responsive design. All panels are fully functional with real-time data operations.

## Features

### 🎓 Student Management
- Student enrollment and profile management
- Grade tracking and report cards
- Attendance monitoring
- Assignment submissions

### 👨‍🏫 Teacher Portal
- Class and subject management
- Attendance marking
- Grade entry and management
- Assignment creation

### 👨‍👩‍👧‍👦 Parent Portal
- View children's academic progress
- Attendance tracking
- Fee payment status
- Communication with teachers

### 💰 Fee Management
- Fee collection and tracking
- Payment history
- Overdue notifications
- Financial reporting

### 📚 Library Management
- Book catalog management
- Issue and return tracking
- Fine calculation
- Reading statistics

### 📊 Administrative Dashboard
- Comprehensive analytics
- User management
- System configuration
- Reports generation

## Technology Stack

- **Backend**: Python Flask
- **Database**: SQLite (development) / MySQL (production)
- **Frontend**: HTML5, CSS3, Bootstrap 5, JavaScript
- **Authentication**: Flask-Login
- **ORM**: SQLAlchemy

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Setup Instructions

1. **Clone or download the project**
   ```bash
   # If you have the files, navigate to the project directory
   cd school-management-system
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   python -m venv venv
   
   # Activate virtual environment
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Initialize the database with sample data**
   ```bash
   python init_sample_data.py
   ```

5. **Run the application**
   ```bash
   python app.py
   ```

6. **Access the application**
   Open your web browser and go to: `http://localhost:5000`

## Demo Credentials

After running `python init_sample_data.py`, you can use these demo accounts:

| Role | Username | Password |
|------|----------|----------|
| Admin | admin | admin123 |
| Teacher | teacher1@school.com | teacher123 |
| Student | student1@school.com | student123 |
| Parent | parent1@school.com | parent123 |

**Note**: The system includes comprehensive sample data including students, teachers, classes, subjects, fees, books, attendance records, and grades for testing all functionality.

## Configuration

### Database Configuration

**For Development (SQLite - Default):**
The application uses SQLite by default, which requires no additional setup.

**For Production (MySQL):**
1. Install MySQL server
2. Create a database named `school_management`
3. Update the database URL in `config.py`:
   ```python
   SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://username:password@localhost/school_management'
   ```
4. Install PyMySQL: `pip install PyMySQL`

### Environment Variables

You can set these environment variables to customize the application:

- `FLASK_CONFIG`: Set to 'development', 'production', or 'testing'
- `SECRET_KEY`: Your secret key for session management
- `DATABASE_URL`: Database connection string

## Project Structure

```
school-management-system/
├── app.py                 # Main application file
├── config.py             # Configuration settings
├── init_db.py            # Database initialization script
├── run.py                # Application runner
├── requirements.txt      # Python dependencies
├── README.md            # This file
└── templates/           # HTML templates
    ├── base.html        # Base template
    ├── index.html       # Home page
    ├── login.html       # Login page
    ├── admin_dashboard.html
    ├── teacher_dashboard.html
    ├── student_dashboard.html
    ├── parent_dashboard.html
    └── admin/           # Admin templates
        └── students.html
```

## Key Features Explained

### Role-Based Access Control
- **Admin**: Full system access, user management, reports
- **Teacher**: Class management, attendance, grades
- **Student**: View grades, attendance, assignments
- **Parent**: Monitor children's progress, communicate with teachers

### Mobile Responsive Design
- **Fully responsive interface** that works perfectly on desktop, tablet, and mobile devices
- **Touch-friendly navigation** with collapsible sidebar and optimized touch targets (44px minimum)
- **Mobile-first CSS** with custom mobile.css for comprehensive mobile optimization
- **Optimized forms** with proper input types to prevent zoom on iOS devices
- **Responsive tables** with horizontal scrolling and touch-friendly controls
- **Mobile-optimized modals** and dialogs that fit perfectly on small screens
- **Cross-device compatibility** tested on iOS Safari, Android Chrome, and various screen sizes

### Security Features
- Password hashing using Werkzeug
- Session management with Flask-Login
- Role-based route protection
- CSRF protection ready

## Customization

### Adding New Features
1. Define new database models in `app.py`
2. Create corresponding routes and views
3. Add HTML templates in the `templates/` directory
4. Update navigation in `base.html`

### Styling
- The application uses Bootstrap 5 for styling
- Custom CSS can be added to the `<style>` section in `base.html`
- Color scheme and branding can be easily modified

## Troubleshooting

### Common Issues

1. **Database errors**: Make sure to run `python init_db.py` before starting the application
2. **Port already in use**: Change the port in `run.py` or stop other applications using port 5000
3. **Module not found**: Ensure all dependencies are installed with `pip install -r requirements.txt`

### Getting Help

If you encounter issues:
1. Check the console output for error messages
2. Ensure all dependencies are properly installed
3. Verify database initialization completed successfully

## Future Enhancements

- Email notifications
- SMS integration
- Online exam system
- Video conferencing integration
- Mobile app development
- Advanced reporting and analytics
- Multi-language support

## License

This project is open source and available under the MIT License.

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.