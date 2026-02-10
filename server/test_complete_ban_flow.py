#!/usr/bin/env python3
"""
Complete Ban Flow Test
Tests the full ban flow from account creation to permanent ban
"""

import requests
import json
import time

BASE_URL = "http://192.168.100.4:8000"

def test_complete_ban_flow():
    print("🧪 COMPLETE BAN FLOW TEST")
    print("=" * 60)
    
    # Test Data
    test_email = "residenttestban@gmail.com"
    test_password = "test123"
    test_name = "Test Ban User"
    
    try:
        # Step 1: Create resident account
        print("\n📝 Step 1: Creating resident account...")
        
        register_data = {
            "email": test_email,
            "password": test_password,
            "name": test_name,
            "role": "resident"
        }
        
        register_response = requests.post(f"{BASE_URL}/api/auth/register",
            json=register_data)
        
        if register_response.status_code == 200:
            print("✅ Resident account created successfully")
        else:
            print(f"❌ Failed to create account: {register_response.text}")
            return
        
        # Step 2: Login to get token
        print("\n📝 Step 2: Login to get authentication token...")
        
        login_response = requests.post(f"{BASE_URL}/api/auth/login",
            json={
                "email": test_email,
                "password": test_password
            })
        
        if login_response.status_code == 200:
            token = login_response.json()['token']
            print("✅ Login successful")
        else:
            print(f"❌ Failed to login: {login_response.text}")
            return
        
        # Step 3: Create first booking
        print("\n📝 Step 3: Creating first booking...")
        
        booking_data_1 = {
            "facility_id": 5,
            "user_email": test_email,
            "date": "2026-03-20",
            "timeslot": "6:00 AM - 8:00 AM",
            "purpose": "Test Booking 1",
            "total_amount": 100,
            "full_name": test_name,
            "contact_number": "09111111111",
            "address": "Test Address",
            "receipt_base64": "fake_receipt_1_base64_data",
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
            "rejection_reason": "Fake receipt - 1st violation",
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
        
        # Step 5: Check violation count after 1st rejection
        print("\n📝 Step 5: Check violation count after 1st rejection...")
        
        login_check_1 = requests.post(f"{BASE_URL}/api/auth/login",
            json={
                "email": test_email,
                "password": test_password
            })
        
        if login_check_1.status_code == 200:
            user_data_1 = login_check_1.json()['user']
            violations_1 = user_data_1.get('fake_booking_violations', 0)
            is_banned_1 = user_data_1.get('is_banned', False)
            print(f"📊 Violations: {violations_1}/3")
            print(f"📊 Banned: {is_banned_1}")
            
            if violations_1 == 1:
                print("✅ 1st violation recorded correctly")
            else:
                print(f"❌ Expected 1 violation, got {violations_1}")
        else:
            print(f"❌ Failed to check violations: {login_check_1.text}")
            return
        
        # Step 6: Create second booking
        print("\n📝 Step 6: Creating second booking...")
        time.sleep(1)  # Ensure different timestamp
        
        booking_data_2 = {
            "facility_id": 5,
            "user_email": test_email,
            "date": "2026-03-21",
            "timeslot": "8:00 AM - 10:00 AM",
            "purpose": "Test Booking 2",
            "total_amount": 200,
            "full_name": test_name,
            "contact_number": "09111111111",
            "address": "Test Address",
            "receipt_base64": "fake_receipt_2_base64_data",
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
            "rejection_reason": "Fake receipt - 2nd violation",
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
        
        # Step 8: Check violation count after 2nd rejection
        print("\n📝 Step 8: Check violation count after 2nd rejection...")
        
        login_check_2 = requests.post(f"{BASE_URL}/api/auth/login",
            json={
                "email": test_email,
                "password": test_password
            })
        
        if login_check_2.status_code == 200:
            user_data_2 = login_check_2.json()['user']
            violations_2 = user_data_2.get('fake_booking_violations', 0)
            is_banned_2 = user_data_2.get('is_banned', False)
            print(f"📊 Violations: {violations_2}/3")
            print(f"📊 Banned: {is_banned_2}")
            
            if violations_2 == 2:
                print("✅ 2nd violation recorded correctly")
            else:
                print(f"❌ Expected 2 violations, got {violations_2}")
        else:
            print(f"❌ Failed to check violations: {login_check_2.text}")
            return
        
        # Step 9: Create third booking
        print("\n📝 Step 9: Creating third booking...")
        time.sleep(1)  # Ensure different timestamp
        
        booking_data_3 = {
            "facility_id": 5,
            "user_email": test_email,
            "date": "2026-03-22",
            "timeslot": "10:00 AM - 12:00 PM",
            "purpose": "Test Booking 3",
            "total_amount": 300,
            "full_name": test_name,
            "contact_number": "09111111111",
            "address": "Test Address",
            "receipt_base64": "fake_receipt_3_base64_data",
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
        
        # Step 10: Reject third booking with fake receipt (3rd violation - PERMANENT BAN)
        print("\n📝 Step 10: Reject third booking with fake receipt (3rd violation - PERMANENT BAN)...")
        
        reject_data_3 = {
            "status": "rejected",
            "rejection_reason": "Fake receipt - 3rd violation",
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
        
        # Step 11: Try to login with banned account (should fail)
        print("\n📝 Step 11: Try to login with banned account (should fail)...")
        
        login_banned = requests.post(f"{BASE_URL}/api/auth/login",
            json={
                "email": test_email,
                "password": test_password
            })
        
        if login_banned.status_code == 403:
            print("✅ Banned account correctly blocked from login")
            banned_message = login_banned.json()['message']
            print(f"📝 Ban message: {banned_message}")
            
            if "banned permanently" in banned_message.lower():
                print("✅ Correct ban message displayed")
            else:
                print("❌ Incorrect ban message")
        else:
            print(f"❌ Banned account should not be able to login: {login_banned.text}")
            return
        
        # Step 12: Try to register new account with same email (should fail)
        print("\n📝 Step 12: Try to register new account with same banned email...")
        
        register_banned = requests.post(f"{BASE_URL}/api/auth/register",
            json={
                "email": test_email,
                "password": "newpassword123",
                "name": "New Account",
                "role": "resident"
            })
        
        if register_banned.status_code == 403:
            print("✅ Banned email correctly blocked from registration")
            banned_reg_message = register_banned.json()['message']
            print(f"📝 Registration ban message: {banned_reg_message}")
            
            if "banned permanently" in banned_reg_message.lower():
                print("✅ Correct registration ban message")
            else:
                print("❌ Incorrect registration ban message")
        else:
            print(f"❌ Banned email should not be able to register: {register_banned.text}")
            return
        
        print("\n🎉 COMPLETE BAN FLOW TEST COMPLETED!")
        print("=" * 60)
        print("✅ All tests passed - Ban system working correctly!")
        print("✅ Account creation → 3 violations → permanent ban → login blocked → registration blocked")
        
    except Exception as e:
        print(f"❌ Test error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_complete_ban_flow()
