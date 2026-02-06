import sqlite3

conn = sqlite3.connect('barangay.db')
cursor = conn.cursor()

# Fix jl052904@gmail.com's verification status
# User submitted as non-resident but was marked as resident (verified = 1)
# Should be non-resident (verified = 2) with 10% discount

cursor.execute('''
    UPDATE users 
    SET verified = 2
    WHERE email = "jl052904@gmail.com"
''')

print("Updated jl052904@gmail.com to verified = 2 (non-resident)")

# Verify the update
cursor.execute('SELECT id, email, verified, discount_rate FROM users WHERE email = "jl052904@gmail.com"')
user = cursor.fetchone()
print(f"Updated user data: ID={user[0]}, Email={user[1]}, Verified={user[2]}, Discount={user[3]}")

conn.commit()
conn.close()
