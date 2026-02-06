import sqlite3
import hashlib

# Connect to database
conn = sqlite3.connect('barangay.db')
cursor = conn.cursor()

# Get all users
cursor.execute("SELECT * FROM users")
users = cursor.fetchall()

print("=== ALL USERS IN DATABASE ===")
print(f"Total users: {len(users)}")

users_to_fix = []

for user in users:
    user_id, email, password_hash, full_name, role, verified, verification_type, discount_rate, contact_number, address, profile_photo_url, profile_photo_base64, is_active, email_verified, last_login, created_at, updated_at, created_by = user
    
    print(f"\nUser {user_id}: {email}")
    print(f"  Name: {full_name}")
    print(f"  Role: {role}")
    print(f"  Password Hash: {password_hash}")
    
    # Check if password is plain text (not a hash)
    if len(password_hash) < 20:  # Plain text passwords are usually shorter
        print(f"  ❌ ISSUE: Password appears to be plain text!")
        users_to_fix.append({
            'id': user_id,
            'email': email,
            'plain_password': password_hash,
            'full_name': full_name
        })
    elif password_hash.startswith('0x') or password_hash.startswith('1x') or password_hash.startswith('2x'):
        print(f"  ❌ ISSUE: Password appears to be plain text!")
        users_to_fix.append({
            'id': user_id,
            'email': email,
            'plain_password': password_hash,
            'full_name': full_name
        })
    else:
        print(f"  ✅ Password appears to be hashed")

print(f"\n=== USERS NEEDING PASSWORD FIX ===")
print(f"Total users to fix: {len(users_to_fix)}")

for user in users_to_fix:
    print(f"- {user['email']} (ID: {user['id']}) - Current: '{user['plain_password']}'")

conn.close()
