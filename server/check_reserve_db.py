import sqlite3

print('=== CHECKING BARANGAY_RESERVE.DB ===')
try:
    conn = sqlite3.connect('barangay_reserve.db')
    cursor = conn.cursor()
    
    # Check if tables exist
    cursor.execute('SELECT name FROM sqlite_master WHERE type="table"')
    tables = cursor.fetchall()
    print(f'Tables: {[table[0] for table in tables]}')
    
    # Check users table
    try:
        cursor.execute('SELECT COUNT(*) FROM users')
        user_count = cursor.fetchone()[0]
        print(f'Users count: {user_count}')
        
        # Look for leo052904@gmail.com
        cursor.execute('SELECT id, email, full_name, role FROM users WHERE email = ?', ('leo052904@gmail.com',))
        leo_user = cursor.fetchone()
        if leo_user:
            print(f'Found leo052904@gmail.com: ID={leo_user[0]}, Name={leo_user[2]}, Role={leo_user[3]}')
        else:
            print('❌ leo052904@gmail.com NOT FOUND')
            
        # Check bookings
        cursor.execute('SELECT COUNT(*) FROM bookings')
        booking_count = cursor.fetchone()[0]
        print(f'Total bookings: {booking_count}')
        
        if booking_count > 0:
            print('Sample bookings:')
            cursor.execute('SELECT id, user_email, facility_name, booking_date, start_time FROM bookings LIMIT 5')
            bookings = cursor.fetchall()
            for booking in bookings:
                print(f'  ID: {booking[0]}, Email: {booking[1]}, Facility: {booking[2]}, Date: {booking[3]}, Time: {booking[4]}')
        
    except Exception as e:
        print(f'Error accessing barangay_reserve.db: {e}')
    
    conn.close()
except Exception as e:
    print(f'Could not open barangay_reserve.db: {e}')
