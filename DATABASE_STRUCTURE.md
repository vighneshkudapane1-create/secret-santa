# 🗄️ Secret Santa - Database Structure Documentation

## Overview

The Secret Santa application uses **MySQL** database with **6 main tables** that handle users, events, participants, wishlists, assignments, and messages.

---

## 📊 Entity Relationship Diagram (ERD)

```
┌─────────────┐
│    users    │
│─────────────│
│ user_id (PK)│
│ name        │
│ email (UK)  │
│ password    │
│ role        │
│ created_at  │
│ is_active   │
└──────┬──────┘
       │
       │ 1
       │
       │ N
┌──────┴──────────────────────────────────────────────┐
│                                                    │
│  ┌─────────────┐         ┌─────────────┐         │
│  │   events    │         │ participants│         │
│  │─────────────│         │─────────────│         │
│  │ event_id(PK)│◄───┐     │participant │         │
│  │ event_name  │    │     │  _id (PK)  │         │
│  │ admin_id(FK)├────┼─────┤ event_id   │         │
│  │ invite_code │    │     │ user_id(FK)│         │
│  │ status      │    │     │ wishlist_id│         │
│  │ budget_min  │    │     │ joined_at  │         │
│  │ budget_max  │    │     │ status     │         │
│  └─────────────┘    │     └──────┬─────┘         │
│                     │            │               │
│                     │            │ N             │
│                     │            │               │
│                     │            │ 1             │
│                     │     ┌──────┴─────┐         │
│                     │     │ wishlists  │         │
│                     │     │────────────│         │
│                     │     │wishlist_id │         │
│                     │     │ user_id(FK)│         │
│                     │     │ event_id   │         │
│                     │     │ preferences│         │
│                     │     │ dislikes   │         │
│                     │     └────────────┘         │
│                     │                            │
│                     │     ┌─────────────┐         │
│                     │     │assignments │         │
│                     └─────┤─────────────│         │
│                           │assignment_ │         │
│                           │  id (PK)   │         │
│                           │ event_id(FK)         │
│                           │ giver_id(FK)         │
│                           │receiver_id(FK)       │
│                           │compatibility_score   │
│                           │ gift_status          │
│                           └─────────────┘         │
│                                                   │
│                     ┌─────────────┐               │
│                     │  messages   │               │
│                     │─────────────│               │
│                     │ message_id  │               │
│                     │ event_id(FK)├───────────────┘
│                     │ sender_id   │
│                     │ receiver_id │
│                     │ message_text│
│                     │ is_encrypted │
│                     │ created_at  │
│                     └─────────────┘
│
└────────────────────────────────────────────────────┘
```

---

## 📋 Table Structures

### 1. **users** Table

Stores all user account information.

| Column Name    | Data Type      | Constraints           | Description                    |
|----------------|----------------|-----------------------|--------------------------------|
| user_id        | INT            | PRIMARY KEY, AUTO_INCREMENT | Unique user identifier      |
| name           | VARCHAR(100)   | NOT NULL              | User's full name              |
| email          | VARCHAR(120)   | NOT NULL, UNIQUE, INDEX | User's email address        |
| password_hash  | VARCHAR(255)   | NOT NULL              | Hashed password (Werkzeug)    |
| role           | VARCHAR(20)    | DEFAULT 'user'        | user, admin, super_admin      |
| created_at     | DATETIME       | DEFAULT CURRENT_TIMESTAMP | Account creation time      |
| is_active      | BOOLEAN        | DEFAULT TRUE           | Account status               |

**Indexes:**
- PRIMARY KEY: `user_id`
- UNIQUE INDEX: `email`
- INDEX: `email` (for fast lookups)

**Relationships:**
- One-to-Many with `events` (as admin/creator)
- One-to-Many with `participants`
- One-to-Many with `wishlists`
- One-to-Many with `messages` (as sender and receiver)

---

### 2. **events** Table

Stores Secret Santa event information.

