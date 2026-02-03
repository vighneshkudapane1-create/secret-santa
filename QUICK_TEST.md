# ⚡ Quick Test - Does It Work?

## 🎯 5-Minute Test

### Step 1: Verify Setup
```bash
python verify_setup.py
```

**Expected:** All checks pass ✅

### Step 2: Start Application
```bash
python run.py
```

**Expected:** `Running on http://0.0.0.0:5000`

### Step 3: Browser Test

1. **Open:** http://localhost:5000
2. **Login:** admin@secretsanta.com / admin123
3. **Create Event:** Fill form, submit
4. **Add Wishlist:** Click "Add My Wishlist", fill, save
5. **Check:** Wishlist saved, button shows "Edit"

**If all work → ✅ IT WORKS!**

---

## ✅ What Should Work

- [x] Login/Logout
- [x] Create Event
- [x] Add Wishlist
- [x] View Event
- [x] Join Event
- [x] Generate Assignments
- [x] View Assignment
- [x] View Receiver's Wishlist
- [x] Update Gift Status

---

## ❌ If Something Doesn't Work

### Check Terminal/Command Prompt
- Look for error messages
- Check if database connection OK
- Verify all routes loaded

### Common Fixes
```bash
# Fix admin
python create_admin_direct.py

# Fix tables
python create_tables.py

# Restart app
python run.py
```

---

**Run `python verify_setup.py` first to check everything! 🎁**
