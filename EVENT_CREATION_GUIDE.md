# 🎁 Event Creation Guide - Step by Step

## How to Create an Event

### Step 1: Login
1. Go to: http://localhost:5000/auth/login
2. Login with your credentials
3. You'll be redirected to Dashboard

### Step 2: Navigate to Create Event
1. Click **"Create Event"** button on dashboard
   OR
2. Go to: http://localhost:5000/events/create

### Step 3: Fill Event Form

**Required Fields:**
- **Event Name** * (Required)
  - Example: "Office Christmas 2024"
  - Must be at least 1 character

**Optional Fields:**
- **Description**
  - Example: "Annual office Secret Santa gift exchange"
  
- **Minimum Budget**
  - Default: 0
  - Example: 500
  
- **Maximum Budget**
  - Default: 1000
  - Example: 2000
  
- **Currency**
  - Options: INR (₹), USD ($), EUR (€)
  - Default: INR

- **Gift Deadline** (Optional)
  - Format: Date and Time
  - Example: 2024-12-20 18:00
  - Leave empty if not needed

- **Event Date** (Optional)
  - Format: Date and Time
  - Example: 2024-12-25 19:00
  - Leave empty if not needed

### Step 4: Submit Form
1. Click **"Create Event"** button
2. If successful, you'll be redirected to event details page
3. You'll see success message: "Event '[name]' created successfully!"

---

## Common Errors & Solutions

### Error 1: "An error occurred while creating the event"

**Possible Causes:**
1. Database connection issue
2. Invalid date format
3. Missing required fields
4. Database constraint violation

**Solutions:**

#### Solution 1: Check Database Connection
```bash
# Verify database is running
# Check WAMP is GREEN
# Test connection
python -c "from app import create_app, db; app = create_app(); app.app_context().push(); db.session.execute(db.text('SELECT 1'))"
```

#### Solution 2: Check Date Format
- Gift Deadline and Event Date should be in format: `YYYY-MM-DDTHH:MM`
- Example: `2024-12-20T18:00`
- Leave empty if not needed

#### Solution 3: Verify Required Fields
- Event Name is required
- Make sure it's not empty

#### Solution 4: Check Database Tables
```bash
# Recreate tables if needed
python create_tables.py
```

#### Solution 5: Check Error Logs
- Look at terminal/command prompt for detailed error messages
- The updated code now shows specific error messages

---

### Error 2: "Event name is required"

**Solution:**
- Make sure Event Name field is filled
- It cannot be empty or just spaces

---

### Error 3: "Invalid gift deadline format" or "Invalid event date format"

**Solution:**
- Use correct datetime format: `YYYY-MM-DDTHH:MM`
- Example: `2024-12-20T18:00`
- Or leave the field empty

---

## Event Creation Process Flow

```
1. User fills form
   ↓
2. Form submitted (POST request)
   ↓
3. Server validates data
   - Event name required?
   - Dates valid format?
   ↓
4. Generate unique invite code
   ↓
5. Create Event object
   ↓
6. Add Event to database
   ↓
7. Add creator as first Participant
   ↓
8. Commit transaction
   ↓
9. Redirect to event details page
```

---

## Testing Event Creation

### Test Case 1: Minimal Event (Only Name)
1. Event Name: "Test Event"
2. Leave all other fields empty/default
3. Click "Create Event"
4. Should succeed

### Test Case 2: Full Event (All Fields)
1. Event Name: "Complete Event"
2. Description: "Test description"
3. Budget: 500 - 2000
4. Currency: INR
5. Gift Deadline: 2024-12-20T18:00
6. Event Date: 2024-12-25T19:00
7. Click "Create Event"
8. Should succeed

### Test Case 3: Invalid Date Format
1. Event Name: "Test"
2. Gift Deadline: "invalid-date"
3. Click "Create Event"
4. Should show error: "Invalid gift deadline format"

---

## After Event Creation

Once event is created:

1. **You'll be redirected** to event details page
2. **You'll see:**
   - Event name and description
   - Budget information
   - Invite code (for sharing)
   - "Manage Event" button (if you're admin)

3. **Next Steps:**
   - Share invite code with others
   - Participants can join using invite code
   - When ready, generate assignments

---

## Admin User Creation

To create admin user for admin login:

```bash
python create_admin_direct.py
```

This will create:
- Email: `admin@secretsanta.com`
- Password: `admin123`
- Role: `super_admin`

---

## Troubleshooting Commands

```bash
# Check database connection
python -c "from app import create_app, db; app = create_app(); app.app_context().push(); print('OK' if db.session.execute(db.text('SELECT 1')) else 'FAIL')"

# Create admin user
python create_admin_direct.py

# Recreate tables
python create_tables.py

# Check existing events
python -c "from app import create_app, db; from app.models import Event; app = create_app(); app.app_context().push(); events = Event.query.all(); print(f'Events: {len(events)}')"
```

---

## Quick Reference

| Field | Required | Format | Example |
|-------|----------|--------|---------|
| Event Name | Yes | Text | "Christmas 2024" |
| Description | No | Text | "Office party" |
| Min Budget | No | Number | 500 |
| Max Budget | No | Number | 2000 |
| Currency | No | Select | INR |
| Gift Deadline | No | DateTime | 2024-12-20T18:00 |
| Event Date | No | DateTime | 2024-12-25T19:00 |

---

**If you still get errors, check the terminal/command prompt for detailed error messages!**
