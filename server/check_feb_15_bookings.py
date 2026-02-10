import sqlite3

def check_feb_15_bookings():
    """Check what bookings exist on Feb 15th"""
    
    conn = sqlite3.connect('barangay.db')
    cursor = conn.cursor()
    
    print("=== CHECKING FEB 15TH BOOKINGS ===")
    
    cursor.execute('''
        SELECT b.id, b.start_time, b.status, u.email, u.role
        FROM bookings b
        LEFT JOIN users u ON b.user_id = u.id
        WHERE b.booking_date = '2026-02-15'
        ORDER BY b.start_time
    ''')
    
    bookings = cursor.fetchall()
    print(f"Found {len(bookings)} bookings for 2026-02-15:")
    
    for booking in bookings:
        booking_id, start_time, status, email, role = booking
        print(f"  📋 Booking ID: {booking_id}")
        print(f"     Email: {email}")
        print(f"     Role: {role}")
        print(f"     Time: {start_time}")
        print(f"     Status: {status}")
    
    conn.close()

if __name__ == "__main__":
    check_feb_15_bookings()
