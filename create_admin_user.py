"""
Script to create admin user
Run this to create an admin account for accessing admin panel
"""
from app import create_app, db
from app.models import User

def create_admin():
    """Create admin user if doesn't exist"""
    app = create_app()
    
    with app.app_context():
        # Check if admin already exists
        existing = User.query.filter_by(email='admin@secretsanta.com').first()
        if existing:
            print("=" * 50)
            print("⚠ Admin user already exists!")
            print("=" * 50)
            print(f"Email: {existing.email}")
            print(f"Role: {existing.role}")
            print("=" * 50)
            return
        
        # Create admin user
        admin = User(
            name='Admin User',
            email='admin@secretsanta.com',
            password='admin123',  # Plain text password
            role='super_admin'
        )
        
        try:
            db.session.add(admin)
            db.session.commit()
            print("=" * 50)
            print("✓ Admin user created successfully!")
            print("=" * 50)
            print("Login Credentials:")
            print("  Email: admin@secretsanta.com")
            print("  Password: admin123")
            print("=" * 50)
            print("\nYou can now:")
            print("  1. Run: python run.py")
            print("  2. Go to: http://localhost:5000")
            print("  3. Login with above credentials")
            print("  4. Create an event to access admin panel")
            print("=" * 50)
        except Exception as e:
            db.session.rollback()
            print(f"✗ Error creating admin user: {e}")
            print("\nPlease check:")
            print("  1. Database is created")
            print("  2. Tables are created (run: python create_tables.py)")
            print("  3. Database connection in config.py is correct")

if __name__ == '__main__':
    create_admin()
