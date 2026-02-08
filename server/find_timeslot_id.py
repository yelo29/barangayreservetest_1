import sqlite3

conn = sqlite3.connect('barangay.db')
cursor = conn.cursor()

# Find the time slot ID for 6:00 AM - 8:00 AM in Community Hall
cursor.execute('SELECT id FROM time_slots WHERE facility_id = 1 AND start_time = ?', ('6:00 AM',))
slot = cursor.fetchone()

if slot:
    print(f'Found time slot ID: {slot[0]} for 6:00 AM - 8:00 AM')
else:
    print('Time slot not found')

conn.close()
