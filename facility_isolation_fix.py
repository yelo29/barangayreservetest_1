#!/usr/bin/env python3
"""
Fix Data Isolation Issue - Facility Filtering Problem
"""

import sqlite3
import os

def check_facility_isolation():
    """Check facility data isolation issues"""
    db_path = os.path.join(os.path.dirname(__file__), 'server', 'barangay.db')
    
    if not os.path.exists(db_path):
        print("❌ Database not found!")
        return
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print("🔍 FACILITY DATA ISOLATION ANALYSIS")
        print("=" * 50)
        
        # Check the specific issue: Basketball Court (facility_id: 10)
        cursor.execute('''
            SELECT b.id, b.facility_id, f.name as facility_name, b.booking_date, b.status, u.email, u.full_name
            FROM bookings b
            LEFT JOIN facilities f ON b.facility_id = f.id
            LEFT JOIN users u ON b.user_id = u.id
            WHERE b.facility_id = 10
            ORDER BY b.booking_date, b.status
        ''')
        
        basketball_bookings = cursor.fetchall()
        print(f"\n🏀 Basketball Court (ID: 10) Bookings:")
        for booking in basketball_bookings:
            booking_id, facility_id, facility_name, date, status, email, name = booking
            print(f"  Booking {booking_id}: {date} - {status} - {email}")
        
        # Check if there are bookings for other facilities showing up in Basketball Court queries
        cursor.execute('''
            SELECT COUNT(*) as total,
                   COUNT(CASE WHEN facility_id = 10 THEN 1 END) as basketball,
                   COUNT(CASE WHEN facility_id != 10 THEN 1 END) as other_facilities
            FROM bookings
        ''')
        
        stats = cursor.fetchone()
        print(f"\n📊 Overall Booking Distribution:")
        print(f"  Total bookings: {stats[0]}")
        print(f"  Basketball Court: {stats[1]}")
        print(f"  Other facilities: {stats[2]}")
        
        # Check the specific user's bookings
        cursor.execute('''
            SELECT b.id, b.facility_id, f.name as facility_name, b.booking_date, b.status
            FROM bookings b
            LEFT JOIN facilities f ON b.facility_id = f.id
            LEFT JOIN users u ON b.user_id = u.id
            WHERE u.email = 'leo052904@gmail.com'
            ORDER BY b.booking_date
        ''')
        
        user_bookings = cursor.fetchall()
        print(f"\n👤 Leo's Bookings:")
        for booking in user_bookings:
            booking_id, facility_id, facility_name, date, status = booking
            print(f"  Booking {booking_id}: {facility_name} ({facility_id}) - {date} - {status}")
        
        # Check for any data corruption
        cursor.execute('''
            SELECT facility_id, COUNT(*) as count
            FROM bookings
            GROUP BY facility_id
            ORDER BY facility_id
        ''')
        
        facility_counts = cursor.fetchall()
        print(f"\n🏢 Bookings by Facility:")
        for facility_id, count in facility_counts:
            cursor.execute('SELECT name FROM facilities WHERE id = ?', (facility_id,))
            facility_name = cursor.fetchone()
            name = facility_name[0] if facility_name else f"Unknown ({facility_id})"
            print(f"  {name}: {count} bookings")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Error checking facility isolation: {e}")

def fix_facility_isolation():
    """Fix facility data isolation issues"""
    db_path = os.path.join(os.path.dirname(__file__), 'server', 'barangay.db')
    
    if not os.path.exists(db_path):
        print("❌ Database not found!")
        return
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print("🔧 FIXING FACILITY DATA ISOLATION")
        print("=" * 50)
        
        # Check for any NULL facility_ids
        cursor.execute('SELECT COUNT(*) FROM bookings WHERE facility_id IS NULL')
        null_facilities = cursor.fetchone()[0]
        
        if null_facilities > 0:
            print(f"⚠️ Found {null_facilities} bookings with NULL facility_id")
            cursor.execute('''
                SELECT id, booking_reference, booking_date 
                FROM bookings 
                WHERE facility_id IS NULL
            ''')
            
            null_bookings = cursor.fetchall()
            for booking in null_bookings:
                print(f"  Booking {booking[0]} ({booking[1]}): {booking[2]}")
        else:
            print("✅ No bookings with NULL facility_id found")
        
        # Verify facility references are valid
        cursor.execute('''
            SELECT b.id, b.facility_id, f.name
            FROM bookings b
            LEFT JOIN facilities f ON b.facility_id = f.id
            WHERE f.name IS NULL
        ''')
        
        invalid_facilities = cursor.fetchall()
        if invalid_facilities:
            print(f"\n⚠️ Found {len(invalid_facilities)} bookings with invalid facility_id:")
            for booking in invalid_facilities:
                print(f"  Booking {booking[0]}: facility_id {booking[1]} doesn't exist")
        else:
            print("✅ All facility references are valid")
        
        # Check for data integrity in the specific issue
        cursor.execute('''
            SELECT b.id, b.facility_id, b.booking_date, b.status
            FROM bookings b
            WHERE b.facility_id = 10
            AND b.booking_date = '2026-03-06'
        ''')
        
        problematic_bookings = cursor.fetchall()
        print(f"\n🎯 Basketball Court on 2026-03-06:")
        for booking in problematic_bookings:
            print(f"  Booking {booking[0]}: facility {booking[1]}, date {booking[2]}, status {booking[3]}")
        
        conn.close()
        print("\n✅ Facility isolation analysis completed!")
        
    except Exception as e:
        print(f"❌ Error fixing facility isolation: {e}")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == '--fix':
        fix_facility_isolation()
    else:
        check_facility_isolation()
