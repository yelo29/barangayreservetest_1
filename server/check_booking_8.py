import sqlite3

def check_booking_8():
    """Check what booking 8 is"""
    
    conn = sqlite3.connect('barangay.db')
    cursor = conn.cursor()
    
    print("=== CHECKING BOOKING 8 ===")
    
    cursor.execute('''
        SELECT b.id, b.user_id, b.start_time, b.status, u.email, u.role, b.booking_date
        FROM bookings b
        LEFT JOIN users u ON b.user_id = u.id
        WHERE b.id = 8
    ''')
    
    booking = cursor.fetchone()
    if booking:
        booking_id, user_id, start_time, status, email, role, booking_date = booking
        print(f"Booking ID: {booking_id}")
        print(f"User ID: {user_id}")
        print(f"Email: {email}")
        print(f"Role: {role}")
        print(f"Booking Date: {booking_date}")
        print(f"Time: {start_time}")
        print(f"Status: {status}")
    else:
        print("Booking 8 not found")
    
    conn.close()

if __name__ == "__main__":
    check_booking_8()
