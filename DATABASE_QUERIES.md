# 📊 Secret Santa - Database Queries Reference

## Common Queries for Development & Testing

### User Management

#### Get All Users
```sql
SELECT user_id, name, email, role, created_at, is_active 
FROM users 
ORDER BY created_at DESC;
```

#### Get User by Email
```sql
SELECT * FROM users WHERE email = 'user@example.com';
```

#### Get Active Users
```sql
SELECT * FROM users WHERE is_active = TRUE;
```

#### Count Users by Role
```sql
SELECT role, COUNT(*) as count 
FROM users 
GROUP BY role;
```

---

### Event Management

#### Get All Events
```sql
SELECT 
    e.*,
    u.name as admin_name,
    COUNT(DISTINCT p.participant_id) as participant_count
FROM events e
LEFT JOIN users u ON e.admin_id = u.user_id
LEFT JOIN participants p ON e.event_id = p.event_id
GROUP BY e.event_id
ORDER BY e.created_at DESC;
```

#### Get Event by Invite Code
```sql
SELECT * FROM events WHERE invite_code = 'XMAS2024';
```

#### Get Events Created by User
```sql
SELECT * FROM events WHERE admin_id = ?;
```

#### Get Events User Participated In
```sql
SELECT 
    e.*,
    p.status as participation_status,
    p.joined_at
FROM events e
JOIN participants p ON e.event_id = p.event_id
WHERE p.user_id = ?;
```

#### Get Events Ready for Assignment
```sql
SELECT * FROM events 
WHERE assignment_done = FALSE 
AND status = 'pending'
AND (SELECT COUNT(*) FROM participants WHERE event_id = events.event_id) >= 2;
```

---

### Participant Management

#### Get All Participants of an Event
```sql
SELECT 
    p.*,
    u.name as user_name,
    u.email as user_email
FROM participants p
JOIN users u ON p.user_id = u.user_id
WHERE p.event_id = ?
ORDER BY p.joined_at;
```

#### Get Active Participants Count
```sql
SELECT event_id, COUNT(*) as active_count
FROM participants
WHERE status = 'active'
GROUP BY event_id;
```

#### Check if User is Participant
```sql
SELECT * FROM participants 
WHERE event_id = ? AND user_id = ?;
```

---

### Assignment Queries

#### Get All Assignments for an Event
```sql
SELECT 
    a.*,
    giver_user.name as giver_name,
    receiver_user.name as receiver_name
FROM assignments a
JOIN participants giver ON a.giver_id = giver.participant_id
JOIN participants receiver ON a.receiver_id = receiver.participant_id
JOIN users giver_user ON giver.user_id = giver_user.user_id
JOIN users receiver_user ON receiver.user_id = receiver_user.user_id
WHERE a.event_id = ?;
```

#### Get User's Assignment (Who they need to gift)
```sql
SELECT 
    a.*,
    receiver_user.name as receiver_name,
    receiver_user.email as receiver_email,
    e.event_name
FROM assignments a
JOIN participants giver ON a.giver_id = giver.participant_id
JOIN participants receiver ON a.receiver_id = receiver.participant_id
JOIN users receiver_user ON receiver.user_id = receiver_user.user_id
JOIN events e ON a.event_id = e.event_id
WHERE giver.user_id = ? AND a.event_id = ?;
```

#### Get Who is Gifting to User
```sql
SELECT 
    a.*,
    giver_user.name as giver_name,
    e.event_name
FROM assignments a
JOIN participants giver ON a.giver_id = giver.participant_id
JOIN participants receiver ON a.receiver_id = receiver.participant_id
JOIN users giver_user ON giver.user_id = giver_user.user_id
JOIN events e ON a.event_id = e.event_id
WHERE receiver.user_id = ? AND a.event_id = ?;
```

#### Check Assignment Validity (No self-assignment)
```sql
SELECT * FROM assignments a
JOIN participants giver ON a.giver_id = giver.participant_id
JOIN participants receiver ON a.receiver_id = receiver.participant_id
WHERE giver.user_id = receiver.user_id;
-- Should return 0 rows
```

#### Get Assignment Statistics
```sql
SELECT 
    event_id,
    COUNT(*) as total_assignments,
    AVG(compatibility_score) as avg_compatibility,
    SUM(CASE WHEN gift_status = 'pending' THEN 1 ELSE 0 END) as pending_gifts,
    SUM(CASE WHEN gift_status = 'purchased' THEN 1 ELSE 0 END) as purchased_gifts,
    SUM(CASE WHEN gift_status = 'delivered' THEN 1 ELSE 0 END) as delivered_gifts
FROM assignments
WHERE event_id = ?
GROUP BY event_id;
```

---

### Wishlist Queries

#### Get User's Wishlist for Event
```sql
SELECT * FROM wishlists 
WHERE user_id = ? AND event_id = ?;
```

#### Get All Wishlists for an Event
```sql
SELECT 
    w.*,
    u.name as user_name
FROM wishlists w
JOIN users u ON w.user_id = u.user_id
WHERE w.event_id = ?;
```

#### Get Wishlists with Preferences
```sql
SELECT 
    w.*,
    u.name as user_name,
    p.participant_id
FROM wishlists w
JOIN users u ON w.user_id = u.user_id
JOIN participants p ON w.user_id = p.user_id AND w.event_id = p.event_id
WHERE w.event_id = ?;
```

---

### Message Queries

#### Get Messages for User (Received)
```sql
SELECT 
    m.*,
    e.event_name,
    sender.name as sender_name
FROM messages m
JOIN events e ON m.event_id = e.event_id
JOIN users sender ON m.sender_id = sender.user_id
WHERE m.receiver_id = ?
ORDER BY m.created_at DESC;
```

