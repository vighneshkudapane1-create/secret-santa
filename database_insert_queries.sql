-- =====================================================
-- Secret Santa Web Application - Sample Data Insert Queries
-- =====================================================
-- This file contains INSERT queries with sample data
-- for testing and development purposes
-- =====================================================

USE secret_santa_db;

-- =====================================================
-- 1. INSERT INTO users
-- =====================================================
-- Note: Password hashes are examples. In production, use Werkzeug's generate_password_hash()
-- Example passwords: admin123, user123, test123

INSERT INTO users (name, email, password_hash, role, created_at, is_active) VALUES
-- Admin Users
('Admin User', 'admin@secretsanta.com', 'pbkdf2:sha256:260000$example1$hash1', 'super_admin', NOW(), TRUE),
('Event Manager', 'manager@secretsanta.com', 'pbkdf2:sha256:260000$example2$hash2', 'admin', NOW(), TRUE),

-- Regular Users
('John Doe', 'john.doe@example.com', 'pbkdf2:sha256:260000$example3$hash3', 'user', NOW(), TRUE),
('Jane Smith', 'jane.smith@example.com', 'pbkdf2:sha256:260000$example4$hash4', 'user', NOW(), TRUE),
('Mike Johnson', 'mike.johnson@example.com', 'pbkdf2:sha256:260000$example5$hash5', 'user', NOW(), TRUE),
('Sarah Williams', 'sarah.williams@example.com', 'pbkdf2:sha256:260000$example6$hash6', 'user', NOW(), TRUE),
('David Brown', 'david.brown@example.com', 'pbkdf2:sha256:260000$example7$hash7', 'user', NOW(), TRUE),
('Emily Davis', 'emily.davis@example.com', 'pbkdf2:sha256:260000$example8$hash8', 'user', NOW(), TRUE),
('Robert Wilson', 'robert.wilson@example.com', 'pbkdf2:sha256:260000$example9$hash9', 'user', NOW(), TRUE),
('Lisa Anderson', 'lisa.anderson@example.com', 'pbkdf2:sha256:260000$example10$hash10', 'user', NOW(), TRUE),
('James Taylor', 'james.taylor@example.com', 'pbkdf2:sha256:260000$example11$hash11', 'user', NOW(), TRUE),
('Maria Garcia', 'maria.garcia@example.com', 'pbkdf2:sha256:260000$example12$hash12', 'user', NOW(), TRUE);

-- =====================================================
-- 2. INSERT INTO events
-- =====================================================

INSERT INTO events (event_name, description, admin_id, budget_min, budget_max, currency, invite_code, status, assignment_done, gift_deadline, event_date, created_at) VALUES
-- Active Event 1 - Office Christmas Party
('Office Christmas 2024', 'Annual office Secret Santa gift exchange', 1, 500.00, 2000.00, 'INR', 'XMAS2024', 'active', TRUE, '2024-12-20 18:00:00', '2024-12-25 19:00:00', NOW()),

-- Active Event 2 - College Friends
('College Friends Secret Santa', 'Secret Santa for our college friend group', 2, 300.00, 1500.00, 'INR', 'COLLEGE2024', 'active', TRUE, '2024-12-22 20:00:00', '2024-12-24 21:00:00', NOW()),

-- Pending Event 3 - Family Gathering
('Family Christmas 2024', 'Family Secret Santa exchange', 1, 1000.00, 5000.00, 'INR', 'FAMILY2024', 'pending', FALSE, '2024-12-23 17:00:00', '2024-12-25 18:00:00', NOW()),

-- Completed Event 4
('New Year Secret Santa 2023', 'New Year celebration gift exchange', 2, 400.00, 2000.00, 'INR', 'NY2023', 'completed', TRUE, '2023-12-28 18:00:00', '2023-12-31 20:00:00', '2023-12-01 10:00:00');

-- =====================================================
-- 3. INSERT INTO wishlists
-- =====================================================

INSERT INTO wishlists (user_id, event_id, preferences, dislikes, gift_category, clothing_size, color_preference, hobby_tags, notes, created_at) VALUES
-- User 3 (John Doe) - Event 1
(3, 1, '["books", "electronics", "coffee"]', '["perfume", "clothes"]', 'Electronics', NULL, 'Blue, Black', 'reading,gaming,coffee', 'I love tech gadgets and books. Prefer practical gifts.', NOW()),

-- User 4 (Jane Smith) - Event 1
(4, 1, '["cosmetics", "jewelry", "handbags"]', '["electronics", "books"]', 'Fashion', 'M', 'Pink, Purple', 'fashion,makeup,shopping', 'Love fashion and beauty products!', NOW()),

