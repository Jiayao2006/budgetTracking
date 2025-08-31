#!/usr/bin/env python3
"""
Emergency fix for missing columns in the spendings table
"""
import os
import sys
import traceback

# Add the current directory to Python path
sys.path.insert(0, '.')

def fix_database():
    """Add missing columns to spendings table"""
    
    print("🚨 URGENT DATABASE FIX STARTING...")
    
    try:
        from sqlalchemy import create_engine, text
        
        # Get database URL
        database_url = os.getenv("DATABASE_URL")
        if not database_url:
            print("❌ No DATABASE_URL found!")
            print("Using default SQLite URL instead")
            database_url = "sqlite:///./budget.db"
            
        print(f"🔗 Connecting to: {database_url[:50]}...")
        engine = create_engine(database_url)
        
        with engine.connect() as conn:
            print("🔧 Checking for missing columns...")
            
            # Check if columns exist
            try:
                conn.execute(text("SELECT original_amount FROM spendings LIMIT 1"))
                print("✅ original_amount column already exists")
                has_original_amount = True
            except Exception:
                print("❌ original_amount column is missing")
                has_original_amount = False
            
            try:
                conn.execute(text("SELECT label FROM spendings LIMIT 1"))
                print("✅ label column already exists")
                has_label = True
            except Exception:
                print("❌ label column is missing")
                has_label = False
            
            # Add missing columns
            if not has_original_amount:
                print("🔧 Adding original_amount column...")
                conn.execute(text("ALTER TABLE spendings ADD COLUMN original_amount FLOAT"))
                conn.execute(text("UPDATE spendings SET original_amount = amount"))
                conn.execute(text("ALTER TABLE spendings ALTER COLUMN original_amount SET NOT NULL"))
                conn.commit()
                print("✅ Added original_amount column")
            
            if not has_label:
                print("🔧 Adding label column...")
                conn.execute(text("ALTER TABLE spendings ADD COLUMN label VARCHAR(100)"))
                conn.commit()
                print("✅ Added label column")
            
            # Test query
            try:
                result = conn.execute(text("SELECT COUNT(*) FROM spendings"))
                count = result.scalar()
                print(f"✅ Database working! Found {count} spending records")
            except Exception as e:
                print(f"⚠️ Test query failed: {e}")
            
            print("🎉 Database fix complete!")
            
    except Exception as e:
        print(f"❌ Fix failed: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    fix_database()
