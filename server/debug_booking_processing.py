import sqlite3

def debug_booking_processing():
    """Debug the booking processing to see what's happening with timeslot"""
    
    conn = sqlite3.connect('barangay.db')
    cursor = conn.cursor()
    
    print("=== DEBUGGING BOOKING PROCESSING ===")
    
    # Simulate the SQL query from the backend
    cursor.execute('''
        SELECT b.id, b.user_id, b.start_time, b.end_time, b.status, u.email as user_email, u.full_name
        FROM bookings b
        LEFT JOIN users u ON b.user_id = u.id
        WHERE b.facility_id = ? 
        AND b.booking_date = ? 
        AND b.status = 'pending'
        AND (u.role = 'resident' OR u.role = '0' OR u.role IS NULL OR u.role LIKE '0.%')
    ''', (1, '2026-02-28'))
    
    overlapping_bookings = cursor.fetchall()
    print(f"Found {len(overlapping_bookings)} overlapping bookings:")
    
    for i, booking in enumerate(overlapping_bookings):
        print(f"  Booking {i}: {booking}")
        print(f"    - booking[0] (id): {booking[0]}")
        print(f"    - booking[1] (user_id): {booking[1]}")
        print(f"    - booking[2] (start_time): {booking[2]}")
        print(f"    - booking[3] (end_time): {booking[3]}")
        print(f"    - booking[4] (status): {booking[4]}")
        print(f"    - booking[5] (user_email): {booking[5]}")
        print(f"    - booking[6] (full_name): {booking[6]}")
        
        # Test the timeslot construction
        resident_timeslot = f"{booking[2]} - {booking[3]}"
        print(f"    - resident_timeslot: '{resident_timeslot}'")
        
        # Test the dictionary construction
        test_dict = {
            'booking_id': booking[0],
            'resident_name': booking[6] if booking[6] else 'Resident',
            'resident_email': booking[5] if booking[5] else 'Unknown',
            'timeslot': resident_timeslot
        }
        print(f"    - test_dict: {test_dict}")
    
    conn.close()

if __name__ == "__main__":
    debug_booking_processing()
