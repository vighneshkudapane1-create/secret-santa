# 📝 Secret Santa - INSERT Queries Guide

## Overview

This guide provides INSERT queries and methods to populate your Secret Santa database with sample data for testing and development.

---

## 📁 Files Included

1. **`database_insert_queries.sql`** - SQL INSERT statements (ready to run in MySQL)
2. **`sample_data_insert.py`** - Python script using SQLAlchemy (recommended)
3. **`INSERT_QUERIES_GUIDE.md`** - This guide

---

## 🚀 Quick Start

### Method 1: Using SQL File (MySQL)

```bash
# Run the SQL file directly
mysql -u root -p secret_santa_db < database_insert_queries.sql
```

Or execute in MySQL command line:
```sql
USE secret_santa_db;
SOURCE database_insert_queries.sql;
```

### Method 2: Using Python Script (Recommended)

```bash
# Make sure you're in the project directory
python sample_data_insert.py
```

This method:
- ✅ Automatically generates password hashes
- ✅ Handles relationships correctly
- ✅ Validates data before insertion
- ✅ Shows progress and summary

---

## 📊 Sample Data Included

### Users (12 users)
- 2 Admin users (super_admin, admin)
- 10 Regular users

**Test Credentials:**
- Admin: `admin@secretsanta.com` / `admin123`
- Manager: `manager@secretsanta.com` / `manager123`
- Users: `[any user email]` / `user123`

### Events (3 events)
1. **Office Christmas 2024** - Active, assignments done
2. **College Friends Secret Santa** - Active, assignments done
3. **Family Christmas 2024** - Pending, no assignments yet

**Invite Codes:**
- `XMAS2024` - Office Christmas
- `COLLEGE2024` - College Friends
- `FAMILY2024` - Family Christmas

### Wishlists (5 wishlists)
- Preferences and dislikes for Event 1 participants
- Various categories: Electronics, Fashion, Sports, Arts, Accessories

### Participants
- Event 1: 6 participants
- Event 2: 6 participants
- Event 3: 3 participants

### Assignments
- Event 1: 6 assignments (circular pairing)
- Event 2: 6 assignments (circular pairing)
- All assignments follow: giver_id ≠ receiver_id

### Messages (3 messages)
- Sample anonymous messages between participants

---

## 🔧 Customizing INSERT Queries

### 1. Adding More Users

```sql
INSERT INTO users (name, email, password_hash, role) VALUES
('New User', 'newuser@example.com', 'pbkdf2:sha256:260000$...', 'user');
```

**Generate Password Hash in Python:**
```python
from werkzeug.security import generate_password_hash
password_hash = generate_password_hash('your_password')
print(password_hash)
```

### 2. Creating New Event

```sql
INSERT INTO events (
    event_name, 
    description, 
    admin_id, 
    budget_min, 
    budget_max, 
    invite_code
) VALUES (
    'My Event',
    'Event description',
    1,  -- admin_id (user who created)
    500.00,
    2000.00,
    'MYEVENT2024'  -- unique invite code
);
```

### 3. Adding Participant to Event

```sql
INSERT INTO participants (event_id, user_id, status) VALUES
(1, 3, 'active');  -- event_id, user_id
```

### 4. Creating Wishlist

```sql
INSERT INTO wishlists (
    user_id,
    event_id,
    preferences,
    dislikes,
    gift_category,
    hobby_tags,
    notes
) VALUES (
    3,  -- user_id
    1,  -- event_id
    '["books", "electronics"]',  -- JSON array as string
    '["perfume"]',
    'Electronics',
    'reading,gaming',
    'I love tech gadgets!'
);
```

### 5. Creating Assignment

**Important:** Ensure:
- `giver_id` ≠ `receiver_id` (no self-assignment)
- Both participants belong to the same event
- Only one assignment per giver per event

```sql
INSERT INTO assignments (
    event_id,
    giver_id,      -- participant_id of giver
    receiver_id,   -- participant_id of receiver
    compatibility_score,
    gift_status
) VALUES (
    1,
    1,  -- giver participant_id
    2,  -- receiver participant_id
    0.75,
    'pending'
);
```

### 6. Sending Message

```sql
INSERT INTO messages (
    event_id,
    sender_id,     -- user_id of sender
    receiver_id,   -- user_id of receiver
    message_text,
    is_read
) VALUES (
    1,
    3,  -- sender user_id
    4,  -- receiver user_id
    'Hello! I got you for Secret Santa!',
    FALSE
);
```

