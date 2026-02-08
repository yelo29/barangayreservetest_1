import sqlite3

conn = sqlite3.connect('barangay.db')
cursor = conn.cursor()

print('=== BOOKINGS TABLE DETAILED SCHEMA ===')
cursor.execute('PRAGMA table_info(bookings)')
columns = cursor.fetchall()
for i, col in enumerate(columns):
    print(f'{i+1}: {col[1]} - {col[2]} - NOT NULL: {col[3]}')

conn.close()
