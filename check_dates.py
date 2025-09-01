#!/usr/bin/env python3
"""
Script to check spending dates and formats
"""

import sqlite3
import os
from datetime import datetime

# Database path
db_path = os.path.join(os.path.dirname(__file__), 'backend', 'budget.db')

def check_spending_dates():
    """Check the exact dates of spending records"""
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, user_id, date, amount, category, description 
            FROM spendings 
            WHERE user_id = 2
            ORDER BY date DESC
        """)
        
        spendings = cursor.fetchall()
        
        print("📅 Spending dates for user 2:")
        for spending in spendings:
            id, user_id, date, amount, category, description = spending
            print(f"   - ID: {id}, Date: '{date}', Amount: {amount}, Category: {category}")
            
        # Also check today's date
        today = datetime.now().strftime('%Y-%m-%d')
        print(f"\n📅 Today's date: {today}")
        
        # Check if any spendings match today
        cursor.execute("""
            SELECT COUNT(*) FROM spendings 
            WHERE user_id = 2 AND date = ?
        """, (today,))
        
        today_count = cursor.fetchone()[0]
        print(f"📅 Spendings for today ({today}): {today_count}")
        
    except Exception as e:
        print(f"❌ Error checking dates: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    check_spending_dates()
