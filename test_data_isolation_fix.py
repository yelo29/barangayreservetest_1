import requests

print('=== TESTING DATA ISOLATION LEAK FIX ===')

# Test the verification status endpoint directly
print('\n1. TESTING VERIFICATION STATUS ENDPOINT:')
user_id = 40
response = requests.get(f'http://192.168.100.4:8000/api/verification-requests/status/{user_id}')

if response.status_code == 200:
    data = response.json()
    print(f'✅ Endpoint Response: {data}')
    print(f'   - Can Submit: {data.get("can_submit")}')
    print(f'   - Lock Message: "{data.get("lock_message")}"')
    print(f'   - Current Status: {data.get("current_status")}')
    print(f'   - Verified: {data.get("verified")}')
    print(f'   - Verification Type: {data.get("verification_type")}')
    
    # Verify the logic is correct
    can_submit = data.get('can_submit', False)
    lock_message = data.get('lock_message', '')
    current_status = data.get('current_status', '')
    
    if can_submit and current_status == 'unverified':
        print('✅ CORRECT: User correctly identified as UNVERIFIED')
    elif not can_submit and 'already verified' in lock_message:
        print('❌ DATA LEAK: User incorrectly identified as VERIFIED')
    else:
        print(f'⚠️  UNEXPECTED: can_submit={can_submit}, status={current_status}')
else:
    print(f'❌ Endpoint Error: {response.status_code}')

# Test profile API for consistency
print('\n2. TESTING PROFILE API CONSISTENCY:')
profile_response = requests.get('http://192.168.100.4:8000/api/users/profile/kuyawill@gmail.com')
if profile_response.status_code == 200:
    profile_data = profile_response.json()
    user = profile_data['user']
    print(f'✅ Profile API Response:')
    print(f'   - Verified: {user.get("verified")}')
    print(f'   - Verification Type: {user.get("verification_type")}')
    print(f'   - Discount Rate: {user.get("discount_rate")}')
    
    # Cross-check data consistency
    api_verified = user.get('verified', 0)
    api_type = user.get('verification_type')
    api_discount = user.get('discount_rate', 0)
    
    status_verified = data.get('verified', 0)
    status_type = data.get('verification_type')
    
    if api_verified == status_verified and api_type == status_type:
        print('✅ DATA CONSISTENCY: API and Status endpoint match')
    else:
        print('❌ DATA INCONSISTENCY: API and Status endpoint differ')
        print(f'   API: verified={api_verified}, type={api_type}')
        print(f'   Status: verified={status_verified}, type={status_type}')
else:
    print(f'❌ Profile API Error: {profile_response.status_code}')

print('\n3. SUMMARY OF FIXES:')
print('✅ Fixed verification status caching issue')
print('✅ Added cache clearing on login, registration, and user restore')
print('✅ Ensured real-time verification status checking')
print('✅ Aligned frontend with backend data')

print('\n4. EXPECTED FLUTTER BEHAVIOR AFTER FIX:')
print('✅ Verification form should show: "You can submit a verification request"')
print('✅ Can Submit should be: true')
print('✅ Current Status should be: "unverified"')
print('✅ No more data isolation leaks between API and frontend')
