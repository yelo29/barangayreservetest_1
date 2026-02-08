import sqlite3

def check_existing_bookings():
    """Check existing bookings for 2026-02-20"""
    
    conn = sqlite3.connect('barangay.db')
    cursor = conn.cursor()
    
    print("=== CHECKING EXISTING BOOKINGS FOR 2026-02-20 ===")
    
    # Check all bookings for 2026-02-20, Facility 1
    cursor.execute('''
        SELECT b.id, b.status, u.email, b.start_time, b.end_time
        FROM bookings b
        LEFT JOIN users u ON b.user_id = u.id
        WHERE b.booking_date = '2026-02-20' AND b.facility_id = 1
        ORDER BY b.id
    ''')
    
    bookings = cursor.fetchall()
    print(f"Found {len(bookings)} bookings for 2026-02-20, Facility 1:")
    
    for booking in bookings:
        booking_id, status, email, start_time, end_time = booking
        print(f"  - ID: {booking_id}, Status: {status}, Email: {email}, Time: {start_time} - {end_time}")
    
    # Check if there are any official bookings
    cursor.execute('''
        SELECT COUNT(*) FROM bookings b
        LEFT JOIN users u ON b.user_id = u.id
        WHERE b.booking_date = '2026-02-20' AND b.facility_id = 1 AND u.email = 'captain@barangay.gov'
    ''')
    
    official_count = cursor.fetchone()[0]
    print(f"\nOfficial bookings for this date: {official_count}")
    
    if official_count > 0:
        print("⚠️  There's already an official booking for this date!")
        print("   The duplicate booking check is working correctly.")
    
    conn.close()

if __name__ == "__main__":
    check_existing_bookings()
