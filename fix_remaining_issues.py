import sqlite3
import hashlib

conn = sqlite3.connect('barangay.db')
cursor = conn.cursor()

# Fix residentresident@gmail.com password
email = 'residentresident@gmail.com'
new_password = 'password123'
password_hash = hashlib.sha256(new_password.encode()).hexdigest()

cursor.execute('UPDATE users SET password = ? WHERE email = ?', (password_hash, email))
conn.commit()

print(f'✅ Updated password for {email} to: {new_password}')

# Verify all test users
print('\n=== VERIFICATION OF ALL TEST USERS ===')
test_emails = ['unresident@gmail.com', 'residentresident@gmail.com', 'diddy@gmail.com']

for email in test_emails:
    cursor.execute('SELECT email, verified, verification_type, discount_rate FROM users WHERE email = ?', (email,))
    user = cursor.fetchone()
    if user:
        print(f'{user[0]}:')
        print(f'  - Verified: {user[1]}')
        print(f'  - Verification Type: {user[2]}')
        print(f'  - Discount Rate: {user[3]}')
        
        # Clarify the logic
        verified = bool(user[1])
        verification_type = user[2]
        discount_rate = user[3]
        
        if verified and verification_type == 'resident' and discount_rate == 0.1:
            classification = 'VERIFIED RESIDENT'
        elif verified and verification_type == 'non-resident' and discount_rate == 0.05:
            classification = 'VERIFIED NON-RESIDENT'
        elif not verified:
            classification = 'UNVERIFIED USER'
        else:
            classification = 'UNKNOWN STATE'
            
        print(f'  - Classification: {classification}')
        print()

conn.close()
