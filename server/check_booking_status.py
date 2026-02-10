import sqlite3

def check_booking_status():
    """Check the status of booking ID 27"""
    
    conn = sqlite3.connect('barangay.db')
    cursor = conn.cursor()
    
    print("=== CHECKING BOOKING 27 STATUS ===")
    
    cursor.execute('''
        SELECT b.id, b.status, b.rejection_reason, u.email
        FROM bookings b
        LEFT JOIN users u ON b.user_id = u.id
        WHERE b.id = 27
    ''')
    
    booking = cursor.fetchone()
    if booking:
        booking_id, status, rejection_reason, email = booking
        print(f"Booking ID: {booking_id}")
        print(f"Status: {status}")
        print(f"Email: {email}")
        print(f"Rejection Reason: {rejection_reason if rejection_reason else 'None'}")
        
        if status == 'rejected' and rejection_reason:
            print("✅ SUCCESS: Auto-rejection fix is working!")
        else:
            print("❌ FAILURE: Auto-rejection fix is not working")
    else:
        print("❌ Booking not found")
    
    conn.close()

if __name__ == "__main__":
    check_booking_status()
