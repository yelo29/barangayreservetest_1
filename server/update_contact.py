#!/usr/bin/env python3
"""
Update user contact number for verification testing
"""

import sqlite3
from config import Config

def update_contact_number():
    try:
        conn = sqlite3.connect(Config.DATABASE_PATH)
        cursor = conn.cursor()
        
        # Update user's contact number
        cursor.execute('UPDATE users SET contact_number = ? WHERE id = ?', ('09656692463', 14))
        
        conn.commit()
        print('✅ Updated user contact number')
        
        # Verify the update
        cursor.execute('SELECT id, email, full_name, contact_number FROM users WHERE id = 14')
        user = cursor.fetchone()
        print('👤 Updated user data:')
        print(f'  ID: {user[0]}')
        print(f'  Email: {user[1]}')
        print(f'  Name: {user[2]}')
        print(f'  Contact: {user[3]}')
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Error updating contact: {e}")
        return False

if __name__ == "__main__":
    update_contact_number()
