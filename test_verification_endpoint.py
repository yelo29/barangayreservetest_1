import requests

print('=== TESTING VERIFICATION STATUS ENDPOINT ===')

# Test the verification status endpoint for kuyawill@gmail.com (user ID 40)
user_id = 40
response = requests.get(f'http://192.168.100.4:8000/api/verification-requests/status/{user_id}')

print(f'Status Code: {response.status_code}')
if response.status_code == 200:
    data = response.json()
    print(f'Response: {data}')
    print(f'Can Submit: {data.get("can_submit")}')
    print(f'Lock Message: "{data.get("lock_message")}"')
    print(f'Current Status: {data.get("current_status")}')
else:
    print(f'Error: {response.text}')

# Compare with profile API
print('\n=== COMPARISON WITH PROFILE API ===')
profile_response = requests.get('http://192.168.100.4:8000/api/users/profile/kuyawill@gmail.com')
if profile_response.status_code == 200:
    profile_data = profile_response.json()
    user = profile_data['user']
    print(f'Profile API - Verified: {user.get("verified")}')
    print(f'Profile API - Verification Type: {user.get("verification_type")}')
    print(f'Profile API - Discount Rate: {user.get("discount_rate")}')
else:
    print(f'Profile API Error: {profile_response.status_code}')
