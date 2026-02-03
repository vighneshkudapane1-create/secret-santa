# 🔧 Admin Login Fix - Step by Step Solution (मराठी)

## समस्या: Admin login करताना "Invalid email or password" error येतो

---

## ✅ जलद Fix (Recommended)

### Step 1: Fix Script Run करा

Command Prompt उघडा आणि run करा:

```bash
cd C:\wamp64\www\secrete-santa
venv\Scripts\activate
python fix_admin_login.py
```

हे script:
- ✅ Database connection तपासेल
- ✅ Admin user नसेल तर तयार करेल
- ✅ Admin user असेल तर password reset करेल
- ✅ सर्वकाही verify करेल

### Step 2: पुन्हा Login करा

Script run केल्यानंतर, login करा:
- **Email:** `admin@secretsanta.com`
- **Password:** `admin123`

---

## 🔍 Manual Troubleshooting Steps

### Step 1: Admin User आहे का तपासा

Python मध्ये run करा:

```bash
python
```

नंतर paste करा:

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

### Step 2: Admin User तयार/Reset करा

जर admin नसेल किंवा password चुकीचा असेल, run करा:

```bash
python create_admin_user.py
```

किंवा manually:

```python
from app import create_app, db
from app.models import User

app = create_app()
with app.app_context():
    # जुना admin असल्यास delete करा
    old_admin = User.query.filter_by(email='admin@secretsanta.com').first()
    if old_admin:
        db.session.delete(old_admin)
        db.session.commit()
    
    # नवीन admin तयार करा
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

### Step 3: Database Connection तपासा

`config.py` तपासा:

```python
MYSQL_HOST = 'localhost'
MYSQL_USER = 'root'
MYSQL_PASSWORD = ''  # WAMP साठी empty
MYSQL_DB = 'secret_santa_db'
MYSQL_PORT = 3306
```

### Step 4: Tables आहेत का तपासा

Run करा:

```bash
python create_tables.py
```

---

## 🎯 सामान्य समस्या आणि उपाय

### समस्या 1: Admin User नाही

**उपाय:**
```bash
python fix_admin_login.py
```

### समस्या 2: चुकीचा Password Hash

**उपाय:**
Fix script password reset करेल आणि बरोबर hash वापरेल.

### समस्या 3: Database Connection Failed

**उपाय:**
1. WAMP चालू आहे का तपासा (GREEN icon)
2. Database आहे का verify करा: `secret_santa_db`
3. `config.py` मध्ये settings तपासा
4. Connection test करा: `mysql -u root -p`

### समस्या 4: User Inactive आहे

**उपाय:**
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

### समस्या 5: Email Case Sensitivity

**उपाय:**
Login code email lowercase करते, म्हणून वापरा:
- `admin@secretsanta.com` (lowercase)

---

## 📋 Complete Fix Procedure

### Method 1: Fix Script वापरून (सर्वात सोपे)

```bash
# 1. प्रोजेक्ट फोल्डरमध्ये जा
cd C:\wamp64\www\secrete-santa

# 2. Virtual Environment Activate करा
venv\Scripts\activate

# 3. Fix script run करा
python fix_admin_login.py

# 4. Application start करा
python run.py

# 5. Login करा:
#    Email: admin@secretsanta.com
#    Password: admin123
```

### Method 2: Manual Fix

```bash
# 1. Admin user तयार करा
python create_admin_user.py

# 2. जर ते काम न करे, fix script वापरा
python fix_admin_login.py
```

---

## ✅ Verification Steps

Fix केल्यानंतर verify करा:

1. **Admin User तपासा:**
```python
from app import create_app, db
from app.models import User

app = create_app()
with app.app_context():
    admin = User.query.filter_by(email='admin@secretsanta.com').first()
    print(f"Email: {admin.email}")
    print(f"Password check: {admin.check_password('admin123')}")
```

2. **Login Test करा:**
   - जा: http://localhost:5000/auth/login
   - Email: `admin@secretsanta.com`
   - Password: `admin123`
   - Login यशस्वी होणे आवश्यक

---

## 🔐 Default Admin Credentials

Fix script run केल्यानंतर:

- **Email:** `admin@secretsanta.com`
- **Password:** `admin123`
- **Role:** `super_admin`

---

## 💡 Tips

1. **नेहमी fix script प्रथम वापरा** - ते सर्व समस्या automatically handle करते
2. **Database connection तपासा** - बहुतेक समस्या DB connection मुळे येतात
3. **Tables आहेत का verify करा** - आवश्यक असल्यास `python create_tables.py` run करा
4. **WAMP status तपासा** - GREEN (running) असणे आवश्यक
5. **Lowercase email वापरा** - Login मध्ये email lowercase होते

---

## 🚨 अजूनही काम न करत असेल?

जर login अजूनही काम न करत असेल:

1. **Application logs तपासा** - Terminal/Command Prompt मध्ये errors पहा
2. **Database verify करा** - phpMyAdmin तपासा: `http://localhost/phpmyadmin`
3. **User table तपासा** - SQL run करा: `SELECT * FROM users WHERE email='admin@secretsanta.com';`
4. **Password hash test करा** - Fix script हे automatically verify करते

---

## 📝 Quick Fix Commands

```bash
# सर्वात सोपा मार्ग
python fix_admin_login.py

# जर ते काम न करे
python create_admin_user.py

# Tables नसतील
python create_tables.py
```

---

**`python fix_admin_login.py` run करा - हे 99% admin login समस्या सोडवेल! 🎁**
