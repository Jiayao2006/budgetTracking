#!/usr/bin/env python3
"""
Database migration script to add label column to spendings table
"""

import sqlite3
import os
import sys

def migrate_database():
    # Get the database path
    db_path = os.path.join(os.path.dirname(__file__), "budget.db")
    
    if not os.path.exists(db_path):
        print(f"❌ Database file not found at {db_path}")
        return False
    
    try:
        # Connect to the database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check if label column already exists
        cursor.execute("PRAGMA table_info(spendings)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'label' in columns:
            print("✅ Label column already exists in spendings table")
            conn.close()
            return True
        
        # Add the label column
        print("🔄 Adding label column to spendings table...")
        cursor.execute("ALTER TABLE spendings ADD COLUMN label VARCHAR(100)")
        
        # Commit the changes
        conn.commit()
        
        print("✅ Successfully added label column to spendings table")
        
        # Verify the column was added
        cursor.execute("PRAGMA table_info(spendings)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'label' in columns:
            print("✅ Migration verified - label column exists")
        else:
            print("❌ Migration verification failed - label column not found")
            return False
        
        conn.close()
        return True
        
    except sqlite3.Error as e:
        print(f"❌ Database error during migration: {e}")
        if 'conn' in locals():
            conn.close()
        return False
    except Exception as e:
        print(f"❌ Unexpected error during migration: {e}")
        if 'conn' in locals():
            conn.close()
        return False

if __name__ == "__main__":
    print("🚀 Starting label column migration...")
    success = migrate_database()
    
    if success:
        print("🎉 Migration completed successfully!")
        sys.exit(0)
    else:
        print("💥 Migration failed!")
        sys.exit(1)
