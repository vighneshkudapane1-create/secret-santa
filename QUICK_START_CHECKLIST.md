# ✅ Secret Santa - Quick Start Checklist

Use this checklist to set up your project step by step.

---

## 📋 Setup Checklist

### Pre-Setup
- [ ] Python 3.8+ installed (`python --version`)
- [ ] pip installed (`pip --version`)
- [ ] WAMP Server installed and running (GREEN icon)
- [ ] MySQL accessible via phpMyAdmin (`http://localhost/phpmyadmin`)

### Step 1: Navigate to Project
- [ ] Open Command Prompt
- [ ] Navigate to: `cd C:\wamp64\www\secrete-santa`
- [ ] Verify files are present (`dir` command)

### Step 2: Create Virtual Environment
- [ ] Run: `python -m venv venv`
- [ ] Activate: `venv\Scripts\activate`
- [ ] See `(venv)` in command prompt

### Step 3: Install Dependencies
- [ ] Run: `pip install -r requirements.txt`
- [ ] Verify: `pip list` shows Flask, SQLAlchemy, etc.

### Step 4: Create Database
- [ ] Open phpMyAdmin: `http://localhost/phpmyadmin`
- [ ] Create database: `secret_santa_db`
- [ ] Collation: `utf8mb4_unicode_ci`

### Step 5: Configure Database
- [ ] Open `config.py`
- [ ] Verify settings:
  - MYSQL_USER = 'root'
  - MYSQL_PASSWORD = '' (empty for WAMP)
  - MYSQL_DB = 'secret_santa_db'
- [ ] Save file

### Step 6: Create Tables
- [ ] Run: `python create_tables.py`
- [ ] See success message
- [ ] Verify in phpMyAdmin: 6 tables exist

### Step 7: Insert Sample Data (Optional)
- [ ] Run: `python sample_data_insert.py`
- [ ] See success message with counts
- [ ] Verify data in phpMyAdmin

### Step 8: Run Application
- [ ] Run: `python run.py`
- [ ] See: `Running on http://0.0.0.0:5000`
- [ ] Open browser: `http://localhost:5000`

### Step 9: Test Application
- [ ] Can see login/register page
- [ ] Can register new user
- [ ] Can login
- [ ] Can see dashboard
- [ ] Can create event
- [ ] Can join event

---

## 🚀 Quick Commands Reference

```bash
# Navigate to project
cd C:\wamp64\www\secrete-santa

# Activate virtual environment
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create tables
python create_tables.py

# Insert sample data
python sample_data_insert.py

# Run application
python run.py
```

---

## 🔧 Troubleshooting Quick Fixes

| Issue | Quick Fix |
|-------|-----------|
| ModuleNotFoundError | `pip install -r requirements.txt` |
| Can't connect to MySQL | Check WAMP is GREEN, verify config.py |
| Port 5000 in use | Change port in `run.py` to 5001 |
| Tables don't exist | Run `python create_tables.py` |
| Password error | Use `python sample_data_insert.py` |

---

## 📝 Test Credentials (After Sample Data)

**Admin:**
- Email: `admin@secretsanta.com`
- Password: `admin123`

**Regular User:**
- Email: `john.doe@example.com`
- Password: `user123`

**Event Invite Codes:**
- `XMAS2024` - Office Christmas
- `COLLEGE2024` - College Friends
- `FAMILY2024` - Family Christmas

---

## ✅ Success Indicators

You're all set when:
- ✅ Flask server runs without errors
- ✅ Can access `http://localhost:5000`
- ✅ Can register/login
- ✅ Can create/join events
- ✅ Database has data

---

**Need detailed instructions? See `STEP_BY_STEP_SETUP.md`**
