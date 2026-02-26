import sqlite3
import os
import hashlib

# Check if unresident@gmail.com has password 123456
db_path = os.path.join('server', 'barangay.db')
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

print('🔍 Checking unresident@gmail.com password...')
cursor.execute('SELECT email, password FROM users WHERE email = ?', ('unresident@gmail.com',))
result = cursor.fetchone()

if result:
    email, stored_hash = result
    print(f'Email: {email}')
    print(f'Stored hash: {stored_hash}')
    
    # Check if it's 123456
    test_hash = hashlib.sha256('123456'.encode()).hexdigest()
    print(f'Hash for "123456": {test_hash}')
    print(f'Hashes match: {stored_hash == test_hash}')
    
    if stored_hash == test_hash:
        print('✅ unresident@gmail.com has password "123456"')
    else:
        print('❌ unresident@gmail.com does NOT have password "123456"')
        
        # Let's find a user that does have 123456
        cursor.execute('SELECT email, password FROM users WHERE password = ?', (test_hash,))
        user_with_123456 = cursor.fetchone()
        if user_with_123456:
            print(f'✅ Found user with password "123456": {user_with_123456[0]}')
        else:
            print('❌ No user has password "123456"')

conn.close()
