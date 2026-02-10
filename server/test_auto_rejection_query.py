import sqlite3

def test_auto_rejection_query():
    """Test the exact query used in auto-rejection logic"""
    
    conn = sqlite3.connect('barangay.db')
    cursor = conn.cursor()
    
    print("🔍 TESTING AUTO-REJECTION QUERY")
    print("=" * 50)
    
    # Test the exact query from server.py
    facility_id = 5
    date = '2026-02-25'
    
    cursor.execute('''
        SELECT b.id, b.user_id, b.start_time, b.end_time, b.status, u.email as user_email, u.full_name
        FROM bookings b
        LEFT JOIN users u ON b.user_id = u.id
        WHERE b.facility_id = ? 
        AND b.booking_date = ? 
        AND (b.status = 'pending' OR b.status = 'approved')
        AND (u.role = 'resident' OR u.role = '0' OR u.role IS NULL OR u.role LIKE '0.%')
    ''', (facility_id, date))
    
    overlapping_bookings = cursor.fetchall()
    print(f"🔍 Found {len(overlapping_bookings)} overlapping resident bookings for {date}")
    
    for booking in overlapping_bookings:
        booking_id = booking[0]
        user_id = booking[1]
        start_time = booking[2]
        end_time = booking[3]
        status = booking[4]
        user_email = booking[5]
        full_name = booking[6]
        
        print(f"  📋 Booking ID: {booking_id}")
        print(f"     User ID: {user_id}")
        print(f"     Email: {user_email}")
        print(f"     Name: {full_name}")
        print(f"     Time: {start_time} - {end_time}")
        print(f"     Status: {status}")
        print()
    
    # Also test what user roles exist
    cursor.execute('''
        SELECT DISTINCT u.role, COUNT(*) as count
        FROM users u
        LEFT JOIN bookings b ON u.id = b.user_id
        WHERE b.facility_id = ? AND b.booking_date = ?
        GROUP BY u.role
    ''', (facility_id, date))
    
    roles = cursor.fetchall()
    print(f"👥 User roles found for {date}:")
    for role, count in roles:
        print(f"     {role}: {count} bookings")
    
    conn.close()

if __name__ == "__main__":
    test_auto_rejection_query()
