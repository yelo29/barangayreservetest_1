#!/usr/bin/env python3
"""
Fix password hashes in database to match auth_data.json passwords
"""

import sqlite3
import json
import hashlib
import os

def fix_password_hashes():
    db_path = 'barangay.db'
    auth_path = 'auth_data.json'
    
    print("🔧 Fixing password hashes in database...")
    
    # Load auth data
    if not os.path.exists(auth_path):
        print(f"❌ {auth_path} not found!")
        return
    
    with open(auth_path, 'r') as f:
        auth_data = json.load(f)
    
    print(f"📋 Found {len(auth_data)} accounts in auth_data.json")
    
    # Connect to database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        for email, user_data in auth_data.items():
            # Hash the password from auth_data.json
            password_hash = hashlib.sha256(user_data['password'].encode()).hexdigest()
            
            print(f"🔐 Updating {email}: {user_data['password']} -> {password_hash[:16]}...")
            
            # Update the password hash in database
            cursor.execute("""
                UPDATE users SET 
                    password_hash = ?
                WHERE email = ?
            """, (password_hash, email))
            
            if cursor.rowcount > 0:
                print(f"✅ Updated {email}")
            else:
                print(f"⚠️ User {email} not found in database")
        
        # Commit changes
        conn.commit()
        
        # Verify the updates
        cursor.execute("SELECT email, password_hash FROM users ORDER BY email")
        users = cursor.fetchall()
        
        print("\n🔍 Verification - Current database users:")
        for email, password_hash in users:
            print(f"  {email} -> {password_hash[:16]}...")
        
        print("\n🎉 Password hashes updated successfully!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    fix_password_hashes()
