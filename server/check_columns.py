import sqlite3

conn = sqlite3.connect('barangay_reserve.db')
cursor = conn.cursor()

cursor.execute('PRAGMA table_info(bookings)')
columns = cursor.fetchall()

print('Bookings table columns:')
for col in columns:
    print(f'{col[1]} ({col[2]})')

conn.close()
