import sqlite3
import hashlib

# Connect to database
conn = sqlite3.connect('barangay.db')
cursor = conn.cursor()

# Get the stored hash
cursor.execute("SELECT password_hash FROM users WHERE email = ?", ('resident01@gmail.com',))
result = cursor.fetchone()

if result:
    stored_hash = result[0]
    print(f"Stored hash: {stored_hash}")
    
    # Try common password patterns based on the user's name "resident One"
    test_passwords = [
        "resident01",  # What user is trying
        "resident",    # Common
        "resident1",   # Common variation
        "residentone", # Name without space
        "Resident01",  # Capitalized
        "Resident",    # Capitalized
        "password",    # Default
        "123456",      # Default
        "resident01@gmail.com",  # Email as password
        "res1",        # Short version of name
        "resident One", # Full name
    ]
    
    print("\nTesting possible passwords:")
    for pwd in test_passwords:
        pwd_hash = hashlib.sha256(pwd.encode()).hexdigest()
        match = pwd_hash == stored_hash
        if match:
            print(f"✅ FOUND MATCH: '{pwd}'")
        else:
            print(f"❌ '{pwd}': no match")
else:
    print("User not found")

conn.close()
