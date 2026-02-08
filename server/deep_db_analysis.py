import sqlite3
import os

print('=== DEEP DATABASE ANALYSIS ===')
db_files = [f for f in os.listdir('.') if f.endswith('.db')]
print(f'DB files found: {db_files}')

for db_file in db_files:
    print(f'\n=== {db_file} ===')
    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        
        # Check if it has tables
        cursor.execute('SELECT name FROM sqlite_master WHERE type="table"')
        tables = cursor.fetchall()
        print(f'Tables: {[table[0] for table in tables]}')
        
        if 'users' in [table[0] for table in tables]:
            cursor.execute('SELECT COUNT(*) FROM users')
            user_count = cursor.fetchone()[0]
            print(f'Users: {user_count}')
            
            # Look for leo052904@gmail.com
            cursor.execute('SELECT id, email, full_name, role FROM users WHERE email LIKE "%leo%"')
            leo_users = cursor.fetchall()
            for leo in leo_users:
                print(f'  LEO user: ID={leo[0]}, Email={leo[1]}, Name={leo[2]}')
        
        if 'bookings' in [table[0] for table in tables]:
            cursor.execute('SELECT COUNT(*) FROM bookings')
            booking_count = cursor.fetchone()[0]
            print(f'Bookings: {booking_count}')
        
        # Check time slots
        if 'time_slots' in [table[0] for table in tables]:
            cursor.execute('SELECT COUNT(*) FROM time_slots')
            slot_count = cursor.fetchone()[0]
            print(f'Time slots: {slot_count}')
        
        conn.close()
    except Exception as e:
        print(f'Error with {db_file}: {e}')
