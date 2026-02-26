import sqlite3
import os

# Test direct database query
db_path = os.path.join('server', 'barangay.db')
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

print('🔍 Testing direct database query...')
try:
    cursor.execute('SELECT id, email, password FROM users WHERE email = ?', ('unresident@gmail.com',))
    result = cursor.fetchone()
    if result:
        print(f'✅ Query successful: {result}')
    else:
        print('❌ User not found')
except Exception as e:
    print(f'❌ Query failed: {e}')

conn.close()
