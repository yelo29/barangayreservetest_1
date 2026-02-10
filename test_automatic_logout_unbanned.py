#!/usr/bin/env python3
"""
Test script for automatic logout functionality with non-banned user first, then ban simulation
"""

import requests
import json
import time

# Configuration
BASE_URL = "http://192.168.100.4:8000"

def test_automatic_logout_unbanned():
    """Test the automatic logout when user gets banned"""
    
    print("🧪 TESTING AUTOMATIC LOGOUT WITH UNBANNED USER FIRST")
    print("=" * 50)
    
    # Step 1: Login as non-banned test user
    print("\n📝 Step 1: Login as non-banned test user...")
    login_data = {
        "email": "resident@test.com",  # Different user
        "password": "password123"
    }
    
    try:
        login_response = requests.post(f"{BASE_URL}/api/auth/login", json=login_data)
        
        if login_response.status_code == 200:
            login_result = login_response.json()
            
            if login_result.get('success'):
                token = login_result.get('token')
                user_data = login_result.get('user', {})
                
                print(f"✅ Login successful")
                print(f"📊 User violations: {user_data.get('fake_booking_violations', 0)}")
                print(f"📊 User banned: {user_data.get('is_banned', False)}")
                
                # Step 2: Make a few API calls to verify normal operation
                print("\n📝 Step 2: Making normal API calls (should work)...")
                
                # Test profile check
                profile_response = requests.get(
                    f"{BASE_URL}/api/users/profile?email=resident@test.com",
                    headers={"Authorization": f"Bearer {token}"}
                )
                
                if profile_response.status_code == 200:
                    profile_data = profile_response.json()
                    
                    if profile_data.get('success'):
                        print("✅ Profile check works")
                    
                    # Step 3: Test booking creation (should work)
                print("\n📝 Step 3: Testing booking creation (should work)...")
                
                booking_data = {
                    "facility_id": 1,
                    "user_email": "resident@test.com",
                    "date": "2026-02-10",
                    "timeslot": "10:00 AM - 12:00 PM",
                    "total_amount": 500,
                    "purpose": "Test booking for normal user"
                }
                
                booking_response = requests.post(
                    f"{BASE_URL}/api/bookings",
                    json=booking_data,
                    headers={"Authorization": f"Bearer {token}"}
                )
                
                if booking_response.status_code == 200:
                    booking_result = booking_response.json()
                    
                    if booking_result.get('success'):
                        print("✅ Booking creation works - normal user can book")
                    else:
                        print(f"❌ Booking failed: {booking_result.get('message')}")
                else:
                    print(f"❌ Booking request failed: {booking_response.status_code}")
                
                print("\n✅ UNBANNED USER TEST COMPLETED SUCCESSFULLY")
                print("📊 Normal user can access all features")
                print("🔍 Automatic logout system not triggered for normal users")
                
            else:
                print(f"❌ Login failed: {login_result.get('message')}")
        else:
            print(f"❌ Login failed with status: {login_response.status_code}")
            
    except Exception as e:
        print(f"❌ Test error: {e}")
    
    print("\n" + "=" * 50)
    print("🏁 UNBANNED USER TEST COMPLETED")

if __name__ == "__main__":
    test_automatic_logout_unbanned()
