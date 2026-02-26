import sqlite3
import os
import hashlib

# Check all users and their passwords
db_path = os.path.join('server', 'barangay.db')
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

print('🔍 Checking all users...')
cursor.execute('SELECT email, password FROM users')
users = cursor.fetchall()

for email, password_hash in users:
    print(f'Email: {email}')
    print(f'Password hash: {password_hash}')
    print('---')

# Try to find a user with password123
test_hash = hashlib.sha256('password123'.encode()).hexdigest()
print(f'Test hash for "password123": {test_hash}')

for email, password_hash in users:
    if password_hash == test_hash:
        print(f'✅ Found user with password123: {email}')
        break
else:
    print('❌ No user has password123')

conn.close()
