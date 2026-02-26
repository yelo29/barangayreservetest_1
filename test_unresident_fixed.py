import requests

# Test login with correct password leo3029
print('=== Testing unresident@gmail.com with password leo3029 ===')
login_data = {
    'email': 'unresident@gmail.com',
    'password': 'leo3029'
}

response = requests.post('http://192.168.100.4:8000/api/auth/login', json=login_data)
print(f'Status: {response.status_code}')
result = response.json()
print(f'Response: {result}')

if result.get('success'):
    user = result['user']
    print(f'\n✅ Login successful!')
    print(f'  Name: {user.get("full_name")}')
    print(f'  Email: {user.get("email")}')
    print(f'  Role: {user.get("role")}')
    print(f'  Verified: {user.get("verified")}')
    print(f'  Verification Type: {user.get("verification_type")}')
    print(f'  Discount Rate: {user.get("discount_rate")}')
    print(f'  Authenticated: {user.get("is_authenticated")}')

# Test API profile endpoint
print('\n=== Testing profile API ===')
profile_response = requests.get('http://192.168.100.4:8000/api/users/profile/unresident@gmail.com')
if profile_response.status_code == 200:
    profile_data = profile_response.json()
    user = profile_data['user']
    print(f'✅ Profile API working:')
    print(f'  Verified: {user.get("verified")}')
    print(f'  Verification Type: {user.get("verification_type")}')
    print(f'  Discount Rate: {user.get("discount_rate")}')
else:
    print(f'❌ Profile API error: {profile_response.status_code}')
