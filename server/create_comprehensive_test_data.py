#!/usr/bin/env python3
"""
Create Comprehensive Test Data
Populate database with diverse scenarios for frontend testing
"""

import sqlite3
import json
from datetime import datetime, timedelta, date
import hashlib
from config import Config

def create_comprehensive_test_data():
    conn = sqlite3.connect(Config.DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    print('🎨 CREATING COMPREHENSIVE TEST DATA FOR FRONTEND TESTING')
    print('=' * 60)
    
    # Get current data
    users = cursor.execute('SELECT * FROM users').fetchall()
    facilities = cursor.execute('SELECT * FROM facilities').fetchall()
    time_slots = cursor.execute('SELECT * FROM time_slots').fetchall()
    
    # Create user lookup
    user_lookup = {user['email']: user for user in users}
    facility_lookup = {facility['name']: facility for facility in facilities}
    
    # Get dates for testing (past, today, future)
    today = date.today()
    past_date = (today - timedelta(days=5)).strftime('%Y-%m-%d')
    today_str = today.strftime('%Y-%m-%d')
    future_dates = [(today + timedelta(days=i)).strftime('%Y-%m-%d') for i in range(1, 15)]
    
    print(f'📅 Today: {today_str}')
    print(f'📅 Past Date: {past_date}')
    print(f'📅 Future Dates: {len(future_dates)} days')
    
    # Clear existing bookings to start fresh
    cursor.execute('DELETE FROM bookings')
    print('🗑️ Cleared existing bookings')
    
    booking_count = 0
    
    # 1. PAST BOOKINGS (should appear GRAY in calendar)
    print('\n📅 CREATING PAST BOOKINGS (GRAY - disabled)')
    past_bookings = [
        {
            'user_email': 'leo052904@gmail.com',
            'facility': 'Covered Court',
            'date': past_date,
            'timeslot': '09:00',
            'status': 'approved',
            'purpose': 'Past basketball practice'
        },
        {
            'user_email': 'saloestillopez@gmail.com',
            'facility': 'Meeting Room',
            'date': past_date,
            'timeslot': '14:00',
            'status': 'approved',
            'purpose': 'Past community meeting'
        }
    ]
    
    for booking in past_bookings:
        user = user_lookup[booking['user_email']]
        facility = facility_lookup[booking['facility']]
        time_slot = cursor.execute('''
            SELECT id, end_time, duration_minutes FROM time_slots 
            WHERE facility_id = ? AND start_time = ?
        ''', (facility['id'], booking['timeslot'])).fetchone()
        
        if time_slot:
            create_booking(cursor, user, facility, time_slot, booking)
            booking_count += 1
            print(f'  ✅ {booking["user_email"]} - {booking["facility"]} on {booking["date"]} {booking["timeslot"]} ({booking["status"]})')
    
    # 2. TODAY'S BOOKINGS (various statuses)
    print(f'\n📅 CREATING TODAY\'S BOOKINGS ({today_str})')
    today_bookings = [
        {
            'user_email': 'official@barangay.com',
            'facility': 'Multi-Purpose Hall',
            'date': today_str,
            'timeslot': '08:00',
            'status': 'approved',
            'purpose': 'Official barangay meeting'
        },
        {
            'user_email': 'leo052904@gmail.com',
            'facility': 'Covered Court',
            'date': today_str,
            'timeslot': '10:00',
            'status': 'pending',
            'purpose': 'Basketball practice'
        },
        {
            'user_email': 'saloestillopez@gmail.com',
            'facility': 'Covered Court',
            'date': today_str,
            'timeslot': '10:00',  # Same time - COMPETITIVE!
            'status': 'pending',
            'purpose': 'Sports training'
        }
    ]
    
    for booking in today_bookings:
        user = user_lookup[booking['user_email']]
        facility = facility_lookup[booking['facility']]
        time_slot = cursor.execute('''
            SELECT id, end_time, duration_minutes FROM time_slots 
            WHERE facility_id = ? AND start_time = ?
        ''', (facility['id'], booking['timeslot'])).fetchone()
        
        if time_slot:
            create_booking(cursor, user, facility, time_slot, booking)
            booking_count += 1
            print(f'  ✅ {booking["user_email"]} - {booking["facility"]} on {booking["date"]} {booking["timeslot"]} ({booking["status"]})')
    
    # 3. FUTURE BOOKINGS (diverse scenarios)
    print(f'\n📅 CREATING FUTURE BOOKINGS')
    
    # Day 1: Mixed statuses
    day1 = future_dates[0]
    day1_bookings = [
        {
            'user_email': 'resident@barangay.com',
            'facility': 'Basketball Court',
            'date': day1,
            'timeslot': '06:00',
            'status': 'approved',
            'purpose': 'Morning exercise'
        },
        {
            'user_email': 'leo052904@gmail.com',
            'facility': 'Community Garden',
            'date': day1,
            'timeslot': '08:00',
            'status': 'pending',
            'purpose': 'Gardening activity'
        }
    ]
    
    for booking in day1_bookings:
        user = user_lookup[booking['user_email']]
        facility = facility_lookup[booking['facility']]
        time_slot = cursor.execute('''
            SELECT id, end_time, duration_minutes FROM time_slots 
            WHERE facility_id = ? AND start_time = ?
        ''', (facility['id'], booking['timeslot'])).fetchone()
        
        if time_slot:
            create_booking(cursor, user, facility, time_slot, booking)
            booking_count += 1
            print(f'  ✅ {booking["user_email"]} - {booking["facility"]} on {booking["date"]} {booking["timeslot"]} ({booking["status"]})')
    
    # Day 2: Competitive booking scenario
    day2 = future_dates[1]
    day2_bookings = [
        {
            'user_email': 'leo052904@gmail.com',
            'facility': 'Meeting Room',
            'date': day2,
            'timeslot': '09:00',
            'status': 'pending',
            'purpose': 'Study group'
        },
        {
            'user_email': 'saloestillopez@gmail.com',
            'facility': 'Meeting Room',
            'date': day2,
            'timeslot': '09:00',  # Same time - COMPETITIVE!
            'status': 'pending',
            'purpose': 'Project meeting'
        },
        {
            'user_email': 'resident@barangay.com',
            'facility': 'Meeting Room',
            'date': day2,
            'timeslot': '09:00',  # Same time - COMPETITIVE!
            'status': 'pending',
            'purpose': 'Club meeting'
        }
    ]
    
    for booking in day2_bookings:
        user = user_lookup[booking['user_email']]
        facility = facility_lookup[booking['facility']]
        time_slot = cursor.execute('''
            SELECT id, end_time, duration_minutes FROM time_slots 
            WHERE facility_id = ? AND start_time = ?
        ''', (facility['id'], booking['timeslot'])).fetchone()
        
        if time_slot:
            create_booking(cursor, user, facility, time_slot, booking)
            booking_count += 1
            print(f'  ✅ {booking["user_email"]} - {booking["facility"]} on {booking["date"]} {booking["timeslot"]} ({booking["status"]})')
    
    # Day 3: Official bookings (GREEN - disabled)
    day3 = future_dates[2]
    day3_bookings = [
        {
            'user_email': 'official@barangay.com',
            'facility': 'Multi-Purpose Hall',
            'date': day3,
            'timeslot': '13:00',
            'status': 'approved',
            'purpose': 'Official event - whole day'
        },
        {
            'user_email': 'secretary@barangay.gov',
            'facility': 'Covered Court',
            'date': day3,
            'timeslot': '15:00',
            'status': 'approved',
            'purpose': 'Barangay sports tournament'
        }
    ]
    
    for booking in day3_bookings:
        user = user_lookup[booking['user_email']]
        facility = facility_lookup[booking['facility']]
        time_slot = cursor.execute('''
            SELECT id, end_time, duration_minutes FROM time_slots 
            WHERE facility_id = ? AND start_time = ?
        ''', (facility['id'], booking['timeslot'])).fetchone()
        
        if time_slot:
            create_booking(cursor, user, facility, time_slot, booking)
            booking_count += 1
            print(f'  ✅ {booking["user_email"]} - {booking["facility"]} on {booking["date"]} {booking["timeslot"]} ({booking["status"]})')
    
    # Day 4-7: Various scenarios
    for i, future_date in enumerate(future_dates[3:7]):
        date_bookings = []
        
        if i == 0:  # Day 4: User's approved bookings
            date_bookings = [
                {
                    'user_email': 'leo052904@gmail.com',
                    'facility': 'Covered Court',
                    'date': future_date,
                    'timeslot': '14:00',
                    'status': 'approved',
                    'purpose': 'Regular practice'
                },
                {
                    'user_email': 'leo052904@gmail.com',
                    'facility': 'Basketball Court',
                    'date': future_date,
                    'timeslot': '16:00',
                    'status': 'pending',
                    'purpose': 'Additional training'
                }
            ]
        elif i == 1:  # Day 5: Mixed user bookings
            date_bookings = [
                {
                    'user_email': 'saloestillopez@gmail.com',
                    'facility': 'Community Garden',
                    'date': future_date,
                    'timeslot': '10:00',
                    'status': 'approved',
                    'purpose': 'Community service'
                },
                {
                    'user_email': 'resident@barangay.com',
                    'facility': 'Meeting Room',
                    'date': future_date,
                    'timeslot': '14:00',
                    'status': 'pending',
                    'purpose': 'Resident meeting'
                }
            ]
        elif i == 2:  # Day 6: Available day (WHITE)
            # No bookings - should appear WHITE in calendar
            pass
        elif i == 3:  # Day 7: Full day bookings
            date_bookings = [
                {
                    'user_email': 'official@barangay.com',
                    'facility': 'Multi-Purpose Hall',
                    'date': future_date,
                    'timeslot': '08:00',
                    'status': 'approved',
                    'purpose': 'Morning event'
                },
                {
                    'user_email': 'leo052904@gmail.com',
                    'facility': 'Multi-Purpose Hall',
                    'date': future_date,
                    'timeslot': '10:00',
                    'status': 'pending',
                    'purpose': 'Afternoon activity'
                },
                {
                    'user_email': 'saloestillopez@gmail.com',
                    'facility': 'Multi-Purpose Hall',
                    'date': future_date,
                    'timeslot': '13:00',
                    'status': 'pending',
                    'purpose': 'Evening event'
                }
            ]
        
        for booking in date_bookings:
            user = user_lookup[booking['user_email']]
            facility = facility_lookup[booking['facility']]
            time_slot = cursor.execute('''
                SELECT id, end_time, duration_minutes FROM time_slots 
                WHERE facility_id = ? AND start_time = ?
            ''', (facility['id'], booking['timeslot'])).fetchone()
            
            if time_slot:
                create_booking(cursor, user, facility, time_slot, booking)
                booking_count += 1
                print(f'  ✅ {booking["user_email"]} - {booking["facility"]} on {booking["date"]} {booking["timeslot"]} ({booking["status"]})')
    
    # Create additional verification requests
    print(f'\n👤 CREATING ADDITIONAL VERIFICATION REQUESTS')
    additional_verifications = [
        {
            'user_email': 'leo052904@gmail.com',
            'verification_type': 'resident',
            'status': 'approved'  # Already verified
        },
        {
            'user_email': 'saloestillopez@gmail.com',
            'verification_type': 'non-resident',
            'status': 'approved'  # Already verified
        },
        {
            'user_email': 'resident@barangay.com',
            'verification_type': 'resident',
            'status': 'pending'  # Still pending
        }
    ]
    
    # Clear existing verification requests
    cursor.execute('DELETE FROM verification_requests')
    
    for vr in additional_verifications:
        user = user_lookup[vr['user_email']]
        if vr['status'] == 'pending':
            # Only create pending requests
            next_id = cursor.execute('SELECT COUNT(*) + 1 FROM verification_requests').fetchone()[0]
            request_reference = f"VRQ-{datetime.now().year}-{next_id:05d}"
            
            cursor.execute('''
                INSERT INTO verification_requests (
                    request_reference, user_id, verification_type, requested_discount_rate,
                    residential_address, years_of_residence, status, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                request_reference, user['id'], vr['verification_type'], 0.10,
                'Test Address', 5, vr['status'], datetime.now(), datetime.now()
            ))
            print(f'  ✅ {vr["user_email"]} - {vr["verification_type"]} ({vr["status"]})')
    
    conn.commit()
    conn.close()
    
    print(f'\n🎉 COMPREHENSIVE TEST DATA CREATED!')
    print(f'📊 Total Bookings Created: {booking_count}')
    print(f'📅 Date Range: {past_date} to {future_dates[-1]}')
    print(f'\n🎨 CALENDAR COLOR TESTING SCENARIOS:')
    print(f'  🔘 GRAY: Past dates ({past_date}) - Disabled')
    print(f'  🔘 WHITE: Available dates (some future dates) - Enabled')
    print(f'  🔘 YELLOW: Pending bookings (today, future dates) - Enabled')
    print(f'  🔘 GREEN: Approved/Official bookings (today, future dates) - Disabled')
    print(f'\n⏰ TIME SLOT COLOR TESTING SCENARIOS:')
    print(f'  🔘 WHITE: Available time slots')
    print(f'  🔘 YELLOW: User\'s pending bookings')
    print(f'  🔘 GREEN: User\'s approved bookings (disabled)')
    print(f'  🔘 Competitive: Multiple users same slot')
    print(f'\n👥 USER TESTING SCENARIOS:')
    print(f'  👤 Officials: Can see all bookings, approve/reject')
    print(f'  👥 Residents: See only their bookings, can create new ones')
    print(f'  💰 Discounts: 0% (unverified), 5% (non-resident), 10% (resident)')
    print(f'  🏆 Competitive: First-approved-wins logic')

def create_booking(cursor, user, facility, time_slot, booking_data):
    """Helper function to create a booking"""
    # Calculate pricing
    duration_hours = time_slot['duration_minutes'] / 60
    base_rate = facility['hourly_rate'] * duration_hours
    discount_rate = user['discount_rate'] if user['verified'] else 0.0
    discount_amount = base_rate * discount_rate
    total_amount = base_rate - discount_amount
    downpayment_amount = total_amount * 0.5
    
    # Get next booking number
    next_id = cursor.execute('SELECT COUNT(*) + 1 FROM bookings').fetchone()[0]
    booking_reference = f"BRG-{datetime.now().year}-{next_id:05d}"
    
    cursor.execute('''
        INSERT INTO bookings (
            booking_reference, user_id, facility_id, time_slot_id,
            booking_date, start_time, end_time, duration_hours,
            purpose, base_rate, discount_rate, discount_amount,
            downpayment_amount, total_amount, status, created_at, updated_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        booking_reference, user['id'], facility['id'], time_slot['id'],
        booking_data['date'], booking_data['timeslot'], time_slot['end_time'], duration_hours,
        booking_data['purpose'], base_rate, discount_rate, discount_amount,
        downpayment_amount, total_amount, booking_data['status'], datetime.now(), datetime.now()
    ))

if __name__ == "__main__":
    create_comprehensive_test_data()
