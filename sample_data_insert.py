"""
Secret Santa - Python Script to Insert Sample Data
This script uses SQLAlchemy to insert sample data into the database
"""

from app import create_app, db
from app.models import User, Event, Participant, Wishlist, Assignment, Message
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta

def insert_sample_data():
    """Insert sample data into the database"""
    app = create_app()
    
    with app.app_context():
        # Clear existing data (optional - be careful in production!)
        # db.drop_all()
        # db.create_all()
        
        print("Starting data insertion...")
        
        # =====================================================
        # 1. Insert Users
        # =====================================================
        print("Inserting users...")
        
        users_data = [
            {'name': 'Admin User', 'email': 'admin@secretsanta.com', 'password': 'admin123', 'role': 'super_admin'},
            {'name': 'Event Manager', 'email': 'manager@secretsanta.com', 'password': 'manager123', 'role': 'admin'},
            {'name': 'John Doe', 'email': 'john.doe@example.com', 'password': 'user123', 'role': 'user'},
            {'name': 'Jane Smith', 'email': 'jane.smith@example.com', 'password': 'user123', 'role': 'user'},
            {'name': 'Mike Johnson', 'email': 'mike.johnson@example.com', 'password': 'user123', 'role': 'user'},
            {'name': 'Sarah Williams', 'email': 'sarah.williams@example.com', 'password': 'user123', 'role': 'user'},
            {'name': 'David Brown', 'email': 'david.brown@example.com', 'password': 'user123', 'role': 'user'},
            {'name': 'Emily Davis', 'email': 'emily.davis@example.com', 'password': 'user123', 'role': 'user'},
            {'name': 'Robert Wilson', 'email': 'robert.wilson@example.com', 'password': 'user123', 'role': 'user'},
            {'name': 'Lisa Anderson', 'email': 'lisa.anderson@example.com', 'password': 'user123', 'role': 'user'},
            {'name': 'James Taylor', 'email': 'james.taylor@example.com', 'password': 'user123', 'role': 'user'},
            {'name': 'Maria Garcia', 'email': 'maria.garcia@example.com', 'password': 'user123', 'role': 'user'},
        ]
        
        users = []
        for user_data in users_data:
            user = User(
                name=user_data['name'],
                email=user_data['email'],
                role=user_data['role']
            )
            user.set_password(user_data['password'])
            users.append(user)
            db.session.add(user)
        
        db.session.commit()
        print(f"✓ Inserted {len(users)} users")
        
        # =====================================================
        # 2. Insert Events
        # =====================================================
        print("Inserting events...")
        
        events_data = [
            {
                'event_name': 'Office Christmas 2024',
                'description': 'Annual office Secret Santa gift exchange',
                'admin_id': users[0].user_id,  # Admin User
                'budget_min': 500.0,
                'budget_max': 2000.0,
                'currency': 'INR',
                'invite_code': 'XMAS2024',
                'status': 'active',
                'assignment_done': True,
                'gift_deadline': datetime(2024, 12, 20, 18, 0, 0),
                'event_date': datetime(2024, 12, 25, 19, 0, 0)
            },
            {
                'event_name': 'College Friends Secret Santa',
                'description': 'Secret Santa for our college friend group',
                'admin_id': users[1].user_id,  # Event Manager
                'budget_min': 300.0,
                'budget_max': 1500.0,
                'currency': 'INR',
                'invite_code': 'COLLEGE2024',
                'status': 'active',
                'assignment_done': True,
                'gift_deadline': datetime(2024, 12, 22, 20, 0, 0),
                'event_date': datetime(2024, 12, 24, 21, 0, 0)
            },
            {
                'event_name': 'Family Christmas 2024',
                'description': 'Family Secret Santa exchange',
                'admin_id': users[0].user_id,  # Admin User
                'budget_min': 1000.0,
                'budget_max': 5000.0,
                'currency': 'INR',
                'invite_code': 'FAMILY2024',
                'status': 'pending',
                'assignment_done': False,
                'gift_deadline': datetime(2024, 12, 23, 17, 0, 0),
                'event_date': datetime(2024, 12, 25, 18, 0, 0)
            }
        ]
        
        events = []
        for event_data in events_data:
            event = Event(**event_data)
            events.append(event)
            db.session.add(event)
        
        db.session.commit()
        print(f"✓ Inserted {len(events)} events")
        
        # =====================================================
        # 3. Insert Wishlists
        # =====================================================
        print("Inserting wishlists...")
        
        wishlists_data = [
            {
                'user_id': users[2].user_id,  # John Doe
                'event_id': events[0].event_id,
                'preferences': '["books", "electronics", "coffee"]',
                'dislikes': '["perfume", "clothes"]',
                'gift_category': 'Electronics',
                'color_preference': 'Blue, Black',
                'hobby_tags': 'reading,gaming,coffee',
                'notes': 'I love tech gadgets and books. Prefer practical gifts.'
            },
            {
                'user_id': users[3].user_id,  # Jane Smith
                'event_id': events[0].event_id,
                'preferences': '["cosmetics", "jewelry", "handbags"]',
                'dislikes': '["electronics", "books"]',
                'gift_category': 'Fashion',
                'clothing_size': 'M',
                'color_preference': 'Pink, Purple',
                'hobby_tags': 'fashion,makeup,shopping',
                'notes': 'Love fashion and beauty products!'
            },
            {
                'user_id': users[4].user_id,  # Mike Johnson
                'event_id': events[0].event_id,
                'preferences': '["sports", "fitness", "gadgets"]',
                'dislikes': '["books", "cosmetics"]',
                'gift_category': 'Sports',
                'clothing_size': 'L',
                'color_preference': 'Red, Blue',
                'hobby_tags': 'fitness,sports,gaming',
                'notes': 'Fitness enthusiast. Love sports equipment.'
            },
            {
                'user_id': users[5].user_id,  # Sarah Williams
                'event_id': events[0].event_id,
                'preferences': '["art supplies", "books", "plants"]',
                'dislikes': '["electronics", "sports"]',
                'gift_category': 'Arts & Crafts',
                'color_preference': 'Green, Yellow',
                'hobby_tags': 'art,reading,gardening',
                'notes': 'Artist and book lover. Love plants too!'
            },
            {
                'user_id': users[6].user_id,  # David Brown
                'event_id': events[0].event_id,
                'preferences': '["watches", "wallets", "grooming"]',
                'dislikes': '["art supplies", "plants"]',
                'gift_category': 'Accessories',
                'color_preference': 'Black, Brown',
                'hobby_tags': 'fashion,grooming',
                'notes': 'Love accessories and grooming products.'
            }
        ]
        
        wishlists = []
        for wishlist_data in wishlists_data:
            wishlist = Wishlist(**wishlist_data)
            wishlists.append(wishlist)
            db.session.add(wishlist)
        
        db.session.commit()
        print(f"✓ Inserted {len(wishlists)} wishlists")
        
        # =====================================================
        # 4. Insert Participants
        # =====================================================
        print("Inserting participants...")
        
        # Event 1 participants
        participants = []
        
        # Event 1: Office Christmas
        for i, user in enumerate([users[0], users[2], users[3], users[4], users[5], users[6]]):
            wishlist_id = wishlists[i-1].wishlist_id if i > 0 and i-1 < len(wishlists) else None
            participant = Participant(
                event_id=events[0].event_id,
                user_id=user.user_id,
                wishlist_id=wishlist_id,
                status='active'
            )
            participants.append(participant)
            db.session.add(participant)
        
        # Event 2: College Friends
        for user in [users[1], users[7], users[8], users[9], users[10], users[11]]:
            participant = Participant(
                event_id=events[1].event_id,
                user_id=user.user_id,
                status='active'
            )
            participants.append(participant)
            db.session.add(participant)
        
        # Event 3: Family (pending)
        for user in [users[0], users[2], users[3]]:
            participant = Participant(
                event_id=events[2].event_id,
                user_id=user.user_id,
                status='active'
            )
            participants.append(participant)
            db.session.add(participant)
        
        db.session.commit()
        print(f"✓ Inserted {len(participants)} participants")
        
        # =====================================================
        # 5. Insert Assignments
        # =====================================================
        print("Inserting assignments...")
        
        # Event 1 assignments (circular: 0->2->3->4->5->6->0)
        event1_participants = [p for p in participants if p.event_id == events[0].event_id]
        assignments = []
        
        for i in range(len(event1_participants)):
            giver = event1_participants[i]
            receiver = event1_participants[(i + 1) % len(event1_participants)]
            
            assignment = Assignment(
                event_id=events[0].event_id,
                giver_id=giver.participant_id,
                receiver_id=receiver.participant_id,
                compatibility_score=0.7,
                gift_status='pending' if i < len(event1_participants) - 1 else 'purchased'
            )
            assignments.append(assignment)
            db.session.add(assignment)
        
        # Event 2 assignments
        event2_participants = [p for p in participants if p.event_id == events[1].event_id]
        for i in range(len(event2_participants)):
            giver = event2_participants[i]
            receiver = event2_participants[(i + 1) % len(event2_participants)]
            
            assignment = Assignment(
                event_id=events[1].event_id,
                giver_id=giver.participant_id,
                receiver_id=receiver.participant_id,
                compatibility_score=0.75,
                gift_status='delivered' if i == len(event2_participants) - 1 else 'pending'
            )
            assignments.append(assignment)
            db.session.add(assignment)
        
        db.session.commit()
        print(f"✓ Inserted {len(assignments)} assignments")
        
        # =====================================================
        # 6. Insert Messages
        # =====================================================
        print("Inserting messages...")
        
        messages_data = [
            {
                'event_id': events[0].event_id,
                'sender_id': users[2].user_id,  # John
                'receiver_id': users[3].user_id,  # Jane
                'message_text': 'Hi! I got you for Secret Santa. Any specific preferences?',
                'is_read': False
            },
            {
                'event_id': events[0].event_id,
                'sender_id': users[3].user_id,  # Jane
                'receiver_id': users[4].user_id,  # Mike
                'message_text': 'Hey! Looking forward to your gift! I love surprises.',
                'is_read': True
            },
            {
                'event_id': events[1].event_id,
                'sender_id': users[7].user_id,  # Emily
                'receiver_id': users[8].user_id,  # Robert
                'message_text': 'Hey! Got you for Secret Santa. What are your interests?',
                'is_read': False
            }
        ]
        
        messages = []
        for msg_data in messages_data:
            message = Message(**msg_data)
            messages.append(message)
            db.session.add(message)
        
        db.session.commit()
        print(f"✓ Inserted {len(messages)} messages")
        
        # =====================================================
        # Summary
        # =====================================================
        print("\n" + "="*50)
        print("DATA INSERTION COMPLETE!")
        print("="*50)
        print(f"Users: {User.query.count()}")
        print(f"Events: {Event.query.count()}")
        print(f"Wishlists: {Wishlist.query.count()}")
        print(f"Participants: {Participant.query.count()}")
        print(f"Assignments: {Assignment.query.count()}")
        print(f"Messages: {Message.query.count()}")
        print("="*50)
        
        print("\nTest Credentials:")
        print("Admin: admin@secretsanta.com / admin123")
        print("Manager: manager@secretsanta.com / manager123")
        print("Users: [any user email] / user123")
        
        print("\nEvent Invite Codes:")
        for event in events:
            print(f"  - {event.event_name}: {event.invite_code}")

if __name__ == '__main__':
    insert_sample_data()
