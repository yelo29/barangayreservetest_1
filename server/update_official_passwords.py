import sqlite3
import hashlib

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

conn = sqlite3.connect('barangay.db')
cursor = conn.cursor()

# Update passwords for specified official accounts
officials_to_update = [
    ('secretary@barangay.gov', 'tatala[secretary]admin'),
    ('administrator@barangay.gov', 'tatala[administrator]admin'),
    ('kagawad1@barangay.gov', 'tatala[kagawad1]admin'),
    ('planning@barangay.gov', 'tatala[planning]admin'),
    ('utility@barangay.gov', 'tatala[utility]admin')
]

print('🔑 Updating Official Account Passwords:')
print('=' * 50)

for email, new_password in officials_to_update:
    hashed_password = hash_password(new_password)
    
    # Update password
    cursor.execute('UPDATE users SET password = ? WHERE email = ?', (hashed_password, email))
    
    # Verify update
    cursor.execute('SELECT full_name FROM users WHERE email = ?', (email,))
    name = cursor.fetchone()[0]
    
    print(f'✅ Updated: {email}')
    print(f'   Name: {name}')
    print(f'   New Password: {new_password}')
    print(f'   Hashed: {hashed_password[:20]}...')
    print('-' * 30)

conn.commit()
conn.close()

print('🎉 All official account passwords updated successfully!')
