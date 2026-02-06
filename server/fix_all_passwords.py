import sqlite3
import hashlib

# Connect to database
conn = sqlite3.connect('barangay.db')
cursor = conn.cursor()

# Users to fix (email -> plain_password)
users_to_fix = {
    'official@barangay.com': 'password123',
    'secretary@barangay.gov': 'barangay123', 
    'saloestillopez@gmail.com': 'salo3029',
    'resident@barangay.com': 'password123'
}

print("=== FIXING ALL PLAIN TEXT PASSWORDS ===")

fixed_count = 0
for email, plain_password in users_to_fix.items():
    print(f"\nFixing {email}...")
    
    # Generate hash
    new_hash = hashlib.sha256(plain_password.encode()).hexdigest()
    
    # Update password
    cursor.execute(
        "UPDATE users SET password_hash = ? WHERE email = ?",
        (new_hash, email)
    )
    
    # Verify update
    cursor.execute("SELECT password_hash FROM users WHERE email = ?", (email,))
    result = cursor.fetchone()
    
    if result and result[0] == new_hash:
        print(f"  ✅ Fixed successfully")
        fixed_count += 1
    else:
        print(f"  ❌ Fix failed")

conn.commit()

print(f"\n=== SUMMARY ===")
print(f"Fixed {fixed_count} out of {len(users_to_fix)} users")

# Verify all users now have proper passwords
print("\n=== VERIFYING ALL USERS ===")
cursor.execute("SELECT email, password_hash FROM users")
all_users = cursor.fetchall()

hash_count = 0
for email, password_hash in all_users:
    if len(password_hash) > 20:  # Hashed passwords are longer
        hash_count += 1

print(f"Users with hashed passwords: {hash_count}/{len(all_users)}")

if hash_count == len(all_users):
    print("✅ ALL USERS NOW HAVE PROPERLY HASHED PASSWORDS!")
else:
    print("❌ Some users still have plain text passwords")

conn.close()
