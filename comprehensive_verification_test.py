import requests
import json

def comprehensive_verification_test():
    base_url = 'http://192.168.100.4:8000'
    
    print('🚀 COMPREHENSIVE VERIFICATION SYSTEM TEST')
    print('=' * 60)
    
    # Test 1: Check user profile first
    print('\n🔍 STEP 1: USER PROFILE VERIFICATION')
    print('-' * 40)
    
    try:
        profile_response = requests.get(f'{base_url}/api/users/profile/neverresident@gmail.com', timeout=5)
        if profile_response.status_code == 200:
            profile_data = profile_response.json()
            if profile_data.get('success') and profile_data.get('user'):
                user = profile_data['user']
                print(f'✅ Profile loaded:')
                print(f'  - ID: {user.get("id")}')
                print(f'  - Email: {user.get("email")}')
                print(f'  - Verified: {user.get("verified")} (type: {type(user.get("verified"))})')
                print(f'  - Verification Type: {user.get("verification_type")} (type: {type(user.get("verification_type"))})')
                print(f'  - Discount Rate: {user.get("discount_rate")} (type: {type(user.get("discount_rate"))})')
                
                user_id = user.get('id')
                
                # Test 2: Check verification status
                print(f'\n🔍 STEP 2: VERIFICATION STATUS CHECK')
                print('-' * 40)
                
                status_response = requests.get(f'{base_url}/api/verification-requests/status/{user_id}', timeout=5)
                if status_response.status_code == 200:
                    status_data = status_response.json()
                    print(f'✅ Verification Status:')
                    print(f'  - Can Submit: {status_data.get("can_submit")}')
                    print(f'  - Current Status: {status_data.get("current_status")}')
                    print(f'  - Lock Message: {status_data.get("lock_message")}')
                    
                    # Test 3: Verification request submission
                    print(f'\n🔍 STEP 3: VERIFICATION REQUEST SUBMISSION')
                    print('-' * 40)
                    
                    if status_data.get('can_submit'):
                        verification_data = {
                            'residentId': user_id,
                            'fullName': user.get('full_name'),
                            'contactNumber': user.get('contact_number'),
                            'address': user.get('address'),
                            'verificationType': 'non-resident',
                            'userPhotoUrl': user.get('profile_photo_url', ''),
                            'validIdUrl': '',
                            'submittedAt': '2026-02-26T16:45:00'
                        }
                        
                        print(f'🔍 Submitting verification request...')
                        print(f'  - User ID: {verification_data["residentId"]}')
                        print(f'  - Verification Type: {verification_data["verificationType"]}')
                        print(f'  - Full Name: {verification_data["fullName"]}')
                        
                        try:
                            submit_response = requests.post(f'{base_url}/api/verification-requests', json=verification_data, timeout=10)
                            
                            print(f'📊 Response Status: {submit_response.status_code}')
                            
                            if submit_response.status_code == 200:
                                result = submit_response.json()
                                print(f'✅ Success: {result.get("success")}')
                                print(f'📝 Message: {result.get("message")}')
                                
                                if result.get('success'):
                                    print('🎉 VERIFICATION REQUEST SUBMITTED SUCCESSFULLY!')
                                    
                                    # Test 4: Check updated verification status
                                    print(f'\n🔍 STEP 4: UPDATED STATUS CHECK')
                                    print('-' * 40)
                                    
                                    updated_status_response = requests.get(f'{base_url}/api/verification-requests/status/{user_id}', timeout=5)
                                    if updated_status_response.status_code == 200:
                                        updated_status = updated_status_response.json()
                                        print(f'✅ Updated Status:')
                                        print(f'  - Can Submit: {updated_status.get("can_submit")}')
                                        print(f'  - Current Status: {updated_status.get("current_status")}')
                                        print(f'  - Lock Message: {updated_status.get("lock_message")}')
                                    else:
                                        print(f'❌ Updated status check failed: {updated_status_response.status_code}')
                                else:
                                    print(f'❌ VERIFICATION REQUEST FAILED: {result.get("message")}')
                            else:
                                print(f'❌ HTTP Error: {submit_response.status_code}')
                                print(f'📝 Response: {submit_response.text}')
                                
                        except Exception as e:
                            print(f'❌ Verification request error: {e}')
                    else:
                        print('❌ User cannot submit verification request (form locked)')
                        print(f'   Reason: {status_data.get("lock_message")}')
                else:
                    print(f'❌ Status check failed: {status_response.status_code}')
            else:
                print(f'❌ Profile response invalid: {profile_data}')
        else:
            print(f'❌ Profile request failed: {profile_response.status_code}')
    except Exception as e:
        print(f'❌ Profile error: {e}')
    
    print('\n🎯 COMPREHENSIVE TEST COMPLETED')
    print('=' * 60)

if __name__ == '__main__':
    comprehensive_verification_test()
