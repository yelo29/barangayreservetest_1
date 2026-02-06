import sqlite3
import hashlib

# Connect to database
conn = sqlite3.connect('barangay.db')
cursor = conn.cursor()

# Get all users
cursor.execute("SELECT id, email, password_hash, full_name, role FROM users")
users = cursor.fetchall()

print("=== THOROUGH PASSWORD VERIFICATION ===")
print(f"Total users: {len(users)}")

issues_found = []

for user in users:
    user_id, email, password_hash, full_name, role = user
    
    print(f"\nUser {user_id}: {email} ({role})")
    print(f"  Name: {full_name}")
    print(f"  Password Hash: {password_hash}")
    
    # Check if password is properly hashed (should be 64 characters for SHA256)
    if len(password_hash) != 64:
        print(f"  ❌ ISSUE: Password hash length is {len(password_hash)} (should be 64 for SHA256)")
        issues_found.append({
            'id': user_id,
            'email': email,
            'issue': f"Hash length: {len(password_hash)} (should be 64)"
        })
    elif not all(c in '0123456789abcdef' for c in password_hash.lower()):
        print(f"  ❌ ISSUE: Password hash contains non-hex characters")
        issues_found.append({
            'id': user_id,
            'email': email,
            'issue': "Non-hex characters in hash"
        })
    else:
        print(f"  ✅ Password appears to be properly hashed (SHA256)")

print(f"\n=== ISSUES FOUND ===")
print(f"Total issues: {len(issues_found)}")

for issue in issues_found:
    print(f"- {issue['email']} (ID: {issue['id']}): {issue['issue']}")

# Test a few known passwords to verify hashing works
test_passwords = {
    'password123': hashlib.sha256('password123'.encode()).hexdigest(),
    'barangay123': hashlib.sha256('barangay123'.encode()).hexdigest(),
    'salo3029': hashlib.sha256('salo3029'.encode()).hexdigest(),
    'resident01': hashlib.sha256('resident01'.encode()).hexdigest(),
}

print(f"\n=== PASSWORD HASH VERIFICATION ===")
for plain, expected_hash in test_passwords.items():
    print(f"'{plain}' → {expected_hash}")

conn.close()
