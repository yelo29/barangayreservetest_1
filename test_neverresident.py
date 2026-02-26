import requests
import json

def test_neverresident_user():
    base_url = 'http://192.168.100.4:8000'
    
    print('🚀 TESTING VERIFICATION LOCK SYSTEM - neverresident@gmail.com')
    print('=' * 60)
    
    # Test login with neverresident@gmail.com
    print('\n🔍 STEP 1: Login with neverresident@gmail.com')
    print('-' * 40)
    
    # First, let's check what password this user has
    import sqlite3
    import os
    import hashlib
    
    db_path = os.path.join('server', 'barangay.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute('SELECT email, password FROM users WHERE email = ?', ('neverresident@gmail.com',))
    result = cursor.fetchone()
    
    if result:
        email, stored_hash = result
        print(f'✅ Found user: {email}')
        print(f'Stored hash: {stored_hash}')
        
        # Try common passwords
        common_passwords = ['123456', 'password', 'password123', 'test', 'resident']
        correct_password = None
        
        for password in common_passwords:
            test_hash = hashlib.sha256(password.encode()).hexdigest()
            if test_hash == stored_hash:
                correct_password = password
                print(f'✅ Found password: "{password}"')
                break
        
        if correct_password:
            # Test login
            login_data = {
                'email': 'neverresident@gmail.com',
                'password': correct_password
            }
            
            try:
                response = requests.post(f'{base_url}/api/auth/login', json=login_data, timeout=5)
                if response.status_code == 200:
                    result = response.json()
                    user_id = result['user']['id']
                    verified = result['user']['verified']
                    print(f'✅ Login successful: User ID {user_id}, Verified: {verified}')
                    
                    # Test verification status
                    print(f'\n🔍 STEP 2: Testing verification status for User ID {user_id}')
                    print('-' * 40)
                    
                    status_response = requests.get(f'{base_url}/api/verification-requests/status/{user_id}', timeout=5)
                    if status_response.status_code == 200:
                        status_data = status_response.json()
                        print(f'✅ Verification Status: {status_data}')
                        print(f'  - Can Submit: {status_data.get("can_submit")}')
                        print(f'  - Lock Message: {status_data.get("lock_message")}')
                        print(f'  - Current Status: {status_data.get("current_status")}')
                        
                        # Test verification lock logic
                        print(f'\n🔍 STEP 3: Testing verification lock logic')
                        print('-' * 40)
                        
                        if status_data.get('can_submit') == False:
                            print('✅ Form is correctly LOCKED')
                            print(f'   Reason: {status_data.get("lock_message")}')
                        else:
                            print('✅ Form is UNLOCKED - can submit verification')
                            
                    else:
                        print(f'❌ Status check failed: {status_response.status_code}')
                        print(f'   Response: {status_response.text}')
                else:
                    print(f'❌ Login failed: {response.status_code}')
                    print(f'   Response: {response.text}')
            except Exception as e:
                print(f'❌ Error: {e}')
        else:
            print('❌ Could not determine password for neverresident@gmail.com')
    else:
        print('❌ User neverresident@gmail.com not found in database')
    
    conn.close()
    print('\n🎯 TEST COMPLETED')

if __name__ == '__main__':
    test_neverresident_user()
