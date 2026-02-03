"""
Fix Admin Login Issues
This script will:
1. Check if admin user exists
2. Create admin user if doesn't exist
3. Reset admin password if exists
4. Verify database connection
"""
from app import create_app, db
from app.models import User

def fix_admin_login():
    """Fix admin login issues"""
    app = create_app()
    
    with app.app_context():
        print("=" * 60)
        print("ADMIN LOGIN FIX SCRIPT")
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
        
        # Check if admin user exists
        admin_email = 'admin@secretsanta.com'
        admin = User.query.filter_by(email=admin_email).first()
        
        if admin:
            print(f"\n✓ Admin user found: {admin.email}")
            print(f"  Name: {admin.name}")
            print(f"  Role: {admin.role}")
            print(f"  Active: {admin.is_active}")
            
            # Reset password
            print("\nResetting admin password...")
            admin.password = 'admin123'  # Plain text password
            try:
                db.session.commit()
                print("✓ Password reset successfully!")
            except Exception as e:
                db.session.rollback()
                print(f"✗ Error resetting password: {e}")
                return
        else:
            print(f"\n✗ Admin user not found: {admin_email}")
            print("Creating new admin user...")
            
            admin = User(
                name='Admin User',
                email=admin_email,
                password='admin123',  # Plain text password
                role='super_admin',
                is_active=True
            )
            
            try:
                db.session.add(admin)
                db.session.commit()
                print("✓ Admin user created successfully!")
            except Exception as e:
                db.session.rollback()
                print(f"✗ Error creating admin user: {e}")
                return
        
        # Verify password
        print("\nVerifying password...")
        test_user = User.query.filter_by(email=admin_email).first()
        if test_user and test_user.password == 'admin123':
            print("✓ Password verification: OK")
        else:
            print("✗ Password verification failed!")
            return
        
        # Final summary
        print("\n" + "=" * 60)
        print("ADMIN LOGIN FIXED!")
        print("=" * 60)
        print("\nLogin Credentials:")
        print(f"  Email: {admin_email}")
        print("  Password: admin123")
        print("\nNext Steps:")
        print("  1. Make sure application is running: python run.py")
        print("  2. Go to: http://localhost:5000/auth/login")
        print("  3. Login with above credentials")
        print("=" * 60)

if __name__ == '__main__':
    fix_admin_login()
