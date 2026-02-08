import sqlite3

conn = sqlite3.connect('barangay.db')
cursor = conn.cursor()

print('=== TIME SLOTS TABLE SCHEMA ===')
cursor.execute('PRAGMA table_info(time_slots)')
columns = cursor.fetchall()
for col in columns:
    print(f'Column: {col[1]}, Type: {col[2]}, NotNull: {col[3]}, Default: {col[4]}, PK: {col[5]}')

conn.close()
