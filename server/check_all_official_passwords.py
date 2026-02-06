import sqlite3

# Check all official accounts and their passwords
conn = sqlite3.connect('barangay.db')
cursor = conn.cursor()

print("All official accounts in database:")
print("=" * 50)

cursor.execute('SELECT email, password, full_name, role FROM users WHERE role = "official"')
officials = cursor.fetchall()

for official in officials:
    print(f"Email: {official[0]}")
    print(f"Password: {official[1]}")
    print(f"Name: {official[2]}")
    print(f"Role: {official[3]}")
    print("-" * 30)

conn.close()

print("\nRecommended login credentials:")
print("1. secretary@barangay.gov / admin123")
print("2. official@barangay.com / password123") 
print("3. captain@barangay.com / captain123")
print("4. treasurer@barangay.gov / treasurer123")
