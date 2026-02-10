import sqlite3

def debug_auto_rejection_query():
    """Debug the exact auto-rejection query"""
    
    conn = sqlite3.connect('barangay.db')
    cursor = conn.cursor()
    
    print("=== DEBUGGING AUTO-REJECTION QUERY ===")
    
    # Test the exact query that should be run for ALL DAY booking
    facility_id = 1
    date = '2026-04-01'
    user_id = 1  # Official user ID
    
    cursor.execute('''
        SELECT b.id, b.user_id, b.start_time, b.end_time, b.status, u.email as user_email, u.full_name
        FROM bookings b
        LEFT JOIN users u ON b.user_id = u.id
        WHERE b.facility_id = ? 
        AND b.booking_date = ?
        AND (b.status = 'pending' OR b.status = 'approved')
        AND (u.role = 'resident' OR u.role = '0' OR u.role IS NULL OR u.role LIKE '0.%')
        AND b.user_id != ?
        ORDER BY b.id
    ''', (facility_id, date, user_id))
    
    overlapping_bookings = cursor.fetchall()
    print(f"🔍 Found {len(overlapping_bookings)} overlapping resident bookings:")
    
    for booking in overlapping_bookings:
        booking_id = booking_user_id = booking[1]
        start_time = booking[2]
        end_time = booking[3]
        status = booking[4]
        user_email = booking[5]
        full_name = booking[6]
        
        print(f"  📋 Booking ID: {booking_id}")
        print(f"     User ID: {booking_user_id}")
        print(f"     Email: {user_email}")
        print(f"     Name: {full_name}")
        print(f"     Time: {start_time} - {end_time}")
        print(f"     Status: {status}")
    
    # Also check all bookings on that date
    cursor.execute('''
        SELECT b.id, b.start_time, b.status, u.email, u.role
        FROM bookings b
        LEFT JOIN users u ON b.user_id = u.id
        WHERE b.facility_id = ? AND b.booking_date = ?
        ORDER BY b.start_time
    ''', (facility_id, date))
    
    all_bookings = cursor.fetchall()
    print(f"\n📅 All bookings on {date}:")
    for booking in all_bookings:
        booking_id, start_time, status, email, role = booking
        print(f"  📋 ID {booking_id}: {start_time} - {status} - {email} ({role})")
    
    conn.close()

if __name__ == "__main__":
    debug_auto_rejection_query()
