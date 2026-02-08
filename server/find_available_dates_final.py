import sqlite3

def find_available_dates():
    """Find dates without any bookings"""
    
    conn = sqlite3.connect('barangay.db')
    cursor = conn.cursor()
    
    print("=== FINDING AVAILABLE DATES ===")
    
    # Check dates in February 2026 that have NO bookings
    cursor.execute('''
        SELECT DISTINCT b.booking_date
        FROM bookings b
        WHERE b.booking_date LIKE '2026-02-%'
        AND b.facility_id = 1
        ORDER BY b.booking_date
    ''')
    
    booked_dates = [row[0] for row in cursor.fetchall()]
    print(f"Dates with bookings: {booked_dates}")
    
    # Find dates that are completely free
    all_february_dates = [f"2026-02-{day:02d}" for day in range(1, 29)]
    available_dates = [date for date in all_february_dates if date not in booked_dates]
    
    print(f"Available dates for testing: {available_dates}")
    
    conn.close()

if __name__ == "__main__":
    find_available_dates()
