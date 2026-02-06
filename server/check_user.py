#!/usr/bin/env python3
import sqlite3

def check_user():
    conn = sqlite3.connect('barangay.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT email, password FROM users WHERE email=?', ('leo052904@gmail.com',))
    result = cursor.fetchone()
    
    if result:
        print(f'✅ User found:')
        print(f'📧 Email: {result[0]}')
        print(f'🔑 Password: {result[1]}')
    else:
        print('❌ User not found')
        
        # Check all users
        cursor.execute('SELECT email, password FROM users LIMIT 5')
        users = cursor.fetchall()
        print(f'📋 Total users found: {len(users)}')
        for user in users:
            print(f'  - {user[0]}')
    
    conn.close()

if __name__ == "__main__":
    check_user()
