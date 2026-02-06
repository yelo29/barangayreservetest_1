#!/usr/bin/env python3
import sqlite3

def check_verification_schema():
    conn = sqlite3.connect('barangay.db')
    cursor = conn.cursor()
    
    print("🔍 Checking verification_requests table schema:")
    cursor.execute('PRAGMA table_info(verification_requests)')
    columns = cursor.fetchall()
    
    for col in columns:
        print(f"  Column {col[0]}: {col[1]} ({col[2]}) - NOT NULL: {col[3]}, DEFAULT: {col[4]}")
    
    print("\n🔍 Checking if table has resident_id column:")
    cursor.execute('PRAGMA table_info(verification_requests)')
    columns = cursor.fetchall()
    has_resident_id = any(col[1] == 'resident_id' for col in columns)
    has_user_id = any(col[1] == 'user_id' for col in columns)
    
    print(f"  Has resident_id: {has_resident_id}")
    print(f"  Has user_id: {has_user_id}")
    
    if has_resident_id and not has_user_id:
        print("\n⚠️  Table has old schema (resident_id)")
    elif has_user_id and not has_resident_id:
        print("\n✅ Table has correct schema (user_id)")
    elif has_resident_id and has_user_id:
        print("\n⚠️  Table has both columns - may need cleanup")
    else:
        print("\n❌ Table has neither column - schema issue")
    
    # Check sample data
    print("\n🔍 Checking sample data:")
    try:
        cursor.execute('SELECT COUNT(*) FROM verification_requests')
        count = cursor.fetchone()[0]
        print(f"  Total records: {count}")
        
        if count > 0:
            cursor.execute('SELECT id, user_id, resident_id FROM verification_requests LIMIT 1')
            sample = cursor.fetchone()
            print(f"  Sample record: ID={sample[0]}, user_id={sample[1]}, resident_id={sample[2] if len(sample) > 2 else 'N/A'}")
    except Exception as e:
        print(f"  Error checking data: {e}")
    
    conn.close()

if __name__ == "__main__":
    check_verification_schema()
