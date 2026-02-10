import sqlite3

def check_resident_booking():
    """Check the resident booking we just created"""
    
    conn = sqlite3.connect('barangay.db')
    cursor = conn.cursor()
    
    print("=== CHECKING RESIDENT BOOKING 41 ===")
    
    cursor.execute('''
        SELECT b.id, b.start_time, b.status, u.email, u.role
        FROM bookings b
        LEFT JOIN users u ON b.user_id = u.id
        WHERE b.id = 41
    ''')
    
    booking = cursor.fetchone()
    if booking:
        booking_id, start_time, status, email, role = booking
        print(f"Booking ID: {booking_id}")
        print(f"Email: {email}")
        print(f"Role: {role}")
        print(f"Time: {start_time}")
        print(f"Status: {status}")
        
        # Check if it matches the resident condition
        is_resident = (role == 'resident' or role == '0' or role is None or str(role).startswith('0.'))
        print(f"Matches resident condition: {is_resident}")
    else:
        print("Booking not found")
    
    conn.close()

if __name__ == "__main__":
    check_resident_booking()
