import sqlite3

conn = sqlite3.connect('barangay.db')
cursor = conn.cursor()

print('=== CURRENT TIME SLOTS FOR COMMUNITY HALL ===')
cursor.execute('SELECT id, start_time, end_time FROM time_slots WHERE facility_id = 1 ORDER BY start_time')
slots = cursor.fetchall()
for slot in slots:
    print(f'ID: {slot[0]}, Time: {slot[1]} - {slot[2]}')

print('\n=== BOOKINGS FOR 2026-02-12 COMMUNITY HALL ===')
cursor.execute('SELECT b.start_time, b.end_time, u.email FROM bookings b JOIN users u ON b.user_id = u.id WHERE b.facility_id = 1 AND b.booking_date = ?', ('2026-02-12',))
bookings = cursor.fetchall()
for booking in bookings:
    print(f'Time: {booking[0]} - {booking[1]}, User: {booking[2]}')

conn.close()