| Column Name     | Data Type      | Constraints           | Description                    |
|-----------------|----------------|-----------------------|--------------------------------|
| event_id        | INT            | PRIMARY KEY, AUTO_INCREMENT | Unique event identifier     |
| event_name      | VARCHAR(200)   | NOT NULL              | Event name                    |
| description     | TEXT           | NULL                  | Event description             |
| admin_id        | INT            | NOT NULL, FOREIGN KEY | Creator/admin user ID         |
| budget_min      | FLOAT          | DEFAULT 0.0           | Minimum gift budget           |
| budget_max      | FLOAT          | DEFAULT 1000.0         | Maximum gift budget           |
| currency        | VARCHAR(10)    | DEFAULT 'INR'          | Currency code (INR, USD, etc) |
| invite_code     | VARCHAR(20)    | NOT NULL, UNIQUE, INDEX | Unique invite code for joining |
| status          | VARCHAR(20)    | DEFAULT 'pending'      | pending, active, completed, cancelled |
| assignment_done | BOOLEAN        | DEFAULT FALSE          | Whether assignments are generated |
| gift_deadline   | DATETIME       | NULL                   | Deadline for gift submission  |
| event_date      | DATETIME       | NULL                   | Event date                    |
| created_at      | DATETIME       | DEFAULT CURRENT_TIMESTAMP | Event creation time        |
| updated_at      | DATETIME       | DEFAULT CURRENT_TIMESTAMP ON UPDATE | Last update time |

**Indexes:**
- PRIMARY KEY: `event_id`
- UNIQUE INDEX: `invite_code`
- INDEX: `invite_code` (for fast lookups)
- FOREIGN KEY: `admin_id` → `users.user_id`

**Relationships:**
- Many-to-One with `users` (admin/creator)
- One-to-Many with `participants`
- One-to-Many with `assignments`
- One-to-Many with `messages`

---

### 3. **participants** Table

Stores event participants (users who joined events).

| Column Name    | Data Type      | Constraints           | Description                    |
|----------------|----------------|-----------------------|--------------------------------|
| participant_id | INT            | PRIMARY KEY, AUTO_INCREMENT | Unique participant ID       |
| event_id       | INT            | NOT NULL, FOREIGN KEY | Event ID                      |
| user_id        | INT            | NOT NULL, FOREIGN KEY | User ID                       |
| wishlist_id    | INT            | NULL, FOREIGN KEY     | Associated wishlist ID         |
| joined_at      | DATETIME       | DEFAULT CURRENT_TIMESTAMP | Join timestamp            |
| status         | VARCHAR(20)    | DEFAULT 'active'       | active, dropped, completed    |

**Indexes:**
- PRIMARY KEY: `participant_id`
- UNIQUE CONSTRAINT: `(event_id, user_id)` - Prevents duplicate participation
- FOREIGN KEY: `event_id` → `events.event_id`
- FOREIGN KEY: `user_id` → `users.user_id`
- FOREIGN KEY: `wishlist_id` → `wishlists.wishlist_id`

**Relationships:**
- Many-to-One with `events`
- Many-to-One with `users`
- One-to-One with `wishlists` (optional)
- One-to-Many with `assignments` (as giver and receiver)

---

### 4. **wishlists** Table

Stores user wishlists and preferences for events.

| Column Name      | Data Type      | Constraints           | Description                    |
|------------------|----------------|-----------------------|--------------------------------|
| wishlist_id      | INT            | PRIMARY KEY, AUTO_INCREMENT | Unique wishlist ID         |
| user_id          | INT            | NOT NULL, FOREIGN KEY | User ID                       |
| event_id         | INT            | NOT NULL, FOREIGN KEY | Event ID                      |
| preferences      | TEXT           | NULL                  | JSON string of preferences    |
| dislikes         | TEXT           | NULL                  | JSON string of dislikes       |
| gift_category    | VARCHAR(100)   | NULL                  | Preferred gift category        |
| clothing_size    | VARCHAR(20)    | NULL                  | Clothing size (if applicable) |
| color_preference | VARCHAR(50)    | NULL                  | Color preferences             |
| hobby_tags       | VARCHAR(200)   | NULL                  | Comma-separated hobby tags     |
| notes            | TEXT           | NULL                  | Additional notes               |
| created_at       | DATETIME       | DEFAULT CURRENT_TIMESTAMP | Creation timestamp        |
| updated_at       | DATETIME       | DEFAULT CURRENT_TIMESTAMP ON UPDATE | Update timestamp |

