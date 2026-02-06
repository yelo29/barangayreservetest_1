import sqlite3

conn = sqlite3.connect('barangay.db')
cursor = conn.cursor()

# Check all tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()
print('Tables in database:')
for table in tables:
    print(f'- {table[0]}')

print('\n' + '='*50 + '\n')

# Check verification_requests table structure
cursor.execute("PRAGMA table_info(verification_requests)")
columns = cursor.fetchall()
print('verification_requests table structure:')
for col in columns:
    print(f'- {col[1]} ({col[2]})')

print('\n' + '='*50 + '\n')

# Check users table structure  
cursor.execute("PRAGMA table_info(users)")
columns = cursor.fetchall()
print('users table structure:')
for col in columns:
    print(f'- {col[1]} ({col[2]})')

conn.close()
