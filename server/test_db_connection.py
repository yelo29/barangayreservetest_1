#!/usr/bin/env python3
"""
Test database connection for verification requests
"""

import sqlite3
from datetime import datetime
from config import Config

def test_verification_insert():
    try:
        conn = sqlite3.connect(Config.DATABASE_PATH)
        cursor = conn.cursor()
        
        # Test data
        test_data = {
            'residentId': 14,
            'verificationType': 'resident',
            'userPhotoUrl': '/9j/test_base64_data',
            'validIdUrl': '/9j/test_base64_data',
            'address': 'Test Address',
            'status': 'pending',
            'submittedAt': datetime.now().isoformat()
        }
        
        # Generate request reference
        request_ref = f"VR-{test_data['residentId']}-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        print(f"🔍 Generated request reference: {request_ref}")
        
        # Test insert
        cursor.execute('''
            INSERT INTO verification_requests 
            (request_reference, user_id, verification_type, requested_discount_rate, user_photo_base64, valid_id_base64, 
             residential_address, status, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            request_ref,
            test_data['residentId'],
            test_data['verificationType'],
            0.1 if test_data['verificationType'] == 'resident' else 0.05,  # Add discount rate
            test_data['userPhotoUrl'],
            test_data['validIdUrl'],
            test_data['address'],
            test_data['status'],
            test_data['submittedAt']
        ))
        
        conn.commit()
        
        # Verify insert
        cursor.execute('SELECT id, request_reference FROM verification_requests WHERE request_reference = ?', (request_ref,))
        result = cursor.fetchone()
        
        if result:
            print(f"✅ Test successful! Inserted record ID: {result[0]}, Reference: {result[1]}")
            # Clean up test record
            cursor.execute('DELETE FROM verification_requests WHERE request_reference = ?', (request_ref,))
            conn.commit()
            print("🧹 Test record cleaned up")
        else:
            print("❌ Test failed - record not found")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Testing database connection and verification insert...")
    test_verification_insert()
