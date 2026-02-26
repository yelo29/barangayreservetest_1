import sqlite3
import requests

print('=== INVESTIGATING DATA LEAK FOR kuyawill@gmail.com ===')

# 1. Check database directly
conn = sqlite3.connect('barangay.db')
cursor = conn.cursor()

cursor.execute('SELECT id, email, verified, verification_type, discount_rate, full_name FROM users WHERE email = ?', ('kuyawill@gmail.com',))
db_user = cursor.fetchone()

if db_user:
    print('1. DATABASE DATA:')
    print(f'   - ID: {db_user[0]}')
    print(f'   - Email: {db_user[1]}')
    print(f'   - Verified: {db_user[2]}')
    print(f'   - Verification Type: {db_user[3]}')
    print(f'   - Discount Rate: {db_user[4]}')
    print(f'   - Full Name: "{db_user[5]}"')

# 2. Check API response
print('\n2. API RESPONSE:')
profile_response = requests.get('http://192.168.100.4:8000/api/users/profile/kuyawill@gmail.com')
if profile_response.status_code == 200:
    api_data = profile_response.json()
    api_user = api_data['user']
    print(f'   - Verified: {api_user.get("verified")}')
    print(f'   - Verification Type: {api_user.get("verification_type")}')
    print(f'   - Discount Rate: {api_user.get("discount_rate")}')
    print(f'   - Full Name: "{api_user.get("full_name")}"')
else:
    print(f'   - API Error: {profile_response.status_code}')

# 3. Check verification requests for this user
print('\n3. VERIFICATION REQUESTS:')
cursor.execute('SELECT id, user_email, status, request_type, reviewed_at FROM verification_requests WHERE user_email = ?', ('kuyawill@gmail.com',))
requests = cursor.fetchall()
if requests:
    for req in requests:
        print(f'   - Request ID: {req[0]}, Status: {req[2]}, Type: {req[3]}, Reviewed: {req[4]}')
else:
    print('   - No verification requests found')

# 4. Check for data inconsistencies
print('\n4. DATA CONSISTENCY CHECK:')
if db_user:
    db_verified = bool(db_user[2])
    db_type = db_user[3]
    db_discount = db_user[4]
    
    # Check if there's a mismatch between database and what the frontend should see
    is_verified_resident = db_verified and db_type == 'resident' and db_discount == 0.1
    is_verified_non_resident = db_verified and db_type == 'non-resident' and db_discount == 0.05
    
    print(f'   - Database Classification:')
    print(f'     * is_verified_resident: {is_verified_resident}')
    print(f'     * is_verified_non_resident: {is_verified_non_resident}')
    
    if not db_verified and db_type is None and db_discount == 0:
        print(f'   - ✅ Database correctly shows UNVERIFIED USER')
    else:
        print(f'   - ❌ Database shows unexpected state')

conn.close()

# 5. Test login to see what session data is returned
print('\n5. LOGIN SESSION DATA:')
login_data = {
    'email': 'kuyawill@gmail.com',
    'password': 'password123'  # Try common password
}

login_response = requests.post('http://192.168.100.4:8000/api/auth/login', json=login_data)
if login_response.status_code == 200:
    login_result = login_response.json()
    login_user = login_result['user']
    print(f'   - Login Verified: {login_user.get("verified")}')
    print(f'   - Login Verification Type: {login_user.get("verification_type")}')
    print(f'   - Login Discount Rate: {login_user.get("discount_rate")}')
    print(f'   - Token Provided: {"Yes" if login_result.get("token") else "No"}')
else:
    # Try to find the correct password
    print(f'   - Login failed, trying to find correct password...')
    # Check if this user was recently registered and needs password setup
