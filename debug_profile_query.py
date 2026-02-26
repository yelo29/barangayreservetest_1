import sqlite3
import os

# Debug the profile endpoint query step by step
db_path = os.path.join('server', 'barangay.db')
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

print('🔍 DEBUGGING PROFILE ENDPOINT QUERY')
print('=' * 50)

# Test the exact query from the profile endpoint
query = '''
            SELECT id, email, full_name, role, verified, verification_type, discount_rate, contact_number, address, profile_photo_url, created_at, fake_booking_violations, is_banned, banned_at, ban_reason
            FROM users 
            WHERE email = ?
        '''

email = 'residentresident@gmail.com'
print(f'Query: {query}')
print(f'Email: {email}')

cursor.execute(query, (email,))
user = cursor.fetchone()

if user:
    print(f'✅ Query successful!')
    print(f'Raw result: {user}')
    print(f'Number of columns: {len(user)}')
    
    # Map fields like the endpoint does
    field_mapping = {
        'id': user[0],
        'email': user[1],
        'full_name': user[2],
        'role': user[3],
        'verified': user[4],
        'verification_type': user[5],
        'discount_rate': user[6],
        'contact_number': user[7],
        'address': user[8],
        'profile_photo_url': user[9],
        'created_at': user[10],
        'fake_booking_violations': user[11] if len(user) > 11 else 0,
        'is_banned': user[12] if len(user) > 12 else False,
        'banned_at': user[13] if len(user) > 13 else None,
        'ban_reason': user[14] if len(user) > 14 else None
    }
    
    print(f'✅ Field mapping:')
    for key, value in field_mapping.items():
        print(f'  - {key}: {value}')
        
    # Check specific fields
    print(f'\n🔍 KEY FIELDS:')
    print(f'  - Verified: {field_mapping["verified"]} (type: {type(field_mapping["verified"])})')
    print(f'  - Discount Rate: {field_mapping["discount_rate"]} (type: {type(field_mapping["discount_rate"])})')
    print(f'  - Verification Type: {field_mapping["verification_type"]} (type: {type(field_mapping["verification_type"])})')
else:
    print('❌ Query failed or user not found')

conn.close()
