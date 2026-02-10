import sqlite3
import hashlib

def check_captain_password():
    """Check captain's actual password hash"""
    
    conn = sqlite3.connect('barangay.db')
    cursor = conn.cursor()
    
    print("=== CHECKING CAPTAIN PASSWORD ===")
    
    cursor.execute('''
        SELECT email, password_hash FROM users 
        WHERE email = 'captain@barangay.gov'
    ''')
    
    user = cursor.fetchone()
    if user:
        email, password_hash = user
        print(f"📧 Email: {email}")
        print(f"🔐 Stored Hash: {password_hash}")
        
        # Test common passwords
        test_passwords = ["admin123", "captain123", "password", "123456"]
        
        for test_pwd in test_passwords:
            test_hash = hashlib.sha256(test_pwd.encode()).hexdigest()
            print(f"🧪 Testing '{test_pwd}': {test_hash}")
            if test_hash == password_hash:
                print(f"✅ MATCH FOUND: '{test_pwd}'")
                return test_pwd
        
        print("❌ No common passwords matched")
    else:
        print("❌ Captain not found")
    
    conn.close()

if __name__ == "__main__":
    check_captain_password()
