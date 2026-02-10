import sqlite3

def verify_booking_18_status():
    """Check if booking 18 was actually rejected"""
    
    conn = sqlite3.connect('barangay.db')
    cursor = conn.cursor()
    
    print("=== VERIFYING BOOKING 18 STATUS ===")
    
    cursor.execute('''
        SELECT b.id, b.status, b.rejection_reason, b.updated_at, u.email
        FROM bookings b
        LEFT JOIN users u ON b.user_id = u.id
        WHERE b.id = 18
    ''')
    
    booking = cursor.fetchone()
    if booking:
        booking_id, status, rejection_reason, updated_at, email = booking
        print(f"Booking ID: {booking_id}")
        print(f"Email: {email}")
        print(f"Status: {status}")
        print(f"Updated At: {updated_at}")
        print(f"Rejection Reason: {rejection_reason if rejection_reason else 'None'}")
        
        if status == 'rejected' and rejection_reason and ('apology' in rejection_reason.lower() or 'automatically rescheduled' in rejection_reason.lower()):
            print("\n🎉 SUCCESS: Auto-rejection fix is working perfectly!")
            print("✅ Approved resident booking was auto-rejected with apology message")
            print("✅ The inconsistency has been FIXED!")
        else:
            print("\n❌ FAILURE: Auto-rejection fix is not working correctly")
    else:
        print("❌ Booking not found")
    
    conn.close()

if __name__ == "__main__":
    verify_booking_18_status()
