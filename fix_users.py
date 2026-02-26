import sqlite3

conn = sqlite3.connect('barangay.db')
cursor = conn.cursor()

# Check verification_requests table structure
cursor.execute('PRAGMA table_info(verification_requests)')
columns = cursor.fetchall()
print('Verification requests table structure:')
for col in columns:
    print(f'  - {col[1]} ({col[2]})')

# Check all verification requests
print('\n=== All Verification Requests ===')
try:
    cursor.execute('SELECT id, email, status, request_type, created_at FROM verification_requests ORDER BY created_at DESC LIMIT 10')
    requests = cursor.fetchall()
    for req in requests:
        print(f'Request: {req}')
except sqlite3.OperationalError as e:
    print(f'Error: {e}')

# Fix unresident@gmail.com - should be non-resident with proper verification
print('\n=== Fixing unresident@gmail.com ===')
cursor.execute('UPDATE users SET verification_type = ?, verified = 1, discount_rate = 0.05 WHERE email = ?', ('non-resident', 'unresident@gmail.com'))
conn.commit()

# Fix diddy@gmail.com - add full name and proper setup
print('\n=== Fixing diddy@gmail.com ===')
cursor.execute('UPDATE users SET full_name = ?, verification_type = ?, verified = 0, discount_rate = 0 WHERE email = ?', ('Diddy User', 'resident', 'diddy@gmail.com'))
conn.commit()

# Verify the fixes
print('\n=== Verification after fixes ===')
cursor.execute('SELECT id, email, full_name, verified, verification_type, discount_rate, is_banned FROM users WHERE email IN (?, ?)', ('unresident@gmail.com', 'diddy@gmail.com'))
users = cursor.fetchall()
for user in users:
    print(f'User: {user}')

conn.close()
