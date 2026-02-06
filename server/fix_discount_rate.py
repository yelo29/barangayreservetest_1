import sqlite3

conn = sqlite3.connect('barangay.db')
cursor = conn.cursor()

# Fix jl052904@gmail.com's discount rate to 5% for non-resident
cursor.execute('''
    UPDATE users 
    SET discount_rate = 0.05
    WHERE email = "jl052904@gmail.com"
''')

print("Updated jl052904@gmail.com discount rate to 5% for non-resident")

# Verify the update
cursor.execute('SELECT id, email, verified, discount_rate FROM users WHERE email = "jl052904@gmail.com"')
user = cursor.fetchone()
print(f"Updated user data: ID={user[0]}, Email={user[1]}, Verified={user[2]}, Discount={user[3]}")

conn.commit()
conn.close()
