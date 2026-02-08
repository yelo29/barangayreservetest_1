import sqlite3

conn = sqlite3.connect('barangay.db')
cursor = conn.cursor()

print('=== BOOKINGS TABLE SCHEMA ===')
cursor.execute('SELECT sql FROM sqlite_master WHERE type="table" AND name="bookings"')
schema = cursor.fetchone()[0]
print(schema)
print()

conn.close()
