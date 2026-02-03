# ✅ Testing Guide - Verify Everything Works

## 🚀 Quick Test Steps

### Step 1: Start Application

```bash
cd C:\wamp64\www\secrete-santa
venv\Scripts\activate
python run.py
```

**Expected:** Server running on http://0.0.0.0:5000

---

### Step 2: Create Admin User (If Not Done)

```bash
python create_admin_direct.py
```

**Expected Output:**
```
✓ Admin user created successfully!
Email: admin@secretsanta.com
Password: admin123
```

---

### Step 3: Test Complete Workflow

#### 3.1 Login as Admin
1. Go to: http://localhost:5000/auth/admin-login
2. Email: `admin@secretsanta.com`
3. Password: `admin123`
4. **Expected:** Redirect to dashboard ✅

#### 3.2 Create Event
1. Click "Create Event"
2. Fill form:
   - Event Name: "Test Event"
   - Description: "Testing"
   - Budget: 500 - 2000
3. Click "Create Event"
4. **Expected:** Event created, redirect to event page ✅

#### 3.3 Add Wishlist
1. On event page, click "Add My Wishlist"
2. Fill form:
   - Category: Electronics
   - Preferences: Books, Coffee
   - Dislikes: Perfume
   - Hobbies: Reading, Gaming
3. Click "Save Wishlist"
4. **Expected:** Wishlist saved, redirect to event ✅

#### 3.4 Register Another User
1. Logout
2. Register new user:
   - Name: Test User
   - Email: test@example.com
   - Password: test123
3. **Expected:** Registration successful ✅

#### 3.5 Join Event
1. Login as new user
2. Click "Join Event"
3. Enter invite code from event
4. **Expected:** Successfully joined ✅

#### 3.6 Generate Assignments (Admin)
1. Login as admin
2. Go to event
3. Click "Manage Event"
4. Click "Generate Assignments"
5. **Expected:** Assignments generated ✅

#### 3.7 View Assignment & Wishlist
1. Login as user who got assignment
2. Go to event page
3. See "Your Secret Santa Assignment" card
4. Click "View Their Wishlist"
5. **Expected:** See receiver's wishlist ✅

#### 3.8 Update Gift Status
1. On wishlist view page
2. Change status dropdown
3. **Expected:** Status updated, success message ✅

---

## ✅ Verification Checklist

### Authentication
- [ ] Admin login works
- [ ] Regular login works
- [ ] Registration works
- [ ] Logout works

### Events
- [ ] Create event works
- [ ] View event works
- [ ] Join event works
- [ ] Invite code works

### Wishlist
- [ ] Add wishlist works
- [ ] Edit wishlist works
- [ ] View wishlist works
- [ ] Wishlist saves correctly

### Assignments
- [ ] Generate assignments works
- [ ] View assignment works
- [ ] View receiver's wishlist works
- [ ] Gift status update works

### Admin
- [ ] Admin dashboard accessible
- [ ] Manage event works
- [ ] Generate assignments works
- [ ] Reshuffle works

---

## 🔍 Common Issues & Fixes

### Issue: "ModuleNotFoundError"
**Fix:**
```bash
venv\Scripts\activate
pip install -r requirements.txt
```

### Issue: "Database connection failed"
**Fix:**
1. Check WAMP is GREEN
2. Verify database exists
3. Check config.py settings

### Issue: "Wishlist page not found"
**Fix:**
- Restart application
- Check routes are registered in `app/__init__.py`

### Issue: "Assignment not showing"
**Fix:**
- Make sure admin generated assignments
- Need at least 2 participants
- Check event status is 'active'

---

## 📊 Expected Behavior

### When Everything Works:

1. **Login** → Dashboard appears
2. **Create Event** → Event page with invite code
3. **Add Wishlist** → Form saves, button changes to "Edit"
4. **Join Event** → User added to participants
5. **Generate Assignments** → All participants get paired
6. **View Assignment** → See receiver's name
7. **View Wishlist** → See receiver's preferences
8. **Update Status** → Status changes, message appears

---

## 🎯 Quick Test Commands

```bash
# Test database connection
python -c "from app import create_app, db; app = create_app(); app.app_context().push(); db.session.execute(db.text('SELECT 1')); print('Database OK')"

# Check admin exists
python -c "from app import create_app, db; from app.models import User; app = create_app(); app.app_context().push(); admin = User.query.filter_by(email='admin@secretsanta.com').first(); print('Admin exists!' if admin else 'Admin NOT found')"

# Check tables
python -c "from app import create_app, db; from app.models import Event, User, Wishlist; app = create_app(); app.app_context().push(); print(f'Users: {User.query.count()}, Events: {Event.query.count()}, Wishlists: {Wishlist.query.count()}')"
```

---

## ✅ Success Indicators

You'll know it's working when:

1. ✅ Can login without errors
2. ✅ Can create events successfully
3. ✅ Can add/edit wishlist
4. ✅ Can see wishlist form
5. ✅ Can generate assignments
6. ✅ Can view receiver's wishlist
7. ✅ Can update gift status
8. ✅ No error messages in browser console
9. ✅ No errors in terminal/command prompt

---

**Run through the test steps above to verify everything works! 🎁**
