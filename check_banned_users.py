#!/usr/bin/env python3
"""
Check for banned users in the database
"""

import sqlite3
import os

def check_banned_users():
    # Database path (in server folder)
    db_path = os.path.join(os.path.dirname(__file__), 'server', 'barangay.db')
    
    if not os.path.exists(db_path):
        print("❌ Database not found!")
        return
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check if ban columns exist
        cursor.execute("PRAGMA table_info(users)")
        columns = [row[1] for row in cursor.fetchall()]
        
        print("📋 Available columns in users table:")
        for col in columns:
            print(f"  - {col}")
        
        if 'is_banned' in columns:
            # Query banned users
            cursor.execute('''
                SELECT id, email, full_name, is_banned, banned_at, ban_reason, fake_booking_violations
                FROM users 
                WHERE is_banned = 1 OR fake_booking_violations > 0
                ORDER BY fake_booking_violations DESC, banned_at DESC
            ''')
            
            banned_users = cursor.fetchall()
            
            if banned_users:
                print(f"\n🚨 Found {len(banned_users)} banned/violating users:")
                print("-" * 80)
                for user in banned_users:
                    user_id, email, full_name, is_banned, banned_at, ban_reason, violations = user
                    print(f"📧 Email: {email}")
                    print(f"👤 Name: {full_name}")
                    print(f"🆔 ID: {user_id}")
                    print(f"🚫 Banned: {'Yes' if is_banned else 'No'}")
                    print(f"⚠️ Violations: {violations}")
                    if banned_at:
                        print(f"📅 Banned at: {banned_at}")
                    if ban_reason:
                        print(f"📝 Reason: {ban_reason}")
                    print("-" * 80)
            else:
                print("\n✅ No banned users found!")
        else:
            print("\n❌ Ban system not implemented in this database version!")
        
        # Check all users with violations
        cursor.execute('''
            SELECT email, full_name, fake_booking_violations 
            FROM users 
            WHERE fake_booking_violations > 0
            ORDER BY fake_booking_violations DESC
        ''')
        
        violating_users = cursor.fetchall()
        if violating_users:
            print(f"\n⚠️ Users with violations (not necessarily banned):")
            for email, name, violations in violating_users:
                print(f"  - {email}: {violations} violations")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Error checking banned users: {e}")

if __name__ == "__main__":
    check_banned_users()