**Indexes:**
- PRIMARY KEY: `wishlist_id`
- FOREIGN KEY: `user_id` → `users.user_id`
- FOREIGN KEY: `event_id` → `events.event_id`

**Relationships:**
- Many-to-One with `users`
- Many-to-One with `events`
- One-to-One with `participants` (optional)

---

### 5. **assignments** Table

Stores Secret Santa assignments (who gives to whom).

| Column Name        | Data Type      | Constraints           | Description                    |
|--------------------|----------------|-----------------------|--------------------------------|
| assignment_id      | INT            | PRIMARY KEY, AUTO_INCREMENT | Unique assignment ID       |
| event_id           | INT            | NOT NULL, FOREIGN KEY | Event ID                      |
| giver_id           | INT            | NOT NULL, FOREIGN KEY | Participant ID (giver)          |
| receiver_id        | INT            | NOT NULL, FOREIGN KEY | Participant ID (receiver)       |
| compatibility_score| FLOAT          | DEFAULT 0.0           | Compatibility score (0.0-1.0)  |
| assigned_at        | DATETIME       | DEFAULT CURRENT_TIMESTAMP | Assignment timestamp       |
| gift_status        | VARCHAR(20)    | DEFAULT 'pending'      | pending, purchased, delivered  |

**Indexes:**
- PRIMARY KEY: `assignment_id`
- UNIQUE CONSTRAINT: `(event_id, giver_id)` - One assignment per giver per event
- FOREIGN KEY: `event_id` → `events.event_id`
- FOREIGN KEY: `giver_id` → `participants.participant_id`
- FOREIGN KEY: `receiver_id` → `participants.participant_id`

**Relationships:**
- Many-to-One with `events`
- Many-to-One with `participants` (as giver)
- Many-to-One with `participants` (as receiver)

**Business Rules:**
- `giver_id` ≠ `receiver_id` (no self-assignment)
- Each participant can only be assigned once per event as giver
- Each participant can only be assigned once per event as receiver

---

### 6. **messages** Table

Stores anonymous messages between participants.

| Column Name   | Data Type      | Constraints           | Description                    |
|---------------|----------------|-----------------------|--------------------------------|
| message_id    | INT            | PRIMARY KEY, AUTO_INCREMENT | Unique message ID          |
| event_id      | INT            | NOT NULL, FOREIGN KEY | Event ID                      |
| sender_id     | INT            | NOT NULL, FOREIGN KEY | Sender user ID (hidden from receiver) |
| receiver_id   | INT            | NOT NULL, FOREIGN KEY | Receiver user ID              |
| message_text  | TEXT           | NOT NULL              | Message content               |
| is_encrypted  | BOOLEAN        | DEFAULT FALSE         | Whether message is encrypted  |
| created_at    | DATETIME       | DEFAULT CURRENT_TIMESTAMP | Message timestamp         |
| is_read       | BOOLEAN        | DEFAULT FALSE         | Read status                   |

**Indexes:**
- PRIMARY KEY: `message_id`
- FOREIGN KEY: `event_id` → `events.event_id`
- FOREIGN KEY: `sender_id` → `users.user_id`
- FOREIGN KEY: `receiver_id` → `users.user_id`

**Relationships:**
- Many-to-One with `events`
- Many-to-One with `users` (as sender)
- Many-to-One with `users` (as receiver)

---

