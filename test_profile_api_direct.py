import requests

print('=== TESTING PROFILE API DIRECTLY ===')

# Test profile API for unresident@gmail.com
response = requests.get('http://192.168.100.4:8000/api/users/profile/unresident@gmail.com')

print(f'Status Code: {response.status_code}')
if response.status_code == 200:
    data = response.json()
    user = data['user']
    print('Profile API Response:')
    print(f'  - Verified: {user.get("verified")} ({type(user.get("verified"))})')
    print(f'  - Verification Type: {user.get("verification_type")} ({type(user.get("verification_type"))})')
    print(f'  - Discount Rate: {user.get("discount_rate")} ({type(user.get("discount_rate"))})')
    
    # Check if verification_type is actually None or empty string
    vt = user.get('verification_type')
    if vt is None:
        print('  ❌ verification_type is None (NULL)')
    elif vt == '':
        print('  ❌ verification_type is empty string')
    elif vt == 'null':
        print('  ❌ verification_type is string "null"')
    else:
        print(f'  ✅ verification_type is: "{vt}"')
else:
    print(f'Error: {response.text}')

print('\n=== COMPARING WITH DATABASE ===')
import sqlite3

conn = sqlite3.connect('server/barangay.db')
cursor = conn.cursor()

cursor.execute('SELECT verification_type FROM users WHERE email = ?', ('unresident@gmail.com',))
db_result = cursor.fetchone()
conn.close()

if db_result:
    print(f'Database verification_type: "{db_result[0]}" ({type(db_result[0])})')
    
    if db_result[0] == 'non-resident':
        print('✅ Database has correct value')
    else:
        print(f'❌ Database has wrong value: {db_result[0]}')
else:
    print('❌ User not found in database')
