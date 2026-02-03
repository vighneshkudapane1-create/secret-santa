"""
Add privacy columns to events table
Run this once to add privacy settings to existing database
"""
from app import create_app, db
from sqlalchemy import text

def add_privacy_columns():
    """Add privacy columns to events table"""
    app = create_app()
    
    with app.app_context():
        try:
            print("=" * 60)
            print("ADDING PRIVACY COLUMNS TO EVENTS TABLE")
            print("=" * 60)
            
            # Check if columns already exist
            result = db.session.execute(text("""
                SELECT COLUMN_NAME 
                FROM INFORMATION_SCHEMA.COLUMNS 
                WHERE TABLE_SCHEMA = DATABASE() 
                AND TABLE_NAME = 'events' 
                AND COLUMN_NAME = 'privacy_type'
            """))
            
            if result.fetchone():
                print("✓ Privacy columns already exist")
                print("=" * 60)
                return
            
            # Add privacy columns
            print("\nAdding privacy columns...")
            
            db.session.execute(text("""
                ALTER TABLE events 
                ADD COLUMN privacy_type VARCHAR(20) DEFAULT 'public' 
                COMMENT 'public, private'
            """))
            
            db.session.execute(text("""
                ALTER TABLE events 
                ADD COLUMN visibility VARCHAR(20) DEFAULT 'all' 
                COMMENT 'all, participants_only, invite_only'
            """))
            
            db.session.execute(text("""
                ALTER TABLE events 
                ADD COLUMN allow_public_join BOOLEAN DEFAULT TRUE 
                COMMENT 'Can anyone with invite code join?'
            """))
            
            db.session.commit()
            
            print("✓ Privacy columns added successfully!")
            print("  - privacy_type (public/private)")
            print("  - visibility (all/participants_only/invite_only)")
            print("  - allow_public_join (true/false)")
            print("=" * 60)
            print("\nAll existing events set to:")
            print("  - Privacy: Public")
            print("  - Visibility: All")
            print("  - Allow Public Join: Yes")
            print("=" * 60)
            
        except Exception as e:
            db.session.rollback()
            print(f"✗ Error: {e}")
            print("\nIf columns already exist, this is normal.")
            print("If error persists, check database connection.")

if __name__ == '__main__':
    add_privacy_columns()