## 🔧 SQL CREATE Statements

### Complete Database Schema

```sql
-- Create Database
CREATE DATABASE IF NOT EXISTS secret_santa_db 
CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE secret_santa_db;

-- 1. Users Table
CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(120) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(20) DEFAULT 'user' COMMENT 'user, admin, super_admin',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    INDEX idx_email (email)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 2. Events Table
CREATE TABLE events (
    event_id INT AUTO_INCREMENT PRIMARY KEY,
    event_name VARCHAR(200) NOT NULL,
    description TEXT,
    admin_id INT NOT NULL,
    budget_min FLOAT DEFAULT 0.0,
    budget_max FLOAT DEFAULT 1000.0,
    currency VARCHAR(10) DEFAULT 'INR',
    invite_code VARCHAR(20) NOT NULL UNIQUE,
    status VARCHAR(20) DEFAULT 'pending' COMMENT 'pending, active, completed, cancelled',
    assignment_done BOOLEAN DEFAULT FALSE,
    gift_deadline DATETIME,
    event_date DATETIME,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_invite_code (invite_code),
    FOREIGN KEY (admin_id) REFERENCES users(user_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 3. Participants Table
CREATE TABLE participants (
    participant_id INT AUTO_INCREMENT PRIMARY KEY,
    event_id INT NOT NULL,
    user_id INT NOT NULL,
    wishlist_id INT NULL,
    joined_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(20) DEFAULT 'active' COMMENT 'active, dropped, completed',
    UNIQUE KEY unique_participant (event_id, user_id),
    FOREIGN KEY (event_id) REFERENCES events(event_id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (wishlist_id) REFERENCES wishlists(wishlist_id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 4. Wishlists Table
CREATE TABLE wishlists (
    wishlist_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    event_id INT NOT NULL,
    preferences TEXT COMMENT 'JSON string of preferences',
    dislikes TEXT COMMENT 'JSON string of dislikes',
    gift_category VARCHAR(100),
    clothing_size VARCHAR(20),
    color_preference VARCHAR(50),
    hobby_tags VARCHAR(200),
    notes TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (event_id) REFERENCES events(event_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 5. Assignments Table
CREATE TABLE assignments (
    assignment_id INT AUTO_INCREMENT PRIMARY KEY,
    event_id INT NOT NULL,
    giver_id INT NOT NULL,
    receiver_id INT NOT NULL,
    compatibility_score FLOAT DEFAULT 0.0,
    assigned_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    gift_status VARCHAR(20) DEFAULT 'pending' COMMENT 'pending, purchased, delivered',
    UNIQUE KEY unique_giver (event_id, giver_id),
    FOREIGN KEY (event_id) REFERENCES events(event_id) ON DELETE CASCADE,
    FOREIGN KEY (giver_id) REFERENCES participants(participant_id) ON DELETE CASCADE,
    FOREIGN KEY (receiver_id) REFERENCES participants(participant_id) ON DELETE CASCADE,
    CHECK (giver_id != receiver_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 6. Messages Table
CREATE TABLE messages (
    message_id INT AUTO_INCREMENT PRIMARY KEY,
    event_id INT NOT NULL,
    sender_id INT NOT NULL,
    receiver_id INT NOT NULL,
    message_text TEXT NOT NULL,
    is_encrypted BOOLEAN DEFAULT FALSE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    is_read BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (event_id) REFERENCES events(event_id) ON DELETE CASCADE,
    FOREIGN KEY (sender_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (receiver_id) REFERENCES users(user_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

---

## 📊 Sample Data Queries

### Insert Sample Data

```sql
-- Insert Sample User
INSERT INTO users (name, email, password_hash, role) VALUES
('John Doe', 'john@example.com', 'pbkdf2:sha256:...', 'user'),
('Admin User', 'admin@example.com', 'pbkdf2:sha256:...', 'super_admin');

