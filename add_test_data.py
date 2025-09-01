#!/usr/bin/env python3
"""
Add test spending data for user ID 2 (tanjiayao2@gmail.com)
"""
import os
import sys
import sqlite3
from pathlib import Path
from datetime import date

# Change to backend directory
backend_dir = Path(__file__).parent / "backend"
db_path = backend_dir / "budget.db"

print(f"📋 Adding test spending for user ID 2...")

# Connect to database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Check if we have required columns
cursor.execute("PRAGMA table_info(spendings)")
columns = [col[1] for col in cursor.fetchall()]
print(f"Available columns: {columns}")

# Insert test spending for user 2
today = date.today().isoformat()
test_spendings = [
    (50.00, 50.00, 'SGD', 'SGD', 1.0, 'Food', 'Lunch at restaurant', 'Coffeehouse', 'lunch', today, 2),
    (25.00, 25.00, 'SGD', 'SGD', 1.0, 'Transportation', 'Bus fare', 'Public Transport', 'transport', today, 2),
    (100.00, 100.00, 'SGD', 'SGD', 1.0, 'Shopping', 'Groceries', 'Supermarket', 'groceries', today, 2),
]

# Determine which columns to insert based on what's available
if 'original_amount' in columns and 'label' in columns:
    # Full schema with all columns
    insert_sql = """
    INSERT INTO spendings (
        amount, original_amount, original_currency, display_currency, exchange_rate,
        category, description, location, label, date, user_id
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """
    cursor.executemany(insert_sql, test_spendings)
elif 'original_amount' in columns:
    # Schema with original_amount but no label
    test_spendings_no_label = [(s[0], s[1], s[2], s[3], s[4], s[5], s[6], s[7], s[9], s[10]) for s in test_spendings]
    insert_sql = """
    INSERT INTO spendings (
        amount, original_amount, original_currency, display_currency, exchange_rate,
        category, description, location, date, user_id
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """
    cursor.executemany(insert_sql, test_spendings_no_label)
else:
    # Basic schema (amount, category, location, date, user_id)
    test_spendings_basic = [(s[0], s[5], s[7], s[9], s[10]) for s in test_spendings]
    insert_sql = """
    INSERT INTO spendings (amount, category, location, date, user_id)
    VALUES (?, ?, ?, ?, ?)
    """
    cursor.executemany(insert_sql, test_spendings_basic)

conn.commit()

# Verify the data was added
cursor.execute("SELECT COUNT(*) FROM spendings WHERE user_id = 2")
count = cursor.fetchone()[0]
print(f"✅ Added test data. User 2 now has {count} spendings.")

cursor.execute("SELECT id, amount, category, location, date FROM spendings WHERE user_id = 2")
user_spendings = cursor.fetchall()
for spending in user_spendings:
    print(f"   - ID: {spending[0]}, Amount: {spending[1]}, Category: {spending[2]}, Location: {spending[3]}, Date: {spending[4]}")

conn.close()
