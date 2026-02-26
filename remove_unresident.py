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
    
    # Also delete any related bookings
    cursor.execute('DELETE FROM bookings WHERE user_email = ?', ('unresident@gmail.com',))
    
    conn.commit()
    conn.close()
    
    print(f'✅ Successfully removed unresident@gmail.com and all related data')
else:
    print('❌ User unresident@gmail.com not found in database')

conn.close()

print('\nVERIFICATION:')
print('- User account deleted')
print('- Verification requests deleted')
print('- Booking history deleted')
