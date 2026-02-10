import sqlite3

def check_feb_23_bookings():
    """Check what happened on February 23rd"""
    
    conn = sqlite3.connect('barangay.db')
    cursor = conn.cursor()
    
    print("=== CHECKING FEBRUARY 23RD BOOKINGS ===")
    
    cursor.execute('''
        SELECT b.id, b.start_time, b.status, b.rejection_reason, b.created_at, b.updated_at, u.email, u.role
        FROM bookings b
        LEFT JOIN users u ON b.user_id = u.id
        WHERE b.facility_id = 1 AND b.booking_date = '2026-02-23'
        ORDER BY b.created_at
    ''')
    
    bookings = cursor.fetchall()
    print(f"Found {len(bookings)} bookings for 2026-02-23 (Community Hall):")
    
    for booking in bookings:
        booking_id, start_time, status, rejection_reason, created_at, updated_at, email, role = booking
        print(f"\n  📋 Booking ID: {booking_id}")
        print(f"     Email: {email}")
        print(f"     Role: {role}")
        print(f"     Time: {start_time}")
        print(f"     Status: {status}")
        print(f"     Created: {created_at}")
        print(f"     Updated: {updated_at}")
        print(f"     Rejection Reason: {rejection_reason if rejection_reason else 'None'}")
    
    # Check which booking was created first
    if len(bookings) >= 2:
        print(f"\n🔍 TIMING ANALYSIS:")
        print(f"   First booking: {bookings[0][0]} by {bookings[0][6]} at {bookings[0][4]}")
        print(f"   Second booking: {bookings[1][0]} by {bookings[1][6]} at {bookings[1][4]}")
        
        if bookings[1][7] == 'official':
            print(f"   ✅ Official booking was created second - should have auto-rejected first booking")
        else:
            print(f"   ❌ Second booking is not official - no auto-rejection expected")
    
    conn.close()

if __name__ == "__main__":
    check_feb_23_bookings()
