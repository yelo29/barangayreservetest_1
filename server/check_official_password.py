import sqlite3

def check_official_password():
    """Check official password in database"""
    
    conn = sqlite3.connect('barangay.db')
    cursor = conn.cursor()
    
    print("=== CHECKING OFFICIAL PASSWORD ===")
    
    cursor.execute('''
        SELECT email, password FROM users 
        WHERE email = 'captain@barangay.gov'
    ''')
    
    user = cursor.fetchone()
    if user:
        email, password = user
        print(f"📧 Email: {email}")
        print(f"🔐 Password: {password}")
    else:
        print("❌ Official not found")
    
    conn.close()

if __name__ == "__main__":
    check_official_password()
