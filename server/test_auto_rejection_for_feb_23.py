import sqlite3

def test_auto_rejection_for_feb_23():
    """Test the exact auto-rejection query for Feb 23"""
    
    conn = sqlite3.connect('barangay.db')
    cursor = conn.cursor()
    
    print("=== TESTING AUTO-REJECTION QUERY FOR FEB 23 ===")
    
    # Test the exact query that should have run when official booking 34 was created
    facility_id = 1
    date = '2026-02-23'
    
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
    print(f"🔍 Found {len(overlapping_bookings)} resident bookings that should have been auto-rejected:")
    
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
    
    # Check if there's an issue with the user role detection
    cursor.execute('''
        SELECT u.id, u.email, u.role
        FROM users u
        WHERE u.email = 'leo052904@gmail.com'
    ''')
    
    user_info = cursor.fetchone()
    if user_info:
        user_id, email, role = user_info
        print(f"\n👤 User info for leo052904@gmail.com:")
        print(f"   ID: {user_id}")
        print(f"   Email: {email}")
        print(f"   Role: {role}")
        
        # Test the role condition
        is_resident = (role == 'resident' or role == '0' or role is None or str(role).startswith('0.'))
        print(f"   Matches resident condition: {is_resident}")
    
    conn.close()

if __name__ == "__main__":
    test_auto_rejection_for_feb_23()
