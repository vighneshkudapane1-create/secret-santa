"""
Simple script to create database tables
Run this after setting up the database
"""
from app import create_app, db

def create_tables():
    """Create all database tables"""
    app = create_app()
    
    with app.app_context():
        try:
            db.create_all()
            print("=" * 50)
            print("✓ Database tables created successfully!")
            print("=" * 50)
            print("\nTables created:")
            print("  - users")
            print("  - events")
            print("  - participants")
            print("  - wishlists")
            print("  - assignments")
            print("  - messages")
            print("\nYou can now insert sample data using:")
            print("  python sample_data_insert.py")
            print("=" * 50)
        except Exception as e:
            print(f"✗ Error creating tables: {e}")
            print("\nPlease check:")
            print("  1. MySQL is running (WAMP should be GREEN)")
            print("  2. Database 'secret_santa_db' exists")
            print("  3. Database credentials in config.py are correct")

if __name__ == '__main__':
    create_tables()
