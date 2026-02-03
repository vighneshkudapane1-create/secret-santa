# 🚀 Secret Santa - Complete Step-by-Step Setup Guide

This guide will walk you through setting up the Secret Santa project from scratch, step by step.

---

## 📋 Prerequisites Checklist

Before starting, make sure you have:

- ✅ **Python 3.8 or higher** installed
- ✅ **MySQL 5.7+ or MariaDB** installed and running
- ✅ **WAMP/XAMPP** (since you're using WAMP64)
- ✅ **Text Editor/IDE** (VS Code, PyCharm, etc.)
- ✅ **Command Prompt/Terminal** access

---

## STEP 1: Verify Python Installation

### 1.1 Check Python Version

Open Command Prompt (Press `Win + R`, type `cmd`, press Enter) and run:

```bash
python --version
```

**Expected Output:** `Python 3.8.x` or higher

**If Python is not installed:**
- Download from: https://www.python.org/downloads/
- During installation, check "Add Python to PATH"

### 1.2 Check pip (Python Package Manager)

```bash
pip --version
```

**Expected Output:** `pip 20.x.x` or higher

---

## STEP 2: Verify MySQL/WAMP Setup

### 2.1 Start WAMP Server

1. Open **WAMP Server** from Start Menu
2. Wait for the icon to turn **GREEN** (means MySQL is running)
3. If it's **ORANGE** or **RED**, click the icon and select "Start All Services"

### 2.2 Access phpMyAdmin

1. Open browser and go to: `http://localhost/phpmyadmin`
2. You should see the phpMyAdmin interface
3. Default username: `root`
4. Default password: (usually empty/blank)

### 2.3 Test MySQL Connection

Open Command Prompt and run:

```bash
mysql -u root -p
```

Press Enter (if no password) or enter your MySQL password.

**If you see `mysql>` prompt, you're good!** Type `exit;` to leave.

---

## STEP 3: Navigate to Project Directory

### 3.1 Open Command Prompt

Press `Win + R`, type `cmd`, press Enter

### 3.2 Navigate to Project Folder

```bash
cd C:\wamp64\www\secrete-santa
```

**Verify you're in the right folder:**

```bash
dir
```

You should see files like `run.py`, `config.py`, `requirements.txt`, etc.

---

## STEP 4: Create Virtual Environment (Recommended)

### 4.1 Create Virtual Environment

```bash
python -m venv venv
```

This creates a folder named `venv` in your project directory.

### 4.2 Activate Virtual Environment

**For Windows:**

```bash
venv\Scripts\activate
```

**You should see `(venv)` at the beginning of your command prompt:**

```
(venv) C:\wamp64\www\secrete-santa>
```

**If activation doesn't work, try:**

```bash
.\venv\Scripts\activate
```

---

## STEP 5: Install Python Dependencies

### 5.1 Install Required Packages

Make sure you're in the project directory and virtual environment is activated, then run:

```bash
pip install -r requirements.txt
```

**This will install:**
- Flask
- Flask-SQLAlchemy
- Flask-Login
- PyMySQL
- And other dependencies

### 5.2 Verify Installation

```bash
pip list
```

You should see Flask, SQLAlchemy, and other packages listed.

---

## STEP 6: Create MySQL Database

### 6.1 Open phpMyAdmin

1. Go to: `http://localhost/phpmyadmin`
2. Click on **"New"** in the left sidebar

### 6.2 Create Database

1. **Database name:** `secret_santa_db`
2. **Collation:** Select `utf8mb4_unicode_ci`
3. Click **"Create"** button

**OR use SQL:**

Click on **"SQL"** tab and run:

```sql
CREATE DATABASE secret_santa_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 6.3 Verify Database Created

You should see `secret_santa_db` in the left sidebar.

---

## STEP 7: Configure Database Connection

### 7.1 Open config.py

Open `config.py` file in your text editor/IDE.

### 7.2 Update Database Settings

Find these lines and update if needed:

```python
MYSQL_HOST = 'localhost'
MYSQL_USER = 'root'           # Usually 'root' for WAMP
MYSQL_PASSWORD = ''           # Usually empty for WAMP
MYSQL_DB = 'secret_santa_db'  # Database name you created
MYSQL_PORT = 3306             # Default MySQL port
```

**For WAMP, usually:**
- User: `root`
- Password: (empty/blank)
- Host: `localhost`
- Port: `3306`

### 7.3 Save the File

Save `config.py` after making changes.

---

## STEP 8: Create Database Tables

### 8.1 Method 1: Using Python (Recommended)

Run this command:

```bash
python -c "from app import create_app, db; app = create_app(); app.app_context().push(); db.create_all(); print('Tables created successfully!')"
```

**OR create a simple script:**

Create a file named `create_tables.py`:

```python
from app import create_app, db

app = create_app()
with app.app_context():
    db.create_all()
    print("✓ Database tables created successfully!")
```

Then run:

```bash
python create_tables.py
```

### 8.2 Method 2: Using SQL File

1. Open phpMyAdmin
2. Select `secret_santa_db` database
3. Click **"Import"** tab
4. Click **"Choose File"**
5. Select `database_schema.sql` from your project folder
6. Click **"Go"** button

### 8.3 Verify Tables Created

In phpMyAdmin:
1. Select `secret_santa_db` database
2. You should see 6 tables:
   - `users`
   - `events`
   - `participants`
   - `wishlists`
   - `assignments`
   - `messages`

---

## STEP 9: Insert Sample Data (Optional but Recommended)

### 9.1 Method 1: Using Python Script (Recommended)

Run:

```bash
python sample_data_insert.py
```

**You should see output like:**

```
Starting data insertion...
Inserting users...
✓ Inserted 12 users
Inserting events...
✓ Inserted 3 events
...
DATA INSERTION COMPLETE!
```

### 9.2 Method 2: Using SQL File

1. Open phpMyAdmin
2. Select `secret_santa_db` database
3. Click **"Import"** tab
4. Choose `database_insert_queries.sql`
5. Click **"Go"**

### 9.3 Verify Data Inserted

In phpMyAdmin, run:

```sql
SELECT 'Users' as Table, COUNT(*) as Count FROM users
UNION ALL
SELECT 'Events', COUNT(*) FROM events
UNION ALL
SELECT 'Participants', COUNT(*) FROM participants;
```

You should see counts for each table.

---

## STEP 10: Run the Application

### 10.1 Start Flask Server

Make sure you're in the project directory with virtual environment activated, then run:

```bash
python run.py
```

**You should see output like:**

```
 * Running on http://0.0.0.0:5000
 * Debug mode: on
```

### 10.2 Open in Browser

Open your web browser and go to:

```
http://localhost:5000
```

**OR**

```
http://127.0.0.1:5000
```

### 10.3 You Should See

- Login page (if not logged in)
- Or Dashboard (if you inserted sample data and want to login)

---

## STEP 11: Test the Application

### 11.1 Register a New User

1. Click **"Register"** link
2. Fill in the form:
   - Name: Your Name
   - Email: your@email.com
   - Password: yourpassword
   - Confirm Password: yourpassword
3. Click **"Create Account"**

### 11.2 Login

1. Use the credentials you just created
2. Or use sample data credentials:
   - Email: `admin@secretsanta.com`
   - Password: `admin123`

### 11.3 Create an Event

1. After login, click **"Create Event"**
2. Fill in:
   - Event Name: Test Event
   - Description: My first Secret Santa
   - Budget: 500 - 2000
   - Click **"Create Event"**

### 11.4 Join an Event

1. Click **"Join Event"**
2. Enter invite code: `XMAS2024` (from sample data)
3. Click **"Join Event"**

### 11.5 Test Admin Features

1. Login as admin: `admin@secretsanta.com` / `admin123`
2. Go to an event you created
3. Click **"Manage Event"**
4. Click **"Generate Assignments"** (if you have 2+ participants)

---

## STEP 12: Troubleshooting Common Issues

### Issue 1: "ModuleNotFoundError"

**Solution:**
```bash
# Make sure virtual environment is activated
venv\Scripts\activate

# Reinstall dependencies
pip install -r requirements.txt
```

### Issue 2: "Can't connect to MySQL server"

**Solution:**
1. Check WAMP is running (icon should be GREEN)
2. Verify MySQL is running in WAMP
3. Check `config.py` database settings
4. Test connection: `mysql -u root -p`

### Issue 3: "Table doesn't exist"

**Solution:**
```bash
# Recreate tables
python create_tables.py
```

### Issue 4: "Port 5000 already in use"

**Solution:**
Edit `run.py` and change port:

```python
app.run(host='0.0.0.0', port=5001)  # Use different port
```

### Issue 5: "Password hash error"

**Solution:**
- Use the Python script (`sample_data_insert.py`) instead of SQL
- It automatically generates correct password hashes

---

## STEP 13: Verify Everything Works

### 13.1 Checklist

- ✅ Python installed and working
- ✅ MySQL/WAMP running
- ✅ Database created
- ✅ Tables created
- ✅ Sample data inserted (optional)
- ✅ Flask server running
- ✅ Can access `http://localhost:5000`
- ✅ Can register/login
- ✅ Can create events
- ✅ Can join events

---

## 📝 Quick Reference Commands

### Start Development Server

```bash
# Activate virtual environment
venv\Scripts\activate

# Run application
python run.py
```

### Create Tables

```bash
python create_tables.py
```

### Insert Sample Data

```bash
python sample_data_insert.py
```

### Install New Package

```bash
pip install package_name
pip freeze > requirements.txt  # Update requirements
```

---

## 🎯 Next Steps After Setup

1. **Explore the Dashboard** - See all your events
2. **Create Your First Event** - Test the full workflow
3. **Join Events** - Use invite codes to join
4. **Test Assignments** - Generate Secret Santa pairs
5. **Customize** - Modify templates, add features

---

## 📞 Need Help?

### Check Logs

If something doesn't work, check the terminal/command prompt for error messages.

### Common Files to Check

- `config.py` - Database configuration
- `run.py` - Application entry point
- `app/__init__.py` - Flask app setup
- `app/models.py` - Database models

### Database Issues

- Check phpMyAdmin: `http://localhost/phpmyadmin`
- Verify database exists: `secret_santa_db`
- Check tables are created

---

## ✅ Success Indicators

You'll know everything is working when:

1. ✅ Flask server starts without errors
2. ✅ You can access `http://localhost:5000`
3. ✅ You can register and login
4. ✅ You can create events
5. ✅ You can see events in dashboard
6. ✅ Database has tables and data

---

**Congratulations! Your Secret Santa application is now set up and ready to use! 🎁🎄**

If you encounter any issues, refer to the troubleshooting section or check the error messages in your terminal.
