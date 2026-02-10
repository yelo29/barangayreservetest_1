import sqlite3

def check_resident_password():
    """Check the password for leo052904@gmail.com"""
    
    conn = sqlite3.connect('barangay.db')
    cursor = conn.cursor()
    
    print("=== CHECKING RESIDENT PASSWORD ===")
    
    cursor.execute('''
        SELECT email, password_hash FROM users WHERE email = 'leo052904@gmail.com'
    ''')
    
    user = cursor.fetchone()
    if user:
        email, password_hash = user
        print(f"Email: {email}")
        print(f"Password hash: {password_hash}")
        print("Try using: 'password123' or 'leo123' or '123456'")
    else:
        print("User not found")
    
    conn.close()

if __name__ == "__main__":
    check_resident_password()
