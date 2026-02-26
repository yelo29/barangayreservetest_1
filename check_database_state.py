import sqlite3

print('=== CHECKING DATABASE FOR UNRESIDENT ===')

conn = sqlite3.connect('server/barangay.db')
cursor = conn.cursor()

# Check unresident@gmail.com in database
cursor.execute('SELECT id, email, verified, verification_type, discount_rate, full_name FROM users WHERE email = ?', ('unresident@gmail.com',))
user = cursor.fetchone()

if user:
    print('DATABASE DATA:')
    print(f'   - ID: {user[0]}')
    print(f'   - Email: {user[1]}')
    print(f'   - Verified: {user[2]}')
    print(f'   - Verification Type: {user[3]}')
    print(f'   - Discount Rate: {user[4]}')
    print(f'   - Full Name: "{user[5]}"')
    
    # Check what the database actually contains
    db_verified = bool(user[2])
    db_type = user[3]
    db_discount = user[4]
    
    print(f'\nDATABASE ANALYSIS:')
    print(f'   - Raw verified value: {user[2]} ({type(user[2])})')
    print(f'   - Raw verification_type value: {user[3]} ({type(user[3])})')
    print(f'   - Raw discount_rate value: {user[4]} ({type(user[4])})')
    
    print(f'\nCLASSIFICATION:')
    if db_verified and db_type == 'non-resident' and db_discount == 0.05:
        print('✅ DATABASE: VERIFIED NON-RESIDENT (CORRECT)')
    elif db_verified and db_type == 'resident' and db_discount == 0.1:
        print('❌ DATABASE: VERIFIED RESIDENT (INCORRECT)')
    elif not db_verified and db_type is None and db_discount == 0:
        print('✅ DATABASE: UNVERIFIED (CORRECT)')
    else:
        print(f'❌ DATABASE: UNEXPECTED STATE')

# Check verification requests for this user
print(f'\nVERIFICATION REQUESTS:')
cursor.execute('SELECT id, status, verification_type, reviewed_at FROM verification_requests WHERE user_id = ?', (user[0],))
requests = cursor.fetchall()
if requests:
    for req in requests:
        print(f'   - Request ID: {req[0]}, Status: {req[1]}, Type: {req[2]}, Reviewed: {req[3]}')
else:
    print('   - No verification requests found')

conn.close()

print(f'\nDATA LEAK ROOT CAUSE:')
print('The verification status endpoint is using WRONG LOGIC!')
print('It should check verification_type = "non-resident" but it only checks verified = 1')
