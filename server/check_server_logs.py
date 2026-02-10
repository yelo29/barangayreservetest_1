import sqlite3

def check_server_logs():
    """Check recent bookings to see if auto-rejection was triggered"""
    
    conn = sqlite3.connect('barangay.db')
    cursor = conn.cursor()
    
    print("=== CHECKING RECENT BOOKINGS FOR AUTO-REJECTION ===")
    
    # Check all bookings created on 2026-03-01 for Test Facility
    cursor.execute('''
        SELECT b.id, b.booking_date, b.start_time, b.status, b.rejection_reason, 
               b.created_at, b.updated_at, u.email, u.role
        FROM bookings b
        LEFT JOIN users u ON b.user_id = u.id
        WHERE b.facility_id = 5 AND b.booking_date = '2026-03-01'
        ORDER BY b.created_at DESC
    ''')
    
    bookings = cursor.fetchall()
    print(f"Found {len(bookings)} bookings for 2026-03-01:")
    
    for booking in bookings:
        booking_id, booking_date, start_time, status, rejection_reason, created_at, updated_at, email, role = booking
        print(f"\n  Booking ID: {booking_id}")
        print(f"  Email: {email}")
        print(f"  Role: {role}")
        print(f"  Time: {start_time}")
        print(f"  Status: {status}")
        print(f"  Created: {created_at}")
        print(f"  Updated: {updated_at}")
        print(f"  Rejection Reason: {rejection_reason if rejection_reason else 'None'}")
    
    # Check if there's an official booking that should have triggered auto-rejection
    cursor.execute('''
        SELECT COUNT(*) FROM bookings b
        LEFT JOIN users u ON b.user_id = u.id
        WHERE b.facility_id = 5 
        AND b.booking_date = '2026-03-01'
        AND u.role = 'official'
        AND b.status = 'approved'
    ''')
    
    official_count = cursor.fetchone()[0]
    print(f"\n🏆 Official bookings on this date: {official_count}")
    
    if official_count > 0:
        print("✅ Official booking exists - should have triggered auto-rejection")
        
        # Check if any resident bookings were rejected
        cursor.execute('''
            SELECT COUNT(*) FROM bookings b
            LEFT JOIN users u ON b.user_id = u.id
            WHERE b.facility_id = 5 
            AND b.booking_date = '2026-03-01'
            AND u.role = 'resident'
            AND b.status = 'rejected'
        ''')
        
        rejected_resident_count = cursor.fetchone()[0]
        print(f"🚫 Rejected resident bookings: {rejected_resident_count}")
        
        if rejected_resident_count > 0:
            print("✅ SUCCESS: Auto-rejection logic is working!")
        else:
            print("❌ FAILURE: Auto-rejection logic is NOT working")
    
    conn.close()

if __name__ == "__main__":
    check_server_logs()
