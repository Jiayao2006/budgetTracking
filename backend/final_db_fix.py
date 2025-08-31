#!/usr/bin/env python3
"""
FINAL DATABASE FIX - Run this in Render shell
This will definitely fix the PostgreSQL schema issues
"""
import os
import sys

def final_fix():
    print("🚨 FINAL DATABASE FIX STARTING...")
    print("=" * 50)
    
    try:
        from sqlalchemy import create_engine, text
        
        # Get database URL
        database_url = os.environ.get('DATABASE_URL')
        if not database_url:
            print("❌ DATABASE_URL environment variable not found!")
            print("Make sure you're running this on Render!")
            return False
            
        print(f"🔗 Connecting to PostgreSQL...")
        print(f"Database: {database_url.split('@')[1] if '@' in database_url else 'Unknown'}")
        
        engine = create_engine(database_url)
        
        with engine.connect() as conn:
            print("\n🔍 Checking current schema...")
            
            # Check current columns
            try:
                result = conn.execute(text("""
                    SELECT column_name 
                    FROM information_schema.columns 
                    WHERE table_name = 'spendings' 
                    ORDER BY column_name
                """))
                current_columns = [row[0] for row in result.fetchall()]
                print(f"Current spendings columns: {current_columns}")
            except Exception as e:
                print(f"⚠️ Could not check columns: {e}")
                current_columns = []
            
            # Fix missing columns
            print("\n🔧 Applying fixes...")
            
            # Fix 1: Add original_amount column
            if 'original_amount' not in current_columns:
                print("Adding original_amount column...")
                try:
                    conn.execute(text("ALTER TABLE spendings ADD COLUMN original_amount FLOAT"))
                    conn.execute(text("UPDATE spendings SET original_amount = amount"))
                    conn.execute(text("ALTER TABLE spendings ALTER COLUMN original_amount SET NOT NULL"))
                    print("✅ original_amount column added")
                except Exception as e:
                    print(f"❌ Error adding original_amount: {e}")
            else:
                print("✅ original_amount column already exists")
            
            # Fix 2: Add label column  
            if 'label' not in current_columns:
                print("Adding label column...")
                try:
                    conn.execute(text("ALTER TABLE spendings ADD COLUMN label VARCHAR(100)"))
                    print("✅ label column added")
                except Exception as e:
                    print(f"❌ Error adding label: {e}")
            else:
                print("✅ label column already exists")
            
            # Fix 3: Check users table
            try:
                result = conn.execute(text("""
                    SELECT column_name 
                    FROM information_schema.columns 
                    WHERE table_name = 'users' AND column_name = 'preferred_currency'
                """))
                if not result.fetchone():
                    print("Adding preferred_currency to users...")
                    conn.execute(text("""
                        ALTER TABLE users 
                        ADD COLUMN preferred_currency VARCHAR(3) NOT NULL DEFAULT 'USD'
                    """))
                    print("✅ preferred_currency column added")
                else:
                    print("✅ preferred_currency column already exists")
            except Exception as e:
                print(f"⚠️ Users table check failed: {e}")
            
            # Commit all changes
            conn.commit()
            print("\n💾 All changes committed!")
            
            # Final test
            print("\n🧪 Testing database...")
            try:
                result = conn.execute(text("""
                    SELECT 
                        COUNT(*) as total_spendings,
                        COUNT(original_amount) as with_original_amount,
                        COUNT(label) as with_labels
                    FROM spendings
                """))
                row = result.fetchone()
                print(f"✅ Test successful!")
                print(f"   Total spendings: {row[0]}")
                print(f"   With original_amount: {row[1]}")
                print(f"   With labels: {row[2]}")
                
                # Test a simple query that was failing
                result = conn.execute(text("""
                    SELECT id, amount, original_amount, label 
                    FROM spendings 
                    LIMIT 1
                """))
                print("✅ Complex query test passed!")
                
                return True
                
            except Exception as e:
                print(f"❌ Database test failed: {e}")
                return False
                
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🚀 Starting final database fix for Render PostgreSQL")
    success = final_fix()
    
    if success:
        print("\n" + "=" * 50)
        print("🎉 DATABASE FIX COMPLETED SUCCESSFULLY!")
        print("🌐 Your website should now work correctly!")
        print("🔄 Refresh your browser to see the changes")
        print("=" * 50)
    else:
        print("\n" + "=" * 50)
        print("❌ DATABASE FIX FAILED!")
        print("📧 Please share this output for further assistance")
        print("=" * 50)
    
    sys.exit(0 if success else 1)
