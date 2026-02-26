import requests
import json

def test_verification_lock_system():
    base_url = 'http://192.168.100.4:8000'
    
    print('🚀 VERIFICATION LOCK SYSTEM - COMPREHENSIVE TEST')
    print('=' * 60)
    
    # Test 1: Login with verified resident (mamamo@gmail.com)
    print('\n🔍 TEST 1: Verified Resident Login')
    print('-' * 40)
    
    login_data = {
        'email': 'mamamo@gmail.com',
        'password': '123456'
    }
    
    try:
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
    except Exception as e:
        print(f'❌ Error: {e}')
    
    # Test 2: Check unverified user
    print(f'\n🔍 TEST 2: Unverified User Check')
    print('-' * 40)
    
    # Find an unverified user
    try:
        # Try leo052904@gmail.com (should be unverified)
        login_data = {
            'email': 'leo052904@gmail.com',
            'password': '123456'
        }
        
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
    except Exception as e:
        print(f'❌ Error: {e}')
    
    print('\n🎯 VERIFICATION LOCK SYSTEM TEST COMPLETED')

if __name__ == '__main__':
    test_verification_lock_system()
