import sqlite3

conn = sqlite3.connect('barangay.db')
cursor = conn.cursor()

# Check all bookings
cursor.execute('SELECT id, user_email, facility_id, date, status FROM bookings ORDER BY date DESC LIMIT 10')
bookings = cursor.fetchall()

print('Recent bookings:')
for booking in bookings:
    print(f'ID: {booking[0]}, Email: {booking[1]}, Facility: {booking[2]}, Date: {booking[3]}, Status: {booking[4]}')

# Check bookings for jl052904@gmail.com
cursor.execute('SELECT id, facility_id, date, status FROM bookings WHERE user_email = "jl052904@gmail.com"')
user_bookings = cursor.fetchall()

print('\nBookings for jl052904@gmail.com:')
for booking in user_bookings:
    print(f'ID: {booking[0]}, Facility: {booking[1]}, Date: {booking[2]}, Status: {booking[3]}')

conn.close()
