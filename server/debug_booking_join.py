#!/usr/bin/env python3
import sqlite3

def debug_booking_join():
    conn = sqlite3.connect('barangay.db')
    cursor = conn.cursor()
    
    # Test the exact query used in server
    cursor.execute('''
        SELECT b.*, f.name as facility_name, u.full_name, u.email as user_email, u.verified, u.discount_rate, u.role as user_role
        FROM bookings b
        LEFT JOIN facilities f ON b.facility_id = f.id
        LEFT JOIN users u ON b.user_id = u.id
        ORDER BY b.booking_date DESC, b.start_time ASC
        LIMIT 3
    ''')
    
    bookings = cursor.fetchall()
    print('Test query results:')
    for i, booking in enumerate(bookings):
        print(f'  Booking {i+1}:')
        print(f'    booking_date: {booking[4]}')  # booking_date
        print(f'    facility_id: {booking[1]}')  # facility_id  
        print(f'    user_id: {booking[2]}')  # user_id
        print(f'    user_email: {booking[17]}')  # user_email (alias)
        print(f'    user_role: {booking[22]}')  # user_role (alias)
        print(f'    status: {booking[8]}')  # status
        print()
    
    conn.close()

if __name__ == '__main__':
    debug_booking_join()
