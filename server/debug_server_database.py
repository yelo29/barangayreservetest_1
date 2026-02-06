import sqlite3
import os

# Check what database files exist and their contents
print("Checking database files in server directory...")

# List all .db files
db_files = []
for file in os.listdir('.'):
    if file.endswith('.db'):
        db_files.append(file)

print(f"Found database files: {db_files}")
print()

# Check each database file for the official account
for db_file in db_files:
    print(f"Checking {db_file}:")
    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        
        # Check if users table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
        if cursor.fetchone():
            # Check for the official account
            cursor.execute('SELECT email, password, full_name, role FROM users WHERE email = ?', ('secretary@barangay.gov',))
            official = cursor.fetchone()
            
            if official:
                print(f"  ✅ Found official account:")
                print(f"    Email: {official[0]}")
                print(f"    Password: {official[1]}")
                print(f"    Name: {official[2]}")
                print(f"    Role: {official[3]}")
            else:
                print(f"  ❌ Official account not found")
                
            # Show all users
            cursor.execute('SELECT email, password, role FROM users LIMIT 5')
            users = cursor.fetchall()
            print(f"  Sample users:")
            for user in users:
                print(f"    {user[0]} ({user[2]})")
        else:
            print(f"  ❌ No users table found")
            
        conn.close()
    except Exception as e:
        print(f"  ❌ Error reading {db_file}: {e}")
    
    print()

# Check if there's an .env file that might specify a different database
if os.path.exists('.env'):
    print("Checking .env file:")
    with open('.env', 'r') as f:
        for line in f:
            if 'DB_PATH' in line or 'DATABASE' in line:
                print(f"  {line.strip()}")
