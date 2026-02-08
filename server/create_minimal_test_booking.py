#!/usr/bin/env python3
"""
Create Minimal Test Booking
Create test booking with only required columns
"""

import sqlite3
from datetime import datetime

def create_test_booking():
    conn = sqlite3.connect('barangay.db')
    cursor = conn.cursor()
    
    print('🎨 CREATING MINIMAL TEST BOOKING')
    
    # Clear existing bookings
    cursor.execute('DELETE FROM bookings')
    
    # Test booking for Feb 18, 2026 - Community Hall (6:00 AM - 8:00 AM)
    # This should match the 6:00 AM - 8:00 AM time slot (ID: 163)
    cursor.execute('''
        INSERT INTO bookings (
            booking_reference, user_id, facility_id, time_slot_id, booking_date, start_time, end_time, status, created_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        f'BKG-{datetime.now().strftime("%Y%m%d%H%M%S")}',  # Generate unique booking reference
        1,  # Official user ID (captain@barangay.gov)
        1,  # Community Hall
        163,  # Time slot ID for 6:00 AM - 8:00 AM
        '2026-02-18',
        '6:00 AM',  # This should match the 6:00 AM - 8:00 AM slot
        '8:00 AM',
        'pending',
        datetime.now().isoformat()
    ))
    
    conn.commit()
    conn.close()
    
    print('✅ Minimal test booking created:')
    print('  - Community Hall: Feb 18, 6:00 AM - 8:00 AM (pending)')
    print('🎯 This should now show as a time slot conflict in the official booking form!')

if __name__ == '__main__':
    create_test_booking()
