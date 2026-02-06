import sqlite3

conn = sqlite3.connect('barangay.db')
cursor = conn.cursor()

# Check if users table exists and its structure
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
table_exists = cursor.fetchone()
print(f'Users table exists: {table_exists}')

if table_exists:
    cursor.execute('PRAGMA table_info(users)')
    columns = cursor.fetchall()
    print('Users table structure:')
    for col in columns:
        print(f'  - {col[1]} ({col[2]})')
else:
    print('Users table does not exist!')

conn.close()
