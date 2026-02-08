import sqlite3

def check_available_dates():
    """Find dates without official bookings"""
    
    conn = sqlite3.connect('barangay.db')
    cursor = conn.cursor()
    
    print("=== FINDING DATES WITHOUT OFFICIAL BOOKINGS ===")
    
    # Check dates in February 2026 that don't have official bookings
    cursor.execute('''
        SELECT DISTINCT b.booking_date
        FROM bookings b
        WHERE b.booking_date LIKE '2026-02-%' 
        AND b.facility_id = 1
        ORDER BY b.booking_date
    ''')
    
    all_dates = [row[0] for row in cursor.fetchall()]
    print(f"Dates with any bookings: {all_dates}")
    
    # Check which dates have official bookings
    cursor.execute('''
        SELECT DISTINCT b.booking_date
        FROM bookings b
        LEFT JOIN users u ON b.user_id = u.id
        WHERE b.booking_date LIKE '2026-02-%' 
        AND b.facility_id = 1
        AND u.email = 'captain@barangay.gov'
        ORDER BY b.booking_date
    ''')
    
    official_dates = [row[0] for row in cursor.fetchall()]
    print(f"Dates with official bookings: {official_dates}")
    
    # Find dates without official bookings
    available_dates = [date for date in all_dates if date not in official_dates]
    print(f"Available dates for testing (no official bookings): {available_dates}")
    
    # Check resident bookings on available dates
    for date in available_dates:
        cursor.execute('''
            SELECT b.id, b.status, u.email, b.start_time, b.end_time
            FROM bookings b
            LEFT JOIN users u ON b.user_id = u.id
            WHERE b.booking_date = ? AND b.facility_id = 1
            AND u.email != 'captain@barangay.gov'
            ORDER BY b.id
        ''', (date,))
        
        resident_bookings = cursor.fetchall()
        print(f"\n{date} - Resident bookings: {len(resident_bookings)}")
        for booking in resident_bookings:
            booking_id, status, email, start_time, end_time = booking
            print(f"  - ID: {booking_id}, Status: {status}, Email: {email}, Time: {start_time} - {end_time}")
    
    conn.close()

if __name__ == "__main__":
    check_available_dates()
