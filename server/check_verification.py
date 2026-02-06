import sqlite3

conn = sqlite3.connect('barangay.db')
cursor = conn.cursor()

# Check verification requests for jl052904@gmail.com
cursor.execute('SELECT * FROM verification_requests WHERE email = "jl052904@gmail.com" ORDER BY created_at DESC LIMIT 1')
request = cursor.fetchone()
print('Latest verification request:')
if request:
    columns = [description[0] for description in cursor.description]
    for i, col in enumerate(columns):
        print(f'{col}: {request[i]}')
else:
    print('No verification request found')

print('\n' + '='*50 + '\n')

# Check current user data
cursor.execute('SELECT * FROM users WHERE email = "jl052904@gmail.com"')
user = cursor.fetchone()
print('Current user data:')
if user:
    columns = [description[0] for description in cursor.description]
    for i, col in enumerate(columns):
        print(f'{col}: {user[i]}')
else:
    print('No user found')

conn.close()
