import sqlite3

def investigate_customer_service_issue():
    """Investigate the customer service display issue"""
    
    conn = sqlite3.connect('barangay.db')
    cursor = conn.cursor()
    
    print("=== INVESTIGATING CUSTOMER SERVICE DISPLAY ISSUE ===")
    
    # Check all users to see what we have
    cursor.execute('''
        SELECT id, email, full_name, contact_number, role, verified
        FROM users
        ORDER BY id
    ''')
    
    users = cursor.fetchall()
    print(f"📋 Total users in database: {len(users)}")
    
    for user in users:
        user_id, email, full_name, contact_number, role, verified = user
        print(f"\n  👤 User ID: {user_id}")
        print(f"     Email: {email}")
        print(f"     Name: {full_name}")
        print(f"     Contact: {contact_number}")
        print(f"     Role: {role}")
        print(f"     Verified: {verified}")
    
    # Check verification requests to see what's being processed
    cursor.execute('''
        SELECT vr.id, vr.user_id, vr.verification_type, vr.status, u.email, u.full_name
        FROM verification_requests vr
        LEFT JOIN users u ON vr.user_id = u.id
        ORDER BY vr.id DESC
        LIMIT 10
    ''')
    
    verification_requests = cursor.fetchall()
    print(f"\n📋 Recent verification requests: {len(verification_requests)}")
    
    for vr in verification_requests:
        vr_id, user_id, verification_type, status, email, full_name = vr
        print(f"\n  📄 Verification Request ID: {vr_id}")
        print(f"     User: {email} ({full_name})")
        print(f"     Type: {verification_type}")
        print(f"     Status: {status}")
    
    # Check if there are any issues with the customer service query
    print(f"\n🔍 Checking customer service query logic...")
    
    # The customer service should show officials differently
    cursor.execute('''
        SELECT u.id, u.email, u.full_name, u.contact_number, u.role, u.verified
        FROM users u
        WHERE u.role = 'official' OR u.verified = 2
        ORDER BY u.full_name
    ''')
    
    customer_service_users = cursor.fetchall()
    print(f"📋 Users that should appear in customer service: {len(customer_service_users)}")
    
    for user in customer_service_users:
        user_id, email, full_name, contact_number, role, verified = user
        print(f"  🏢 {full_name} ({email}) - Role: {role}, Verified: {verified}")
    
    conn.close()

if __name__ == "__main__":
    investigate_customer_service_issue()
