import sqlite3
import os

# Check if there are multiple database files
db_dir = 'server'
print(f'🔍 Checking database files in {db_dir}...')

for file in os.listdir(db_dir):
    if file.endswith('.db'):
        file_path = os.path.join(db_dir, file)
        print(f'Found database: {file_path}')
        
        # Check schema
        conn = sqlite3.connect(file_path)
        cursor = conn.cursor()
        cursor.execute('PRAGMA table_info(users)')
        columns = cursor.fetchall()
        print(f'  Columns: {[col[1] for col in columns]}')
        conn.close()
        print('---')
