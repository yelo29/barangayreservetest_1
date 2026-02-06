#!/usr/bin/env python3
import sqlite3

def test_verification_system():
    conn = sqlite3.connect('barangay.db')
    cursor = conn.cursor()
    
    print("🔍 Testing Verification System Database State:")
    print("=" * 50)
    
    # Check verification_requests table
    cursor.execute('''
        SELECT COUNT(*) FROM verification_requests
    ''')
    total_requests = cursor.fetchone()[0]
    print(f"📋 Total verification requests: {total_requests}")
    
    # Check pending requests
    cursor.execute('''
        SELECT COUNT(*) FROM verification_requests WHERE status = 'pending'
    ''')
    pending_requests = cursor.fetchone()[0]
    print(f"⏳ Pending verification requests: {pending_requests}")
    
    # Show all requests if any exist
    if total_requests > 0:
        cursor.execute('''
            SELECT vr.id, vr.resident_id, vr.full_name, vr.contact_number, 
                   vr.verification_type, vr.status, vr.submitted_at, u.email
            FROM verification_requests vr
            LEFT JOIN users u ON vr.resident_id = u.id
            ORDER BY vr.submitted_at DESC
        ''')
        requests = cursor.fetchall()
        
        print("\n📄 All Verification Requests:")
        for req in requests:
            print(f"  ID: {req[0]}")
            print(f"  Name: {req[2]}")
            print(f"  Email: {req[7] or 'No email'}")
            print(f"  Type: {req[4]}")
            print(f"  Status: {req[5]}")
            print(f"  Submitted: {req[6]}")
            print("  " + "-" * 30)
    
    # Check users table for verification status
    cursor.execute('''
        SELECT id, email, full_name, verified, discount_rate, role
        FROM users 
        WHERE role = 'resident'
        ORDER BY id
    ''')
    residents = cursor.fetchall()
    
    print(f"\n👥 Resident Users ({len(residents)} total):")
    for resident in residents:
        print(f"  ID: {resident[0]}")
        print(f"  Email: {resident[1]}")
        print(f"  Name: {resident[2]}")
        print(f"  Verified: {resident[3]}")
        print(f"  Discount: {resident[4] or 0}%")
        print("  " + "-" * 30)
    
    conn.close()
    print("\n✅ Verification system test completed!")

if __name__ == "__main__":
    test_verification_system()
