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

# 3. Check verification requests table structure first
print('\n3. VERIFICATION REQUESTS TABLE STRUCTURE:')
cursor.execute('PRAGMA table_info(verification_requests)')
columns = cursor.fetchall()
for col in columns:
    print(f'   - {col[1]} ({col[2]})')

# 4. Check verification requests for this user
print('\n4. VERIFICATION REQUESTS:')
# Find the user_id first
cursor.execute('SELECT id FROM users WHERE email = ?', ('kuyawill@gmail.com',))
user_id_result = cursor.fetchone()
if user_id_result:
    user_id = user_id_result[0]
    cursor.execute('SELECT id, status, request_type, reviewed_at FROM verification_requests WHERE user_id = ?', (user_id,))
    requests = cursor.fetchall()
    if requests:
        for req in requests:
            print(f'   - Request ID: {req[0]}, Status: {req[1]}, Type: {req[2]}, Reviewed: {req[3]}')
    else:
        print('   - No verification requests found')

# 5. Check for data inconsistencies
print('\n5. DATA CONSISTENCY CHECK:')
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

# 6. THE CRITICAL ISSUE: Frontend Verification Form Logic
print('\n6. CRITICAL ISSUE - VERIFICATION FORM LOGIC:')
print('   From logs: "You are already verified as a Resident with full benefits"')
print('   But API shows: verified=0, verification_type=null')
print('   This indicates FRONTEND VERIFICATION FORM is reading WRONG DATA!')

# 7. Check if there's cached data or different endpoint being used
print('\n7. POSSIBLE CAUSES:')
print('   - Frontend verification form using different API endpoint')
print('   - Cached data in Flutter app')
print('   - Different data source in verification form logic')
print('   - Race condition in data loading')

conn.close()

# 8. Check verification status endpoint (if it exists)
print('\n8. TESTING VERIFICATION STATUS ENDPOINT:')
try:
    verification_response = requests.get('http://192.168.100.4:8000/api/verification-status/kuyawill@gmail.com')
    if verification_response.status_code == 200:
        verification_data = verification_response.json()
        print(f'   - Verification Status API: {verification_data}')
    else:
        print(f'   - Verification Status API: {verification_response.status_code}')
except:
    print('   - Verification status endpoint not available')
