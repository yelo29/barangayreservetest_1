#!/usr/bin/env python3
"""
Test the fixed login authentication
"""

import sqlite3
import hashlib
import json

def test_login():
    print("🧪 Testing login authentication...")
    
    # Test credentials
    test_email = "captain@barangay.gov"
    test_password = "tatalaPunongBarangayadmin"
    
    # Hash the password (same as server does)
    password_hash = hashlib.sha256(test_password.encode()).hexdigest()
    
    print(f"📧 Testing: {test_email}")
    print(f"🔐 Password: {test_password}")
    print(f"🔑 Hash: {password_hash}")
    
    # Check database
    conn = sqlite3.connect('barangay.db')
    cursor = conn.cursor()
    
    # Find user
    user = cursor.execute(
        'SELECT * FROM users WHERE email = ?',
        (test_email,)
    ).fetchone()
    
    if user:
        print(f"✅ User found: {user[1]}")
        print(f"🔐 DB Hash: {user[2]}")
        print(f"👤 Name: {user[3]}")
        print(f"🏷️ Role: {user[4]}")
        print(f"✅ Verified: {user[5]}")
        
        # Check if passwords match
        if user[2] == password_hash:
            print("🎉 PASSWORD MATCH - Login should work!")
        else:
            print("❌ PASSWORD MISMATCH - Login will fail")
    else:
        print("❌ User not found in database")
    
    conn.close()

if __name__ == "__main__":
    test_login()
