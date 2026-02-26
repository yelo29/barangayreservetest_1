import sqlite3
import hashlib

conn = sqlite3.connect('barangay.db')
cursor = conn.cursor()

# Fix password for unresident@gmail.com
new_password = 'password123'
password_hash = hashlib.sha256(new_password.encode()).hexdigest()

cursor.execute('UPDATE users SET password = ? WHERE email = ?', (password_hash, 'unresident@gmail.com'))
conn.commit()

print(f'Updated password for unresident@gmail.com to: {new_password}')
print(f'New hash: {password_hash}')

# Verify the update
cursor.execute('SELECT email, password FROM users WHERE email = ?', ('unresident@gmail.com',))
user = cursor.fetchone()
print(f'Verified: {user[0]} - {user[1]}')

conn.close()
