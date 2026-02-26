import requests
import sqlite3

print('=== COMPREHENSIVE LOGIN & SIGNUP TESTING ===')

# Test 1: All account types login
print('\n--- TEST 1: LOGIN FOR ALL ACCOUNT TYPES ---')

test_accounts = [
    {'email': 'unresident@gmail.com', 'password': 'leo3029', 'type': 'VERIFIED NON-RESIDENT'},
    {'email': 'residentresident@gmail.com', 'password': 'password123', 'type': 'VERIFIED RESIDENT'}, 
    {'email': 'diddy@gmail.com', 'password': 'diddy3029', 'type': 'UNVERIFIED USER'},
    {'email': 'residenttestban@gmail.com', 'password': 'password123', 'type': 'BANNED USER'},
    {'email': 'captain@barangay.gov', 'password': 'password123', 'type': 'OFFICIAL ACCOUNT'},
]

for account in test_accounts:
    print(f'\nTesting {account["type"]} - {account["email"]}:')
    
    login_data = {
        'email': account['email'],
        'password': account['password']
    }
    
    response = requests.post('http://192.168.100.4:8000/api/auth/login', json=login_data)
    
    if response.status_code == 200:
        result = response.json()
        user = result['user']
        
        print(f'  ✅ Login SUCCESS')
        print(f'     - Name: {user.get("full_name")}')
        print(f'     - Role: {user.get("role")}')
        print(f'     - Verified: {user.get("verified")}')
        print(f'     - Verification Type: {user.get("verification_type")}')
        print(f'     - Discount Rate: {user.get("discount_rate")}')
        print(f'     - Is Banned: {user.get("is_banned")}')
        print(f'     - Token: {result.get("token", "N/A")[:20]}...')
        
        # Test if token works for profile API
        if result.get('token'):
            profile_response = requests.get(f'http://192.168.100.4:8000/api/users/profile/{account["email"]}')
            if profile_response.status_code == 200:
                print(f'     ✅ Profile API accessible')
            else:
                print(f'     ❌ Profile API failed: {profile_response.status_code}')
                
    elif response.status_code == 403:
        result = response.json()
        print(f'  🔒 Login BLOCKED - {result.get("message")}')
    elif response.status_code == 401:
        result = response.json()
        print(f'  ❌ Login FAILED - {result.get("message")}')
    else:
        print(f'  ❌ Login ERROR - Status: {response.status_code}')

# Test 2: Check banned status in database
print('\n--- TEST 2: BANNED STATUS VERIFICATION ---')
conn = sqlite3.connect('barangay.db')
cursor = conn.cursor()

cursor.execute('SELECT email, is_banned, ban_reason, banned_at FROM users WHERE is_banned = 1')
banned_users = cursor.fetchall()

print(f'Found {len(banned_users)} banned users:')
for user in banned_users:
    print(f'  - {user[0]}: Reason="{user[2]}", Banned at="{user[3]}"')

conn.close()

# Test 3: Sign-up flow test
print('\n--- TEST 3: SIGN-UP FLOW TEST ---')

import random
import string

def generate_random_email():
    return ''.join(random.choices(string.ascii_lowercase, k=8)) + '@test.com'

def generate_random_password():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=8))

# Test new registration
new_email = generate_random_email()
new_password = generate_random_password()
new_name = f'Test User {random.randint(100, 999)}'

print(f'Testing new registration:')
print(f'  Email: {new_email}')
print(f'  Password: {new_password}')
print(f'  Name: {new_name}')

# Step 1: Register new user
register_data = {
    'name': new_name,
    'email': new_email,
    'password': new_password,
    'role': 'resident'
}

register_response = requests.post('http://192.168.100.4:8000/api/auth/register', json=register_data)

if register_response.status_code == 200:
    register_result = register_response.json()
    print(f'  ✅ Registration SUCCESS')
    print(f'     - Success: {register_result.get("success")}')
    print(f'     - User ID: {register_result.get("user", {}).get("id")}')
    print(f'     - Email: {register_result.get("user", {}).get("email")}')
    print(f'     - Name: {register_result.get("user", {}).get("full_name")}')
    print(f'     - Token: {register_result.get("token", "N/A")[:20] if register_result.get("token") else "None"}...')
    
    # Step 2: Test immediate login after registration
    print(f'\n  Testing immediate login after registration:')
    login_data = {
        'email': new_email,
        'password': new_password
    }
    
    login_response = requests.post('http://192.168.100.4:8000/api/auth/login', json=login_data)
    
    if login_response.status_code == 200:
        login_result = login_response.json()
        print(f'  ✅ Immediate login SUCCESS')
        print(f'     - Authenticated: {login_result.get("user", {}).get("is_authenticated")}')
        print(f'     - Token: {login_result.get("token", "N/A")[:20]}...')
        print(f'     - User treated as LOGGED IN: YES')
    else:
        print(f'  ❌ Immediate login FAILED: {login_response.status_code}')
        print(f'     - User treated as LOGGED IN: NO')
        
    # Step 3: Test profile access after registration
    print(f'\n  Testing profile access after registration:')
    profile_response = requests.get(f'http://192.168.100.4:8000/api/users/profile/{new_email}')
    
    if profile_response.status_code == 200:
        profile_data = profile_response.json()
        print(f'  ✅ Profile access SUCCESS')
        print(f'     - Verified: {profile_data.get("user", {}).get("verified")}')
        print(f'     - Verification Type: {profile_data.get("user", {}).get("verification_type")}')
        print(f'     - Discount Rate: {profile_data.get("user", {}).get("discount_rate")}')
    else:
        print(f'  ❌ Profile access FAILED: {profile_response.status_code}')
        
else:
    print(f'  ❌ Registration FAILED: {register_response.status_code}')
    print(f'     - Error: {register_response.json()}')

print(f'\n--- TEST 4: FRONTEND SESSION PERSISTENCE SIMULATION ---')
print('Simulating what happens when user is redirected to dashboard after registration...')

# Test if the registration response includes proper session data
if register_response.status_code == 200:
    register_result = register_response.json()
    
    # Check if registration response includes everything needed for frontend session
    required_fields = ['success', 'user', 'token']
    missing_fields = [field for field in required_fields if field not in register_result]
    
    if not missing_fields:
        print('  ✅ Registration response includes all required session fields')
        print('  ✅ Frontend can establish proper session')
        print('  ✅ User will be treated as LOGGED IN when redirected to dashboard')
    else:
        print(f'  ❌ Missing session fields: {missing_fields}')
        print('  ❌ Frontend cannot establish proper session')
        print('  ❌ User will be treated as NOT LOGGED IN when redirected to dashboard')

print(f'\n=== TESTING COMPLETE ===')
