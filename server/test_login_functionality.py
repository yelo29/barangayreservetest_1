import sqlite3
import hashlib

def test_login(email, password):
    conn = sqlite3.connect('barangay.db')
    cursor = conn.cursor()
    
    try:
        # Hash the password
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        
        # Test login
        cursor.execute('SELECT id, email, full_name, role, verified FROM users WHERE email = ? AND password_hash = ?', (email, password_hash))
        user = cursor.fetchone()
        
        if user:
            print(f'✅ Login successful for {email}')
            print(f'   User ID: {user[0]}')
            print(f'   Name: {user[2]}')
            print(f'   Role: {user[3]}')
            print(f'   Verified: {user[4]}')
            return True
        else:
            print(f'❌ Login failed for {email}')
            return False
    finally:
        conn.close()

print('=== TESTING LOGIN FUNCTIONALITY ===')
test_accounts = [
    ('captain@barangay.gov', 'tatalaPunongBarangayadmin'),
    ('secretary@barangay.gov', 'tatalaSecretaryadmin'),
    ('administrator@barangay.gov', 'tatalaAdministratoradmin'),
]

for email, password in test_accounts:
    test_login(email, password)
    print()
