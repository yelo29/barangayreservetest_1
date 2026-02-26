import sqlite3
import os

# Check residentresident@gmail.com status
db_path = os.path.join('server', 'barangay.db')
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

print('🔍 ANALYZING residentresident@gmail.com DATA LEAK')
print('=' * 60)

# Get user details
cursor.execute('SELECT id, email, verified, discount_rate, verification_type FROM users WHERE email = ?', ('residentresident@gmail.com',))
user = cursor.fetchone()

if user:
    user_id, email, verified, discount_rate, verification_type = user
    print(f'📋 USER DETAILS:')
    print(f'  - User ID: {user_id}')
    print(f'  - Email: {email}')
    print(f'  - Verified: {verified} (1=verified, 0=unverified)')
    print(f'  - Discount Rate: {discount_rate}')
    print(f'  - Verification Type: {verification_type}')
    
    print(f'\n🔍 ANALYSIS:')
    if verified == 1:
        print(f'✅ User is VERIFIED')
        if discount_rate == 0.10:
            print(f'✅ Correct discount rate: 10% (verified resident)')
        elif discount_rate == 0.05:
            print(f'❌ WRONG discount rate: 5% (should be 10% for verified resident)')
        else:
            print(f'❌ UNKNOWN discount rate: {discount_rate}')
    else:
        print(f'❌ User is NOT verified')
        if discount_rate == 0.05:
            print(f'✅ Correct discount rate: 5% (non-resident/unverified)')
        elif discount_rate == 0.10:
            print(f'❌ WRONG discount rate: 10% (should be 5% for unverified)')
        else:
            print(f'❌ UNKNOWN discount rate: {discount_rate}')
    
    # Check verification requests
    print(f'\n🔍 CHECKING VERIFICATION REQUESTS:')
    cursor.execute('SELECT id, status, created_at FROM verification_requests WHERE user_id = ?', (user_id,))
    requests = cursor.fetchall()
    
    if requests:
        print(f'Found {len(requests)} verification requests:')
        for req in requests:
            print(f'  - Request ID: {req[0]}, Status: {req[1]}, Created: {req[2]}')
    else:
        print('No verification requests found')
    
    # Check what the API returns
    print(f'\n🔍 TESTING API RESPONSE:')
    import requests
    
    try:
        base_url = 'http://192.168.100.4:8000'
        response = requests.get(f'{base_url}/api/users/profile/{email}', timeout=5)
        
        if response.status_code == 200:
            profile_data = response.json()
            print(f'✅ Profile API Response:')
            print(f'  - Verified: {profile_data.get("verified")}')
            print(f'  - Discount Rate: {profile_data.get("discount_rate")}')
            print(f'  - Verification Type: {profile_data.get("verification_type")}')
            
            # Check if there's a mismatch
            api_verified = profile_data.get("verified")
            api_discount = profile_data.get("discount_rate")
            
            if api_verified != verified:
                print(f'❌ DATA LEAK: API verified ({api_verified}) != DB verified ({verified})')
            if api_discount != discount_rate:
                print(f'❌ DATA LEAK: API discount ({api_discount}) != DB discount ({discount_rate})')
        else:
            print(f'❌ Profile API failed: {response.status_code}')
    except Exception as e:
        print(f'❌ API test error: {e}')

else:
    print('❌ User residentresident@gmail.com not found')

conn.close()
print('\n🎯 ANALYSIS COMPLETED')
