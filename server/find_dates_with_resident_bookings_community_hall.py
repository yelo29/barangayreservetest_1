import sqlite3

def find_dates_with_resident_bookings():
    """Find dates with resident bookings for Community Hall"""
    
    conn = sqlite3.connect('barangay.db')
    cursor = conn.cursor()
    
    print("=== FINDING DATES WITH RESIDENT BOOKINGS (COMMUNITY HALL) ===")
    
    cursor.execute('''
        SELECT DISTINCT b.booking_date, COUNT(*) as resident_count
        FROM bookings b
        LEFT JOIN users u ON b.user_id = u.id
        WHERE b.facility_id = 1 
        AND (u.role = 'resident' OR u.role = '0' OR u.role IS NULL OR u.role LIKE '0.%')
        AND (b.status = 'pending' OR b.status = 'approved')
        GROUP BY b.booking_date
        ORDER BY b.booking_date
    ''')
    
    dates = cursor.fetchall()
    print(f"Found {len(dates)} dates with resident bookings for Community Hall:")
    
    for booking_date, count in dates:
        print(f"  📅 {booking_date}: {count} resident booking(s)")
        
        # Check if official also has booking on this date
        cursor.execute('''
            SELECT COUNT(*) FROM bookings b
            LEFT JOIN users u ON b.user_id = u.id
            WHERE b.facility_id = 1 
            AND b.booking_date = ?
            AND u.role = 'official'
        ''', (booking_date,))
        
        official_count = cursor.fetchone()[0]
        print(f"     🏆 Official bookings on this date: {official_count}")
        
        if official_count == 0:
            print(f"     ✅ GOOD DATE: No official conflict - can test ALL DAY auto-rejection")
        else:
            print(f"     ❌ BAD DATE: Official already exists")
    
    conn.close()

if __name__ == "__main__":
    find_dates_with_resident_bookings()
