import sqlite3

def check_current_customer_service_query():
    """Check the current customer service query"""
    
    conn = sqlite3.connect('barangay.db')
    cursor = conn.cursor()
    
    print("=== CHECKING CURRENT CUSTOMER SERVICE QUERY ===")
    
    # Test the exact query that's in the server
    cursor.execute('''
        SELECT id, full_name, contact_number, role, email
        FROM users 
        WHERE role = 'official' AND full_name IS NOT NULL AND full_name != ''
        ORDER BY role, full_name
    ''')
    
    officials_only = cursor.fetchall()
    print(f"📋 Officials only (role = 'official'): {len(officials_only)}")
    
    # Test what should be the query based on the investigation results
    cursor.execute('''
        SELECT id, full_name, contact_number, role, email
        FROM users 
        WHERE role = 'official' OR verified = 2
        AND full_name IS NOT NULL AND full_name != ''
        ORDER BY role, full_name
    ''')
    
    officials_plus_verified2 = cursor.fetchall()
    print(f"📋 Officials + verified=2: {len(officials_plus_verified2)}")
    
    print("\n📋 Officials only:")
    for user in officials_only:
        user_id, full_name, contact_number, role, email = user
        print(f"  🏢 {full_name} ({email}) - {role}")
    
    print("\n📋 Officials + verified=2:")
    for user in officials_plus_verified2:
        user_id, full_name, contact_number, role, email = user
        print(f"  👤 {full_name} ({email}) - {role}")
    
    conn.close()

if __name__ == "__main__":
    check_current_customer_service_query()
