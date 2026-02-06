import sqlite3

# Update the official account password to something simple
conn = sqlite3.connect('barangay.db')
cursor = conn.cursor()

# Update secretary@barangay.gov password to 'admin123'
cursor.execute('''
    UPDATE users 
    SET password = ?
    WHERE email = ?
''', ('admin123', 'secretary@barangay.gov'))

conn.commit()

# Verify the update
cursor.execute('SELECT email, password, full_name, role FROM users WHERE email = ?', ('secretary@barangay.gov',))
official = cursor.fetchone()

if official:
    print('Updated official account:')
    print(f'  Email: {official[0]}')
    print(f'  Password: {official[1]}')
    print(f'  Name: {official[2]}')
    print(f'  Role: {official[3]}')
    print(f'\n✅ Password updated to: admin123')
else:
    print('❌ Official account not found')

conn.close()
