"""
Direct Admin User Creation Script
Creates admin user directly in database using SQL
Run this to create admin user for admin login
"""
from app import create_app, db
from app.models import User

def create_admin_direct():
    """Create admin user directly"""
    app = create_app()
    
    with app.app_context():
        print("=" * 60)
        print("ADMIN USER CREATION SCRIPT")
        print("=" * 60)
        
        # Check database connection
        try:
            db.session.execute(db.text("SELECT 1"))
            print("✓ Database connection: OK")
        except Exception as e:
            print(f"✗ Database connection failed: {e}")
            print("\nPlease check:")
            print("  1. MySQL/WAMP is running (GREEN icon)")
            print("  2. Database 'secret_santa_db' exists")
            print("  3. config.py has correct database settings")
            return
        
        # Check if users table exists
        try:
            User.query.first()
            print("✓ Users table exists")
        except Exception as e:
            print(f"✗ Users table error: {e}")
            print("\nPlease run: python create_tables.py")
            return
        
        admin_email = 'admin@secretsanta.com'
        admin_password = 'admin123'
        
        # Check if admin already exists
        existing = User.query.filter_by(email=admin_email).first()
        
        if existing:
            print(f"\n⚠ Admin user already exists!")
            print(f"  Email: {existing.email}")
            print(f"  Name: {existing.name}")
            print(f"  Role: {existing.role}")
            
            # Update password and role
            print("\nUpdating admin user...")
            existing.password = admin_password
            existing.role = 'super_admin'
            existing.is_active = True
            
            try:
                db.session.commit()
                print("✓ Admin user updated successfully!")
            except Exception as e:
                db.session.rollback()
                print(f"✗ Error updating admin: {e}")
                return
        else:
            print(f"\nCreating new admin user...")
            
            admin = User(
                name='Admin User',
                email=admin_email,
                password=admin_password,  # Plain text password
                role='super_admin',
                is_active=True
            )
            
            try:
                db.session.add(admin)
                db.session.commit()
                print("✓ Admin user created successfully!")
            except Exception as e:
                db.session.rollback()
                print(f"✗ Error creating admin: {e}")
                print("\nError details:")
                import traceback
                print(traceback.format_exc())
                return
        
        # Verify admin user
        verify_admin = User.query.filter_by(email=admin_email).first()
        if verify_admin:
            print("\n" + "=" * 60)
            print("ADMIN USER READY!")
            print("=" * 60)
            print("\nLogin Credentials:")
            print(f"  Email: {admin_email}")
            print(f"  Password: {admin_password}")
            print(f"  Role: {verify_admin.role}")
            print("\nAccess URLs:")
            print("  Regular Login: http://localhost:5000/auth/login")
            print("  Admin Login: http://localhost:5000/auth/admin-login")
            print("=" * 60)
        else:
            print("✗ Verification failed - admin user not found!")

if __name__ == '__main__':
    create_admin_direct()
