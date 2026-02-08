#!/usr/bin/env python3
"""
Create Test Bookings
Create test bookings to verify time slot logic works correctly
"""

import sqlite3
from datetime import datetime

def create_test_bookings():
    conn = sqlite3.connect('barangay.db')
    cursor = conn.cursor()
    
    print('🎨 CREATING TEST BOOKINGS')
    
    # Clear existing bookings
    cursor.execute('DELETE FROM bookings')
    
    # Test booking for Feb 18, 2026 - Community Hall (6:00 AM - 8:00 AM)
    cursor.execute('''
        INSERT INTO bookings (
            user_id, facility_id, facility_name, booking_date, start_time, end_time, status, created_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        1,  # Official user ID (captain@barangay.gov)
        1,  # Community Hall
        'Community Hall',
        '2026-02-18',
        '6:00 AM',  # This should now match a 2-hour slot
        '8:00 AM',
        'pending',
        datetime.now().isoformat()
    ))
    
    # Test booking for Feb 18, 2026 - Basketball Court (10:00 AM - 12:00 PM)
    cursor.execute('''
        INSERT INTO bookings (
            user_id, facility_id, facility_name, booking_date, start_time, end_time, status, created_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        1,  # Official user ID (captain@barangay.gov)
        2,  # Basketball Court
        'Basketball Court',
        '2026-02-18',
        '10:00 AM',  # This should now match a 2-hour slot
        '12:00 PM',
        'pending',
        datetime.now().isoformat()
    ))
    
    conn.commit()
    conn.close()
    
    print('✅ Test bookings created:')
    print('  - Community Hall: Feb 18, 6:00 AM - 8:00 AM (pending)')
    print('  - Basketball Court: Feb 18, 10:00 AM - 12:00 PM (pending)')
    print()
    print('🎯 These should now show as time slot conflicts in the official booking form!')

if __name__ == '__main__':
    create_test_bookings()
