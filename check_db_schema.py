import sqlite3
import os

db_path = os.path.join('server', 'barangay.db')
conn = sqlite3.connect(db_path)
cursor = conn.cursor()
cursor.execute('PRAGMA table_info(users)')
columns = cursor.fetchall()
print('📋 Users table columns:')
for col in columns:
    print(f'  - {col[1]} ({col[2]})')
conn.close()
