import sqlite3

conn = sqlite3.connect('barangay.db')
cursor = conn.cursor()

# Check secretary account
cursor.execute('SELECT id, email, verified, verification_type, role FROM users WHERE email = "secretary@barangay.gov"')
result = cursor.fetchone()
print('Secretary account:', result)

# Check all officials
cursor.execute('SELECT email, verified, verification_type, role FROM users WHERE role = "official"')
officials = cursor.fetchall()
print('\nAll officials:')
for official in officials:
    print(f'  {official[0]} - verified: {official[1]}, type: {official[2]}, role: {official[3]}')

conn.close()
