import sqlite3

def check_booking_41():
    """Check if booking 41 exists"""
    
    conn = sqlite3.connect('barangay.db')
    cursor = conn.cursor()
    
    print("=== CHECKING BOOKING 41 ===")
    
    cursor.execute('''
        SELECT b.id, b.user_id, b.start_time, b.status, u.email, u.role
        FROM bookings b
        LEFT JOIN users u ON b.user_id = u.id
        WHERE b.id = 41
    ''')
    
    booking = cursor.fetchone()
    if booking:
        booking_id, user_id, start_time, status, email, role = booking
        print(f"Booking ID: {booking_id}")
        print(f"User ID: {user_id}")
        print(f"Email: {email}")
        print(f"Role: {role}")
        print(f"Time: {start_time}")
        print(f"Status: {status}")
    else:
        print("Booking 41 not found")
    
    conn.close()

if __name__ == "__main__":
    check_booking_41()
