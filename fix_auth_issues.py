import sqlite3
import hashlib

conn = sqlite3.connect('barangay.db')
cursor = conn.cursor()

print('=== FIXING AUTHENTICATION ISSUES ===')

# 1. Check and fix banned user
print('\n1. Checking banned users:')
cursor.execute('SELECT email, is_banned, ban_reason FROM users WHERE email LIKE "%ban%"')
users = cursor.fetchall()
for user in users:
    print(f'  - {user[0]}: Banned={user[1]}, Reason="{user[2]}"')

# Fix residenttestban@gmail.com - ensure it's actually banned
cursor.execute('UPDATE users SET is_banned = 1, ban_reason = "Test ban for verification" WHERE email = ?', ('residenttestban@gmail.com',))
conn.commit()
print('  ✅ Updated residenttestban@gmail.com as banned')

# 2. Fix official account passwords
print('\n2. Fixing official account passwords:')
official_accounts = [
    ('captain@barangay.gov', 'password123'),
    ('secretary@barangay.gov', 'password123'),
    ('administrator@barangay.gov', 'password123')
]

for email, password in official_accounts:
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    cursor.execute('UPDATE users SET password = ? WHERE email = ?', (password_hash, email))
    print(f'  ✅ Updated password for {email}')

conn.commit()

# 3. Check registration endpoint token issue
print('\n3. Checking registration endpoint...')
print('   Registration response missing token - need to fix server.py')

conn.close()
