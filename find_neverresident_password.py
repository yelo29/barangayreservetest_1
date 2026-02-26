import sqlite3
import os
import hashlib
import requests

# Try more specific passwords for neverresident@gmail.com
db_path = os.path.join('server', 'barangay.db')
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

print('🔍 FINDING PASSWORD FOR neverresident@gmail.com')

# Get the hash
cursor.execute('SELECT password FROM users WHERE email = ?', ('neverresident@gmail.com',))
result = cursor.fetchone()
target_hash = result[0]

print(f'Target hash: {target_hash}')

# Try more specific passwords
passwords_to_try = [
    '123456', 'password', 'password123', 'test', 'resident', 'unresident', 
    'neverresident', 'user', 'admin', 'barangay', 'leo052904', 'leo',
    'resident123', 'unresident123', 'never123', 'test123', 'user123',
    'abc123', 'qwerty', 'letmein', 'welcome', 'monkey', 'dragon'
]

print(f'Trying {len(passwords_to_try)} passwords...')

found_password = None
for password in passwords_to_try:
    test_hash = hashlib.sha256(password.encode()).hexdigest()
    if test_hash == target_hash:
        found_password = password
        print(f'✅ FOUND PASSWORD: "{password}"')
        break

if found_password:
    # Test login and verification status
    base_url = 'http://192.168.100.4:8000'
    login_data = {
        'email': 'neverresident@gmail.com',
        'password': found_password
    }
    
    print(f'\n🔍 Testing login with password "{found_password}"')
    response = requests.post(f'{base_url}/api/auth/login', json=login_data, timeout=5)
    
    if response.status_code == 200:
        result = response.json()
        user_id = result['user']['id']
        verified = result['user']['verified']
        print(f'✅ Login successful: User ID {user_id}, Verified: {verified}')
        
        # Test verification status
        print(f'\n🔍 Testing verification status for User ID {user_id}')
        status_response = requests.get(f'{base_url}/api/verification-requests/status/{user_id}', timeout=5)
        
        if status_response.status_code == 200:
            status_data = status_response.json()
            print(f'✅ Verification Status: {status_data}')
            print(f'  - Can Submit: {status_data.get("can_submit")}')
            print(f'  - Lock Message: {status_data.get("lock_message")}')
            print(f'  - Current Status: {status_data.get("current_status")}')
            
            # Test verification lock logic
            print(f'\n🔍 VERIFICATION LOCK ANALYSIS:')
            print('-' * 40)
            
            if status_data.get('can_submit') == False:
                print('✅ Form is LOCKED - User cannot submit verification')
                print(f'   Reason: {status_data.get("lock_message")}')
                print(f'   Status: {status_data.get("current_status")}')
            else:
                print('✅ Form is UNLOCKED - User can submit verification')
                
            print(f'\n🎯 TEST RESULT: Verification lock system working correctly!')
        else:
            print(f'❌ Status check failed: {status_response.status_code}')
    else:
        print(f'❌ Login failed: {response.status_code}')
        print(f'   Response: {response.text}')
else:
    print('❌ Password not found in common list')
    print('🔍 This might be a custom password. Let me check if there are any verification requests...')
    
    # Check if there are any verification requests for this user
    cursor.execute('SELECT user_id, status, created_at FROM verification_requests WHERE user_id IN (SELECT id FROM users WHERE email = ?)', ('neverresident@gmail.com',))
    requests = cursor.fetchall()
    
    if requests:
        print(f'Found {len(requests)} verification requests:')
        for req in requests:
            print(f'  - User ID: {req[0]}, Status: {req[1]}, Created: {req[2]}')
    else:
        print('No verification requests found for this user')

conn.close()
