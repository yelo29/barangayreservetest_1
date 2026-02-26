import sqlite3
import os
import hashlib

# Check what's actually in the password field
db_path = os.path.join('server', 'barangay.db')
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

print('🔍 Checking password field content...')
cursor.execute('SELECT email, password FROM users WHERE email = ?', ('unresident@gmail.com',))
result = cursor.fetchone()

if result:
    email, stored_password = result
    print(f'Email: {email}')
    print(f'Stored password: {stored_password}')
    
    # Check if it's a hash
    test_password = 'password123'
    test_hash = hashlib.sha256(test_password.encode()).hexdigest()
    print(f'Test hash: {test_hash}')
    print(f'Hashes match: {stored_password == test_hash}')

conn.close()
