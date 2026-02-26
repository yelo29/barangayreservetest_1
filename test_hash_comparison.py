import sqlite3
import os
import hashlib

db_path = os.path.join('server', 'barangay.db')
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Test the exact same logic as server
test_password = 'password123'
test_hash = hashlib.sha256(test_password.encode()).hexdigest()

print(f'🔍 Test password: {test_password}')
print(f'🔍 Test hash: {test_hash}')

# Get stored hash for unresident@gmail.com
cursor.execute('SELECT password_hash FROM users WHERE email = ?', ('unresident@gmail.com',))
result = cursor.fetchone()
stored_hash = result[0] if result else None

print(f'🔍 Stored hash: {stored_hash}')
print(f'🔍 Hashes match: {test_hash == stored_hash}')

conn.close()