-- User 5 (Mike Johnson) - Event 1
(5, 1, '["sports", "fitness", "gadgets"]', '["books", "cosmetics"]', 'Sports', 'L', 'Red, Blue', 'fitness,sports,gaming', 'Fitness enthusiast. Love sports equipment.', NOW()),

-- User 6 (Sarah Williams) - Event 1
(6, 1, '["art supplies", "books", "plants"]', '["electronics", "sports"]', 'Arts & Crafts', NULL, 'Green, Yellow', 'art,reading,gardening', 'Artist and book lover. Love plants too!', NOW()),

-- User 7 (David Brown) - Event 1
(7, 1, '["watches", "wallets", "grooming"]', '["art supplies", "plants"]', 'Accessories', NULL, 'Black, Brown', 'fashion,grooming', 'Love accessories and grooming products.', NOW()),

-- User 8 (Emily Davis) - Event 2
(8, 2, '["music", "headphones", "vinyl"]', '["clothes", "perfume"]', 'Electronics', NULL, 'Any', 'music,concerts', 'Music lover! Headphones or vinyl records would be great.', NOW()),

-- User 9 (Robert Wilson) - Event 2
(9, 2, '["cooking", "kitchen gadgets", "spices"]', '["electronics", "music"]', 'Home & Kitchen', NULL, 'Any', 'cooking,food', 'Love cooking! Kitchen gadgets or cookbooks.', NOW()),

-- User 10 (Lisa Anderson) - Event 2
(10, 2, '["yoga", "meditation", "wellness"]', '["cooking", "sports"]', 'Wellness', 'S', 'White, Beige', 'yoga,meditation,wellness', 'Wellness enthusiast. Yoga mats or meditation items.', NOW()),

-- User 11 (James Taylor) - Event 2
(11, 2, '["photography", "cameras", "lenses"]', '["fashion", "cosmetics"]', 'Electronics', NULL, 'Black', 'photography,travel', 'Photography hobbyist. Camera accessories welcome!', NOW()),

-- User 12 (Maria Garcia) - Event 2
(12, 2, '["travel", "luggage", "travel accessories"]', '["electronics", "photography"]', 'Travel', NULL, 'Any', 'travel,adventure', 'Love traveling! Travel accessories or luggage.', NOW());

-- =====================================================
-- 4. INSERT INTO participants
-- =====================================================

INSERT INTO participants (event_id, user_id, wishlist_id, joined_at, status) VALUES
-- Event 1 Participants (Office Christmas 2024)
(1, 1, NULL, NOW(), 'active'),  -- Admin
(1, 3, 1, NOW(), 'active'),     -- John Doe
(1, 4, 2, NOW(), 'active'),     -- Jane Smith
(1, 5, 3, NOW(), 'active'),     -- Mike Johnson
(1, 6, 4, NOW(), 'active'),     -- Sarah Williams
(1, 7, 5, NOW(), 'active'),     -- David Brown

-- Event 2 Participants (College Friends)
(2, 2, NULL, NOW(), 'active'),  -- Manager
(2, 8, 6, NOW(), 'active'),     -- Emily Davis
(2, 9, 7, NOW(), 'active'),     -- Robert Wilson
(2, 10, 8, NOW(), 'active'),    -- Lisa Anderson
(2, 11, 9, NOW(), 'active'),    -- James Taylor
(2, 12, 10, NOW(), 'active'),   -- Maria Garcia

-- Event 3 Participants (Family Christmas - Pending)
(3, 1, NULL, NOW(), 'active'),  -- Admin
(3, 3, NULL, NOW(), 'active'),  -- John Doe
(3, 4, NULL, NOW(), 'active'),  -- Jane Smith

-- Event 4 Participants (Completed Event)
(4, 2, NULL, '2023-12-01 10:00:00', 'completed'),
(4, 5, NULL, '2023-12-01 10:00:00', 'completed'),
(4, 6, NULL, '2023-12-01 10:00:00', 'completed');

-- =====================================================
-- 5. INSERT INTO assignments
-- =====================================================
-- Note: These assignments follow the rule: giver_id != receiver_id
-- Each participant gives to exactly one person and receives from exactly one person

INSERT INTO assignments (event_id, giver_id, receiver_id, compatibility_score, assigned_at, gift_status) VALUES
-- Event 1 Assignments (Office Christmas 2024)
-- Circular assignment: 1->3->4->5->6->7->1
(1, 1, 3, 0.75, NOW(), 'pending'),   -- Admin gives to John
(1, 3, 4, 0.60, NOW(), 'pending'),   -- John gives to Jane
(1, 4, 5, 0.50, NOW(), 'pending'),   -- Jane gives to Mike
(1, 5, 6, 0.65, NOW(), 'pending'),   -- Mike gives to Sarah
(1, 6, 7, 0.70, NOW(), 'pending'),   -- Sarah gives to David
(1, 7, 1, 0.80, NOW(), 'purchased'), -- David gives to Admin

