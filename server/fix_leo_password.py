import sqlite3
import hashlib

# Connect to database
conn = sqlite3.connect('barangay.db')
cursor = conn.cursor()

# Generate hash for the desired password
new_password = "zepol052904"
new_hash = hashlib.sha256(new_password.encode()).hexdigest()

print(f"Setting password to '{new_password}'")
print(f"New hash: {new_hash}")

# Update the password
cursor.execute(
    "UPDATE users SET password_hash = ? WHERE email = ?",
    (new_hash, 'leo052904@gmail.com')
)

conn.commit()

# Verify the update
cursor.execute("SELECT password_hash FROM users WHERE email = ?", ('leo052904@gmail.com',))
result = cursor.fetchone()

if result:
    print(f"Updated successfully. New stored hash: {result[0]}")
    print(f"Hashes match: {result[0] == new_hash}")
else:
    print("Update failed")

conn.close()
