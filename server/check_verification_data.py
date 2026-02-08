import sqlite3

conn = sqlite3.connect('barangay.db')
cursor = conn.cursor()

print('🔍 Checking all users:')
cursor.execute('SELECT id, email, full_name FROM users LIMIT 5')
users = cursor.fetchall()
for user in users:
    print(f'ID: {user[0]}, Email: {user[1]}, Name: {user[2]}')

print('\n🔍 Checking verification_requests table:')
cursor.execute('SELECT COUNT(*) FROM verification_requests')
total = cursor.fetchone()[0]
print(f'Total requests: {total}')

if total > 0:
    cursor.execute('SELECT id, user_id, verification_type, status, created_at FROM verification_requests LIMIT 5')
    requests = cursor.fetchall()
    for req in requests:
        print(f'ID: {req[0]}, User: {req[1]}, Type: {req[2]}, Status: {req[3]}, Created: {req[4]}')
    
    print('\n🔍 Full verification request details:')
    cursor.execute('SELECT * FROM verification_requests LIMIT 1')
    request = cursor.fetchone()
    if request:
        columns = [description[0] for description in cursor.description]
        for i, col in enumerate(columns):
            print(f'{col}: {request[i]}')
else:
    print('No verification requests found')

conn.close()
