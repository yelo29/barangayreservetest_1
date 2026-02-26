import sqlite3
import os
import hashlib

# Check all users with the same hash as neverresident@gmail.com
db_path = os.path.join('server', 'barangay.db')
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

print('🔍 ANALYZING neverresident@gmail.com HASH')

# Get neverresident's hash
cursor.execute('SELECT email, password FROM users WHERE email = ?', ('neverresident@gmail.com',))
neverresident_result = cursor.fetchone()

if neverresident_result:
    email, neverresident_hash = neverresident_result
    print(f'neverresident@gmail.com hash: {neverresident_hash}')
    
    # Find all users with the same hash
    cursor.execute('SELECT email FROM users WHERE password = ?', (neverresident_hash,))
    same_hash_users = cursor.fetchall()
    
    print(f'Users with same hash ({len(same_hash_users)}):')
    for user in same_hash_users:
        print(f'  - {user[0]}')
    
    # Check if unresident@gmail.com has the same hash
    cursor.execute('SELECT email, password FROM users WHERE email = ?', ('unresident@gmail.com',))
    unresident_result = cursor.fetchone()
    
    if unresident_result:
        unresident_hash = unresident_result[1]
        print(f'\nunresident@gmail.com hash: {unresident_hash}')
        print(f'Hashes match: {neverresident_hash == unresident_hash}')
        
        if neverresident_hash == unresident_hash:
            print('✅ Both users have the same password!')
            
            # Try to find the password by checking if it's a common pattern
            common_passwords = ['123456', 'password', 'password123', 'test', 'resident', 'unresident', 'neverresident', 'user']
            
            for password in common_passwords:
                test_hash = hashlib.sha256(password.encode()).hexdigest()
                if test_hash == neverresident_hash:
                    print(f'✅ Found password: "{password}"')
                    
                    # Test login with this password
                    import requests
                    
                    base_url = 'http://192.168.100.4:8000'
                    login_data = {
                        'email': 'neverresident@gmail.com',
                        'password': password
                    }
                    
                    print(f'\n🔍 Testing login with password "{password}"')
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
                        else:
                            print(f'❌ Status check failed: {status_response.status_code}')
                    else:
                        print(f'❌ Login failed: {response.status_code}')
                        print(f'   Response: {response.text}')
                    
                    break
            else:
                print('❌ No common password matches found')
        else:
            print('❌ Users have different passwords')
else:
    print('❌ neverresident@gmail.com not found')

conn.close()
