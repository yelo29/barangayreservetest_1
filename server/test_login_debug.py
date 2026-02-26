import requests
import hashlib

# Test login for unresident@gmail.com
print('=== Testing unresident@gmail.com login ===')
login_data = {
    'email': 'unresident@gmail.com',
    'password': 'password123'  # Common test password
}

response = requests.post('http://192.168.100.4:8000/api/auth/login', json=login_data)
print(f'Status: {response.status_code}')
print(f'Response: {response.json()}')

# Test login for diddy@gmail.com
print('\n=== Testing diddy@gmail.com login ===')
login_data = {
    'email': 'diddy@gmail.com',
    'password': 'diddy3029'
}

response = requests.post('http://192.168.100.4:8000/api/auth/login', json=login_data)
print(f'Status: {response.status_code}')
print(f'Response: {response.json()}')

# Check what password hash is stored for both users
import sqlite3
conn = sqlite3.connect('barangay.db')
cursor = conn.cursor()

print('\n=== Password hashes ===')
cursor.execute('SELECT email, password FROM users WHERE email IN (?, ?)', ('unresident@gmail.com', 'diddy@gmail.com'))
users = cursor.fetchall()
for user in users:
    print(f'{user[0]}: {user[1]}')
    
    # Test common passwords
    test_passwords = ['password123', 'diddy3029', 'password', '123456']
    for pwd in test_passwords:
        test_hash = hashlib.sha256(pwd.encode()).hexdigest()
        if user[1] == test_hash:
            print(f'  ✓ Password matches: {pwd}')
            break
    else:
        print(f'  ✗ No common password matches')

conn.close()
