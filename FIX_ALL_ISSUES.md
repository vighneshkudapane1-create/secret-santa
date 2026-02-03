# 🔧 Fix All Issues - Complete Solution

## Issue 1: Admin Login Not Working

### Solution: Create Admin User

Run this command:

```bash
python create_admin_direct.py
```

This will:
- ✅ Create admin user in database
- ✅ Set password as plain text: `admin123`
- ✅ Set role as `super_admin`
- ✅ Verify everything works

**Admin Credentials:**
- Email: `admin@secretsanta.com`
- Password: `admin123`

**Admin Login URL:** http://localhost:5000/auth/admin-login

---

## Issue 2: Event Creation Error

### Solution: Fixed Event Creation Route

The event creation route has been updated to:
- ✅ Handle datetime parsing errors properly
- ✅ Show specific error messages
- ✅ Fix participant creation issue (using flush())

### Test Event Creation:

1. **Login** first: http://localhost:5000/auth/login
2. Go to **Create Event**: http://localhost:5000/events/create
3. Fill form:
   - Event Name: "Test Event" (Required)
   - Other fields optional
4. Click **"Create Event"**

### If Still Getting Errors:

```bash
# 1. Check database connection
python -c "from app import create_app, db; app = create_app(); app.app_context().push(); db.session.execute(db.text('SELECT 1')); print('Database OK')"

# 2. Recreate tables
python create_tables.py

# 3. Create admin user
python create_admin_direct.py

# 4. Restart application
python run.py
```

---

## Complete Setup Commands

### Step 1: Navigate to Project
```bash
cd C:\wamp64\www\secrete-santa
```

### Step 2: Activate Virtual Environment
```bash
venv\Scripts\activate
```

### Step 3: Create/Update Database Tables
```bash
python create_tables.py
```

### Step 4: Create Admin User
```bash
python create_admin_direct.py
```

### Step 5: Run Application
```bash
python run.py
```

### Step 6: Access Application
- Regular Login: http://localhost:5000/auth/login
- Admin Login: http://localhost:5000/auth/admin-login

---

## Quick Fix Commands

### Fix Admin Login:
```bash
python create_admin_direct.py
```

### Fix Event Creation:
```bash
# Already fixed in code, just restart:
python run.py
```

### Fix Database Issues:
```bash
python create_tables.py
python create_admin_direct.py
```

---

## Verification Steps

### 1. Check Admin User Exists:
```bash
python -c "from app import create_app, db; from app.models import User; app = create_app(); app.app_context().push(); admin = User.query.filter_by(email='admin@secretsanta.com').first(); print('Admin exists!' if admin else 'Admin NOT found')"
```

### 2. Check Database Tables:
```bash
python -c "from app import create_app, db; from app.models import Event, User, Participant; app = create_app(); app.app_context().push(); print(f'Users: {User.query.count()}, Events: {Event.query.count()}, Participants: {Participant.query.count()}')"
```

### 3. Test Event Creation:
1. Login as admin
2. Go to Create Event
3. Fill minimal form (just event name)
4. Submit
5. Should redirect to event page

---

## Common Error Messages & Fixes

| Error Message | Solution |
|---------------|----------|
| "Invalid email or password" | Run: `python create_admin_direct.py` |
| "An error occurred while creating the event" | Check database connection, restart app |
| "Event name is required" | Fill event name field |
| "Invalid gift deadline format" | Use format: YYYY-MM-DDTHH:MM or leave empty |
| "Database connection failed" | Check WAMP is running, verify config.py |

---

## Files Updated

1. ✅ `app/routes/events.py` - Fixed event creation with better error handling
2. ✅ `create_admin_direct.py` - New script to create admin user
3. ✅ `EVENT_CREATION_GUIDE.md` - Complete guide for event creation

---

## Success Indicators

You'll know everything is working when:

1. ✅ Can login as admin: `admin@secretsanta.com` / `admin123`
2. ✅ Can see dashboard after login
3. ✅ Can access "Create Event" page
4. ✅ Can create event successfully
5. ✅ See success message and redirect to event page
6. ✅ Can see event details with invite code

---

**Run `python create_admin_direct.py` first, then test event creation!**
