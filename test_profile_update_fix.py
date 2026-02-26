import requests

print('=== TESTING PROFILE UPDATE FIX ===')

# First, register a new user
reg_data = {
    'name': 'TestProfileUser',
    'email': 'testprofile@gmail.com',
    'password': 'password123',
    'role': 'resident',
    'contact_number': '1234567890',
    'address': 'Initial Address'
}

print('1. Registering new user...')
reg_response = requests.post('http://192.168.100.4:8000/api/auth/register', json=reg_data)
if reg_response.status_code == 200:
    reg_result = reg_response.json()
    print(f'✅ Registration successful: {reg_result.get("user", {}).get("full_name")}')
else:
    print(f'❌ Registration failed: {reg_response.text}')

# Test profile update with only contact and address (should NOT overwrite name)
update_data = {
    'email': 'testprofile@gmail.com',
    'contact_number': '9876543210',
    'address': 'Updated Address'
    # Note: NOT including full_name field
}

print('\n2. Updating profile (without full_name)...')
update_response = requests.put('http://192.168.100.4:8000/api/users/profile', json=update_data)
if update_response.status_code == 200:
    print('✅ Profile update successful')
else:
    print(f'❌ Profile update failed: {update_response.text}')

# Check if name is preserved
print('\n3. Checking profile after update...')
profile_response = requests.get('http://192.168.100.4:8000/api/users/profile/testprofile@gmail.com')
if profile_response.status_code == 200:
    profile_data = profile_response.json()
    user = profile_data['user']
    print(f'Full Name: "{user.get("full_name")}"')
    print(f'Contact: {user.get("contact_number")}')
    print(f'Address: {user.get("address")}')
    
    if user.get('full_name') == 'TestProfileUser':
        print('✅ SUCCESS: Name field preserved!')
    else:
        print('❌ FAILED: Name field was lost!')
else:
    print(f'❌ Profile check failed: {profile_response.status_code}')
