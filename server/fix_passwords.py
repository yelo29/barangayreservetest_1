#!/usr/bin/env python3
import sqlite3

conn = sqlite3.connect('barangay.db')
cursor = conn.cursor()

# Update test users to have plain text passwords for testing
test_users = [
    ('leo052904@gmail.com', 'zepol052904'),
    ('saloestillopez@gmail.com', 'salo3029'),
    ('resident@barangay.com', 'password123'),
    ('official@barangay.com', 'password123'),
    ('secretary@barangay.gov', 'barangay123')
]

for email, password in test_users:
    cursor.execute('UPDATE users SET password_hash = ? WHERE email = ?', (password, email))
    print(f'Updated password for {email}')

conn.commit()
conn.close()
print('All test passwords updated!')