-- Event 2 Assignments (College Friends)
-- Circular assignment: 2->8->9->10->11->12->2
(2, 2, 8, 0.85, NOW(), 'pending'),   -- Manager gives to Emily
(2, 8, 9, 0.55, NOW(), 'pending'),   -- Emily gives to Robert
(2, 9, 10, 0.70, NOW(), 'pending'),  -- Robert gives to Lisa
(2, 10, 11, 0.60, NOW(), 'pending'), -- Lisa gives to James
(2, 11, 12, 0.75, NOW(), 'pending'), -- James gives to Maria
(2, 12, 2, 0.90, NOW(), 'delivered'),-- Maria gives to Manager

-- Event 4 Assignments (Completed Event - Historical)
(4, 13, 14, 0.80, '2023-12-05 10:00:00', 'delivered'),
(4, 14, 15, 0.75, '2023-12-05 10:00:00', 'delivered'),
(4, 15, 13, 0.85, '2023-12-05 10:00:00', 'delivered');

-- =====================================================
-- 6. INSERT INTO messages
-- =====================================================

INSERT INTO messages (event_id, sender_id, receiver_id, message_text, is_encrypted, created_at, is_read) VALUES
-- Event 1 Messages
(1, 3, 4, 'Hi! I got you for Secret Santa. Any specific preferences?', FALSE, NOW(), FALSE),
(1, 4, 5, 'Hey! Looking forward to your gift! I love surprises.', FALSE, NOW(), TRUE),
(1, 5, 6, 'Hello! Just wanted to say I\'m excited to be your Secret Santa!', FALSE, NOW(), FALSE),
(1, 6, 7, 'Hi there! Any hints about what you might like?', FALSE, NOW(), FALSE),
(1, 7, 1, 'Thank you for organizing this! Can\'t wait for the exchange!', FALSE, NOW(), TRUE),

-- Event 2 Messages
(2, 8, 9, 'Hey! Got you for Secret Santa. What are your interests?', FALSE, NOW(), FALSE),
(2, 9, 10, 'Hi! I\'m your Secret Santa. Any gift ideas?', FALSE, NOW(), FALSE),
(2, 10, 11, 'Hello! Looking forward to finding the perfect gift for you!', FALSE, NOW(), TRUE),
(2, 11, 12, 'Hi! I got you! Any preferences or wishlist?', FALSE, NOW(), FALSE),
(2, 12, 2, 'Thank you for organizing this event!', FALSE, NOW(), TRUE);

-- =====================================================
-- Verification Queries
-- =====================================================

-- Check all inserted data
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

-- Verify assignments (should have no self-assignments)
SELECT 
    a.assignment_id,
    giver.user_id as giver_user_id,
    receiver.user_id as receiver_user_id,
    CASE 
        WHEN giver.user_id = receiver.user_id THEN 'INVALID - Self Assignment'
        ELSE 'VALID'
    END as validation
FROM assignments a
JOIN participants giver ON a.giver_id = giver.participant_id
JOIN participants receiver ON a.receiver_id = receiver.participant_id;

-- Check event participant counts
SELECT 
    e.event_name,
    COUNT(DISTINCT p.participant_id) as participant_count,
    COUNT(DISTINCT a.assignment_id) as assignment_count
FROM events e
LEFT JOIN participants p ON e.event_id = p.event_id
LEFT JOIN assignments a ON e.event_id = a.event_id
GROUP BY e.event_id, e.event_name;

-- =====================================================
-- Additional Sample Data (Optional)
-- =====================================================

-- Insert more users for testing
INSERT INTO users (name, email, password_hash, role) VALUES
('Test User 1', 'test1@example.com', 'pbkdf2:sha256:260000$test1$hash', 'user', NOW(), TRUE),
('Test User 2', 'test2@example.com', 'pbkdf2:sha256:260000$test2$hash', 'user', NOW(), TRUE),
('Test User 3', 'test3@example.com', 'pbkdf2:sha256:260000$test3$hash', 'user', NOW(), TRUE);

-- =====================================================
-- Notes for Production Use
-- =====================================================
-- 1. Replace password hashes with actual Werkzeug-generated hashes
-- 2. Adjust dates according to your needs
-- 3. Modify invite codes to be unique
-- 4. Update user IDs based on your actual user table
-- 5. Ensure participant IDs match when creating assignments
-- 6. Verify all foreign key relationships before inserting

-- =====================================================
-- How to Generate Password Hash in Python
-- =====================================================
-- from werkzeug.security import generate_password_hash
-- password_hash = generate_password_hash('your_password')
-- print(password_hash)
-- Then use the output in INSERT statements

-- =====================================================
-- End of Insert Queries
-- =====================================================
