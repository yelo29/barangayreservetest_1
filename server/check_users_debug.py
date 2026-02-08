import sqlite3

conn = sqlite3.connect('barangay.db')
cursor = conn.cursor()

print('=== ALL USERS IN DATABASE ===')
cursor.execute('SELECT id, email, full_name, role, verified FROM users ORDER BY id')
users = cursor.fetchall()

for user in users:
    print(f'ID: {user[0]}, Email: {user[1]}, Name: {user[2]}, Role: {user[3]}, Verified: {user[4]}')

print('\n=== OFFICIAL USERS ===')
cursor.execute('SELECT id, email, full_name, role FROM users WHERE role = "official"')
officials = cursor.fetchall()

for official in officials:
    print(f'ID: {official[0]}, Email: {official[1]}, Name: {official[2]}')

conn.close()
