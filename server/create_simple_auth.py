import sqlite3
import json

# Create a simple authentication bypass for testing
def create_simple_auth_server():
    conn = sqlite3.connect('barangay.db')
    cursor = conn.cursor()
    
    print("Creating simple authentication data...")
    
    # Get all users and create a simple auth map
    cursor.execute('SELECT email, password, full_name, role, verified, discount_rate FROM users')
    users = cursor.fetchall()
    
    auth_data = {}
    for user in users:
        email, password, full_name, role, verified, discount_rate = user
        auth_data[email] = {
            'password': password,
            'full_name': full_name,
            'role': role,
            'verified': bool(verified),
            'discount_rate': discount_rate,
            'id': str(user[0])  # Convert ID to string
        }
    
    # Save to a simple JSON file for reference
    with open('auth_data.json', 'w') as f:
        json.dump(auth_data, f, indent=2)
    
    print("Authentication data created:")
    print("=" * 50)
    
    for email, data in auth_data.items():
        print(f"Email: {email}")
        print(f"Password: {data['password']}")
        print(f"Name: {data['full_name']}")
        print(f"Role: {data['role']}")
        print(f"Verified: {data['verified']}")
        print(f"Discount: {data['discount_rate']}")
        print("-" * 30)
    
    conn.close()
    
    print("\n✅ Simple authentication data created!")
    print("📄 Saved to: auth_data.json")
    
    # Test credentials
    print("\n🔑 Working credentials:")
    print("1. official@barangay.com / password123")
    print("2. secretary@barangay.gov / barangay123") 
    print("3. captain@barangay.com / barangay123")
    print("4. leo052904@gmail.com / [check password]")
    print("5. saloestillopez@gmail.com / [check password]")

if __name__ == "__main__":
    create_simple_auth_server()
