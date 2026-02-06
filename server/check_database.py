import sqlite3

def check_database():
    conn = sqlite3.connect('barangay.db')
    cursor = conn.cursor()
    
    # Get all tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    print('📊 Available Tables:')
    for table in tables:
        print(f'  - {table[0]}')
    
    print('\n' + '='*50)
    
    # Check users table structure
    cursor.execute('PRAGMA table_info(users)')
    users_columns = cursor.fetchall()
    print('👥 Users Table Structure:')
    for col in users_columns:
        print(f'  - {col[1]} ({col[2]})')
    
    # Check sample data
    cursor.execute('SELECT COUNT(*) FROM users')
    user_count = cursor.fetchone()[0]
    print(f'📊 Total Users: {user_count}')
    
    cursor.execute('SELECT id, email, full_name, role FROM users LIMIT 3')
    users = cursor.fetchall()
    print('👥 Sample Users:')
    for user in users:
        print(f'  - ID: {user[0]}, Email: {user[1]}, Name: {user[2]}, Role: {user[3]}')
    
    print('\n' + '='*50)
    
    # Check facilities table structure  
    cursor.execute('PRAGMA table_info(facilities)')
    facilities_columns = cursor.fetchall()
    print('🏢 Facilities Table Structure:')
    for col in facilities_columns:
        print(f'  - {col[1]} ({col[2]})')
    
    # Check sample facilities
    cursor.execute('SELECT COUNT(*) FROM facilities')
    facility_count = cursor.fetchone()[0]
    print(f'📊 Total Facilities: {facility_count}')
    
    cursor.execute('SELECT id, name, hourly_rate, active FROM facilities LIMIT 3')
    facilities = cursor.fetchall()
    print('🏢 Sample Facilities:')
    for facility in facilities:
        print(f'  - ID: {facility[0]}, Name: {facility[1]}, Rate: {facility[2]}, Active: {facility[3]}')
    
    print('\n' + '='*50)
    
    # Check bookings table structure
    cursor.execute('PRAGMA table_info(bookings)')
    bookings_columns = cursor.fetchall()
    print('📅 Bookings Table Structure:')
    for col in bookings_columns:
        print(f'  - {col[1]} ({col[2]})')
    
    # Check sample bookings
    cursor.execute('SELECT COUNT(*) FROM bookings')
    booking_count = cursor.fetchone()[0]
    print(f'📊 Total Bookings: {booking_count}')
    
    if booking_count > 0:
        cursor.execute('SELECT id, user_id, facility_id, status, booking_date FROM bookings LIMIT 3')
        bookings = cursor.fetchall()
        print('📅 Sample Bookings:')
        for booking in bookings:
            print(f'  - ID: {booking[0]}, User: {booking[1]}, Facility: {booking[2]}, Status: {booking[3]}, Date: {booking[4]}')
    
    conn.close()

if __name__ == '__main__':
    check_database()
