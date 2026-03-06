import sqlite3

conn = sqlite3.connect('barangay.db')
cursor = conn.cursor()

# Check for existing booking
cursor.execute('''
    SELECT id, facility_id, booking_date, start_time, end_time, status, user_id 
    FROM bookings 
    WHERE user_id = 52 AND facility_id = 16 AND booking_date = '2026-03-12' AND start_time = '2:00 PM - 4:00 PM'
''')

result = cursor.fetchall()
print('Existing booking:', result)

# Also check all bookings for this user on this date
cursor.execute('''
    SELECT id, facility_id, booking_date, start_time, end_time, status, user_id 
    FROM bookings 
    WHERE user_id = 52 AND booking_date = '2026-03-12'
''')

all_bookings = cursor.fetchall()
print('All bookings for user 52 on 2026-03-12:', all_bookings)

conn.close()
