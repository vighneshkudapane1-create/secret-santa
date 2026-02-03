# 🔧 Admin Login Fix - Step by Step Solution

## Problem: "Invalid email or password" when trying to login as admin

---

## ✅ Quick Fix (Recommended)

### Step 1: Run the Fix Script

Open Command Prompt and run:

```bash
cd C:\wamp64\www\secrete-santa
venv\Scripts\activate
python fix_admin_login.py
```

This script will:
- ✅ Check database connection
- ✅ Create admin user if doesn't exist
- ✅ Reset admin password if exists
- ✅ Verify everything works

### Step 2: Login Again

After running the script, try logging in:
- **Email:** `admin@secretsanta.com`
- **Password:** `admin123`

---

## 🔍 Manual Troubleshooting Steps

### Step 1: Check if Admin User Exists

Run this in Python:

```bash
python
```

Then paste:

```python
from app import create_app, db
from app.models import User

app = create_app()
with app.app_context():
    admin = User.query.filter_by(email='admin@secretsanta.com').first()
    if admin:
        print(f"Admin exists: {admin.name}")
        print(f"Role: {admin.role}")
        print(f"Active: {admin.is_active}")
    else:
        print("Admin user NOT found!")
```

### Step 2: Create/Reset Admin User

If admin doesn't exist or password is wrong, run:

```bash
python create_admin_user.py
```

Or manually:

```python
from app import create_app, db
from app.models import User

app = create_app()
with app.app_context():
    # Delete old admin if exists
    old_admin = User.query.filter_by(email='admin@secretsanta.com').first()
    if old_admin:
        db.session.delete(old_admin)
        db.session.commit()
    
    # Create new admin
    admin = User(
        name='Admin User',
        email='admin@secretsanta.com',
        role='super_admin',
        is_active=True
    )
    admin.set_password('admin123')
    db.session.add(admin)
    db.session.commit()
    print("Admin created successfully!")
```

### Step 3: Verify Database Connection

Check `config.py`:

```python
MYSQL_HOST = 'localhost'
MYSQL_USER = 'root'
MYSQL_PASSWORD = ''  # Empty for WAMP
MYSQL_DB = 'secret_santa_db'
MYSQL_PORT = 3306
```

### Step 4: Check if Tables Exist

Run:

```bash
python create_tables.py
```

---

## 🎯 Common Issues & Solutions

### Issue 1: Admin User Doesn't Exist

**Solution:**
```bash
python fix_admin_login.py
```

### Issue 2: Wrong Password Hash

**Solution:**
The fix script will reset the password with correct hash.

### Issue 3: Database Connection Failed

**Solution:**
1. Check WAMP is running (GREEN icon)
2. Verify database exists: `secret_santa_db`
3. Check `config.py` settings
4. Test connection: `mysql -u root -p`

### Issue 4: User is Inactive

**Solution:**
```python
from app import create_app, db
from app.models import User

app = create_app()
with app.app_context():
    admin = User.query.filter_by(email='admin@secretsanta.com').first()
    if admin:
        admin.is_active = True
        db.session.commit()
        print("Admin activated!")
```

### Issue 5: Email Case Sensitivity

**Solution:**
The login code converts email to lowercase, so use:
- `admin@secretsanta.com` (lowercase)

---

## 📋 Complete Fix Procedure

### Method 1: Using Fix Script (Easiest)

```bash
# 1. Navigate to project
cd C:\wamp64\www\secrete-santa

# 2. Activate virtual environment
venv\Scripts\activate

# 3. Run fix script
python fix_admin_login.py

# 4. Start application
python run.py

# 5. Login with:
#    Email: admin@secretsanta.com
#    Password: admin123
```

### Method 2: Manual Fix

```bash
# 1. Create admin user
python create_admin_user.py

# 2. If that doesn't work, use fix script
python fix_admin_login.py
```

---

## ✅ Verification Steps

After fixing, verify:

1. **Check Admin User:**
```python
from app import create_app, db
from app.models import User

app = create_app()
with app.app_context():
    admin = User.query.filter_by(email='admin@secretsanta.com').first()
    print(f"Email: {admin.email}")
    print(f"Password check: {admin.check_password('admin123')}")
```

2. **Test Login:**
   - Go to: http://localhost:5000/auth/login
   - Email: `admin@secretsanta.com`
   - Password: `admin123`
   - Should login successfully

---

## 🔐 Default Admin Credentials

After running fix script:

- **Email:** `admin@secretsanta.com`
- **Password:** `admin123`
- **Role:** `super_admin`

---

## 💡 Tips

1. **Always use the fix script first** - It handles all issues automatically
2. **Check database connection** - Most issues are due to DB connection
3. **Verify tables exist** - Run `python create_tables.py` if needed
4. **Check WAMP status** - Must be GREEN (running)
5. **Use lowercase email** - Email is converted to lowercase in login

---

## 🚨 Still Not Working?

If login still doesn't work:

1. **Check application logs** - Look at terminal/command prompt for errors
2. **Verify database** - Check phpMyAdmin: `http://localhost/phpmyadmin`
3. **Check user table** - Run SQL: `SELECT * FROM users WHERE email='admin@secretsanta.com';`
4. **Test password hash** - The fix script verifies this automatically

---

**Run `python fix_admin_login.py` - This should fix 99% of admin login issues!**
