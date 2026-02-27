#!/usr/bin/env python3
import sqlite3

conn = sqlite3.connect('server/barangay.db')
cursor = conn.cursor()
cursor.execute('SELECT id, email, full_name, role FROM users WHERE role = "resident" LIMIT 5')
users = cursor.fetchall()
print('Resident users in database:')
for user in users:
    print(f'  ID: {user[0]}, Email: {user[1]}, Name: {user[2]}, Role: {user[3]}')
conn.close()
