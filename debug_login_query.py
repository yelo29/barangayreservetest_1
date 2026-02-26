import sqlite3

conn = sqlite3.connect('barangay.db')
cursor = conn.cursor()

# Check the actual structure of the users table
cursor.execute('PRAGMA table_info(users)')
columns = cursor.fetchall()
print('Users table structure:')
for col in columns:
    print(f'  {col[1]} ({col[2]}) - Index: {col[0]}')

# Test the exact query used in login
print('\n=== Testing login query ===')
query = 'SELECT id, email, password, full_name, role, verified, discount_rate, contact_number, address, created_at, verification_type FROM users WHERE email = ?'
cursor.execute(query, ('unresident@gmail.com',))
user = cursor.fetchone()

if user:
    print(f'Query result: {user}')
    print(f'Length: {len(user)}')
    for i, value in enumerate(user):
        print(f'  Index {i}: {value}')
else:
    print('No user found')

conn.close()
