import sqlite3

conn = sqlite3.connect('barangay.db')
cursor = conn.cursor()

# Check if there's a uid field in the users table
cursor.execute('PRAGMA table_info(users)')
columns = cursor.fetchall()

print('Users table structure:')
for col in columns:
    print(f'  {col[1]} ({col[2]})')

print('\n' + '='*50 + '\n')

# Check all users to see if any have uid fields
cursor.execute('SELECT * FROM users LIMIT 5')
users = cursor.fetchall()

print('Sample users:')
for user in users:
    print(f'  ID: {user[0]}, Email: {user[1]}, Name: {user[3]}')

print('\n' + '='*50 + '\n')

# Check if there's a mapping between Firebase UIDs and database IDs
cursor.execute('SELECT * FROM users WHERE email = "saloestillopez@gmail.com"')
user = cursor.fetchone()

if user:
    print('Salo Estil Lopez user data:')
    columns = [description[0] for description in cursor.description]
    for i, col in enumerate(columns):
        print(f'  {col}: {user[i]}')

conn.close()
