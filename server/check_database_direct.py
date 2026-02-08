import sqlite3

def check_database_direct():
    """Check the database directly to see what's happening"""
    
    conn = sqlite3.connect('barangay.db')
    cursor = conn.cursor()
    
    print("=== DATABASE DIRECT CHECK ===")
    
    # Check all bookings for 2026-02-23, Facility 1
    cursor.execute('''
        SELECT b.id, b.status, u.email, b.start_time, b.rejection_reason
        FROM bookings b
        LEFT JOIN users u ON b.user_id = u.id
        WHERE b.booking_date = '2026-02-23' AND b.facility_id = 1
        ORDER BY b.id
    ''')
    
    bookings = cursor.fetchall()
    print(f"Found {len(bookings)} bookings in database:")
    
    for booking in bookings:
        booking_id, status, email, start_time, rejection_reason = booking
        print(f"  - ID: {booking_id}, Status: {status}, Email: {email}, Time: {start_time}")
        
        if status == 'rejected' and rejection_reason:
            print(f"    💬 Rejection Reason: {rejection_reason[:100]}...")
        elif status == 'rejected':
            print(f"    ❌ No rejection reason found")
    
    conn.close()

if __name__ == "__main__":
    check_database_direct()
