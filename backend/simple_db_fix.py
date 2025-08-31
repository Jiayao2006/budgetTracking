#!/usr/bin/env python3
"""
Simple direct database fix for production
"""
import os
import sys

def fix_production_db():
    print("🚨 FIXING PRODUCTION DATABASE...")
    
    try:
        # Import required modules
        from sqlalchemy import create_engine, text
        
        # Get production database URL
        database_url = os.environ.get('DATABASE_URL')
        if not database_url:
            print("❌ DATABASE_URL not found!")
            return False
            
        print(f"🔗 Connecting to database...")
        engine = create_engine(database_url)
        
        with engine.connect() as conn:
            print("🔧 Adding missing columns...")
            
            # Add original_amount column
            try:
                conn.execute(text("ALTER TABLE spendings ADD COLUMN original_amount FLOAT"))
                print("✅ Added original_amount column")
            except Exception as e:
                if "already exists" in str(e).lower():
                    print("✅ original_amount column already exists")
                else:
                    print(f"⚠️ Error adding original_amount: {e}")
            
            # Add label column
            try:
                conn.execute(text("ALTER TABLE spendings ADD COLUMN label VARCHAR(100)"))
                print("✅ Added label column")
            except Exception as e:
                if "already exists" in str(e).lower():
                    print("✅ label column already exists")
                else:
                    print(f"⚠️ Error adding label: {e}")
            
            # Update original_amount values
            try:
                result = conn.execute(text("UPDATE spendings SET original_amount = amount WHERE original_amount IS NULL"))
                print(f"✅ Updated {result.rowcount} rows with original_amount")
            except Exception as e:
                print(f"⚠️ Error updating original_amount: {e}")
            
            # Make original_amount NOT NULL
            try:
                conn.execute(text("ALTER TABLE spendings ALTER COLUMN original_amount SET NOT NULL"))
                print("✅ Made original_amount NOT NULL")
            except Exception as e:
                print(f"⚠️ Error setting NOT NULL: {e}")
            
            conn.commit()
            print("✅ All changes committed!")
            
            # Test the fix
            try:
                result = conn.execute(text("SELECT COUNT(*) FROM spendings"))
                count = result.scalar()
                print(f"✅ Database test passed! Found {count} spending records")
                return True
            except Exception as e:
                print(f"❌ Database test failed: {e}")
                return False
                
    except Exception as e:
        print(f"❌ Fix failed: {e}")
        return False

if __name__ == "__main__":
    success = fix_production_db()
    if success:
        print("🎉 DATABASE FIX COMPLETED SUCCESSFULLY!")
        print("Your application should now work correctly.")
    else:
        print("❌ DATABASE FIX FAILED!")
        print("Please contact support or try manual SQL commands.")
    
    sys.exit(0 if success else 1)
