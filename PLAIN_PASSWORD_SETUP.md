# 🔓 Plain Password Setup Guide

## Changes Made

1. ✅ **Removed Password Hashing** - Passwords are now stored as plain text
2. ✅ **Separate Admin Login Page** - Created `/auth/admin-login` route
3. ✅ **Updated Database Schema** - Changed `password_hash` to `password` column

---

## 📋 Setup Steps

### Step 1: Update Database Schema

If you have existing database with `password_hash` column, run:

```bash
python update_password_column.py
```

This will rename `password_hash` to `password` column.

**OR** if starting fresh, just use the updated `database_schema.sql` which already has `password` column.

### Step 2: Recreate Tables (If Needed)

If you want to start fresh:

```bash
# Drop and recreate tables
python create_tables.py
```

### Step 3: Create Admin User

```bash
python create_admin_user.py
```

This will create admin with plain text password: `admin123`

### Step 4: Run Application

```bash
python run.py
```

---

## 🔐 Admin Login

### Access Admin Login Page

**URL:** http://localhost:5000/auth/admin-login

**OR** click "Admin Login" link from:
- Navigation bar (when not logged in)
- Regular login page

### Admin Credentials

- **Email:** `admin@secretsanta.com`
- **Password:** `admin123`

### Features

- ✅ Separate admin login page with red theme
- ✅ Only users with `admin` or `super_admin` role can login
- ✅ Regular users will see "Access denied" message

---

## 📝 Regular User Login

Regular users can still login at:

**URL:** http://localhost:5000/auth/login

This works for all users (regular, admin, super_admin).

---

## 🔄 Migration from Hashed Passwords

If you have existing users with hashed passwords:

1. **Option 1:** Reset all passwords (recommended for development)
   ```bash
   python fix_admin_login.py
   ```

2. **Option 2:** Manually update passwords in database
   ```sql
   UPDATE users SET password = 'newpassword' WHERE email = 'user@example.com';
   ```

---

## ⚠️ Security Note

**Important:** Plain text passwords are **NOT secure** for production use!

This is suitable for:
- ✅ Development/Testing
- ✅ Internal applications
- ✅ Educational projects

**For production**, you should:
- Use password hashing (Werkzeug's `generate_password_hash`)
- Implement proper security measures
- Use HTTPS
- Add rate limiting

---

## 📁 Files Modified

1. `app/models.py` - Removed hashing, plain text password
2. `app/routes/auth.py` - Added admin login route, plain text comparison
3. `app/templates/auth/admin_login.html` - New admin login page
4. `app/templates/base.html` - Added admin login link
5. `app/templates/auth/login.html` - Added admin login link
6. `database_schema.sql` - Updated to use `password` column
7. `create_admin_user.py` - Updated for plain text
8. `fix_admin_login.py` - Updated for plain text

---

## ✅ Testing

1. **Test Regular Login:**
   - Go to: http://localhost:5000/auth/login
   - Login with any user credentials

2. **Test Admin Login:**
   - Go to: http://localhost:5000/auth/admin-login
   - Login with admin credentials
   - Regular users should see "Access denied"

3. **Test Navigation:**
   - Check "Admin Login" link in navigation
   - Check "Admin Login" link on regular login page

---

## 🎯 Quick Commands

```bash
# Update existing database
python update_password_column.py

# Create admin user
python create_admin_user.py

# Run application
python run.py
```

---

**Setup Complete! You now have plain text passwords and separate admin login page! 🎁**
