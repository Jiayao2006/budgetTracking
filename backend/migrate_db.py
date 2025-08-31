#!/usr/bin/env python3
"""
Database migration script to add currency support
"""
import sqlite3
import os
from pathlib import Path

def migrate_database():
    # Path to the database file
    db_path = Path(__file__).parent / "budget.db"
    
    if not db_path.exists():
        print("Database file does not exist yet. Skipping migration.")
        return
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Check if migration is needed by looking for the new columns
        cursor.execute("PRAGMA table_info(users)")
        user_columns = [col[1] for col in cursor.fetchall()]
        
        cursor.execute("PRAGMA table_info(spendings)")
        spending_columns = [col[1] for col in cursor.fetchall()]
        
        # Add preferred_currency to users table if not exists
        if 'preferred_currency' not in user_columns:
            print("Adding preferred_currency column to users table...")
            cursor.execute("ALTER TABLE users ADD COLUMN preferred_currency VARCHAR(3) DEFAULT 'USD'")
            cursor.execute("UPDATE users SET preferred_currency = 'USD' WHERE preferred_currency IS NULL")
        
        # Add currency columns to spendings table if not exists
        new_spending_columns = [
            ('original_amount', 'FLOAT'),
            ('original_currency', 'VARCHAR(3)'),
            ('display_currency', 'VARCHAR(3)'),
            ('exchange_rate', 'FLOAT')
        ]
        
        for col_name, col_type in new_spending_columns:
            if col_name not in spending_columns:
                print(f"Adding {col_name} column to spendings table...")
                cursor.execute(f"ALTER TABLE spendings ADD COLUMN {col_name} {col_type}")
        
        # Update existing records with default values
        print("Updating existing spending records with default currency values...")
        cursor.execute("""
            UPDATE spendings 
            SET original_amount = amount,
                original_currency = 'USD',
                display_currency = 'USD',
                exchange_rate = 1.0
            WHERE original_amount IS NULL
        """)
        
        conn.commit()
        print("✅ Database migration completed successfully!")
        
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    migrate_database()
