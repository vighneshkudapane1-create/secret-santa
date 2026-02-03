"""
Script to update database: Change password_hash column to password
Run this once to migrate existing database
"""
from app import create_app, db
from sqlalchemy import text

def update_password_column():
    """Update password_hash column to password"""
    app = create_app()
    
    with app.app_context():
        try:
            # Check if password_hash column exists
            result = db.session.execute(text("""
                SELECT COLUMN_NAME 
                FROM INFORMATION_SCHEMA.COLUMNS 
                WHERE TABLE_SCHEMA = DATABASE() 
                AND TABLE_NAME = 'users' 
                AND COLUMN_NAME = 'password_hash'
            """))
            
            if result.fetchone():
                print("=" * 60)
                print("Updating database: password_hash -> password")
                print("=" * 60)
                
                # Rename column
                db.session.execute(text("ALTER TABLE users CHANGE password_hash password VARCHAR(255) NOT NULL"))
                db.session.commit()
                
                print("✓ Column renamed successfully!")
                print("  password_hash -> password")
                print("=" * 60)
                print("\nNote: Existing hashed passwords need to be reset.")
                print("Run: python create_admin_user.py to create admin with plain password")
                print("=" * 60)
            else:
                # Check if password column exists
                result = db.session.execute(text("""
                    SELECT COLUMN_NAME 
                    FROM INFORMATION_SCHEMA.COLUMNS 
                    WHERE TABLE_SCHEMA = DATABASE() 
                    AND TABLE_NAME = 'users' 
                    AND COLUMN_NAME = 'password'
                """))
                
                if result.fetchone():
                    print("✓ Password column already exists. No changes needed.")
                else:
                    print("✗ Neither password_hash nor password column found!")
                    print("Please create tables first: python create_tables.py")
                    
        except Exception as e:
            db.session.rollback()
            print(f"✗ Error: {e}")
            print("\nIf column doesn't exist, you may need to:")
            print("  1. Drop and recreate tables: python create_tables.py")
            print("  2. Or manually update database schema")

if __name__ == '__main__':
    update_password_column()
