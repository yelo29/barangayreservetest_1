#!/usr/bin/env python3
"""
Create Simple Test Data
Populate database with test data for current facilities
"""

import sqlite3
import json
from datetime import datetime, timedelta, date
import hashlib
from config import Config

def create_test_data():
    conn = sqlite3.connect(Config.DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    print('🎨 CREATING SIMPLE TEST DATA')
    print('=' * 40)
    
    # Get current data
    users = cursor.execute('SELECT * FROM users').fetchall()
    facilities = cursor.execute('SELECT * FROM facilities').fetchall()
    
    print(f'Found {len(users)} users and {len(facilities)} facilities')
    
    # Get dates for testing
    today = date.today()
    past_date = (today - timedelta(days=5)).strftime('%Y-%m-%d')
    today_str = today.strftime('%Y-%m-%d')
    future_dates = [(today + timedelta(days=i)).strftime('%Y-%m-%d') for i in range(1, 10)]
    
    print(f'📅 Today: {today_str}')
    print(f'📅 Testing with {len(future_dates)} future dates')
    
    # Clear existing bookings to start fresh
    cursor.execute('DELETE FROM bookings')
    cursor.execute('DELETE FROM verification_requests')
    print('🗑️ Cleared existing bookings and verification requests')
    
    booking_count = 0
    
    # Create test bookings for leo052904@gmail.com
    leo_email = 'leo052904@gmail.com'
    
    # Past booking (should be gray)
    cursor.execute('''
        INSERT INTO bookings (user_email, facility_id, facility_name, booking_date, start_time, end_time, status, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        leo_email, 1, 'Community Hall', past_date, '09:00 AM', '10:00 AM', 'approved', 
        datetime.now().isoformat()
    ))
    booking_count += 1
    
    # Today's booking (pending)
    cursor.execute('''
        INSERT INTO bookings (user_email, facility_id, facility_name, booking_date, start_time, end_time, status, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        leo_email, 2, 'Basketball Court', today_str, '10:00 AM', '11:00 AM', 'pending', 
        datetime.now().isoformat()
    ))
    booking_count += 1
    
    # Future bookings
    for i, future_date in enumerate(future_dates[:5]):
        facility_id = (i % 4) + 1  # Rotate through facilities
        facility_names = {1: 'Community Hall', 2: 'Basketball Court', 3: 'Swimming Pool', 4: 'Shooting Range'}
        facility_name = facility_names[facility_id]
        
        # Create booking
        cursor.execute('''
            INSERT INTO bookings (user_email, facility_id, facility_name, booking_date, start_time, end_time, status, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            leo_email, facility_id, facility_name, future_date, '14:00', '15:00', 'approved', 
            datetime.now().isoformat()
        ))
        booking_count += 1
    
    # Create verification request for leo
    cursor.execute('''
        INSERT INTO verification_requests (user_email, verification_type, status, created_at)
        VALUES (?, ?, ?, ?)
    ''', (
        leo_email, 'resident', 'approved', datetime.now().isoformat()
    ))
    
    # Update leo's verification status
    cursor.execute('UPDATE users SET verified = 1, discount_rate = 0.05 WHERE email = ?', (leo_email,))
    
    conn.commit()
    conn.close()
    
    print(f'✅ Created {booking_count} test bookings')
    print(f'✅ Created verification request for {leo_email}')
    print(f'✅ Updated {leo_email} verification status')
    print('\n🎯 Test Data Summary:')
    print(f'  - User: {leo_email} (password: leo3029)')
    print(f'  - Past booking: {past_date} (gray/disabled)')
    print(f'  - Today booking: {today_str} (pending)')
    print(f'  - Future bookings: {len(future_dates[:5])} days (approved)')
    print(f'  - Verification: Approved with 5% discount')

if __name__ == '__main__':
    create_test_data()
