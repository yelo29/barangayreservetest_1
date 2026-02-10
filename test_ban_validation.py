#!/usr/bin/env python3
"""
Test script to verify ban validation implementation
Tests both booking creation and verification request endpoints
"""

import sqlite3
import requests
import json

DATABASE_PATH = 'server/barangay.db'
BASE_URL = 'http://localhost:8000'

def test_ban_validation():
    print("🧪 TESTING BAN VALIDATION IMPLEMENTATION")
    print("=" * 60)
    
    try:
        # Connect to database
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        
        # Step 1: Find a banned user or create one for testing
        print("\n📋 STEP 1: Find/Create banned user for testing")
        cursor.execute('SELECT id, email, is_banned, ban_reason FROM users WHERE is_banned = 1 LIMIT 1')
        banned_user = cursor.fetchone()
        
        if not banned_user:
            print("❌ No banned users found. Creating test banned user...")
            # Create a test banned user
            cursor.execute('''
                INSERT INTO users (email, full_name, password, role, is_banned, ban_reason, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', ('testbanned@barangay.com', 'Test Banned User', 'password123', 'resident', 1, 'Testing ban validation'))
            conn.commit()
            
            cursor.execute('SELECT id, email, is_banned, ban_reason FROM users WHERE email = ?', ('testbanned@barangay.com',))
            banned_user = cursor.fetchone()
            print(f"✅ Created test banned user: {banned_user[1]}")
        else:
            print(f"✅ Found existing banned user: {banned_user[1]} (Reason: {banned_user[3]})")
        
        user_id, user_email, is_banned, ban_reason = banned_user
        
        # Step 2: Test booking creation with banned user
        print("\n📋 STEP 2: Test booking creation with banned user")
        booking_data = {
            'facility_id': 1,
            'user_email': user_email,
            'date': '2026-02-28',
            'timeslot': '8:00 AM - 10:00 AM',
            'total_amount': '300',
            'status': 'pending'
        }
        
        try:
            response = requests.post(f'{BASE_URL}/api/bookings', json=booking_data)
            print(f"📊 Booking API Response Status: {response.status_code}")
            print(f"📊 Booking API Response: {response.text}")
            
            if response.status_code == 403:
                response_data = response.json()
                if response_data.get('error_type') == 'user_banned':
                    print("✅ SUCCESS: Banned user correctly blocked from booking!")
                    print(f"   Error message: {response_data.get('message')}")
                    print(f"   Ban reason: {response_data.get('ban_reason')}")
                else:
                    print("❌ UNEXPECTED: User blocked but not for ban reason")
            elif response.status_code == 200:
                print("❌ FAILURE: Banned user was allowed to create booking!")
            else:
                print(f"❌ UNEXPECTED: Status code {response.status_code}")
                
        except requests.exceptions.ConnectionError:
            print("⚠️  WARNING: Could not connect to server. Make sure server is running on localhost:5000")
            return
        except Exception as e:
            print(f"❌ ERROR: {e}")
        
        # Step 3: Test verification request with banned user
        print("\n📋 STEP 3: Test verification request with banned user")
        verification_data = {
            'residentId': user_id,
            'verificationType': 'resident',
            'userPhotoUrl': 'data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQ...',
            'validIdUrl': 'data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQ...',
            'address': 'Test Address'
        }
        
        try:
            response = requests.post(f'{BASE_URL}/api/verification-requests', json=verification_data)
            print(f"📊 Verification API Response Status: {response.status_code}")
            print(f"📊 Verification API Response: {response.text}")
            
            if response.status_code == 403:
                response_data = response.json()
                if response_data.get('error_type') == 'user_banned':
                    print("✅ SUCCESS: Banned user correctly blocked from verification!")
                    print(f"   Error message: {response_data.get('message')}")
                    print(f"   Ban reason: {response_data.get('ban_reason')}")
                else:
                    print("❌ UNEXPECTED: User blocked but not for ban reason")
            elif response.status_code == 200:
                print("❌ FAILURE: Banned user was allowed to submit verification!")
            else:
                print(f"❌ UNEXPECTED: Status code {response.status_code}")
                
        except requests.exceptions.ConnectionError:
            print("⚠️  WARNING: Could not connect to server. Make sure server is running on localhost:5000")
        except Exception as e:
            print(f"❌ ERROR: {e}")
        
        # Step 4: Test user status endpoint
        print("\n📋 STEP 4: Test user status endpoint")
        try:
            response = requests.get(f'{BASE_URL}/api/users/status/{user_email}')
            print(f"📊 Status API Response Status: {response.status_code}")
            print(f"📊 Status API Response: {response.text}")
            
            if response.status_code == 200:
                status_data = response.json()
                if status_data.get('is_banned') == True:
                    print("✅ SUCCESS: User status endpoint correctly reports banned status!")
                    print(f"   Is banned: {status_data.get('is_banned')}")
                    print(f"   Ban reason: {status_data.get('ban_reason')}")
                else:
                    print("❌ FAILURE: User status endpoint does not report banned status")
            else:
                print(f"❌ UNEXPECTED: Status code {response.status_code}")
                
        except requests.exceptions.ConnectionError:
            print("⚠️  WARNING: Could not connect to server. Make sure server is running on localhost:5000")
        except Exception as e:
            print(f"❌ ERROR: {e}")
        
        # Step 5: Test with non-banned user (should work)
        print("\n📋 STEP 5: Test with non-banned user (control test)")
        cursor.execute('SELECT id, email FROM users WHERE is_banned = 0 LIMIT 1')
        normal_user = cursor.fetchone()
        
        if normal_user:
            normal_user_id, normal_user_email = normal_user
            print(f"✅ Found normal user: {normal_user_email}")
            
            booking_data['user_email'] = normal_user_email
            try:
                response = requests.post(f'{BASE_URL}/api/bookings', json=booking_data)
                print(f"📊 Normal User Booking Status: {response.status_code}")
                
                if response.status_code == 200:
                    print("✅ SUCCESS: Normal user can create bookings!")
                elif response.status_code == 403:
                    print("❌ FAILURE: Normal user incorrectly blocked!")
                else:
                    print(f"❌ UNEXPECTED: Status code {response.status_code}")
                    
            except Exception as e:
                print(f"❌ ERROR: {e}")
        else:
            print("⚠️  WARNING: No normal users found for control test")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ DATABASE ERROR: {e}")
    
    print("\n" + "=" * 60)
    print("🎯 TEST SUMMARY:")
    print("   - Server should block banned users from bookings (403)")
    print("   - Server should block banned users from verification (403)")
    print("   - Server should report correct ban status (200)")
    print("   - Server should allow normal users (200)")
    print("   - Check server logs for ban validation messages")
    print("\n📱 CLIENT-SIDE TESTING:")
    print("   - Try booking in Flutter app with banned user")
    print("   - Try verification in Flutter app with banned user")
    print("   - Ban dialog should appear for banned users")
    print("   - Normal users should work normally")

if __name__ == "__main__":
    test_ban_validation()
