# 🚀 Secret Santa - Setup Instructions

## Prerequisites

Before setting up the project, ensure you have the following installed:

- **Python 3.8+** (Check with `python --version`)
- **MySQL 5.7+** or **MariaDB**
- **pip** (Python package manager)
- **Git** (optional, for version control)

## Step-by-Step Setup

### 1. Database Setup

#### Create MySQL Database

1. Open MySQL command line or phpMyAdmin
2. Create a new database:

```sql
CREATE DATABASE secret_santa_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

3. Create a user (optional, or use root):

```sql
CREATE USER 'santauser'@'localhost' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON secret_santa_db.* TO 'santauser'@'localhost';
FLUSH PRIVILEGES;
```

### 2. Configure Application

1. Open `config.py` in the project root
2. Update database credentials:

```python
MYSQL_HOST = 'localhost'
MYSQL_USER = 'root'  # or 'santauser'
MYSQL_PASSWORD = 'your_password'
MYSQL_DB = 'secret_santa_db'
MYSQL_PORT = 3306
```

3. Generate a secret key (optional, for production):

```python
import secrets
print(secrets.token_hex(32))
```

Update `SECRET_KEY` in `config.py` with the generated key.

### 3. Install Python Dependencies

1. Open terminal/command prompt in the project directory
2. Create virtual environment (recommended):

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

3. Install packages:

```bash
pip install -r requirements.txt
```

### 4. Initialize Database

The database tables will be created automatically when you first run the application. However, you can also create them manually:

```python
from app import create_app, db

app = create_app()
with app.app_context():
    db.create_all()
    print("Database tables created successfully!")
```

### 5. Run the Application

1. Start the Flask development server:

```bash
python run.py
```

2. Open your browser and navigate to:

```
http://localhost:5000
```

### 6. Create First Admin User (Optional)

You can create a super admin user directly in the database or through the registration page:

```python
from app import create_app, db
from app.models import User

app = create_app()
with app.app_context():
    admin = User(
        name='Admin User',
        email='admin@example.com',
        role='super_admin'
    )
    admin.set_password('admin123')
    db.session.add(admin)
    db.session.commit()
    print("Admin user created!")
```

## Project Structure Overview

```
secrete-santa/
├── app/                    # Main application
│   ├── routes/            # URL routes
│   ├── templates/         # HTML templates
│   ├── utils/             # Utility functions
│   └── models.py          # Database models
├── static/                # Static files (CSS, JS)
├── config.py              # Configuration
├── run.py                 # Application entry point
└── requirements.txt       # Dependencies
```

## Common Issues & Solutions

### Issue: ModuleNotFoundError

**Solution**: Make sure you're in the project root directory and virtual environment is activated.

### Issue: Database Connection Error

**Solution**: 
- Check MySQL is running
- Verify credentials in `config.py`
- Ensure database exists

### Issue: Port Already in Use

**Solution**: Change port in `run.py`:
```python
app.run(host='0.0.0.0', port=5001)  # Use different port
```

### Issue: Import Errors

**Solution**: Install all dependencies:
```bash
pip install --upgrade -r requirements.txt
```

## Development Tips

1. **Enable Debug Mode**: Already enabled in `run.py` for development
2. **Database Migrations**: For production, consider using Flask-Migrate
3. **Environment Variables**: Use `.env` file for sensitive data (install `python-dotenv`)
4. **Logging**: Check console for error messages

## Testing the Application

1. **Register a new user**: Go to `/auth/register`
2. **Create an event**: Login → Dashboard → Create Event
3. **Join event**: Use the invite code from event details
4. **Generate assignments**: As admin, go to event dashboard → Generate Assignments

## Production Deployment

For production deployment:

1. Set `FLASK_ENV=production` in environment
2. Update `SECRET_KEY` with a strong random key
3. Set `SESSION_COOKIE_SECURE = True` in `config.py` (requires HTTPS)
4. Use a production WSGI server (Gunicorn, uWSGI)
5. Configure proper database backups
6. Set up email service for notifications

## Support

For issues or questions, refer to:
- `README.md` - Project overview
- `PROJECT_STRUCTURE.md` - Detailed file structure
- Flask documentation: https://flask.palletsprojects.com/

---

**Happy Coding! 🎁🎄**