#### Get Unread Messages Count
```sql
SELECT COUNT(*) as unread_count
FROM messages
WHERE receiver_id = ? AND is_read = FALSE;
```

#### Get Messages for Event
```sql
SELECT 
    m.*,
    sender.name as sender_name,
    receiver.name as receiver_name
FROM messages m
JOIN users sender ON m.sender_id = sender.user_id
JOIN users receiver ON m.receiver_id = receiver.user_id
WHERE m.event_id = ?
ORDER BY m.created_at DESC;
```

---

### Analytics & Statistics

#### Event Statistics Dashboard
```sql
SELECT 
    e.event_id,
    e.event_name,
    e.status,
    e.assignment_done,
    COUNT(DISTINCT p.participant_id) as total_participants,
    COUNT(DISTINCT a.assignment_id) as assignments_done,
    COUNT(DISTINCT w.wishlist_id) as wishlists_created,
    COUNT(DISTINCT m.message_id) as total_messages,
    e.created_at,
    e.updated_at
FROM events e
LEFT JOIN participants p ON e.event_id = p.event_id AND p.status = 'active'
LEFT JOIN assignments a ON e.event_id = a.event_id
LEFT JOIN wishlists w ON e.event_id = w.event_id
LEFT JOIN messages m ON e.event_id = m.event_id
WHERE e.event_id = ?
GROUP BY e.event_id;
```

#### User Activity Summary
```sql
SELECT 
    u.user_id,
    u.name,
    u.email,
    COUNT(DISTINCT e.event_id) as events_created,
    COUNT(DISTINCT p.event_id) as events_joined,
    COUNT(DISTINCT a.assignment_id) as assignments_received,
    COUNT(DISTINCT w.wishlist_id) as wishlists_created
FROM users u
LEFT JOIN events e ON u.user_id = e.admin_id
LEFT JOIN participants p ON u.user_id = p.user_id
LEFT JOIN assignments a ON u.user_id = (
    SELECT user_id FROM participants WHERE participant_id = a.receiver_id
)
LEFT JOIN wishlists w ON u.user_id = w.user_id
WHERE u.user_id = ?
GROUP BY u.user_id;
```

#### Platform Statistics
```sql
SELECT 
    (SELECT COUNT(*) FROM users) as total_users,
    (SELECT COUNT(*) FROM events) as total_events,
    (SELECT COUNT(*) FROM participants) as total_participants,
    (SELECT COUNT(*) FROM assignments) as total_assignments,
    (SELECT COUNT(*) FROM wishlists) as total_wishlists,
    (SELECT COUNT(*) FROM messages) as total_messages;
```

---

### Data Validation Queries

#### Check for Orphaned Records
```sql
-- Orphaned participants
SELECT * FROM participants p
LEFT JOIN events e ON p.event_id = e.event_id
WHERE e.event_id IS NULL;

-- Orphaned assignments
SELECT * FROM assignments a
LEFT JOIN events e ON a.event_id = e.event_id
WHERE e.event_id IS NULL;

-- Participants without valid users
SELECT * FROM participants p
LEFT JOIN users u ON p.user_id = u.user_id
WHERE u.user_id IS NULL;
```

#### Check for Invalid Assignments
```sql
-- Self-assignments (should be 0)
SELECT * FROM assignments a
JOIN participants giver ON a.giver_id = giver.participant_id
JOIN participants receiver ON a.receiver_id = receiver.participant_id
WHERE giver.user_id = receiver.user_id;

-- Duplicate givers in same event
SELECT event_id, giver_id, COUNT(*) as count
FROM assignments
GROUP BY event_id, giver_id
HAVING count > 1;
```

---

### Maintenance Queries

#### Clean Up Inactive Users
```sql
UPDATE users SET is_active = FALSE 
WHERE user_id NOT IN (
    SELECT DISTINCT user_id FROM participants
    UNION
    SELECT DISTINCT admin_id FROM events
);
```

#### Archive Completed Events
```sql
UPDATE events 
SET status = 'completed' 
WHERE event_id IN (
    SELECT event_id FROM assignments
    WHERE gift_status = 'delivered'
    GROUP BY event_id
    HAVING COUNT(*) = (
        SELECT COUNT(*) FROM participants 
        WHERE event_id = assignments.event_id
    )
);
```

#### Delete Old Messages (Optional)
```sql
DELETE FROM messages 
WHERE created_at < DATE_SUB(NOW(), INTERVAL 1 YEAR)
AND event_id IN (
    SELECT event_id FROM events WHERE status = 'completed'
);
```

---

## Performance Optimization Queries

### Check Table Sizes
```sql
SELECT 
    table_name,
    ROUND(((data_length + index_length) / 1024 / 1024), 2) AS 'Size (MB)',
    table_rows
FROM information_schema.TABLES
WHERE table_schema = 'secret_santa_db'
ORDER BY (data_length + index_length) DESC;
```

### Analyze Tables
```sql
ANALYZE TABLE users, events, participants, assignments, wishlists, messages;
```

### Optimize Tables
```sql
OPTIMIZE TABLE users, events, participants, assignments, wishlists, messages;
```

---

## Backup & Restore

### Export Specific Table
```bash
mysqldump -u root -p secret_santa_db users > users_backup.sql
```

### Export All Data
```bash
mysqldump -u root -p secret_santa_db > full_backup.sql
```

### Export Structure Only
```bash
mysqldump -u root -p --no-data secret_santa_db > structure_only.sql
```

---

**Note**: Replace `?` placeholders with actual values when using these queries in your application.
