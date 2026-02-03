# 🔐 Secret Santa - Admin Panel Access Guide

## Quick Commands to Run Application (Includes Admin Panel)

### Step 1: Navigate to Project
```bash
cd C:\wamp64\www\secrete-santa
```

### Step 2: Activate Virtual Environment
```bash
venv\Scripts\activate
```

### Step 3: Run Application
```bash
python run.py
```

### Step 4: Open Browser
```
http://localhost:5000
```

---

## Accessing Admin Panel

### Method 1: Using Sample Data (If Already Inserted)

1. **Login as Admin:**
   - Go to: http://localhost:5000/auth/login
   - Email: `admin@secretsanta.com`
   - Password: `admin123`

2. **Access Admin Dashboard:**
   - After login, go to any event you created
   - Click **"Manage Event"** button
   - OR go to: http://localhost:5000/admin/event/[event_id]

### Method 2: Create Admin User via Command

Run this command to create an admin user:

```bash
python create_admin_user.py
```

Or manually in Python:

```bash
python
```

Then paste:

```python
from app import create_app, db
from app.models import User

app = create_app()
with app.app_context():
    admin = User(
        name='Admin User',
        email='admin@secretsanta.com',
        role='super_admin'
    )
    admin.set_password('admin123')
    db.session.add(admin)
    db.session.commit()
    print("Admin user created!")
    print("Email: admin@secretsanta.com")
    print("Password: admin123")
```

Press `Ctrl + Z` then Enter to exit Python.

---

## Admin Panel Features

Once logged in as admin, you can:

1. **Event Management Dashboard**
   - View all participants
   - See assignment statistics
   - Generate Secret Santa assignments
   - Reshuffle assignments

2. **Access URLs:**
   - Admin Dashboard: `http://localhost:5000/admin/event/[event_id]`
   - Generate Assignments: Click "Generate Assignments" button
   - Reshuffle: Click "Reshuffle Assignments" button

---

## Create Admin User Script

Create a file `create_admin_user.py`:

```python
from app import create_app, db
from app.models import User

def create_admin():
    app = create_app()
    with app.app_context():
        # Check if admin already exists
        existing = User.query.filter_by(email='admin@secretsanta.com').first()
        if existing:
            print("Admin user already exists!")
            return
        
        admin = User(
            name='Admin User',
            email='admin@secretsanta.com',
            role='super_admin'
        )
        admin.set_password('admin123')
        db.session.add(admin)
        db.session.commit()
        print("=" * 50)
        print("✓ Admin user created successfully!")
        print("=" * 50)
        print("Email: admin@secretsanta.com")
        print("Password: admin123")
        print("=" * 50)

if __name__ == '__main__':
    create_admin()
```

Then run:
```bash
python create_admin_user.py
```

---

## All-in-One Command Sequence

```bash
# Navigate to project
cd C:\wamp64\www\secrete-santa

# Activate virtual environment
venv\Scripts\activate

# Create admin user (if not exists)
python create_admin_user.py

# Run application
python run.py
```

Then open browser: http://localhost:5000

---

## Admin Panel URLs

- **Login:** http://localhost:5000/auth/login
- **Dashboard:** http://localhost:5000/dashboard
- **Admin Event Dashboard:** http://localhost:5000/admin/event/[event_id]
- **All Events:** http://localhost:5000/events

---

## Admin Credentials (After Sample Data)

**Super Admin:**
- Email: `admin@secretsanta.com`
- Password: `admin123`

**Event Manager:**
- Email: `manager@secretsanta.com`
- Password: `manager123`

---

## Quick Reference

| Task | Command/URL |
|------|-------------|
| Run Application | `python run.py` |
| Create Admin | `python create_admin_user.py` |
| Login URL | http://localhost:5000/auth/login |
| Admin Dashboard | http://localhost:5000/admin/event/[id] |
| Stop Server | `Ctrl + C` |

---

**Note:** The admin panel is part of the main application. Just run `python run.py` and login as admin to access admin features!
