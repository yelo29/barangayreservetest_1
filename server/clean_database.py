#!/usr/bin/env python3
"""
Clean database - Remove all resident accounts and old official accounts
Keep only the 6 new official accounts from auth_data.json
"""

import sqlite3
import json
import os

def clean_database():
    db_path = 'barangay.db'
    auth_path = 'auth_data.json'
    
    print("🧹 Cleaning database...")
    
    # Load new official accounts from auth_data.json
    if not os.path.exists(auth_path):
        print(f"❌ {auth_path} not found!")
        return
    
    with open(auth_path, 'r') as f:
        auth_data = json.load(f)
    
    print(f"📋 Found {len(auth_data)} official accounts in auth_data.json")
    
    # Connect to database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Get current users
        cursor.execute("SELECT id, email, role FROM users")
        current_users = cursor.fetchall()
        print(f"👥 Current users in database: {len(current_users)}")
        
        # Identify users to keep (official accounts from auth_data.json)
        official_emails = list(auth_data.keys())
        print(f"✅ Official emails to keep: {official_emails}")
        
        # Delete bookings for users to be removed
        users_to_remove = []
        for user_id, email, role in current_users:
            if email not in official_emails:
                users_to_remove.append(user_id)
                print(f"🗑️ Marking for removal: {email} (ID: {user_id})")
        
        if users_to_remove:
            # Delete bookings for removed users
            placeholders = ','.join(['?' for _ in users_to_remove])
            cursor.execute(f"DELETE FROM bookings WHERE user_id IN ({placeholders})", users_to_remove)
            deleted_bookings = cursor.rowcount
            print(f"📅 Deleted {deleted_bookings} bookings")
            
            # Delete verification requests for removed users
            cursor.execute(f"DELETE FROM verification_requests WHERE user_id IN ({placeholders})", users_to_remove)
            deleted_verifications = cursor.rowcount
            print(f"📋 Deleted {deleted_verifications} verification requests")
            
            # Delete the users
            cursor.execute(f"DELETE FROM users WHERE id IN ({placeholders})", users_to_remove)
            deleted_users = cursor.rowcount
            print(f"👤 Deleted {deleted_users} users")
        
        # Update/Insert official accounts from auth_data.json
        for email, user_data in auth_data.items():
            # Check if user exists
            cursor.execute("SELECT id FROM users WHERE email = ?", (email,))
            existing_user = cursor.fetchone()
            
            if existing_user:
                # Update existing user
                user_id = existing_user[0]
                cursor.execute("""
                    UPDATE users SET 
                        password_hash = ?,
                        full_name = ?,
                        role = ?,
                        verified = ?,
                        discount_rate = ?,
                        is_active = 1,
                        email_verified = 1
                    WHERE email = ?
                """, (
                    user_data['password'],  # Using password directly for now (should be hashed)
                    user_data['full_name'],
                    user_data['role'],
                    user_data['verified'],
                    user_data['discount_rate'],
                    email
                ))
                print(f"✏️ Updated: {email}")
            else:
                # Insert new user
                cursor.execute("""
                    INSERT INTO users (
                        email, password_hash, full_name, role, verified, 
                        discount_rate, is_active, email_verified, created_at, updated_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, datetime('now'), datetime('now'))
                """, (
                    email,
                    user_data['password'],  # Using password directly for now (should be hashed)
                    user_data['full_name'],
                    user_data['role'],
                    user_data['verified'],
                    user_data['discount_rate'],
                    1,  # is_active
                    1   # email_verified
                ))
                print(f"➕ Added: {email}")
        
        # Commit changes
        conn.commit()
        
        # Show final status
        cursor.execute("SELECT COUNT(*) FROM users")
        final_users = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM bookings")
        final_bookings = cursor.fetchone()[0]
        
        print("\n🎉 Database cleanup completed!")
        print(f"👥 Final users: {final_users}")
        print(f"📅 Final bookings: {final_bookings}")
        
        # Show remaining users
        cursor.execute("SELECT email, full_name, role FROM users ORDER BY role, email")
        remaining_users = cursor.fetchall()
        
        print("\n📋 Remaining users:")
        for email, name, role in remaining_users:
            print(f"  ✅ {email} - {name} ({role})")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    clean_database()
