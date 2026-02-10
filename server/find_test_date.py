import sqlite3

def find_test_date():
    """Find a date with resident bookings but no official bookings for Community Hall"""
    
    conn = sqlite3.connect('barangay.db')
    cursor = conn.cursor()
    
    print("=== FINDING TEST DATE FOR COMMUNITY HALL ===")
    
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
            print(f"     ✅ GOOD DATE: No official conflict - can test auto-rejection")
            
            # Show the resident bookings for this date
            cursor.execute('''
                SELECT b.id, b.start_time, b.status, u.email
                FROM bookings b
                LEFT JOIN users u ON b.user_id = u.id
                WHERE b.facility_id = 1 
                AND b.booking_date = ?
                AND (u.role = 'resident' OR u.role = '0' OR u.role IS NULL OR u.role LIKE '0.%')
                AND (b.status = 'pending' OR b.status = 'approved')
            ''', (booking_date,))
            
            resident_bookings = cursor.fetchall()
            print(f"     📋 Resident bookings:")
            for rb in resident_bookings:
                rb_id, rb_time, rb_status, rb_email = rb
                print(f"        - ID {rb_id}: {rb_time} - {rb_status} - {rb_email}")
        else:
            print(f"     ❌ BAD DATE: Official already exists")
        print()
    
    conn.close()

if __name__ == "__main__":
    find_test_date()
