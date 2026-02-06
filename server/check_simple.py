import sqlite3

conn = sqlite3.connect('barangay.db')
cursor = conn.cursor()

# Get user ID for jl052904@gmail.com
cursor.execute('SELECT id, full_name, verified, discount_rate FROM users WHERE email = "jl052904@gmail.com"')
user = cursor.fetchone()
print('User data:')
print(f'ID: {user[0]}')
print(f'Name: {user[1]}')
print(f'Verified: {user[2]}')
print(f'Discount Rate: {user[3]}')

print('\n' + '='*30 + '\n')

# Get verification request for this user
if user:
    cursor.execute('SELECT verification_type, status, discount_rate FROM verification_requests WHERE resident_id = ? ORDER BY submitted_at DESC LIMIT 1', (user[0],))
    request = cursor.fetchone()
    print('Verification request:')
    if request:
        print(f'Type: {request[0]}')
        print(f'Status: {request[1]}')
        print(f'Discount Rate: {request[2]}')
    else:
        print('No verification request found')

conn.close()
