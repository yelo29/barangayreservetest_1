import sqlite3

conn = sqlite3.connect('barangay.db')
cursor = conn.cursor()

# Check bookings for 2026-02-23, Facility 1
cursor.execute('''
    SELECT b.id, u.full_name, u.email 
    FROM bookings b 
    LEFT JOIN users u ON b.user_id = u.id 
    WHERE b.booking_date = "2026-02-23" AND b.facility_id = 1 
    LIMIT 2
''')

results = cursor.fetchall()
print('Database check - Bookings for 2026-02-23, Facility 1:')
for result in results:
    print(f'  ID: {result[0]}, Name: {result[1]}, Email: {result[2]}')

conn.close()
