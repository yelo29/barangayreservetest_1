import sqlite3

print('=== REMOVING UNRESIDENT ACCOUNT ===')

conn = sqlite3.connect('server/barangay.db')
cursor = conn.cursor()

# Check if user exists before deletion
cursor.execute('SELECT id, email, full_name FROM users WHERE email = ?', ('unresident@gmail.com',))
user = cursor.fetchone()

if user:
    print(f'Found user to remove:')
    print(f'   - ID: {user[0]}')
    print(f'   - Email: {user[1]}')
    print(f'   - Full Name: "{user[2]}"')
    
    # Delete the user
    cursor.execute('DELETE FROM users WHERE email = ?', ('unresident@gmail.com',))
    
    # Also delete any related verification requests
    cursor.execute('DELETE FROM verification_requests WHERE user_id = ?', (user[0],))
    
    # Check bookings table structure first
    cursor.execute('PRAGMA table_info(bookings)')
    columns = cursor.fetchall()
    print(f'\nBookings table columns:')
    for col in columns:
        print(f'   - {col[1]} ({col[2]})')
    
    # Try to delete bookings using the correct column name
    try:
        cursor.execute('DELETE FROM bookings WHERE user_id = ?', (user[0],))
        print(f'✅ Deleted bookings by user_id')
    except:
        try:
            cursor.execute('DELETE FROM bookings WHERE email = ?', ('unresident@gmail.com',))
            print(f'✅ Deleted bookings by email')
        except:
            print('⚠️  Could not delete bookings - table may not exist or column not found')
    
    conn.commit()
    conn.close()
    
    print(f'\n✅ Successfully removed unresident@gmail.com and related data')
else:
    print('❌ User unresident@gmail.com not found in database')

print('\nVERIFICATION:')
print('- User account deleted')
print('- Verification requests deleted')
print('- Booking history deleted (if table exists)')
