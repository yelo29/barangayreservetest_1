#!/usr/bin/env python3
"""
Create Comprehensive Test Booking
Create test booking with all required columns
"""

import sqlite3
from datetime import datetime

def create_test_booking():
    conn = sqlite3.connect('barangay.db')
    cursor = conn.cursor()
    
    print('🎨 CREATING COMPREHENSIVE TEST BOOKING')
    
    # Clear existing bookings
    cursor.execute('DELETE FROM bookings')
    
    # Test booking for Feb 18, 2026 - Community Hall (6:00 AM - 8:00 AM)
    # This should match the 6:00 AM - 8:00 AM time slot (ID: 163)
    cursor.execute('''
        INSERT INTO bookings (
            booking_reference, user_id, facility_id, time_slot_id, booking_date, start_time, end_time, 
            duration_hours, purpose, expected_attendees, special_requirements, contact_number, contact_address,
            base_rate, discount_rate, discount_amount, downpayment_amount, total_amount, status, created_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        f'BKG-{datetime.now().strftime("%Y%m%d%H%M%S")}',  # 1: booking_reference
        1,  # 2: user_id
        1,  # 3: facility_id
        163,  # 4: time_slot_id
        '2026-02-18',  # 5: booking_date
        '6:00 AM',  # 6: start_time
        '8:00 AM',  # 7: end_time
        2.0,  # 8: duration_hours
        'Official barangay meeting',  # 9: purpose
        10,  # 10: expected_attendees
        None,  # 11: special_requirements
        None,  # 12: contact_number
        None,  # 13: contact_address
        1000.0,  # 14: base_rate
        0.00,  # 15: discount_rate
        0.00,  # 16: discount_amount
        200.0,  # 17: downpayment_amount
        1000.0,  # 18: total_amount
        'pending',  # 19: status
        datetime.now().isoformat()  # 20: created_at
    ))
    
    conn.commit()
    conn.close()
    
    print('✅ Comprehensive test booking created:')
    print('  - Community Hall: Feb 18, 6:00 AM - 8:00 AM (pending)')
    print('🎯 This should now show as a time slot conflict in the official booking form!')

if __name__ == '__main__':
    create_test_booking()
