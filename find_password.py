import sqlite3
import os
import hashlib

# Try to find the correct password
db_path = os.path.join('server', 'barangay.db')
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

print('🔍 Trying to find the correct password...')
cursor.execute('SELECT email, password FROM users WHERE email = ?', ('unresident@gmail.com',))
result = cursor.fetchone()

if result:
    email, stored_hash = result
    print(f'Email: {email}')
    print(f'Stored hash: {stored_hash}')
    
    # Try common passwords
    common_passwords = ['password123', 'password', '123456', 'admin', 'test', 'unresident']
    
    for password in common_passwords:
        test_hash = hashlib.sha256(password.encode()).hexdigest()
        if test_hash == stored_hash:
            print(f'✅ FOUND PASSWORD: "{password}"')
            break
    else:
        print('❌ No common password matches found')

conn.close()
