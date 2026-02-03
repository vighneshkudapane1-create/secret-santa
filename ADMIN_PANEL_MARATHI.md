# 🔐 Secret Santa - Admin Panel Access (मराठी)

## ⚡ Application चालवण्यासाठी Commands (Admin Panel सह)

### Step 1: प्रोजेक्ट फोल्डरमध्ये जा
```bash
cd C:\wamp64\www\secrete-santa
```

### Step 2: Virtual Environment Activate करा
```bash
venv\Scripts\activate
```

### Step 3: Application चालवा
```bash
python run.py
```

### Step 4: Browser उघडा
```
http://localhost:5000
```

---

## 🔑 Admin Panel Access करणे

### Method 1: Sample Data वापरून (जर आधीच Insert केले असेल)

1. **Admin म्हणून Login करा:**
   - जा: http://localhost:5000/auth/login
   - Email: `admin@secretsanta.com`
   - Password: `admin123`

2. **Admin Dashboard Access करा:**
   - Login नंतर, तुम्ही तयार केलेल्या कोणत्याही Event वर जा
   - **"Manage Event"** button click करा
   - किंवा: http://localhost:5000/admin/event/[event_id]

### Method 2: Command द्वारे Admin User तयार करा

Admin user तयार करण्यासाठी हा command run करा:

```bash
python create_admin_user.py
```

---

## 👤 Admin User तयार करणे

### Command द्वारे:
```bash
python create_admin_user.py
```

**Output:**
```
✓ Admin user created successfully!
Email: admin@secretsanta.com
Password: admin123
```

---

## 🎯 Admin Panel Features

Admin म्हणून login केल्यानंतर, तुम्ही करू शकता:

1. **Event Management Dashboard**
   - सर्व participants पाहणे
   - Assignment statistics पाहणे
   - Secret Santa assignments generate करणे
   - Assignments reshuffle करणे

2. **Access URLs:**
   - Admin Dashboard: `http://localhost:5000/admin/event/[event_id]`
   - Generate Assignments: "Generate Assignments" button click करा
   - Reshuffle: "Reshuffle Assignments" button click करा

---

## 📋 Complete Command Sequence

```bash
# 1. प्रोजेक्ट फोल्डरमध्ये जा
cd C:\wamp64\www\secrete-santa

# 2. Virtual Environment Activate करा
venv\Scripts\activate

# 3. Admin User तयार करा (पहिल्यांदा फक्त)
python create_admin_user.py

# 4. Application चालवा
python run.py
```

नंतर browser उघडा: http://localhost:5000

---

## 🌐 Admin Panel URLs

- **Login:** http://localhost:5000/auth/login
- **Dashboard:** http://localhost:5000/dashboard
- **Admin Event Dashboard:** http://localhost:5000/admin/event/[event_id]
- **All Events:** http://localhost:5000/events

---

## 🔐 Admin Credentials (Sample Data नंतर)

**Super Admin:**
- Email: `admin@secretsanta.com`
- Password: `admin123`

**Event Manager:**
- Email: `manager@secretsanta.com`
- Password: `manager123`

---

## 📝 Quick Reference

| काम | Command/URL |
|------|-------------|
| Application चालवा | `python run.py` |
| Admin User तयार करा | `python create_admin_user.py` |
| Login URL | http://localhost:5000/auth/login |
| Admin Dashboard | http://localhost:5000/admin/event/[id] |
| Server थांबवा | `Ctrl + C` |

---

## ✅ Steps Summary

1. ✅ `cd C:\wamp64\www\secrete-santa`
2. ✅ `venv\Scripts\activate`
3. ✅ `python create_admin_user.py` (पहिल्यांदा)
4. ✅ `python run.py`
5. ✅ Browser: http://localhost:5000
6. ✅ Login: admin@secretsanta.com / admin123
7. ✅ Event create करा किंवा existing event वर जा
8. ✅ "Manage Event" click करा → Admin Panel!

---

## 💡 Tips

- **पहिल्यांदा:** `python create_admin_user.py` run करा
- **दर वेळी:** फक्त `python run.py` run करा
- **Admin Panel:** Event create केल्यानंतर "Manage Event" button दिसेल
- **Assignments:** किमान 2 participants असणे आवश्यक

---

**तयार! आता तुम्ही Admin Panel वापरू शकता! 🎁**
