import sqlite3

conn = sqlite3.connect('barangay.db')
cursor = conn.cursor()

print('=== Checking unresident@gmail.com (ID: 32) ===')
cursor.execute('SELECT id, email, full_name, verified, verification_type, discount_rate, is_banned FROM users WHERE email = ?', ('unresident@gmail.com',))
user = cursor.fetchone()

if user:
    print(f'User found: {user}')
    print(f'ID: {user[0]}, Email: {user[1]}, Name: {user[2]}')
    print(f'Verified: {user[3]}, Verification Type: {user[4]}, Discount Rate: {user[5]}, Banned: {user[6]}')
else:
    print('User not found')

print('\n=== Checking diddy@gmail.com (ID: 35) ===')
cursor.execute('SELECT id, email, full_name, verified, verification_type, discount_rate, is_banned FROM users WHERE email = ?', ('diddy@gmail.com',))
user = cursor.fetchone()

if user:
    print(f'User found: {user}')
    print(f'ID: {user[0]}, Email: {user[1]}, Name: {user[2]}')
    print(f'Verified: {user[3]}, Verification Type: {user[4]}, Discount Rate: {user[5]}, Banned: {user[6]}')
else:
    print('User not found')

# Check verification requests for these users
print('\n=== Verification Requests ===')
cursor.execute('SELECT id, user_email, status, request_type, created_at FROM verification_requests WHERE user_email IN (?, ?)', ('unresident@gmail.com', 'diddy@gmail.com'))
requests = cursor.fetchall()
for req in requests:
    print(f'Request: {req}')

# Check all verification requests to see patterns
print('\n=== All Verification Requests ===')
cursor.execute('SELECT id, user_email, status, request_type, created_at FROM verification_requests ORDER BY created_at DESC LIMIT 10')
requests = cursor.fetchall()
for req in requests:
    print(f'Request: {req}')

conn.close()
