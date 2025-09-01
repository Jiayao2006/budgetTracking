#!/usr/bin/env python3
"""
Script to reset a user's password for testing purposes
"""

import sqlite3
import bcrypt
import os

# Database path
db_path = os.path.join(os.path.dirname(__file__), 'backend', 'budget.db')

def reset_user_password(email: str, new_password: str):
    """Reset a user's password"""
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Hash the new password
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), salt)
        
        # Update the user's password
        cursor.execute(
            "UPDATE users SET hashed_password = ? WHERE email = ?", 
            (hashed_password, email)
        )
        
        if cursor.rowcount == 0:
            print(f"❌ User with email {email} not found")
            return False
            
        conn.commit()
        print(f"✅ Password reset successfully for {email}")
        print(f"🔑 New password: {new_password}")
        return True
        
    except Exception as e:
        print(f"❌ Error resetting password: {e}")
        return False
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    # Reset password for test user
    email = "tanjiayao2@gmail.com"
    password = "test123"
    
    print(f"🔄 Resetting password for {email}...")
    reset_user_password(email, password)
