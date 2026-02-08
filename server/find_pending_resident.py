import sqlite3

def find_pending_resident():
    """Find dates with pending resident bookings"""
    
    conn = sqlite3.connect('barangay.db')
    cursor = conn.cursor()
    
    print("=== FINDING DATES WITH PENDING RESIDENT BOOKINGS ===")
    
    # Find all dates with pending resident bookings
    cursor.execute('''
        SELECT b.booking_date, COUNT(*) as pending_count
        FROM bookings b
        LEFT JOIN users u ON b.user_id = u.id
        WHERE b.booking_date LIKE '2026-02-%'
        AND b.facility_id = 1
        AND b.status = 'pending'
        AND (u.role = 'resident' OR u.role = '0' OR u.role IS NULL OR u.role LIKE '0.%')
        AND u.email != 'captain@barangay.gov'
        GROUP BY b.booking_date
        ORDER BY b.booking_date
    ''')
    
    pending_dates = cursor.fetchall()
    print(f"Dates with pending resident bookings:")
    
    for date_info in pending_dates:
        date, count = date_info
        print(f"  - {date}: {count} pending resident bookings")
        
        # Get details of pending bookings for this date
        cursor.execute('''
            SELECT b.id, u.email, b.start_time, b.end_time, u.full_name
            FROM bookings b
            LEFT JOIN users u ON b.user_id = u.id
            WHERE b.booking_date = ? AND b.facility_id = 1
            AND b.status = 'pending'
            AND u.email != 'captain@barangay.gov'
            ORDER BY b.start_time
        ''', (date,))
        
        bookings = cursor.fetchall()
        for booking in bookings:
            booking_id, email, start_time, end_time, full_name = booking
            print(f"    - ID: {booking_id}, Email: {email}, Time: {start_time} - {end_time}, Name: {full_name}")
    
    conn.close()

if __name__ == "__main__":
    find_pending_resident()
