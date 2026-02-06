import sqlite3

# Check the official account in the database
conn = sqlite3.connect('barangay.db')
cursor = conn.cursor()

# Check if secretary@barangay.gov exists
cursor.execute('SELECT * FROM users WHERE email = ?', ('secretary@barangay.gov',))
official = cursor.fetchone()

print('Checking official account: secretary@barangay.gov')
print('=' * 50)

if official:
    columns = [description[0] for description in cursor.description]
    print('Official account found:')
    for i, col in enumerate(columns):
        print(f'  {col}: {official[i]}')
else:
    print('Official account NOT found in database')

print('\n' + '=' * 50)

# Check all users to see what accounts exist
cursor.execute('SELECT id, email, full_name, role, verified FROM users')
users = cursor.fetchall()

print('All users in database:')
for user in users:
    print(f'  ID: {user[0]}, Email: {user[1]}, Name: {user[2]}, Role: {user[3]}, Verified: {user[4]}')

print('\n' + '=' * 50)

# Check if we need to create the official account
if not official:
    print('Creating official account...')
    cursor.execute('''
        INSERT INTO users (email, password, full_name, role, verified, discount_rate)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', ('secretary@barangay.gov', 'admin123', 'Barangay Secretary', 'official', True, 0.0))
    
    conn.commit()
    print('Official account created successfully!')
    
    # Verify creation
    cursor.execute('SELECT * FROM users WHERE email = ?', ('secretary@barangay.gov',))
    official = cursor.fetchone()
    
    if official:
        columns = [description[0] for description in cursor.description]
        print('New official account:')
        for i, col in enumerate(columns):
            print(f'  {col}: {official[i]}')

conn.close()
