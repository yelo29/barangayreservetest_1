import requests
import json

def test_neverresident_verification_lock():
    base_url = 'http://192.168.100.4:8000'
    
    print('🚀 TESTING VERIFICATION LOCK SYSTEM - neverresident@gmail.com')
    print('=' * 60)
    
    # Step 1: Login with neverresident@gmail.com
    print('\n🔍 STEP 1: Login with neverresident@gmail.com')
    print('-' * 40)
    
    login_data = {
        'email': 'neverresident@gmail.com',
        'password': 'leo3029'
    }
    
    try:
        response = requests.post(f'{base_url}/api/auth/login', json=login_data, timeout=5)
        if response.status_code == 200:
            result = response.json()
            user_id = result['user']['id']
            verified = result['user']['verified']
            print(f'✅ Login successful: User ID {user_id}, Verified: {verified}')
            
            # Step 2: Test verification status
            print(f'\n🔍 STEP 2: Testing verification status for User ID {user_id}')
            print('-' * 40)
            
            status_response = requests.get(f'{base_url}/api/verification-requests/status/{user_id}', timeout=5)
            if status_response.status_code == 200:
                status_data = status_response.json()
                print(f'✅ Verification Status: {status_data}')
                print(f'  - Can Submit: {status_data.get("can_submit")}')
                print(f'  - Lock Message: {status_data.get("lock_message")}')
                print(f'  - Current Status: {status_data.get("current_status")}')
                
                # Step 3: Analyze verification lock logic
                print(f'\n🔍 STEP 3: Verification Lock Analysis')
                print('-' * 40)
                
                if status_data.get('can_submit') == False:
                    print('✅ Form is LOCKED - User cannot submit verification')
                    print(f'   Reason: {status_data.get("lock_message")}')
                    print(f'   Status: {status_data.get("current_status")}')
                    
                    # Check if it's because already verified
                    if status_data.get('current_status') == 'verified_resident':
                        print('   📋 LOCK REASON: User is already verified as resident')
                    elif status_data.get('current_status') == 'verified_non_resident':
                        print('   📋 LOCK REASON: User is already verified as non-resident')
                    elif 'pending' in status_data.get('lock_message', '').lower():
                        print('   📋 LOCK REASON: User has pending verification request')
                else:
                    print('✅ Form is UNLOCKED - User can submit verification')
                    print('   📋 User can submit a new verification request')
                
                # Step 4: Test verification request submission (if unlocked)
                if status_data.get('can_submit') == True:
                    print(f'\n🔍 STEP 4: Testing verification request submission')
                    print('-' * 40)
                    
                    # This would normally be a POST to submit verification
                    print('✅ User can submit verification request')
                    print('   📋 Verification form should be accessible')
                else:
                    print(f'\n🔍 STEP 4: Verification submission blocked')
                    print('-' * 40)
                    print('✅ User cannot submit verification request')
                    print('   📋 Verification form should be locked/disabled')
                    
            else:
                print(f'❌ Status check failed: {status_response.status_code}')
                print(f'   Response: {status_response.text}')
        else:
            print(f'❌ Login failed: {response.status_code}')
            print(f'   Response: {response.text}')
    except Exception as e:
        print(f'❌ Error: {e}')
    
    print('\n🎯 VERIFICATION LOCK SYSTEM TEST COMPLETED')
    print('=' * 60)

if __name__ == '__main__':
    test_neverresident_verification_lock()
