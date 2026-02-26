import sqlite3
import hashlib

conn = sqlite3.connect('barangay.db')
cursor = conn.cursor()

# Fix unresident@gmail.com - set as non-resident and update password to leo3029
email = 'unresident@gmail.com'
new_password = 'leo3029'
password_hash = hashlib.sha256(new_password.encode()).hexdigest()

print(f'=== Fixing {email} ===')
print(f'New password: {new_password}')
print(f'Password hash: {password_hash}')

# Update user data
cursor.execute('''
    UPDATE users 
    SET verification_type = ?, 
        verified = 1, 
        discount_rate = 0.05,
        password = ?,
        role = 'resident'  -- Keep role as resident since non-resident is a verification type, not a role
    WHERE email = ?
''', ('non-resident', password_hash, email))

conn.commit()

# Verify the changes
cursor.execute('SELECT id, email, full_name, verified, verification_type, discount_rate, role FROM users WHERE email = ?', (email,))
user = cursor.fetchone()

if user:
    print(f'\n✅ Updated successfully:')
    print(f'  ID: {user[0]}')
    print(f'  Email: {user[1]}')
    print(f'  Name: {user[2]}')
    print(f'  Verified: {user[3]}')
    print(f'  Verification Type: {user[4]}')
    print(f'  Discount Rate: {user[5]}')
    print(f'  Role: {user[6]}')
else:
    print('❌ User not found')

conn.close()
