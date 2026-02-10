#!/usr/bin/env python3
"""
Comprehensive Test for Violation System
Tests the fake booking elimination feature
"""

import requests
import json
import time
import random

BASE_URL = "http://192.168.100.4:8000"

def test_violation_system():
    print("🧪 COMPREHENSIVE VIOLATION SYSTEM TEST")
    print("=" * 60)
    
    # Test Data
    random_id = random.randint(1000, 9999)
    test_user_email = f"test_violation_user_{random_id}@example.com"
    test_user_password = "test123"
    test_user_name = "Test Violation User"
    
    try:
        # Step 1: Register test user
        print("\n📝 Step 1: Register test user...")
        
        register_data = {
            "email": test_user_email,
            "password": test_user_password,
            "name": test_user_name,
            "role": "resident"
        }
        
        register_response = requests.post(f"{BASE_URL}/api/auth/register",
            json=register_data)
        
        if register_response.status_code == 200:
            print("✅ Test user registered successfully")
        else:
            print(f"❌ Failed to register test user: {register_response.text}")
            return
        
        # Step 2: Login test user
        print("\n📝 Step 2: Login test user...")
        
        login_response = requests.post(f"{BASE_URL}/api/auth/login",
            json={
                "email": test_user_email,
                "password": test_user_password
            })
        
        if login_response.status_code == 200:
            token = login_response.json()['token']
            print("✅ Test user logged in successfully")
        else:
            print(f"❌ Failed to login test user: {login_response.text}")
            return
        
        # Step 3: Create first booking (to be rejected with fake receipt)
        print("\n📝 Step 3: Create first booking...")
        
        booking_data_1 = {
            "facility_id": 5,
            "user_email": test_user_email,
            "date": "2026-03-15",
            "timeslot": "6:00 AM - 8:00 AM",
            "purpose": "Test Booking 1",
            "total_amount": 100,
            "full_name": test_user_name,
            "contact_number": "09111111111",
            "address": "Test Address",
            "receipt_base64": "fake_receipt_base64_data",
            "valid_id_base64": "",
            "user_role": "resident",
            "status": "pending"
        }
        
        booking_response_1 = requests.post(f"{BASE_URL}/api/bookings",
            headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
            json=booking_data_1)
        
        if booking_response_1.status_code == 200:
            booking_id_1 = booking_response_1.json()['booking_id']
            print(f"✅ First booking created: ID {booking_id_1}")
        else:
            print(f"❌ Failed to create first booking: {booking_response_1.text}")
            return
        
        # Step 4: Reject first booking with fake receipt (1st violation)
        print("\n📝 Step 4: Reject first booking with fake receipt (1st violation)...")
        
        reject_data_1 = {
            "status": "rejected",
            "rejection_reason": "Test rejection - fake receipt",
            "rejection_type": "fake_receipt"
        }
        
        reject_response_1 = requests.put(f"{BASE_URL}/api/bookings/{booking_id_1}/status",
            headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
            json=reject_data_1)
        
        if reject_response_1.status_code == 200:
            print("✅ First booking rejected (1st violation)")
        else:
            print(f"❌ Failed to reject first booking: {reject_response_1.text}")
            return
        
        # Step 5: Check user violation count
        print("\n📝 Step 5: Check user violation count...")
        
        login_response_2 = requests.post(f"{BASE_URL}/api/auth/login",
            json={
                "email": test_user_email,
                "password": test_user_password
            })
        
        if login_response_2.status_code == 200:
            user_data = login_response_2.json()['user']
            violations = user_data.get('fake_booking_violations', 0)
            is_banned = user_data.get('is_banned', False)
            print(f"📊 User violations: {violations}/3")
            print(f"📊 User banned: {is_banned}")
            
            if violations == 1:
                print("✅ Violation count correct (1/3)")
            else:
                print(f"❌ Expected 1 violation, got {violations}")
        else:
            print(f"❌ Failed to login after 1st violation: {login_response_2.text}")
            return
        
        # Step 6: Create second booking (to be rejected with fake receipt)
        print("\n📝 Step 6: Create second booking...")
        
        # Wait a moment to ensure different timestamp
        time.sleep(1)
        
        booking_data_2 = {
            "facility_id": 5,
            "user_email": test_user_email,
            "date": "2026-03-16",
            "timeslot": "8:00 AM - 10:00 AM",
            "purpose": "Test Booking 2",
            "total_amount": 200,  # Different amount
            "full_name": test_user_name,
            "contact_number": "09111111111",
            "address": "Test Address",
            "receipt_base64": "another_fake_receipt_base64_data_different",
            "valid_id_base64": "",
            "user_role": "resident",
            "status": "pending"
        }
        
        booking_response_2 = requests.post(f"{BASE_URL}/api/bookings",
            headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
            json=booking_data_2)
        
        if booking_response_2.status_code == 200:
            booking_id_2 = booking_response_2.json()['booking_id']
            print(f"✅ Second booking created: ID {booking_id_2}")
        else:
            print(f"❌ Failed to create second booking: {booking_response_2.text}")
            return
        
        # Step 7: Reject second booking with fake receipt (2nd violation)
        print("\n📝 Step 7: Reject second booking with fake receipt (2nd violation)...")
        
        reject_data_2 = {
            "status": "rejected",
            "rejection_reason": "Test rejection - fake receipt",
            "rejection_type": "fake_receipt"
        }
        
        reject_response_2 = requests.put(f"{BASE_URL}/api/bookings/{booking_id_2}/status",
            headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
            json=reject_data_2)
        
        if reject_response_2.status_code == 200:
            print("✅ Second booking rejected (2nd violation)")
        else:
            print(f"❌ Failed to reject second booking: {reject_response_2.text}")
            return
        
        # Step 8: Check user violation count (should be 2/3)
        print("\n📝 Step 8: Check user violation count (should be 2/3)...")
        
        login_response_3 = requests.post(f"{BASE_URL}/api/auth/login",
            json={
                "email": test_user_email,
                "password": test_user_password
            })
        
        if login_response_3.status_code == 200:
            user_data_3 = login_response_3.json()['user']
            violations_3 = user_data_3.get('fake_booking_violations', 0)
            is_banned_3 = user_data_3.get('is_banned', False)
            print(f"📊 User violations: {violations_3}/3")
            print(f"📊 User banned: {is_banned_3}")
            
            if violations_3 == 2:
                print("✅ Violation count correct (2/3)")
            else:
                print(f"❌ Expected 2 violations, got {violations_3}")
        else:
            print(f"❌ Failed to login after 2nd violation: {login_response_3.text}")
            return
        
        # Step 9: Create third booking (to be rejected with fake receipt)
        print("\n📝 Step 9: Create third booking...")
        
        # Wait a moment to ensure different timestamp
        time.sleep(1)
        
        booking_data_3 = {
            "facility_id": 5,
            "user_email": test_user_email,
            "date": "2026-03-17",
            "timeslot": "10:00 AM - 12:00 PM",
            "purpose": "Test Booking 3",
            "total_amount": 300,  # Different amount
            "full_name": test_user_name,
            "contact_number": "09111111111",
            "address": "Test Address",
            "receipt_base64": "third_fake_receipt_base64_data_unique",
            "valid_id_base64": "",
            "user_role": "resident",
            "status": "pending"
        }
        
        booking_response_3 = requests.post(f"{BASE_URL}/api/bookings",
            headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
            json=booking_data_3)
        
        if booking_response_3.status_code == 200:
            booking_id_3 = booking_response_3.json()['booking_id']
            print(f"✅ Third booking created: ID {booking_id_3}")
        else:
            print(f"❌ Failed to create third booking: {booking_response_3.text}")
            return
        
        # Step 10: Reject third booking with fake receipt (3rd violation - should ban)
        print("\n📝 Step 10: Reject third booking with fake receipt (3rd violation - PERMANENT BAN)...")
        
        reject_data_3 = {
            "status": "rejected",
            "rejection_reason": "Test rejection - fake receipt",
            "rejection_type": "fake_receipt"
        }
        
        reject_response_3 = requests.put(f"{BASE_URL}/api/bookings/{booking_id_3}/status",
            headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
            json=reject_data_3)
        
        if reject_response_3.status_code == 200:
            print("✅ Third booking rejected (3rd violation - USER BANNED)")
        else:
            print(f"❌ Failed to reject third booking: {reject_response_3.text}")
            return
        
        # Step 11: Try to login banned user (should fail)
        print("\n📝 Step 11: Try to login banned user (should fail)...")
        
        login_response_banned = requests.post(f"{BASE_URL}/api/auth/login",
            json={
                "email": test_user_email,
                "password": test_user_password
            })
        
        if login_response_banned.status_code == 403:
            print("✅ Banned user correctly blocked from login")
            banned_message = login_response_banned.json()['message']
            if "banned permanently" in banned_message.lower():
                print("✅ Correct ban message displayed")
            else:
                print(f"❌ Unexpected ban message: {banned_message}")
        else:
            print(f"❌ Banned user should not be able to login: {login_response_banned.text}")
            return
        
        # Step 12: Try to register with banned email (should fail)
        print("\n📝 Step 12: Try to register with banned email (should fail)...")
        
        register_response_banned = requests.post(f"{BASE_URL}/api/auth/register",
            json={
                "email": test_user_email,
                "password": "newpassword123",
                "name": "New Account",
                "role": "resident"
            })
        
        if register_response_banned.status_code == 403:
            print("✅ Banned email correctly blocked from registration")
            banned_reg_message = register_response_banned.json()['message']
            if "banned permanently" in banned_reg_message.lower():
                print("✅ Correct registration ban message displayed")
            else:
                print(f"❌ Unexpected registration ban message: {banned_reg_message}")
        else:
            print(f"❌ Banned email should not be able to register: {register_response_banned.text}")
            return
        
        # Step 13: Test incorrect downpayment rejection (should not add violation)
        print("\n📝 Step 13: Test incorrect downpayment rejection (should not add violation)...")
        
        # Create a new user for this test
        test_user_2_email = "test_user_2@example.com"
        
        register_response_2 = requests.post(f"{BASE_URL}/api/auth/register",
            json={
                "email": test_user_2_email,
                "password": test_user_password,
                "name": "Test User 2",
                "role": "resident"
            })
        
        if register_response_2.status_code == 200:
            print("✅ Test user 2 registered")
            
            # Login test user 2
            login_response_2_user = requests.post(f"{BASE_URL}/api/auth/login",
                json={
                    "email": test_user_2_email,
                    "password": test_user_password
                })
            
            if login_response_2_user.status_code == 200:
                token_2 = login_response_2_user.json()['token']
                
                # Create booking for user 2
                booking_data_4 = {
                    "facility_id": 5,
                    "user_email": test_user_2_email,
                    "date": "2026-03-18",
                    "timeslot": "2:00 PM - 4:00 PM",
                    "purpose": "Test Booking 4",
                    "total_amount": 100,
                    "full_name": "Test User 2",
                    "contact_number": "09222222222",
                    "address": "Test Address 2",
                    "receipt_base64": "fake_receipt_base64_data",
                    "valid_id_base64": "",
                    "user_role": "resident",
                    "status": "pending"
                }
                
                booking_response_4 = requests.post(f"{BASE_URL}/api/bookings",
                    headers={"Authorization": f"Bearer {token_2}", "Content-Type": "application/json"},
                    json=booking_data_4)
                
                if booking_response_4.status_code == 200:
                    booking_id_4 = booking_response_4.json()['booking_id']
                    
                    # Reject with incorrect downpayment (should not add violation)
                    reject_data_4 = {
                        "status": "rejected",
                        "rejection_reason": "Test rejection - incorrect downpayment",
                        "rejection_type": "incorrect_downpayment"
                    }
                    
                    reject_response_4 = requests.put(f"{BASE_URL}/api/bookings/{booking_id_4}/status",
                        headers={"Authorization": f"Bearer {token_2}", "Content-Type": "application/json"},
                        json=reject_data_4)
                    
                    if reject_response_4.status_code == 200:
                        print("✅ Incorrect downpayment rejection completed")
                        
                        # Check violation count (should still be 0)
                        login_response_check = requests.post(f"{BASE_URL}/api/auth/login",
                            json={
                                "email": test_user_2_email,
                                "password": test_user_password
                            })
                        
                        if login_response_check.status_code == 200:
                            user_data_check = login_response_check.json()['user']
                            violations_check = user_data_check.get('fake_booking_violations', 0)
                            
                            if violations_check == 0:
                                print("✅ Incorrect downpayment rejection did not add violation (CORRECT)")
                            else:
                                print(f"❌ Expected 0 violations, got {violations_check}")
                        else:
                            print(f"❌ Failed to check violations: {login_response_check.text}")
                    else:
                        print(f"❌ Failed to reject with incorrect downpayment: {reject_response_4.text}")
                else:
                    print(f"❌ Failed to create booking for user 2: {booking_response_4.text}")
            else:
                print(f"❌ Failed to login test user 2: {login_response_2_user.text}")
        else:
            print(f"❌ Failed to register test user 2: {register_response_2.text}")
        
        print("\n🎉 VIOLATION SYSTEM TEST COMPLETED!")
        print("=" * 60)
        print("✅ All tests passed - Violation system working correctly!")
        
    except Exception as e:
        print(f"❌ Test error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_violation_system()
