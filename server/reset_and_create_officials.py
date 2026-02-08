#!/usr/bin/env python3
"""
Reset Database and Create Official Accounts
Clears all data and creates only the specified official accounts
"""

import sqlite3
import hashlib
from datetime import datetime
from config import Config

def reset_and_create_officials():
    conn = sqlite3.connect(Config.DATABASE_PATH)
    cursor = conn.cursor()
    
    print('🔄 RESETTING DATABASE AND CREATING OFFICIAL ACCOUNTS')
    print('=' * 60)
    
    # Clear all existing data
    tables_to_clear = ['bookings', 'verification_requests', 'user_sessions', 'users']
    for table in tables_to_clear:
        try:
            cursor.execute(f'DELETE FROM {table}')
            print(f'🗑️ Cleared {table}')
        except Exception as e:
            print(f'⚠️ Could not clear {table}: {e}')
    
    # Reset auto-increment
    cursor.execute('DELETE FROM sqlite_sequence WHERE name IN ("users", "bookings", "verification_requests")')
    
    # Official accounts data
    officials = [
        {
            'email': 'captain@barangay.gov',
            'password': 'tatalaPunongBarangayadmin',
            'full_name': 'Punong Barangay (Barangay Captain)',
            'role': 'official'
        },
        {
            'email': 'secretary@barangay.gov',
            'password': 'tatalaSecretaryadmin',
            'full_name': 'Barangay Secretary',
            'role': 'official'
        },
        {
            'email': 'administrator@barangay.gov',
            'password': 'tatalaAdministratoradmin',
            'full_name': 'Barangay Administrator',
            'role': 'official'
        },
        {
            'email': 'kagawad1@barangay.gov',
            'password': 'tatalaKagawad1admin',
            'full_name': 'Barangay Councilor (Bookings)',
            'role': 'official'
        },
        {
            'email': 'planning@barangay.gov',
            'password': 'tatalaPlanningOfficeradmin',
            'full_name': 'Barangay Planning Officer',
            'role': 'official'
        },
        {
            'email': 'utility@barangay.gov',
            'password': 'tatalaUtilityadmin',
            'full_name': 'Barangay Utility Worker',
            'role': 'official'
        }
    ]
    
    print(f'\n👤 CREATING {len(officials)} OFFICIAL ACCOUNTS')
    
    # Insert official accounts
    for official in officials:
        # Hash password
        password_hash = hashlib.sha256(official['password'].encode()).hexdigest()
        
        # Insert user with correct structure
        cursor.execute('''
            INSERT INTO users (
                email, 
                password_hash, 
                full_name, 
                role, 
                verified, 
                is_active,
                created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            official['email'],
            password_hash,
            official['full_name'],
            official['role'],
            1,  # verified
            1,  # is_active
            datetime.now().isoformat()
        ))
        
        print(f'✅ Created: {official["email"]}')
    
    # Keep existing facilities and time slots
    cursor.execute('SELECT COUNT(*) FROM facilities')
    facility_count = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM time_slots')
    timeslot_count = cursor.fetchone()[0]
    
    print(f'\n🏢 FACILITIES: {facility_count} facilities preserved')
    print(f'⏰ TIME SLOTS: {timeslot_count} time slots preserved')
    
    conn.commit()
    conn.close()
    
    print('\n🎯 DATABASE RESET COMPLETE')
    print('=' * 40)
    print('📋 Official Accounts Created:')
    for official in officials:
        print(f'  📧 {official["email"]}')
        print(f'     🔑 Password: {official["password"]}')
        print(f'     👤 Name: {official["full_name"]}')
        print(f'     🎭 Role: {official["role"]}')
        print()
    
    print('✅ Ready for testing!')
    print('📱 You can now login with any of these official accounts')

if __name__ == '__main__':
    reset_and_create_officials()
