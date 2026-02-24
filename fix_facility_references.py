#!/usr/bin/env python3
"""
Fix Invalid Facility References
"""

import sqlite3
import os

def check_and_fix_facilities():
    """Check existing facilities and fix invalid references"""
    db_path = os.path.join(os.path.dirname(__file__), 'server', 'barangay.db')
    
    if not os.path.exists(db_path):
        print("❌ Database not found!")
        return
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print("🔍 CHECKING FACILITY REFERENCES")
        print("=" * 50)
        
        # Check what facilities actually exist
        cursor.execute('SELECT id, name FROM facilities ORDER BY id')
        existing_facilities = cursor.fetchall()
        
        print("📋 Existing Facilities:")
        for facility_id, name in existing_facilities:
            print(f"  ID {facility_id}: {name}")
        
        # Find invalid facility_ids in bookings
        cursor.execute('''
            SELECT DISTINCT facility_id 
            FROM bookings 
            WHERE facility_id NOT IN (SELECT id FROM facilities)
            ORDER BY facility_id
        ''')
        
        invalid_ids = [row[0] for row in cursor.fetchall()]
        
        if invalid_ids:
            print(f"\n⚠️ Invalid facility_ids found: {invalid_ids}")
            
            # Option 1: Delete bookings with invalid facility_ids
            print(f"\n🗑️ Deleting bookings with invalid facility_ids...")
            
            cursor.execute('''
                DELETE FROM bookings 
                WHERE facility_id NOT IN (SELECT id FROM facilities)
            ''')
            
            deleted_count = cursor.rowcount
            print(f"  ✅ Deleted {deleted_count} invalid bookings")
            
            conn.commit()
            
        else:
            print("\n✅ All facility references are valid")
        
        # Verify the fix
        cursor.execute('''
            SELECT b.id, b.facility_id, f.name as facility_name, b.booking_date, b.status
            FROM bookings b
            LEFT JOIN facilities f ON b.facility_id = f.id
            WHERE b.facility_id = 10
            ORDER BY b.booking_date
        ''')
        
        basketball_bookings = cursor.fetchall()
        print(f"\n🏀 Basketball Court Bookings After Fix:")
        for booking in basketball_bookings:
            booking_id, facility_id, facility_name, date, status = booking
            print(f"  Booking {booking_id}: {facility_name} - {date} - {status}")
        
        # Check Leo's bookings again
        cursor.execute('''
            SELECT b.id, b.facility_id, f.name as facility_name, b.booking_date, b.status
            FROM bookings b
            LEFT JOIN facilities f ON b.facility_id = f.id
            LEFT JOIN users u ON b.user_id = u.id
            WHERE u.email = 'leo052904@gmail.com'
            ORDER BY b.booking_date
        ''')
        
        user_bookings = cursor.fetchall()
        print(f"\n👤 Leo's Bookings After Fix:")
        for booking in user_bookings:
            booking_id, facility_id, facility_name, date, status = booking
            print(f"  Booking {booking_id}: {facility_name or 'Unknown'} ({facility_id}) - {date} - {status}")
        
        conn.close()
        print("\n✅ Facility reference fix completed!")
        
    except Exception as e:
        print(f"❌ Error fixing facility references: {e}")

if __name__ == "__main__":
    check_and_fix_facilities()
