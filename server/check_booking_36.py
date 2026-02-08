import sqlite3

def check_booking_36():
    """Check the specific booking 36"""
    
    conn = sqlite3.connect('barangay.db')
    cursor = conn.cursor()
    
    print("=== CHECKING BOOKING 36 ===")
    
    # Get full details of booking 36
    cursor.execute('''
        SELECT b.id, b.status, b.start_time, b.end_time, b.booking_date, b.facility_id,
               u.email, u.role, u.full_name
        FROM bookings b
        LEFT JOIN users u ON b.user_id = u.id
        WHERE b.id = 36
    ''')
    
    booking = cursor.fetchone()
    if booking:
        print(f"Booking 36 details:")
        print(f"  - ID: {booking[0]}")
        print(f"  - Status: {booking[1]}")
        print(f"  - Start Time: {booking[2]}")
        print(f"  - End Time: {booking[3]}")
        print(f"  - Date: {booking[4]}")
        print(f"  - Facility ID: {booking[5]}")
        print(f"  - User Email: {booking[6]}")
        print(f"  - User Role: {booking[7]}")
        print(f"  - Full Name: {booking[8]}")
        
        # Check if it matches the query conditions
        is_pending = booking[1] == 'pending'
        is_resident_role = booking[7] in ['resident', '0'] or booking[7] is None or (booking[7] and booking[7].startswith('0.'))
        matches_date = booking[4] == '2026-02-28'
        matches_facility = booking[5] == 1
        
        print(f"\nQuery condition checks:")
        print(f"  - Status is 'pending': {is_pending}")
        print(f"  - User role matches resident criteria: {is_resident_role}")
        print(f"  - Date matches: {matches_date}")
        print(f"  - Facility matches: {matches_facility}")
        print(f"  - Overall should be included: {is_pending and is_resident_role and matches_date and matches_facility}")
    else:
        print("Booking 36 not found!")
    
    conn.close()

if __name__ == "__main__":
    check_booking_36()
