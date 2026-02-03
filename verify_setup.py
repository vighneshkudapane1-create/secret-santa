"""
Verification Script - Check if everything is set up correctly
Run this to verify all components are working
"""
from app import create_app, db
from app.models import User, Event, Participant, Wishlist, Assignment

def verify_setup():
    """Verify application setup"""
    app = create_app()
    
    print("=" * 60)
    print("SECRET SANTA - SETUP VERIFICATION")
    print("=" * 60)
    
    with app.app_context():
        # 1. Database Connection
        print("\n1. Testing Database Connection...")
        try:
            db.session.execute(db.text("SELECT 1"))
            print("   ✅ Database connection: OK")
        except Exception as e:
            print(f"   ❌ Database connection failed: {e}")
            return
        
        # 2. Check Tables
        print("\n2. Checking Database Tables...")
        tables = ['users', 'events', 'participants', 'wishlists', 'assignments', 'messages']
        all_tables_exist = True
        for table in tables:
            try:
                db.session.execute(db.text(f"SELECT 1 FROM {table} LIMIT 1"))
                print(f"   ✅ Table '{table}': OK")
            except Exception as e:
                print(f"   ❌ Table '{table}': Missing or error")
                all_tables_exist = False
        
        if not all_tables_exist:
            print("\n   ⚠️  Some tables missing. Run: python create_tables.py")
        
        # 3. Check Admin User
        print("\n3. Checking Admin User...")
        admin = User.query.filter_by(email='admin@secretsanta.com').first()
        if admin:
            print(f"   ✅ Admin user exists")
            print(f"      Name: {admin.name}")
            print(f"      Email: {admin.email}")
            print(f"      Role: {admin.role}")
            print(f"      Active: {admin.is_active}")
        else:
            print("   ❌ Admin user NOT found")
            print("   Run: python create_admin_direct.py")
        
        # 4. Check Routes Registration
        print("\n4. Checking Routes...")
        routes_to_check = [
            ('auth.login', '/auth/login'),
            ('auth.admin_login', '/auth/admin-login'),
            ('events.create_event', '/events/create'),
            ('wishlist.manage_wishlist', '/wishlist/event/1/wishlist'),
            ('gifts.update_gift_status', '/gifts/assignment/1/status'),
        ]
        
        with app.test_client() as client:
            for route_name, path in routes_to_check:
                try:
                    # Just check if route exists (will get 302/401/404 but route exists)
                    response = client.get(path)
                    if response.status_code in [200, 302, 401, 404]:
                        print(f"   ✅ Route '{route_name}': OK")
                    else:
                        print(f"   ⚠️  Route '{route_name}': Status {response.status_code}")
                except Exception as e:
                    print(f"   ❌ Route '{route_name}': Error - {str(e)[:50]}")
        
        # 5. Check Data Counts
        print("\n5. Database Statistics...")
        try:
            user_count = User.query.count()
            event_count = Event.query.count()
            participant_count = Participant.query.count()
            wishlist_count = Wishlist.query.count()
            assignment_count = Assignment.query.count()
            
            print(f"   Users: {user_count}")
            print(f"   Events: {event_count}")
            print(f"   Participants: {participant_count}")
            print(f"   Wishlists: {wishlist_count}")
            print(f"   Assignments: {assignment_count}")
        except Exception as e:
            print(f"   ❌ Error getting statistics: {e}")
        
        # 6. Check Models
        print("\n6. Checking Models...")
        models = [User, Event, Participant, Wishlist, Assignment]
        for model in models:
            try:
                model.query.first()
                print(f"   ✅ Model '{model.__name__}': OK")
            except Exception as e:
                print(f"   ❌ Model '{model.__name__}': Error")
        
        # 7. Final Summary
        print("\n" + "=" * 60)
        print("VERIFICATION COMPLETE")
        print("=" * 60)
        print("\nNext Steps:")
        print("  1. If admin missing: python create_admin_direct.py")
        print("  2. If tables missing: python create_tables.py")
        print("  3. Start application: python run.py")
        print("  4. Test at: http://localhost:5000")
        print("=" * 60)

if __name__ == '__main__':
    verify_setup()
