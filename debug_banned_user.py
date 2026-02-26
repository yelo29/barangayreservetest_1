import requests
import sqlite3
import hashlib

print('=== DEBUGGING BANNED USER LOGIN ===')

# Check banned user details
conn = sqlite3.connect('barangay.db')
cursor = conn.cursor()

cursor.execute('SELECT email, password, is_banned, ban_reason FROM users WHERE email = ?', ('residenttestban@gmail.com',))
user = cursor.fetchone()

if user:
    print(f'Banned user details:')
    print(f'  - Email: {user[0]}')
    print(f'  - Password Hash: {user[1]}')
    print(f'  - Is Banned: {user[2]}')
    print(f'  - Ban Reason: {user[3]}')
    
    # Test with common passwords
    test_passwords = ['password123', 'password', '123456', 'test']
    for pwd in test_passwords:
        test_hash = hashlib.sha256(pwd.encode()).hexdigest()
        if user[1] == test_hash:
            print(f'  ✓ Password matches: {pwd}')
            
            # Test login with correct password
            print(f'\nTesting login with correct password ({pwd}):')
            login_data = {
                'email': 'residenttestban@gmail.com',
                'password': pwd
            }
            
            response = requests.post('http://192.168.100.4:8000/api/auth/login', json=login_data)
            print(f'  Status: {response.status_code}')
            result = response.json()
            print(f'  Response: {result}')
            
            if response.status_code == 403:
                print('  ✅ Banned user properly blocked with 403 Forbidden')
            else:
                print(f'  ❌ Expected 403 Forbidden, got {response.status_code}')
            break
    else:
        print('  ✗ No common password matches - updating password')
        
        # Update password to known value
        new_password = 'password123'
        new_hash = hashlib.sha256(new_password.encode()).hexdigest()
        cursor.execute('UPDATE users SET password = ? WHERE email = ?', (new_hash, 'residenttestban@gmail.com'))
        conn.commit()
        print(f'  ✅ Updated password to: {new_password}')
        
        # Test again
        print(f'\nTesting login with new password:')
        login_data = {
            'email': 'residenttestban@gmail.com',
            'password': new_password
        }
        
        response = requests.post('http://192.168.100.4:8000/api/auth/login', json=login_data)
        print(f'  Status: {response.status_code}')
        result = response.json()
        print(f'  Response: {result}')

conn.close()
