import requests

# Test the complete flow for unresident@gmail.com
print('=== Testing unresident@gmail.com complete flow ===')

# 1. Test login
login_data = {
    'email': 'unresident@gmail.com',
    'password': 'leo3029'
}

response = requests.post('http://192.168.100.4:8000/api/auth/login', json=login_data)
print(f'1. Login Status: {response.status_code}')
if response.status_code == 200:
    login_result = response.json()
    user = login_result['user']
    print(f'   - Verified: {user.get("verified")}')
    print(f'   - Verification Type: {user.get("verification_type")}')
    print(f'   - Discount Rate: {user.get("discount_rate")}')
    print(f'   - Role: {user.get("role")}')
    
    # 2. Test profile API
    profile_response = requests.get('http://192.168.100.4:8000/api/users/profile/unresident@gmail.com')
    if profile_response.status_code == 200:
        profile_data = profile_response.json()
        profile_user = profile_data['user']
        print(f'2. Profile API:')
        print(f'   - Verified: {profile_user.get("verified")}')
        print(f'   - Verification Type: {profile_user.get("verification_type")}')
        print(f'   - Discount Rate: {profile_user.get("discount_rate")}')
    else:
        print(f'2. Profile API Error: {profile_response.status_code}')
        
    # 3. Test frontend logic simulation
    print(f'3. Frontend Logic Simulation:')
    verified = user.get('verified', False)
    verification_type = user.get('verification_type')
    discount_rate = user.get('discount_rate', 0)
    
    # This is how frontend determines resident vs non-resident
    is_verified_resident = verified and verification_type == 'resident' and discount_rate == 0.1
    is_verified_non_resident = verified and verification_type == 'non-resident' and discount_rate == 0.05
    
    print(f'   - is_verified_resident: {is_verified_resident}')
    print(f'   - is_verified_non_resident: {is_verified_non_resident}')
    
    if is_verified_resident:
        print('   ❌ DATA LEAK: Being treated as VERIFIED RESIDENT')
    elif is_verified_non_resident:
        print('   ✅ CORRECT: Being treated as VERIFIED NON-RESIDENT')
    else:
        print('   ⚠️  Being treated as UNVERIFIED')
else:
    print(f'Login failed: {response.json()}')

# 4. Check database directly
print(f'\n4. Database Check:')
import sqlite3
conn = sqlite3.connect('barangay.db')
cursor = conn.cursor()
cursor.execute('SELECT verified, verification_type, discount_rate FROM users WHERE email = ?', ('unresident@gmail.com',))
db_result = cursor.fetchone()
if db_result:
    print(f'   - DB Verified: {db_result[0]}')
    print(f'   - DB Verification Type: {db_result[1]}')
    print(f'   - DB Discount Rate: {db_result[2]}')
conn.close()
