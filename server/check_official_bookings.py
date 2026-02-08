#!/usr/bin/env python3
import sqlite3

def check_official_bookings():
    conn = sqlite3.connect('barangay.db')
    cursor = conn.cursor()
    
    # Check official bookings
    cursor.execute('''
        SELECT b.id, b.booking_date, b.start_time, b.status, u.email, u.role, f.name
        FROM bookings b
        LEFT JOIN users u ON b.user_id = u.id
        LEFT JOIN facilities f ON b.facility_id = f.id
        WHERE u.role = 'official'
        ORDER BY b.booking_date DESC, b.created_at DESC
        LIMIT 10
    ''')
    
    official_bookings = cursor.fetchall()
    print('Official bookings:')
    for booking in official_bookings:
        print(f'  ID: {booking[0]}, Date: {booking[1]}, Time: {booking[2]}, Status: {booking[3]}, Email: {booking[4]}, Role: {booking[5]}, Facility: {booking[6]}')
    
    # Check specifically for 2026-02-10
    print(f'\n🔍 Checking 2026-02-10 specifically:')
    cursor.execute('''
        SELECT b.id, b.booking_date, b.start_time, b.status, u.email, u.role, f.name
        FROM bookings b
        LEFT JOIN users u ON b.user_id = u.id
        LEFT JOIN facilities f ON b.facility_id = f.id
        WHERE u.role = 'official'
        AND b.booking_date = '2026-02-10'
        AND b.status = 'approved'
    ''')
    
    target_date_bookings = cursor.fetchall()
    if target_date_bookings:
        for booking in target_date_bookings:
            print(f'  ✅ Found: ID {booking[0]} - {booking[6]} - {booking[4]}')
    else:
        print(f'  ❌ No official bookings found for 2026-02-10')
    
    conn.close()

if __name__ == '__main__':
    check_official_bookings()
