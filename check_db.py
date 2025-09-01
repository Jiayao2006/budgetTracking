#!/usr/bin/env python3
"""
Quick script to check if there are any spendings in the database
"""
import os
import sys
import sqlite3
from pathlib import Path

# Change to backend directory
backend_dir = Path(__file__).parent / "backend"
os.chdir(backend_dir)

# Add backend to path for imports
sys.path.insert(0, str(backend_dir))

# Check if database file exists
db_path = backend_dir / "budget.db"
if not db_path.exists():
    print("❌ Database file does not exist!")
    sys.exit(1)

print(f"✅ Database file found: {db_path}")

# Connect and check tables
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Check if tables exist
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
print(f"📋 Tables found: {[table[0] for table in tables]}")

# Check users
if ('users',) in tables:
    cursor.execute("SELECT id, email, full_name, preferred_currency FROM users;")
    users = cursor.fetchall()
    print(f"👥 Users in database: {len(users)}")
    for user in users:
        print(f"   - ID: {user[0]}, Email: {user[1]}, Name: {user[2]}, Currency: {user[3]}")

# Check spendings
if ('spendings',) in tables:
    cursor.execute("SELECT COUNT(*) FROM spendings;")
    spending_count = cursor.fetchone()[0]
    print(f"💰 Spendings in database: {spending_count}")
    
    if spending_count > 0:
        cursor.execute("SELECT id, amount, category, location, date, user_id FROM spendings LIMIT 5;")
        spendings = cursor.fetchall()
        print("   Recent spendings:")
        for spending in spendings:
            print(f"   - ID: {spending[0]}, Amount: {spending[1]}, Category: {spending[2]}, User: {spending[5]}")

conn.close()
