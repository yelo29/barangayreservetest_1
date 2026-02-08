import sqlite3

conn = sqlite3.connect('barangay.db')
cursor = conn.cursor()

print('=== ALL TABLES ===')
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()
for table in tables:
    print(f'Table: {table[0]}')

print('\n=== FACILITIES ===')
try:
    cursor.execute('SELECT id, name FROM facilities ORDER BY id')
    facilities = cursor.fetchall()
    for f in facilities:
        print(f'ID: {f[0]}, Name: {f[1]}')
except Exception as e:
    print(f'Error: {e}')

print('\n=== TIME SLOTS ===')
try:
    cursor.execute('SELECT facility_id, start_time, end_time FROM time_slots ORDER BY facility_id, start_time')
    slots = cursor.fetchall()
    for slot in slots:
        print(f'Facility ID: {slot[0]}, Start: {slot[1]}, End: {slot[2]}')
except Exception as e:
    print(f'Error: {e}')

conn.close()
