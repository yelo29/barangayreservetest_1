import sqlite3

def check_existing_bookings():
    """Check existing bookings for Test Facility (ID 5)"""
    
    conn = sqlite3.connect('barangay.db')
    cursor = conn.cursor()
    
    print("=== CHECKING EXISTING BOOKINGS FOR TEST FACILITY (ID 5) ===")
    
    # Check all bookings for Test Facility on 2026-02-25
    cursor.execute('''
        SELECT b.id, b.booking_date, b.start_time, b.status, u.email
        FROM bookings b
        LEFT JOIN users u ON b.user_id = u.id
        WHERE b.facility_id = 5 AND b.booking_date = '2026-03-01'
        ORDER BY b.start_time
    ''')
    
    bookings = cursor.fetchall()
    print(f"Found {len(bookings)} bookings for Test Facility on 2026-03-01:")
    
    for booking in bookings:
        booking_id, booking_date, start_time, status, email = booking
        print(f"  - ID: {booking_id}, Time: {start_time}, Status: {status}, Email: {email}")
    
    # Check resident's existing bookings
    cursor.execute('''
        SELECT b.id, b.booking_date, b.start_time, b.status
        FROM bookings b
        LEFT JOIN users u ON b.user_id = u.id
        WHERE u.email = 'saloestillopez@gmail.com' AND b.facility_id = 5
        ORDER BY b.booking_date, b.start_time
    ''')
    
    resident_bookings = cursor.fetchall()
    print(f"\nResident's existing bookings for Test Facility:")
    for booking in resident_bookings:
        booking_id, booking_date, start_time, status = booking
        print(f"  - ID: {booking_id}, Date: {booking_date}, Time: {start_time}, Status: {status}")
    
    conn.close()

if __name__ == "__main__":
    check_existing_bookings()
