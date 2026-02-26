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

# Check what password hash is stored for diddy@gmail.com
import sqlite3
conn = sqlite3.connect('barangay.db')
cursor = conn.cursor()
cursor.execute('SELECT email, password FROM users WHERE email = ?', ('diddy@gmail.com',))
user = cursor.fetchone()
if user:
    print(f'\n=== Password hash for diddy@gmail.com ===')
    print(f'Stored hash: {user[1]}')
    
    # Test the provided password
    test_hash = hashlib.sha256('diddy3029'.encode()).hexdigest()
    print(f'Test hash: {test_hash}')
    print(f'Match: {user[1] == test_hash}')
conn.close()
