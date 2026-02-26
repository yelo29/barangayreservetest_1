import sqlite3

print('=== CHECKING ORIGINAL USER DATA ===')

conn = sqlite3.connect('server/barangay.db')
cursor = conn.cursor()

# Check the original user from the logs
cursor.execute('SELECT id, email, full_name, contact_number, address FROM users WHERE email = ?', ('TestNonresiden@gmail.com',))
user = cursor.fetchone()

if user:
    print('DATABASE DATA FOR TestNonresiden@gmail.com:')
    print(f'   - ID: {user[0]}')
    print(f'   - Email: {user[1]}')
    print(f'   - Full Name: "{user[2]}"')
    print(f'   - Contact: {user[3]}')
    print(f'   - Address: {user[4]}')
    
    if user[2] is None or user[2] == '':
        print('❌ DATABASE: Full Name is empty!')
        print('❌ This means the registration did NOT save the name to database')
    else:
        print('✅ DATABASE: Full Name is saved correctly')
else:
    print('❌ User not found in database')

# Check the test user
cursor.execute('SELECT id, email, full_name, contact_number, address FROM users WHERE email = ?', ('testname@gmail.com',))
test_user = cursor.fetchone()

if test_user:
    print('\nDATABASE DATA FOR testname@gmail.com:')
    print(f'   - ID: {test_user[0]}')
    print(f'   - Email: {test_user[1]}')
    print(f'   - Full Name: "{test_user[2]}"')
    print(f'   - Contact: {test_user[3]}')
    print(f'   - Address: {test_user[4]}')

conn.close()

print('\nROOT CAUSE ANALYSIS:')
print('The original user TestNonresiden@gmail.com has an empty name in the database!')
print('This means the registration endpoint is NOT saving the name field correctly.')
print('The issue is in the REGISTRATION endpoint, not the LOGIN endpoint!')
