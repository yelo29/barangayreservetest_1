import sqlite3

def check_date_2026_02_10():
    """Check what bookings exist for 2026-02-10"""
    
    conn = sqlite3.connect('barangay.db')
    cursor = conn.cursor()
    
    print("=== CHECKING BOOKINGS FOR 2026-02-10 ===")
    
    cursor.execute('''
        SELECT b.id, b.start_time, b.status, u.email, u.role
        FROM bookings b
        LEFT JOIN users u ON b.user_id = u.id
        WHERE b.facility_id = 5 AND b.booking_date = '2026-02-10'
        ORDER BY b.start_time
    ''')
    
    bookings = cursor.fetchall()
    print(f"Found {len(bookings)} bookings for 2026-02-10:")
    
    for booking in bookings:
        booking_id, start_time, status, email, role = booking
        print(f"  - ID: {booking_id}, Time: {start_time}, Status: {status}, Email: {email}, Role: {role}")
    
    conn.close()

if __name__ == "__main__":
    check_date_2026_02_10()
