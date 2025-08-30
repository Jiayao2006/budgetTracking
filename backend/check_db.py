import sqlite3

# Connect to the database
conn = sqlite3.connect('budget.db')
cursor = conn.cursor()

# Check the spendings table structure
cursor.execute('PRAGMA table_info(spendings)')
columns = cursor.fetchall()

print("Spendings table columns:")
for col in columns:
    print(f"  {col[1]} - {col[2]}")

# Check if user_id column exists
user_id_exists = any(col[1] == 'user_id' for col in columns)
print(f"\nuser_id column exists: {user_id_exists}")

# Check if there are any records
cursor.execute('SELECT COUNT(*) FROM spendings')
count = cursor.fetchone()[0]
print(f"Number of spending records: {count}")

cursor.execute('SELECT COUNT(*) FROM users')
user_count = cursor.fetchone()[0]
print(f"Number of users: {user_count}")

conn.close()
