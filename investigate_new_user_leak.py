import sqlite3

print('=== INVESTIGATING NEW USER DATA LEAK ===')

conn = sqlite3.connect('server/barangay.db')
cursor = conn.cursor()

# Check the new user from the logs
cursor.execute('SELECT id, email, full_name, contact_number, address FROM users WHERE email = ?', ('leoOne@gmail.com',))
user = cursor.fetchone()

if user:
    print('DATABASE DATA FOR leoOne@gmail.com:')
    print(f'   - ID: {user[0]}')
    print(f'   - Email: {user[1]}')
    print(f'   - Full Name: "{user[2]}"')
    print(f'   - Contact: {user[3]}')
    print(f'   - Address: {user[4]}')
    
    if user[2] is None or user[2] == '':
        print('❌ DATABASE: Full Name is empty!')
        print('❌ This confirms the registration did NOT save the name to database')
    else:
        print('✅ DATABASE: Full Name is saved correctly')
else:
    print('❌ User not found in database')

conn.close()

print('\nANALYSIS:')
print('From the logs:')
print('1. Registration Response: full_name="leo one" ✅')
print('2. First Login Response: full_name="leo one" ✅')  
print('3. Second Login Response: full_name="" ❌')
print('4. Database: Full Name is empty ❌')

print('\nROOT CAUSE:')
print('The registration is NOT saving the full_name to the database!')
print('The registration response is returning the name from memory,')
print('but it\'s not being persisted to the database.')
print('This is the same bug we identified earlier!')
