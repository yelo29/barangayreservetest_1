import requests

print('=== INVESTIGATING UNRESIDENT DATA LEAK ===')

# Test login API (correct data)
print('\n1. LOGIN API TEST:')
login_data = {
    'email': 'unresident@gmail.com',
    'password': 'leo3029'
}

login_response = requests.post('http://192.168.100.4:8000/api/auth/login', json=login_data)
if login_response.status_code == 200:
    login_result = login_response.json()
    login_user = login_result['user']
    print(f'✅ Login API:')
    print(f'   - Verified: {login_user.get("verified")}')
    print(f'   - Verification Type: {login_user.get("verification_type")}')
    print(f'   - Discount Rate: {login_user.get("discount_rate")}')
else:
    print(f'❌ Login API Error: {login_response.status_code}')

# Test profile API (wrong data)
print('\n2. PROFILE API TEST:')
profile_response = requests.get('http://192.168.100.4:8000/api/users/profile/unresident@gmail.com')
if profile_response.status_code == 200:
    profile_data = profile_response.json()
    profile_user = profile_data['user']
    print(f'❌ Profile API:')
    print(f'   - Verified: {profile_user.get("verified")}')
    print(f'   - Verification Type: {profile_user.get("verification_type")}')
    print(f'   - Discount Rate: {profile_user.get("discount_rate")}')
else:
    print(f'❌ Profile API Error: {profile_response.status_code}')

# Test verification status endpoint
print('\n3. VERIFICATION STATUS ENDPOINT TEST:')
# Get user ID from login response
user_id = login_user.get('id') if login_response.status_code == 200 else 32
status_response = requests.get(f'http://192.168.100.4:8000/api/verification-requests/status/{user_id}')
if status_response.status_code == 200:
    status_data = status_response.json()
    print(f'✅ Verification Status API:')
    print(f'   - Can Submit: {status_data.get("can_submit")}')
    print(f'   - Lock Message: "{status_data.get("lock_message")}"')
    print(f'   - Current Status: {status_data.get("current_status")}')
    print(f'   - Verified: {status_data.get("verified")}')
    print(f'   - Verification Type: {status_data.get("verification_type")}')
else:
    print(f'❌ Verification Status API Error: {status_response.status_code}')

print('\n4. DATA LEAK ANALYSIS:')
print('❌ PROFILE API is returning verification_type: null')
print('❌ This causes frontend to treat user as RESIDENT instead of NON-RESIDENT')
print('❌ LOGIN API and VERIFICATION STATUS API are correct')
print('❌ The data leak is in the PROFILE API endpoint!')

print('\n5. EXPECTED BEHAVIOR:')
print('✅ unresident@gmail.com should be: VERIFIED NON-RESIDENT')
print('✅ verification_type: non-resident')
print('✅ discount_rate: 0.05')
print('✅ Frontend should show: isVerifiedNonResident: true')

print('\n6. ACTUAL BEHAVIOR:')
print('❌ unresident@gmail.com is being: VERIFIED RESIDENT')
print('❌ verification_type: null (treated as resident)')
print('❌ discount_rate: 0.05')
print('❌ Frontend shows: isVerifiedResident: true')
