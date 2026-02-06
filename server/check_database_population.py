#!/usr/bin/env python3
"""
Check Database Population
Verify we have adequate test data for frontend features
"""

import sqlite3
import json
from datetime import datetime, timedelta
from config import Config

def check_database_population():
    conn = sqlite3.connect(Config.DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    print('🔍 CHECKING CURRENT DATABASE POPULATION')
    print('=' * 50)

    # Check users
    users = cursor.execute('SELECT * FROM users').fetchall()
    print(f'📊 Users: {len(users)}')
    for user in users:
        print(f'  - {user["email"]} ({user["role"]}, verified: {user["verified"]}, discount: {user["discount_rate"]})')

    # Check facilities
    facilities = cursor.execute('SELECT * FROM facilities').fetchall()
    print(f'\n🏢 Facilities: {len(facilities)}')
    for facility in facilities:
        print(f'  - {facility["name"]} (₱{facility["hourly_rate"]}/hour)')

    # Check time slots
    time_slots = cursor.execute('SELECT * FROM time_slots').fetchall()
    print(f'\n⏰ Time Slots: {len(time_slots)}')

    # Check bookings by status
    bookings = cursor.execute('SELECT status, COUNT(*) as count FROM bookings GROUP BY status').fetchall()
    print(f'\n📅 Bookings by Status:')
    for booking in bookings:
        print(f'  - {booking["status"]}: {booking["count"]}')

    # Check bookings with details
    bookings_detail = cursor.execute('''
        SELECT b.*, f.name as facility_name, u.email as user_email, u.full_name as user_name
        FROM bookings b
        JOIN facilities f ON b.facility_id = f.id
        JOIN users u ON b.user_id = u.id
        ORDER BY b.booking_date
    ''').fetchall()
    print(f'\n📅 Detailed Bookings:')
    for booking in bookings_detail:
        print(f'  - {booking["booking_reference"]}: {booking["facility_name"]} on {booking["booking_date"]} ({booking["start_time"]}) - {booking["status"]} by {booking["user_name"]}')

    # Check verification requests
    verifications = cursor.execute('SELECT * FROM verification_requests').fetchall()
    print(f'\n👤 Verification Requests: {len(verifications)}')
    for vr in verifications:
        print(f'  - {vr["request_reference"]}: {vr["verification_type"]} - {vr["status"]}')

    # Check if we need more test data for calendar testing
    print(f'\n🎨 CALENDAR TESTING DATA CHECK:')
    
    # Get today and future dates
    today = datetime.now().date()
    future_dates = [(today + timedelta(days=i)).strftime('%Y-%m-%d') for i in range(1, 15)]
    
    for date in future_dates[:5]:  # Check next 5 days
        date_bookings = cursor.execute('''
            SELECT b.*, f.name as facility_name, u.email as user_email
            FROM bookings b
            JOIN facilities f ON b.facility_id = f.id
            JOIN users u ON b.user_id = u.id
            WHERE b.booking_date = ?
            ORDER BY b.start_time
        ''', (date,)).fetchall()
        
        print(f'  📅 {date}: {len(date_bookings)} bookings')
        for booking in date_bookings:
            print(f'    - {booking["facility_name"]} {booking["start_time"]} ({booking["status"]}) by {booking["user_email"]}')

    conn.close()

if __name__ == "__main__":
    check_database_population()
