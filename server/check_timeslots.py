import sqlite3
import os

db_path = 'barangay.db'
if os.path.exists(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Check if time_slots table exists and what's in it
    cursor.execute('SELECT name FROM sqlite_master WHERE type="table" AND name="time_slots"')
    table_exists = cursor.fetchone()
    
    if table_exists:
        print('Time slots table exists')
        cursor.execute('SELECT * FROM time_slots LIMIT 5')
        time_slots = cursor.fetchall()
        print('Sample time slots:')
        for slot in time_slots:
            print(f'   - ID: {slot[0]}, Start: {slot[1]}, End: {slot[2]}')
    else:
        print('Time slots table does not exist')
    
    conn.close()
else:
    print('Database file not found')
