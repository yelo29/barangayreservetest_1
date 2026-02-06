import sqlite3
import os

db_path = 'barangay.db'
if os.path.exists(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Check if there are any tables with 'booking' in the name
    cursor.execute('SELECT name FROM sqlite_master WHERE type="table" AND name LIKE "%booking%"')
    tables = cursor.fetchall()
    print('Booking-related tables:')
    for table in tables:
        print(f'   - {table[0]}')
    
    # Check the actual schema of the bookings table
    cursor.execute('SELECT sql FROM sqlite_master WHERE type="table" AND name="bookings"')
    schema = cursor.fetchone()
    if schema:
        print('Bookings table schema:')
        print(schema[0])
    
    conn.close()
else:
    print('Database file not found')
