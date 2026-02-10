import sqlite3

def verify_resident_removed():
    """Verify that resident user is no longer in customer service"""
    
    conn = sqlite3.connect('barangay.db')
    cursor = conn.cursor()
    
    print("=== VERIFYING RESIDENT REMOVED FROM CUSTOMER SERVICE ===")
    
    # Check current customer service query
    cursor.execute('''
        SELECT id, full_name, contact_number, role, email
        FROM users 
        WHERE role = 'official' AND full_name IS NOT NULL AND full_name != ''
        ORDER BY role, full_name
    ''')
    
    officials = cursor.fetchall()
    print(f"📋 Customer service now shows: {len(officials)} users")
    
    # Check if Salo E. Lopez appears
    found_resident = False
    for user in officials:
        user_id, full_name, contact_number, role, email = user
        print(f"  🏢 {full_name} ({email}) - {role}")
        if 'Salo E. Lopez' in full_name or 'saloestillopez@gmail.com' in email:
            found_resident = True
    
    if not found_resident:
        print("✅ SUCCESS: Resident user (Salo E. Lopez) is no longer in customer service!")
    else:
        print("❌ ISSUE: Resident user still appears in customer service")
    
    # Verify Salo E. Lopez still exists in database
    cursor.execute('''
        SELECT id, full_name, role, verified
        FROM users 
        WHERE email = 'saloestillopez@gmail.com'
    ''')
    
    resident = cursor.fetchone()
    if resident:
        user_id, full_name, role, verified = resident
        print(f"\n📋 Salo E. Lopez still exists in database:")
        print(f"  📧 Email: saloestillopez@gmail.com")
        print(f"  👤 Name: {full_name}")
        print(f"  🏷️  Role: {role}")
        print(f"  ✅ Verified: {verified}")
        print("✅ This is correct - resident should remain in database, just not in customer service")
    
    conn.close()

if __name__ == "__main__":
    verify_resident_removed()