-- Insert Sample Event
INSERT INTO events (event_name, description, admin_id, budget_min, budget_max, invite_code) VALUES
('Christmas 2024', 'Office Secret Santa', 1, 500, 2000, 'XMAS2024');

-- Insert Sample Participant
INSERT INTO participants (event_id, user_id, status) VALUES
(1, 1, 'active');

-- Insert Sample Wishlist
INSERT INTO wishlists (user_id, event_id, gift_category, hobby_tags, notes) VALUES
(1, 1, 'Electronics', 'gaming,reading', 'I love books and gadgets');

-- Insert Sample Assignment
INSERT INTO assignments (event_id, giver_id, receiver_id, compatibility_score) VALUES
(1, 1, 2, 0.75);
```

---

## 🔍 Useful Queries

### Get User's Events
```sql
SELECT e.*, p.status as participation_status
FROM events e
JOIN participants p ON e.event_id = p.event_id
WHERE p.user_id = ?;
```

### Get Event Participants
```sql
SELECT u.name, u.email, p.joined_at, p.status
FROM participants p
JOIN users u ON p.user_id = u.user_id
WHERE p.event_id = ?;
```

### Get User's Assignment
```sql
SELECT 
    a.*,
    giver.user_id as giver_user_id,
    receiver.user_id as receiver_user_id,
    receiver_user.name as receiver_name
FROM assignments a
JOIN participants giver ON a.giver_id = giver.participant_id
JOIN participants receiver ON a.receiver_id = receiver.participant_id
JOIN users receiver_user ON receiver.user_id = receiver_user.user_id
WHERE giver.user_id = ? AND a.event_id = ?;
```

### Get Event Statistics
```sql
SELECT 
    e.event_id,
    e.event_name,
    COUNT(DISTINCT p.participant_id) as total_participants,
    COUNT(DISTINCT a.assignment_id) as assignments_done,
    COUNT(DISTINCT w.wishlist_id) as wishlists_created
FROM events e
LEFT JOIN participants p ON e.event_id = p.event_id
LEFT JOIN assignments a ON e.event_id = a.event_id
LEFT JOIN wishlists w ON e.event_id = w.event_id
WHERE e.event_id = ?
GROUP BY e.event_id;
```

---

## 🔐 Security Considerations

1. **Password Storage**: Passwords are hashed using Werkzeug's `generate_password_hash()` (PBKDF2)
2. **SQL Injection**: Use parameterized queries (SQLAlchemy ORM handles this)
3. **Data Validation**: All inputs validated at application level
4. **Foreign Keys**: CASCADE deletes ensure data integrity
5. **Unique Constraints**: Prevent duplicate entries

---

## 📈 Database Statistics

- **Total Tables**: 6
- **Total Relationships**: 10+ foreign keys
- **Indexes**: 8+ indexes for performance
- **Constraints**: Multiple unique and check constraints
- **Storage Engine**: InnoDB (supports transactions and foreign keys)

---

## 🛠️ Maintenance Queries

### Backup Database
```bash
mysqldump -u root -p secret_santa_db > backup.sql
```

### Restore Database
```bash
mysql -u root -p secret_santa_db < backup.sql
```

### Check Table Sizes
```sql
SELECT 
    table_name AS 'Table',
    ROUND(((data_length + index_length) / 1024 / 1024), 2) AS 'Size (MB)'
FROM information_schema.TABLES
WHERE table_schema = 'secret_santa_db'
ORDER BY (data_length + index_length) DESC;
```

---

## ✅ Database Validation Rules

1. **Email Uniqueness**: Each email can only register once
2. **Participant Uniqueness**: User can only join an event once
3. **Assignment Uniqueness**: Each participant can only be assigned once per event
4. **No Self-Assignment**: Giver cannot be receiver
5. **Referential Integrity**: All foreign keys must reference valid records

---

**Last Updated**: 2024
**Database Version**: MySQL 5.7+ / MariaDB 10.3+
**ORM**: SQLAlchemy (Flask-SQLAlchemy)
