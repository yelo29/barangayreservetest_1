import sqlite3

print('=== CHECKING DEBUGUSER2 IN DATABASE ===')

conn = sqlite3.connect('server/barangay.db')
cursor = conn.cursor()

# Check the debug test user
cursor.execute('SELECT id, email, full_name, contact_number, address FROM users WHERE email = ?', ('debuguser2@gmail.com',))
user = cursor.fetchone()

if user:
    print('DATABASE DATA FOR debuguser2@gmail.com:')
    print(f'   - ID: {user[0]}')
    print(f'   - Email: {user[1]}')
    print(f'   - Full Name: "{user[2]}"')
    print(f'   - Contact: {user[3]}')
    print(f'   - Address: {user[4]}')
    
    if user[2] and user[2] != '':
        print('✅ SUCCESS: Name field was saved correctly!')
    else:
        print('❌ FAILED: Name field is empty!')
else:
    print('❌ User not found in database')

conn.close()
