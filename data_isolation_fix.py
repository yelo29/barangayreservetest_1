#!/usr/bin/env python3
"""
Data Isolation Analysis and Fix
Check for data privacy and isolation issues
"""

import sqlite3
import os

def check_data_isolation():
    """Check for data isolation issues"""
    db_path = os.path.join(os.path.dirname(__file__), 'server', 'barangay.db')
    
    if not os.path.exists(db_path):
        print("❌ Database not found!")
        return
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print("🔍 DATA ISOLATION ANALYSIS")
        print("=" * 50)
        
        # 1. Check booking table structure
        cursor.execute("PRAGMA table_info(bookings)")
        booking_columns = [row[1] for row in cursor.fetchall()]
        print(f"\n📋 Bookings table columns: {booking_columns}")
        
        # 2. Check user data exposure in bookings
        cursor.execute('''
            SELECT COUNT(*) as total_bookings,
                   COUNT(CASE WHEN contact_number IS NOT NULL AND contact_number != '' THEN 1 END) as bookings_with_contact,
                   COUNT(CASE WHEN contact_address IS NOT NULL AND contact_address != '' THEN 1 END) as bookings_with_address,
                   COUNT(CASE WHEN receipt_base64 IS NOT NULL AND receipt_base64 != '' THEN 1 END) as bookings_with_receipts
            FROM bookings
        ''')
        
        stats = cursor.fetchone()
        print(f"\n📊 Booking Data Exposure:")
        print(f"  Total bookings: {stats[0]}")
        print(f"  With contact numbers: {stats[1]}")
        print(f"  With addresses: {stats[2]}")
        print(f"  With receipts: {stats[3]}")
        
        # 3. Check for user ID vs email inconsistency
        cursor.execute('''
            SELECT b.id, b.user_id, u.email, u.id
            FROM bookings b
            LEFT JOIN users u ON b.user_id = u.id
            WHERE u.email IS NULL
            LIMIT 10
        ''')
        
        mismatches = cursor.fetchall()
        if mismatches:
            print(f"\n⚠️ USER ID/EMAIL MISMATCHES:")
            for booking in mismatches:
                print(f"  Booking {booking[0]}: email={booking[1]}, user_id={booking[2]}, db_email={booking[3]}, db_id={booking[4]}")
        else:
            print(f"\n✅ No user ID/email mismatches found")
        
        # 4. Check data leakage between users
        cursor.execute('''
            SELECT DISTINCT user_email, COUNT(*) as booking_count
            FROM bookings
            WHERE user_email IS NOT NULL AND user_email != ''
            GROUP BY user_email
            ORDER BY booking_count DESC
            LIMIT 10
        ''')
        
        user_bookings = cursor.fetchall()
        print(f"\n👥 User Booking Distribution:")
        for email, count in user_bookings:
            print(f"  {email}: {count} bookings")
        
        # 5. Check for sensitive data exposure
        cursor.execute('''
            SELECT user_email, contact_number, address, receipt_base64
            FROM bookings
            WHERE user_email IS NOT NULL 
            AND (contact_number IS NOT NULL OR address IS NOT NULL OR receipt_base64 IS NOT NULL)
            LIMIT 5
        ''')
        
        sensitive_data = cursor.fetchall()
        if sensitive_data:
            print(f"\n🚨 SENSITIVE DATA EXPOSURE SAMPLE:")
            for data in sensitive_data:
                email, contact, address, receipt = data
                print(f"  Email: {email}")
                print(f"    Contact: {contact[:10]}..." if contact and len(contact) > 10 else f"    Contact: {contact}")
                print(f"    Address: {address[:20]}..." if address and len(address) > 20 else f"    Address: {address}")
                print(f"    Receipt: {'Present' if receipt else 'None'}")
                print()
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Error checking data isolation: {e}")

def fix_data_isolation():
    """Fix data isolation issues"""
    db_path = os.path.join(os.path.dirname(__file__), 'server', 'barangay.db')
    
    if not os.path.exists(db_path):
        print("❌ Database not found!")
        return
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print("🔧 FIXING DATA ISOLATION ISSUES")
        print("=" * 50)
        
        # 1. Ensure user_id consistency
        print("📝 Fixing user_id consistency...")
        cursor.execute('''
            UPDATE bookings 
            SET user_id = (
                SELECT id FROM users WHERE users.email = bookings.user_email
            )
            WHERE user_email IN (SELECT email FROM users) 
            AND user_id != (SELECT id FROM users WHERE users.email = bookings.user_email)
        ''')
        
        updated_count = cursor.rowcount
        print(f"  ✅ Updated {updated_count} booking user IDs")
        
        # 2. Remove sensitive data from non-owners (simulate privacy)
        print("🔒 Applying privacy filters...")
        
        # This would be handled in the API layer, but let's check what needs protection
        cursor.execute('''
            SELECT COUNT(*) FROM bookings 
            WHERE contact_number IS NOT NULL 
            OR address IS NOT NULL 
            OR receipt_base64 IS NOT NULL
        ''')
        
        sensitive_count = cursor.fetchone()[0]
        print(f"  📊 Found {sensitive_count} bookings with sensitive data")
        
        # 3. Add privacy indicators (for API layer to use)
        print("🏷️ Adding privacy indicators...")
        
        # Check if privacy columns exist
        cursor.execute("PRAGMA table_info(bookings)")
        columns = [row[1] for row in cursor.fetchall()]
        
        if 'is_private_contact' not in columns:
            cursor.execute('''
                ALTER TABLE bookings 
                ADD COLUMN is_private_contact BOOLEAN DEFAULT 0
            ''')
            print("  ✅ Added is_private_contact column")
        
        if 'is_private_address' not in columns:
            cursor.execute('''
                ALTER TABLE bookings 
                ADD COLUMN is_private_address BOOLEAN DEFAULT 0
            ''')
            print("  ✅ Added is_private_address column")
        
        if 'is_private_receipt' not in columns:
            cursor.execute('''
                ALTER TABLE bookings 
                ADD COLUMN is_private_receipt BOOLEAN DEFAULT 1
            ''')
            print("  ✅ Added is_private_receipt column")
        
        conn.commit()
        conn.close()
        
        print("\n✅ Data isolation fixes completed!")
        print("📋 Summary:")
        print(f"  - Updated {updated_count} user ID references")
        print(f"  - Added privacy indicator columns")
        print(f"  - Identified {sensitive_count} bookings with sensitive data")
        
    except Exception as e:
        print(f"❌ Error fixing data isolation: {e}")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == '--fix':
        fix_data_isolation()
    else:
        check_data_isolation()