---

## ⚠️ Important Notes

### Password Hashes

**Never use plain text passwords!** Always hash passwords:

```python
from werkzeug.security import generate_password_hash
hash = generate_password_hash('password123')
```

### Foreign Key Relationships

When inserting data, respect the order:
1. **users** (no dependencies)
2. **events** (depends on users)
3. **wishlists** (depends on users, events)
4. **participants** (depends on users, events, wishlists)
5. **assignments** (depends on events, participants)
6. **messages** (depends on events, users)

### Unique Constraints

- **email** in `users` table must be unique
- **invite_code** in `events` table must be unique
- **(event_id, user_id)** in `participants` table must be unique
- **(event_id, giver_id)** in `assignments` table must be unique

### Assignment Rules

1. **No Self-Assignment**: `giver_id` ≠ `receiver_id`
2. **One-to-One**: Each participant gives to exactly one person
3. **Circular Pairing**: All participants should be in a cycle
4. **Same Event**: Both giver and receiver must be in the same event

---

## 🧪 Testing Your Data

### Verify All Data Inserted

```sql
SELECT 'Users' as TableName, COUNT(*) as Count FROM users
UNION ALL
SELECT 'Events', COUNT(*) FROM events
UNION ALL
SELECT 'Wishlists', COUNT(*) FROM wishlists
UNION ALL
SELECT 'Participants', COUNT(*) FROM participants
UNION ALL
SELECT 'Assignments', COUNT(*) FROM assignments
UNION ALL
SELECT 'Messages', COUNT(*) FROM messages;
```

### Check for Invalid Assignments

```sql
-- Should return 0 rows (no self-assignments)
SELECT * FROM assignments a
JOIN participants giver ON a.giver_id = giver.participant_id
JOIN participants receiver ON a.receiver_id = receiver.participant_id
WHERE giver.user_id = receiver.user_id;
```

### Verify Event Participants

```sql
SELECT 
    e.event_name,
    COUNT(DISTINCT p.participant_id) as participant_count,
    COUNT(DISTINCT a.assignment_id) as assignment_count
FROM events e
LEFT JOIN participants p ON e.event_id = p.event_id
LEFT JOIN assignments a ON e.event_id = a.event_id
GROUP BY e.event_id, e.event_name;
```

---

## 🔄 Resetting Sample Data

### Clear All Data (Be Careful!)

```sql
-- Delete in reverse order of dependencies
DELETE FROM messages;
DELETE FROM assignments;
DELETE FROM participants;
DELETE FROM wishlists;
DELETE FROM events;
DELETE FROM users;

-- Reset auto-increment
ALTER TABLE users AUTO_INCREMENT = 1;
ALTER TABLE events AUTO_INCREMENT = 1;
ALTER TABLE wishlists AUTO_INCREMENT = 1;
ALTER TABLE participants AUTO_INCREMENT = 1;
ALTER TABLE assignments AUTO_INCREMENT = 1;
ALTER TABLE messages AUTO_INCREMENT = 1;
```

### Using Python Script

```python
from app import create_app, db
from app.models import User, Event, Participant, Wishlist, Assignment, Message

app = create_app()
with app.app_context():
    # Delete all data
    Message.query.delete()
    Assignment.query.delete()
    Participant.query.delete()
    Wishlist.query.delete()
    Event.query.delete()
    User.query.delete()
    
    db.session.commit()
    print("All data cleared!")
```

---

## 📋 Sample Data Summary

After running the insert queries, you'll have:

- ✅ **12 Users** (2 admins, 10 regular users)
- ✅ **3 Events** (2 active with assignments, 1 pending)
- ✅ **5 Wishlists** (with preferences and dislikes)
- ✅ **15 Participants** (across 3 events)
- ✅ **12 Assignments** (valid circular pairings)
- ✅ **3 Messages** (sample anonymous messages)

---

## 🎯 Next Steps

1. **Run the insert queries** using your preferred method
2. **Verify the data** using the test queries above
3. **Test the application** by logging in with sample credentials
4. **Create your own events** and test the full workflow

---

## 💡 Tips

- Use the Python script for easier password hash generation
- Always verify foreign key relationships before inserting
- Test assignment algorithm with the sample data
- Use the invite codes to test the join event feature
- Check the admin dashboard with the sample events

---

**Happy Testing! 🎁🎄**
