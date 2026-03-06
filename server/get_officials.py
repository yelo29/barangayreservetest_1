import sqlite3

conn = sqlite3.connect('barangay.db')
cursor = conn.cursor()

# Get all official accounts
cursor.execute('SELECT email, full_name, password FROM users WHERE role = "official" OR verified = 2')
officials = cursor.fetchall()

print('🏛️ OFFICIAL ACCOUNTS:')
print('=' * 50)
for official in officials:
    print(f'📧 Email: {official[0]}')
    print(f'👤 Name: {official[1]}')
    print(f'🔑 Password: {official[2]}')
    print('-' * 30)

conn.close()
