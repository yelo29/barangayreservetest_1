#!/usr/bin/env python3
"""
Database Migration Script for Violation Tracking
Adds fake booking violation tracking to users table
"""

import sqlite3
from config import Config

def migrate_violation_tracking():
    conn = sqlite3.connect(Config.DATABASE_PATH)
    cursor = conn.cursor()
    
    print("🔄 Adding violation tracking columns to users table...")
    
    try:
        # Add violation tracking columns to users table
        cursor.execute('''
            ALTER TABLE users ADD COLUMN fake_booking_violations INTEGER DEFAULT 0
        ''')
        print("✅ Added fake_booking_violations column")
        
        cursor.execute('''
            ALTER TABLE users ADD COLUMN is_banned BOOLEAN DEFAULT FALSE
        ''')
        print("✅ Added is_banned column")
        
        cursor.execute('''
            ALTER TABLE users ADD COLUMN banned_at TIMESTAMP NULL
        ''')
        print("✅ Added banned_at column")
        
        cursor.execute('''
            ALTER TABLE users ADD COLUMN ban_reason TEXT NULL
        ''')
        print("✅ Added ban_reason column")
        
        # Add rejection_type column to bookings table for detailed tracking
        cursor.execute('''
            ALTER TABLE bookings ADD COLUMN rejection_type VARCHAR(50) NULL
        ''')
        print("✅ Added rejection_type column to bookings table")
        
        # Create indexes for performance
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_users_violations ON users(fake_booking_violations, is_banned)
        ''')
        print("✅ Created violation tracking index")
        
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_bookings_rejection_type ON bookings(rejection_type)
        ''')
        print("✅ Created rejection_type index")
        
        conn.commit()
        print("✅ Migration completed successfully!")
        
    except sqlite3.OperationalError as e:
        if "duplicate column name" in str(e):
            print("ℹ️  Columns already exist - migration not needed")
        else:
            print(f"❌ Migration error: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    migrate_violation_tracking()
