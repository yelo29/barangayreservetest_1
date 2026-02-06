import sqlite3
import hashlib

# Connect to database
conn = sqlite3.connect('barangay.db')
cursor = conn.cursor()

# Check the user with email resident01@gmail.com
cursor.execute("SELECT * FROM users WHERE email = ?", ('resident01@gmail.com',))
user = cursor.fetchone()

if user:
    print(f"User found: {user}")
    print(f"ID: {user[0]}")
    print(f"Email: {user[1]}")
    print(f"Password Hash: {user[2]}")
    print(f"Full Name: {user[3]}")
    print(f"Role: {user[4]}")
    
    # Test password hashing
    test_password = "resident01"
    test_hash = hashlib.sha256(test_password.encode()).hexdigest()
    print(f"\nTesting password '{test_password}':")
    print(f"Generated hash: {test_hash}")
    print(f"Stored hash:    {user[2]}")
    print(f"Hashes match: {test_hash == user[2]}")
    
    # Test other common passwords
    other_passwords = ["password", "123456", "resident", "resident01@gmail.com"]
    for pwd in other_passwords:
        pwd_hash = hashlib.sha256(pwd.encode()).hexdigest()
        match = pwd_hash == user[2]
        print(f"Password '{pwd}': {'MATCH' if match else 'NO MATCH'}")
else:
    print("User not found in database")

conn.close()
