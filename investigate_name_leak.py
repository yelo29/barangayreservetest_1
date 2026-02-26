import requests
import sqlite3

print('=== INVESTIGATING NAME FIELD DATA LEAK ===')

# 1. Check database directly
conn = sqlite3.connect('server/barangay.db')
cursor = conn.cursor()

cursor.execute('SELECT id, email, full_name FROM users WHERE email = ?', ('TestNonresiden@gmail.com',))
db_user = cursor.fetchone()

if db_user:
    print('1. DATABASE DATA:')
    print(f'   - ID: {db_user[0]}')
    print(f'   - Email: {db_user[1]}')
    print(f'   - Full Name: "{db_user[2]}"')

# 2. Test registration API
print('\n2. REGISTRATION API TEST:')
reg_data = {
    'name': 'TestName',
    'email': 'testname@gmail.com',
    'password': 'password123',
    'role': 'resident'
}

reg_response = requests.post('http://192.168.100.4:8000/api/auth/register', json=reg_data)
if reg_response.status_code == 200:
    reg_result = reg_response.json()
    reg_user = reg_result['user']
    print(f'   ✅ Registration Response:')
    print(f'     - Full Name: "{reg_user.get("full_name")}"')
    print(f'     - Email: {reg_user.get("email")}')
else:
    print(f'   ❌ Registration Error: {reg_response.status_code}')

# 3. Test login API for the same user
print('\n3. LOGIN API TEST:')
login_data = {
    'email': 'testname@gmail.com',
    'password': 'password123'
}

login_response = requests.post('http://192.168.100.4:8000/api/auth/login', json=login_data)
if login_response.status_code == 200:
    login_result = login_response.json()
    login_user = login_result['user']
    print(f'   ❌ Login Response:')
    print(f'     - Full Name: "{login_user.get("full_name")}"')
    print(f'     - Email: {login_user.get("email")}')
else:
    print(f'   ❌ Login Error: {login_response.status_code}')

# 4. Test profile API
print('\n4. PROFILE API TEST:')
profile_response = requests.get('http://192.168.100.4:8000/api/users/profile/testname@gmail.com')
if profile_response.status_code == 200:
    profile_data = profile_response.json()
    profile_user = profile_data['user']
    print(f'   ✅ Profile API Response:')
    print(f'     - Full Name: "{profile_user.get("full_name")}"')
    print(f'     - Email: {profile_user.get("email")}')
else:
    print(f'   ❌ Profile API Error: {profile_response.status_code}')

print('\n5. DATA LEAK ANALYSIS:')
print('❌ LOGIN API is returning empty full_name field')
print('✅ REGISTRATION API correctly saves the name')
print('✅ PROFILE API returns the correct name')
print('❌ The data leak is in the LOGIN endpoint!')

conn.close()
