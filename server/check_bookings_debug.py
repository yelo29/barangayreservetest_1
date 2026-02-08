#!/usr/bin/env python3
import sqlite3

def check_bookings():
    conn = sqlite3.connect('barangay.db')
    cursor = conn.cursor()
    
    # Check total bookings
    cursor.execute('SELECT COUNT(*) FROM bookings')
    count = cursor.fetchone()[0]
    print(f'Total bookings in database: {count}')
    
    # Check sample bookings
    cursor.execute('SELECT booking_date, facility_id, user_email, status, user_role FROM bookings LIMIT 10')
    bookings = cursor.fetchall()
    print('Sample bookings:')
    for booking in bookings:
        print(f'  Date: {booking[0]}, Facility: {booking[1]}, Email: {booking[2]}, Status: {booking[3]}, Role: {booking[4]}')
    
    # Check specific date from logs
    target_date = '2026-02-20'
    target_facility = '2'
    cursor.execute('SELECT * FROM bookings WHERE booking_date = ? AND facility_id = ?', (target_date, target_facility))
    specific_bookings = cursor.fetchall()
    print(f'Bookings for {target_date}, facility {target_facility}: {len(specific_bookings)}')
    for booking in specific_bookings:
        print(f'  {booking}')
    
    conn.close()

if __name__ == '__main__':
    check_bookings()
