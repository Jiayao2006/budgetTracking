#!/usr/bin/env python3
"""
Urgent database fix for missing preferred_currency column
Run this manually if deployment times out
"""
import os
import sys

# Add current directory to path
sys.path.insert(0, '.')

def urgent_fix():
    print("🚨 URGENT DATABASE FIX STARTING...")
    
    try:
        from sqlalchemy import create_engine, text
        
        # Get database URL
        database_url = os.getenv("DATABASE_URL")
        if not database_url:
            print("❌ No DATABASE_URL found!")
            return
            
        print(f"🔗 Connecting to: {database_url[:50]}...")
        engine = create_engine(database_url)
        
        with engine.connect() as conn:
            # Check if column exists
            try:
                result = conn.execute(text("""
                    SELECT column_name 
                    FROM information_schema.columns 
                    WHERE table_name = 'users' 
                    AND column_name = 'preferred_currency'
                """))
                
                if result.fetchone():
                    print("✅ preferred_currency column already exists!")
                    return
                    
            except Exception:
                print("⚠️ Could not check column (might be SQLite)")
            
            # Add the missing column
            print("🔧 Adding preferred_currency column...")
            conn.execute(text("""
                ALTER TABLE users 
                ADD COLUMN preferred_currency VARCHAR(3) NOT NULL DEFAULT 'USD'
            """))
            conn.commit()
            print("✅ SUCCESS! preferred_currency column added!")
            
            # Test query
            result = conn.execute(text("SELECT COUNT(*) FROM users"))
            count = result.scalar()
            print(f"✅ Database working! Found {count} users")
            
    except Exception as e:
        print(f"❌ Fix failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    urgent_fix()
