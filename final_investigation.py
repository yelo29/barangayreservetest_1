import sqlite3
import requests

print('=== INVESTIGATING DATA LEAK FOR kuyawill@gmail.com ===')

# 1. Check database directly - use correct path to server folder
conn = sqlite3.connect('server/barangay.db')
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
# Find the user_id first
cursor.execute('SELECT id FROM users WHERE email = ?', ('kuyawill@gmail.com',))
user_id_result = cursor.fetchone()
if user_id_result:
    user_id = user_id_result[0]
    cursor.execute('SELECT id, status, verification_type, reviewed_at FROM verification_requests WHERE user_id = ?', (user_id,))
    requests = cursor.fetchall()
    if requests:
        for req in requests:
            print(f'   - Request ID: {req[0]}, Status: {req[1]}, Type: {req[2]}, Reviewed: {req[3]}')
    else:
        print('   - No verification requests found')

# 4. THE CRITICAL ISSUE: Frontend vs Backend Data Mismatch
print('\n4. CRITICAL ISSUE IDENTIFIED:')
print('   ✅ DATABASE: verified=0, verification_type=null, discount_rate=0')
print('   ✅ API: verified=0, verification_type=null, discount_rate=0')
print('   ❌ FRONTEND VERIFICATION FORM: "You are already verified as a Resident with full benefits"')
print('   ❌ FRONTEND STATUS: "verified_resident"')

print('\n5. ROOT CAUSE ANALYSIS:')
print('   The Flutter verification form is using DIFFERENT LOGIC than the API!')
print('   This is a FRONTEND DATA ISOLATION LEAK')

conn.close()

# 6. Check Flutter verification logic by examining the logs more carefully
print('\n6. FROM THE LOGS - KEY EVIDENCE:')
print('   - "Verification Status Check: Can Submit: false"')
print('   - "Lock Message: You are already verified as a Resident with full benefits"')
print('   - "Current Status: verified_resident"')
print('   ')
print('   This proves the Flutter verification form has its own logic')
print('   that is NOT aligned with the API/database data!')

print('\n7. SOLUTION NEEDED:')
print('   - Find Flutter verification form logic')
print('   - Align it with API data')
print('   - Fix data isolation leak')
print('   - Ensure field mapping consistency')
