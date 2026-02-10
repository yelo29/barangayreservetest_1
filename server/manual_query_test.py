import sqlite3

def manual_query_test():
    """Manually test the query step by step"""
    
    conn = sqlite3.connect('barangay.db')
    cursor = conn.cursor()
    
    print("=== MANUAL QUERY TEST ===")
    
    # Step 1: Check all bookings for facility 1
    cursor.execute('''
        SELECT b.id, b.facility_id, b.booking_date, b.start_time, b.status, u.email, u.role
        FROM bookings b
        LEFT JOIN users u ON b.user_id = u.id
        WHERE b.facility_id = 1
        ORDER BY b.booking_date, b.id
    ''')
    
    all_facility_bookings = cursor.fetchall()
    print(f"📋 All bookings for facility 1:")
    for booking in all_facility_bookings:
        booking_id, facility_id, booking_date, start_time, status, email, role = booking
        print(f"  ID {booking_id}: {booking_date} - {start_time} - {status} - {email} ({role})")
    
    # Step 2: Check bookings for 2026-04-01 specifically
    cursor.execute('''
        SELECT b.id, b.facility_id, b.booking_date, b.start_time, b.status, u.email, u.role
        FROM bookings b
        LEFT JOIN users u ON b.user_id = u.id
        WHERE b.facility_id = 1 AND b.booking_date = '2026-04-01'
        ORDER BY b.id
    ''')
    
    date_bookings = cursor.fetchall()
    print(f"\n📅 Bookings for 2026-04-01:")
    for booking in date_bookings:
        booking_id, facility_id, booking_date, start_time, status, email, role = booking
        print(f"  ID {booking_id}: {start_time} - {status} - {email} ({role})")
    
    # Step 3: Test the exact query
    cursor.execute('''
        SELECT b.id, b.user_id, b.start_time, b.end_time, b.status, u.email as user_email, u.full_name
        FROM bookings b
        LEFT JOIN users u ON b.user_id = u.id
        WHERE b.facility_id = 1 
        AND b.booking_date = '2026-04-01'
        AND (b.status = 'pending' OR b.status = 'approved')
        AND (u.role = 'resident' OR u.role = '0' OR u.role IS NULL OR u.role LIKE '0.%')
        AND b.user_id != 1
        ORDER BY b.id
    ''')
    
    query_results = cursor.fetchall()
    print(f"\n🔍 Query results:")
    for booking in query_results:
        booking_id, user_id, start_time, end_time, status, user_email, full_name = booking
        print(f"  ID {booking_id}: User {user_id} - {start_time} - {status} - {user_email}")
    
    conn.close()

if __name__ == "__main__":
    manual_query_test()
