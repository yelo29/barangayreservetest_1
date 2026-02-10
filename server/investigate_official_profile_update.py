import sqlite3

def investigate_official_profile_update():
    """Investigate official profile update and customer service data"""
    
    conn = sqlite3.connect('barangay.db')
    cursor = conn.cursor()
    
    print("=== INVESTIGATING OFFICIAL PROFILE UPDATE ISSUE ===")
    
    # Check current official data in database
    cursor.execute('''
        SELECT id, email, full_name, contact_number, role, updated_at
        FROM users 
        WHERE role = 'official' AND email = 'captain@barangay.gov'
    ''')
    
    official = cursor.fetchone()
    if official:
        user_id, email, full_name, contact_number, role, updated_at = official
        print(f"📋 Official in database:")
        print(f"  👤 ID: {user_id}")
        print(f"  📧 Email: {email}")
        print(f"  👨‍💼 Name: {full_name}")
        print(f"  📞 Contact: {contact_number}")
        print(f"  🏷️  Role: {role}")
        print(f"  🕒 Updated: {updated_at}")
    else:
        print("❌ Official not found in database")
    
    # Check what customer service endpoint returns
    print(f"\n🔍 Checking customer service endpoint logic...")
    
    cursor.execute('''
        SELECT id, full_name, contact_number, role, email
        FROM users 
        WHERE role = 'official' AND full_name IS NOT NULL AND full_name != ''
        ORDER BY role, full_name
    ''')
    
    officials = cursor.fetchall()
    print(f"📋 Customer service query returns: {len(officials)} officials")
    
    for user in officials:
        user_id, full_name, contact_number, role, email = user
        print(f"  🏢 {full_name} ({email}) - Contact: {contact_number}")
        
        # Check if this is the captain
        if 'captain@barangay.gov' in email:
            print(f"    🎯 This is the captain - showing: '{full_name}' with contact: '{contact_number}'")
    
    # Check if there are any update logs or recent changes
    print(f"\n🔍 Checking for potential update issues...")
    
    # Look for any users with similar names that might cause confusion
    cursor.execute('''
        SELECT id, email, full_name, contact_number, role, updated_at
        FROM users 
        WHERE full_name LIKE '%Captain%' OR email LIKE '%captain%'
        ORDER BY updated_at DESC
    ''')
    
    captain_users = cursor.fetchall()
    print(f"📋 Users with 'Captain' in name/email: {len(captain_users)}")
    
    for user in captain_users:
        user_id, email, full_name, contact_number, role, updated_at = user
        print(f"  👤 ID {user_id}: {full_name} ({email}) - {role} - Updated: {updated_at}")
    
    conn.close()

if __name__ == "__main__":
    investigate_official_profile_update()
