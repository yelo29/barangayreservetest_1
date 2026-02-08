#!/usr/bin/env python3
import sqlite3

def check_users_table():
    conn = sqlite3.connect('barangay.db')
    cursor = conn.cursor()
    
    # Get users table schema
    cursor.execute('PRAGMA table_info(users)')
    columns = cursor.fetchall()
    print('Users table columns:')
    for col in columns:
        print(f'  {col[1]} ({col[2]})')
    
    # Check sample users
    cursor.execute('SELECT id, email, role FROM users LIMIT 5')
    users = cursor.fetchall()
    print('\nSample users:')
    for user in users:
        print(f'  ID: {user[0]}, Email: {user[1]}, Role: {user[2]}')
    
    conn.close()

if __name__ == '__main__':
    check_users_table()
