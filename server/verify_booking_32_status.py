import sqlite3

def verify_booking_32_status():
    """Check if booking 32 was actually rejected"""
    
    conn = sqlite3.connect('barangay.db')
    cursor = conn.cursor()
    
    print("=== VERIFYING BOOKING 32 STATUS (LATEST TEST) ===")
    
    cursor.execute('''
        SELECT b.id, b.status, b.rejection_reason, b.updated_at, u.email
        FROM bookings b
        LEFT JOIN users u ON b.user_id = u.id
        WHERE b.id = 32
    ''')
    
    booking = cursor.fetchone()
    if booking:
        booking_id, status, rejection_reason, updated_at, email = booking
        print(f"Booking ID: {booking_id}")
        print(f"Email: {email}")
        print(f"Status: {status}")
        print(f"Updated At: {updated_at}")
        print(f"Rejection Reason: {rejection_reason if rejection_reason else 'None'}")
        
        if status == 'rejected' and rejection_reason:
            print("\n🎉 SUCCESS: Auto-rejection fix IS working!")
            print("✅ The approved overlap logic is working correctly")
        else:
            print(f"\n❌ ISSUE: Booking status is '{status}' (should be 'rejected')")
    else:
        print("❌ Booking not found")
    
    # Also check the official booking that triggered this
    cursor.execute('''
        SELECT b.id, b.booking_date, b.start_time, b.status
        FROM bookings b
        LEFT JOIN users u ON b.user_id = u.id
        WHERE b.id = 35
    ''')
    
    official_booking = cursor.fetchone()
    if official_booking:
        booking_id, booking_date, start_time, status = official_booking
        print(f"\n🏆 Official booking {booking_id}: {booking_date} - {start_time} - {status}")
    
    conn.close()

if __name__ == "__main__":
    verify_booking_32_status()
