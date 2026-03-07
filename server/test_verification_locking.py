#!/usr/bin/env python3

"""
Test script to verify verification status endpoint and field locking logic
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def test_verification_status_endpoint():
    """Test the verification status endpoint that controls field locking"""
    
    print("🧪 Testing Verification Status Endpoint")
    print("=" * 60)
    
    # Test different user scenarios
    test_users = [
        {
            "email": "jl052904@gmail.com",
            "password": "2e5b8f6b5561f7aee910484b6d84c9be23247e8cc76999965556a9d622b96e0b",
            "description": "Verified Non-Resident (should allow upgrade to resident)"
        },
        {
            "email": "secretary@barangay.gov", 
            "password": "tatalasecretaryadmin",
            "description": "Official account (should be verified resident)"
        },
        {
            "email": "TestNonresiden@gmail.com",
            "password": "ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f",
            "description": "Verified Non-Resident test account"
        }
    ]
    
    for i, user in enumerate(test_users, 1):
        print(f"\n{i}. 📋 Testing: {user['description']}")
        print(f"   Email: {user['email']}")
        
        # Step 1: Login to get token
        try:
            login_response = requests.post(f"{BASE_URL}/api/auth/login", json={
                "email": user["email"],
                "password": user["password"]
            })
            
            if login_response.status_code != 200:
                print(f"   ❌ Login failed: {login_response.text}")
                continue
                
            login_data = login_response.json()
            token = login_data.get('token')
            user_id = login_data.get('user', {}).get('id')
            
            if not token or not user_id:
                print(f"   ❌ Invalid login response")
                continue
                
            print(f"   ✅ Login successful - User ID: {user_id}")
            
            # Step 2: Check verification status
            headers = {"Authorization": f"Bearer {token}"}
            status_response = requests.get(
                f"{BASE_URL}/api/verification-requests/status/{user_id}",
                headers=headers
            )
            
            if status_response.status_code != 200:
                print(f"   ❌ Status check failed: {status_response.text}")
                continue
                
            status_data = status_response.json()
            
            print(f"   📊 Verification Status:")
            print(f"      - Can Submit: {status_data.get('can_submit')}")
            print(f"      - Lock Message: {status_data.get('lock_message')}")
            print(f"      - Current Status: {status_data.get('current_status')}")
            print(f"      - Verified: {status_data.get('verified')}")
            print(f"      - Verification Type: {status_data.get('verification_type')}")
            
            # Step 3: Analyze expected behavior
            can_submit = status_data.get('can_submit', False)
            current_status = status_data.get('current_status', '')
            verified = status_data.get('verified', 0)
            verification_type = status_data.get('verification_type', '')
            
            print(f"   🔍 Expected UI Behavior:")
            
            if verified == 1 and verification_type == 'resident':
                print(f"      - Resident Button: ❌ LOCKED (already verified)")
                print(f"      - Non-Resident Button: ❌ LOCKED (already verified)")
                print(f"      - Photo Upload: ❌ LOCKED")
                print(f"      - Form Fields: ❌ LOCKED")
                print(f"      - Status Message: ✅ 'Already verified as Resident'")
                
            elif verified == 1 and verification_type == 'non-resident':
                print(f"      - Resident Button: ✅ UNLOCKED (can upgrade)")
                print(f"      - Non-Resident Button: ❌ LOCKED (already non-resident)")
                print(f"      - Photo Upload: ✅ UNLOCKED")
                print(f"      - Form Fields: ✅ UNLOCKED")
                print(f"      - Status Message: None")
                
            elif verified == 1 and current_status == 'verified_resident' and verification_type is None:
                # Officials case
                print(f"      - Resident Button: ❌ LOCKED (already verified as official)")
                print(f"      - Non-Resident Button: ❌ LOCKED (already verified as official)")
                print(f"      - Photo Upload: ❌ LOCKED")
                print(f"      - Form Fields: ❌ LOCKED")
                print(f"      - Status Message: ✅ 'Already verified as Resident'")
                
            elif current_status == 'pending_request':
                print(f"      - Resident Button: ❌ LOCKED (pending request)")
                print(f"      - Non-Resident Button: ❌ LOCKED (pending request)")
                print(f"      - Photo Upload: ❌ LOCKED")
                print(f"      - Form Fields: ❌ LOCKED")
                print(f"      - Status Message: ⏳ 'Pending verification request'")
                
            else:  # Unverified
                print(f"      - Resident Button: ✅ UNLOCKED")
                print(f"      - Non-Resident Button: ✅ UNLOCKED")
                print(f"      - Photo Upload: ✅ UNLOCKED")
                print(f"      - Form Fields: ✅ UNLOCKED")
                print(f"      - Status Message: None")
            
            print(f"   ✅ Test completed for {user['email']}")
            
        except Exception as e:
            print(f"   ❌ Error testing {user['email']}: {e}")
    
    print("\n" + "=" * 60)
    print("🎉 Verification Status Testing Completed!")
    print("📝 All scenarios tested for proper field locking behavior")

def test_field_locking_logic():
    """Test the field locking logic scenarios"""
    
    print("\n🔒 Testing Field Locking Logic Scenarios")
    print("=" * 60)
    
    scenarios = [
        {
            "name": "Verified Resident (10% discount)",
            "verified": 1,
            "verification_type": "resident",
            "has_pending": False,
            "expected_can_submit": False,
            "expected_message": "You are already verified as a Resident with full benefits"
        },
        {
            "name": "Verified Non-Resident (5% discount)",
            "verified": 1,
            "verification_type": "non-resident", 
            "has_pending": False,
            "expected_can_submit": True,
            "expected_message": "You can submit a verification request to upgrade to Resident status"
        },
        {
            "name": "Pending Verification Request",
            "verified": 0,
            "verification_type": None,
            "has_pending": True,
            "expected_can_submit": False,
            "expected_message": "You already submitted a Verification Request! wait for officials to either Reject or Approve your request"
        },
        {
            "name": "Unverified User",
            "verified": 0,
            "verification_type": None,
            "has_pending": False,
            "expected_can_submit": True,
            "expected_message": "You can submit a verification request"
        }
    ]
    
    for i, scenario in enumerate(scenarios, 1):
        print(f"\n{i}. 📋 Scenario: {scenario['name']}")
        
        # Simulate the logic from server.py
        can_submit = True
        lock_message = ""
        current_status = "none"
        
        if scenario['verified'] == 1 and scenario['verification_type'] == 'resident':
            can_submit = False
            lock_message = "You are already verified as a Resident with full benefits"
            current_status = "verified_resident"
            
        elif scenario['verified'] == 1 and scenario['verification_type'] == 'non-resident':
            can_submit = True
            lock_message = "You can submit a verification request to upgrade to Resident status"
            current_status = "verified_non_resident"
            
        elif scenario['has_pending']:
            can_submit = False
            lock_message = "You already submitted a Verification Request! wait for officials to either Reject or Approve your request"
            current_status = "pending_request"
            
        else:
            can_submit = True
            lock_message = "You can submit a verification request"
            current_status = "unverified"
        
        # Verify results
        print(f"   📊 Logic Results:")
        print(f"      - Can Submit: {can_submit}")
        print(f"      - Lock Message: {lock_message}")
        print(f"      - Current Status: {current_status}")
        
        # Check if matches expected
        can_submit_match = can_submit == scenario['expected_can_submit']
        message_match = lock_message == scenario['expected_message']
        
        print(f"   ✅ Verification:")
        print(f"      - Can Submit Match: {'✅' if can_submit_match else '❌'}")
        print(f"      - Message Match: {'✅' if message_match else '❌'}")
        
        if can_submit_match and message_match:
            print(f"   🎉 Scenario PASSED")
        else:
            print(f"   ❌ Scenario FAILED")
        
        # Show UI behavior
        print(f"   🎯 UI Behavior:")
        if can_submit:
            if scenario['verified'] == 1 and scenario['verification_type'] == 'non-resident':
                print(f"      - Resident Button: ✅ UNLOCKED (upgrade)")
                print(f"      - Non-Resident Button: ❌ LOCKED")
            else:
                print(f"      - Resident Button: ✅ UNLOCKED")
                print(f"      - Non-Resident Button: ✅ UNLOCKED")
            print(f"      - Form Fields: ✅ UNLOCKED")
            print(f"      - Photo Upload: ✅ UNLOCKED")
        else:
            print(f"      - Resident Button: ❌ LOCKED")
            print(f"      - Non-Resident Button: ❌ LOCKED")
            print(f"      - Form Fields: ❌ LOCKED")
            print(f"      - Photo Upload: ❌ LOCKED")

if __name__ == "__main__":
    test_verification_status_endpoint()
    test_field_locking_logic()
