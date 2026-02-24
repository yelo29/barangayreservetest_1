#!/usr/bin/env python3
"""
Unban users from the database - Admin tool
"""

import sqlite3
import os

def unban_user(email=None, user_id=None, unban_all=False):
    """
    Unban a user by email, ID, or unban all banned users
    """
    # Database path (in server folder)
    db_path = os.path.join(os.path.dirname(__file__), 'server', 'barangay.db')
    
    if not os.path.exists(db_path):
        print("❌ Database not found!")
        return
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        if unban_all:
            # Unban ALL banned users
            cursor.execute('''
                UPDATE users 
                SET is_banned = 0, 
                    banned_at = NULL, 
                    ban_reason = NULL
                WHERE is_banned = 1
            ''')
            
            affected_rows = cursor.rowcount
            conn.commit()
            
            print(f"✅ Successfully unbanned {affected_rows} users!")
            
            # Show updated status
            cursor.execute('''
                SELECT email, full_name, fake_booking_violations 
                FROM users 
                WHERE fake_booking_violations > 0
                ORDER BY fake_booking_violations DESC
            ''')
            
            users = cursor.fetchall()
            print("\n📋 Users with violations (now unbanned):")
            for email, name, violations in users:
                status = "🚫 BANNED" if violations >= 3 else f"⚠️ {violations}/3 violations"
                print(f"  - {email}: {name} - {status}")
        
        elif email:
            # Unban by email
            cursor.execute('''
                UPDATE users 
                SET is_banned = 0, 
                    banned_at = NULL, 
                    ban_reason = NULL
                WHERE email = ? AND is_banned = 1
            ''', (email,))
            
            affected_rows = cursor.rowcount
            conn.commit()
            
            if affected_rows > 0:
                print(f"✅ Successfully unbanned {email}!")
                
                # Show user's current status
                cursor.execute('''
                    SELECT email, full_name, fake_booking_violations 
                    FROM users 
                    WHERE email = ?
                ''', (email,))
                
                user = cursor.fetchone()
                if user:
                    email, name, violations = user
                    print(f"📧 Email: {email}")
                    print(f"👤 Name: {name}")
                    print(f"⚠️ Violations: {violations}")
                    if violations >= 3:
                        print("⚠️ WARNING: User still has 3 violations and may be banned again!")
            else:
                print(f"❌ User {email} not found or already unbanned!")
        
        elif user_id:
            # Unban by ID
            cursor.execute('''
                UPDATE users 
                SET is_banned = 0, 
                    banned_at = NULL, 
                    ban_reason = NULL
                WHERE id = ? AND is_banned = 1
            ''', (user_id,))
            
            affected_rows = cursor.rowcount
            conn.commit()
            
            if affected_rows > 0:
                print(f"✅ Successfully unbanned user ID {user_id}!")
                
                # Show user's current status
                cursor.execute('''
                    SELECT email, full_name, fake_booking_violations 
                    FROM users 
                    WHERE id = ?
                ''', (user_id,))
                
                user = cursor.fetchone()
                if user:
                    email, name, violations = user
                    print(f"📧 Email: {email}")
                    print(f"👤 Name: {name}")
                    print(f"⚠️ Violations: {violations}")
                    if violations >= 3:
                        print("⚠️ WARNING: User still has 3 violations and may be banned again!")
            else:
                print(f"❌ User ID {user_id} not found or already unbanned!")
        
        else:
            print("❌ Please specify email, user_id, or use --unban-all")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Error unbanning user: {e}")

def reset_violations(email=None, user_id=None, reset_all=False):
    """
    Reset violation counts (use with caution!)
    """
    db_path = os.path.join(os.path.dirname(__file__), 'server', 'barangay.db')
    
    if not os.path.exists(db_path):
        print("❌ Database not found!")
        return
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        if reset_all:
            cursor.execute('UPDATE users SET fake_booking_violations = 0')
            affected_rows = cursor.rowcount
            conn.commit()
            print(f"⚠️ Reset violations for {affected_rows} users!")
        
        elif email:
            cursor.execute('UPDATE users SET fake_booking_violations = 0 WHERE email = ?', (email,))
            affected_rows = cursor.rowcount
            conn.commit()
            if affected_rows > 0:
                print(f"✅ Reset violations for {email}")
            else:
                print(f"❌ User {email} not found!")
        
        elif user_id:
            cursor.execute('UPDATE users SET fake_booking_violations = 0 WHERE id = ?', (user_id,))
            affected_rows = cursor.rowcount
            conn.commit()
            if affected_rows > 0:
                print(f"✅ Reset violations for user ID {user_id}")
            else:
                print(f"❌ User ID {user_id} not found!")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Error resetting violations: {e}")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python unban_users.py --email user@example.com")
        print("  python unban_users.py --id 123")
        print("  python unban_users.py --unban-all")
        print("  python unban_users.py --reset-violations --email user@example.com")
        print("  python unban_users.py --reset-violations --id 123")
        print("  python unban_users.py --reset-violations --all")
        sys.exit(1)
    
    # Parse arguments
    args = sys.argv[1:]
    email = None
    user_id = None
    unban_all = False
    reset_violations_flag = False
    
    i = 0
    while i < len(args):
        if args[i] == '--email' and i + 1 < len(args):
            email = args[i + 1]
            i += 2
        elif args[i] == '--id' and i + 1 < len(args):
            user_id = int(args[i + 1])
            i += 2
        elif args[i] == '--unban-all':
            unban_all = True
            i += 1
        elif args[i] == '--reset-violations':
            reset_violations_flag = True
            i += 1
        elif args[i] == '--all' and reset_violations_flag:
            reset_violations(email=None, user_id=None, reset_all=True)
            sys.exit(0)
        else:
            i += 1
    
    if reset_violations_flag:
        reset_violations(email=email, user_id=user_id, reset_all=False)
    else:
        unban_user(email=email, user_id=user_id, unban_all=unban_all)
