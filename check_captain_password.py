import sqlite3

print('=== CHECKING PASSWORD FOR captain@barangay.gov ===')

conn = sqlite3.connect('server/barangay.db')
cursor = conn.cursor()

cursor.execute('SELECT email, password FROM users WHERE email = ?', ('captain@barangay.gov',))
user = cursor.fetchone()

if user:
    print(f'Email: {user[0]}')
    print(f'Password Hash: {user[1]}')
    
    # Test common passwords
    import hashlib
    test_passwords = ['password123', 'password', 'admin', 'captain', 'barangay']
    
    for pwd in test_passwords:
        test_hash = hashlib.sha256(pwd.encode()).hexdigest()
        if user[1] == test_hash:
            print(f'✅ Password matches: {pwd}')
            break
    else:
        print('❌ No common password matches')
        print('Available options:')
        print('1. Set a new password')
        print('2. Try other common passwords')
else:
    print('User not found')

conn.close()
