#!/usr/bin/env python3
"""
Complete database reset - Remove ALL data except the 6 new official accounts
"""

import sqlite3
import json
import hashlib
import os

def complete_reset():
    db_path = 'barangay.db'
    auth_path = 'auth_data.json'
    
    print("🧹 COMPLETE DATABASE RESET...")
    
    # Load official accounts
    if not os.path.exists(auth_path):
        print(f"❌ {auth_path} not found!")
        return
    
    with open(auth_path, 'r') as f:
        auth_data = json.load(f)
    
    print(f"📋 Official accounts to preserve: {len(auth_data)}")
    
    # Connect to database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        print("\n🗑️ DELETING ALL DATA...")
        
        # Delete ALL bookings
        cursor.execute("DELETE FROM bookings")
        deleted_bookings = cursor.rowcount
        print(f"📅 Deleted {deleted_bookings} bookings")
        
        # Delete ALL verification requests
        cursor.execute("DELETE FROM verification_requests")
        deleted_verifications = cursor.rowcount
        print(f"📋 Deleted {deleted_verifications} verification requests")
        
        # Delete ALL facilities
        cursor.execute("DELETE FROM facilities")
        deleted_facilities = cursor.rowcount
        print(f"🏢 Deleted {deleted_facilities} facilities")
        
        # Delete ALL time slots
        cursor.execute("DELETE FROM time_slots")
        deleted_timeslots = cursor.rowcount
        print(f"⏰ Deleted {deleted_timeslots} time slots")
        
        # Delete ALL users except our officials
        official_emails = list(auth_data.keys())
        placeholders = ','.join(['?' for _ in official_emails])
        
        cursor.execute(f"DELETE FROM users WHERE email NOT IN ({placeholders})", official_emails)
        deleted_users = cursor.rowcount
        print(f"👤 Deleted {deleted_users} non-official users")
        
        # Reset auto-increment sequences
        cursor.execute("DELETE FROM sqlite_sequence WHERE name IN ('bookings', 'users', 'facilities', 'time_slots', 'verification_requests')")
        print("🔄 Reset auto-increment sequences")
        
        print("\n✅ UPDATING OFFICIAL ACCOUNTS...")
        
        # Update official accounts with proper password hashes
        for email, user_data in auth_data.items():
            password_hash = hashlib.sha256(user_data['password'].encode()).hexdigest()
            
            cursor.execute("""
                UPDATE users SET 
                    password_hash = ?,
                    full_name = ?,
                    role = ?,
                    verified = ?,
                    discount_rate = ?,
                    is_active = 1,
                    email_verified = 1,
                    updated_at = datetime('now')
                WHERE email = ?
            """, (
                password_hash,
                user_data['full_name'],
                user_data['role'],
                user_data['verified'],
                user_data['discount_rate'],
                email
            ))
            
            if cursor.rowcount > 0:
                print(f"✅ Updated {email}")
            else:
                print(f"⚠️ {email} not found - inserting...")
                cursor.execute("""
                    INSERT INTO users (
                        email, password_hash, full_name, role, verified, 
                        discount_rate, is_active, email_verified, created_at, updated_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, datetime('now'), datetime('now'))
                """, (
                    email,
                    password_hash,
                    user_data['full_name'],
                    user_data['role'],
                    user_data['verified'],
                    user_data['discount_rate'],
                    1,  # is_active
                    1   # email_verified
                ))
        
        # Commit all changes
        conn.commit()
        
        print("\n🔍 VERIFYING CLEAN DATABASE...")
        
        # Check final state
        cursor.execute("SELECT COUNT(*) FROM users")
        user_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM bookings")
        booking_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM facilities")
        facility_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM time_slots")
        timeslot_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM verification_requests")
        verification_count = cursor.fetchone()[0]
        
        print(f"\n📊 Final Database State:")
        print(f"  👤 Users: {user_count}")
        print(f"  📅 Bookings: {booking_count}")
        print(f"  🏢 Facilities: {facility_count}")
        print(f"  ⏰ Time Slots: {timeslot_count}")
        print(f"  📋 Verification Requests: {verification_count}")
        
        # Show remaining users
        cursor.execute("SELECT email, full_name, role, verified FROM users ORDER BY email")
        users = cursor.fetchall()
        
        print(f"\n📋 Remaining Users:")
        for email, name, role, verified in users:
            print(f"  ✅ {email} - {name} ({role}) - Verified: {verified}")
        
        print("\n🎉 COMPLETE DATABASE RESET SUCCESSFUL!")
        print("🚀 Ready for fresh testing with clean data!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    complete_reset()
