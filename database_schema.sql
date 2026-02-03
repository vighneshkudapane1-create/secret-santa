-- =====================================================
-- Secret Santa Web Application - Database Schema
-- =====================================================
-- Database: secret_santa_db
-- Engine: InnoDB
-- Character Set: utf8mb4
-- =====================================================

-- Create Database
CREATE DATABASE IF NOT EXISTS secret_santa_db 
CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE secret_santa_db;

-- =====================================================
-- Table 1: users
-- Stores all user account information
-- =====================================================
CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(120) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL COMMENT 'Plain text password (no hashing)',
    role VARCHAR(20) DEFAULT 'user' COMMENT 'user, admin, super_admin',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    INDEX idx_email (email)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='User accounts table';

-- =====================================================
-- Table 2: events
-- Stores Secret Santa event information
-- =====================================================
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
    privacy_type VARCHAR(20) DEFAULT 'public' COMMENT 'public, private',
    visibility VARCHAR(20) DEFAULT 'all' COMMENT 'all, participants_only, invite_only',
    allow_public_join BOOLEAN DEFAULT TRUE COMMENT 'Can anyone with invite code join?',
    gift_deadline DATETIME,
    event_date DATETIME,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_invite_code (invite_code),
    FOREIGN KEY (admin_id) REFERENCES users(user_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='Secret Santa events table';

-- =====================================================
-- Table 3: wishlists
-- Stores user wishlists and preferences for events
-- =====================================================
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='User wishlists and preferences';

-- =====================================================
-- Table 4: participants
-- Stores event participants (users who joined events)
-- =====================================================
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='Event participants table';

-- =====================================================
-- Table 5: assignments
-- Stores Secret Santa assignments (who gives to whom)
-- =====================================================
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
    FOREIGN KEY (receiver_id) REFERENCES participants(participant_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='Secret Santa assignments table';

-- =====================================================
-- Table 6: messages
-- Stores anonymous messages between participants
-- =====================================================
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='Anonymous messages table';

-- =====================================================
-- Sample Data (Optional - for testing)
-- =====================================================

-- Insert sample admin user (password: admin123)
-- Note: In production, use proper password hashing
INSERT INTO users (name, email, password_hash, role) VALUES
('Admin User', 'admin@secretsanta.com', 'pbkdf2:sha256:260000$...', 'super_admin');

-- =====================================================
-- Useful Views (Optional)
-- =====================================================

-- View: Event Participants with User Info
CREATE OR REPLACE VIEW v_event_participants AS
SELECT 
    p.participant_id,
    p.event_id,
    p.user_id,
    u.name as user_name,
    u.email as user_email,
    p.joined_at,
    p.status,
    e.event_name
FROM participants p
JOIN users u ON p.user_id = u.user_id
JOIN events e ON p.event_id = e.event_id;

-- View: Assignment Details
CREATE OR REPLACE VIEW v_assignments AS
SELECT 
    a.assignment_id,
    a.event_id,
    e.event_name,
    giver.user_id as giver_user_id,
    giver_user.name as giver_name,
    receiver.user_id as receiver_user_id,
    receiver_user.name as receiver_name,
    a.compatibility_score,
    a.assigned_at,
    a.gift_status
FROM assignments a
JOIN events e ON a.event_id = e.event_id
JOIN participants giver ON a.giver_id = giver.participant_id
JOIN participants receiver ON a.receiver_id = receiver.participant_id
JOIN users giver_user ON giver.user_id = giver_user.user_id
JOIN users receiver_user ON receiver.user_id = receiver_user.user_id;

-- =====================================================
-- Indexes for Performance (Additional)
-- =====================================================

-- Index on participants for faster event lookups
CREATE INDEX idx_participants_event ON participants(event_id);
CREATE INDEX idx_participants_user ON participants(user_id);

-- Index on assignments for faster queries
CREATE INDEX idx_assignments_event ON assignments(event_id);
CREATE INDEX idx_assignments_giver ON assignments(giver_id);
CREATE INDEX idx_assignments_receiver ON assignments(receiver_id);

-- Index on messages for faster lookups
CREATE INDEX idx_messages_event ON messages(event_id);
CREATE INDEX idx_messages_receiver ON messages(receiver_id);
CREATE INDEX idx_messages_created ON messages(created_at);

-- =====================================================
-- End of Schema
-- =====================================================
