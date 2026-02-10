#!/usr/bin/env python3
"""
Test script for automatic logout functionality when user gets banned
"""

import requests
import json
import time

# Configuration
BASE_URL = "http://192.168.100.4:8000"

def test_automatic_logout():
    """Test the automatic logout when user gets banned"""
    
    print("🧪 TESTING AUTOMATIC LOGOUT FUNCTIONALITY")
    print("=" * 50)
    
    # Step 1: Login as test user
    print("\n📝 Step 1: Login as test user...")
    login_data = {
        "email": "papamo@gmail.com",
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
                
                # Step 2: Wait for periodic ban check to trigger
                print("\n📝 Step 2: Waiting 35 seconds for periodic ban check...")
                time.sleep(35)
                
                # Step 3: Make API call to trigger ban check
                print("\n📝 Step 3: Making API call to trigger ban detection...")
                
                # This should trigger the periodic ban check in the app
                profile_response = requests.get(
                    f"{BASE_URL}/api/users/profile?email=papamo@gmail.com",
                    headers={"Authorization": f"Bearer {token}"}
                )
                
                if profile_response.status_code == 200:
                    profile_data = profile_response.json()
                    
                    if profile_data.get('success'):
                        updated_user = profile_data.get('user', {})
                        is_banned = updated_user.get('is_banned', False)
                        
                        print(f"📊 Updated user violations: {updated_user.get('fake_booking_violations', 0)}")
                        print(f"📊 Updated user banned: {is_banned}")
                        
                        # Step 4: Try to make a booking (should be blocked if user is banned)
                        print("\n📝 Step 4: Attempting to create booking (should be blocked if banned)...")
                        
                        booking_data = {
                            "facility_id": 1,
                            "user_email": "papamo@gmail.com",
                            "date": "2026-02-10",
                            "timeslot": "10:00 AM - 12:00 PM",
                            "total_amount": 500,
                            "purpose": "Test booking after ban"
                        }
                        
                        booking_response = requests.post(
                            f"{BASE_URL}/api/bookings",
                            json=booking_data,
                            headers={"Authorization": f"Bearer {token}"}
                        )
                        
                        print(f"📊 Booking response status: {booking_response.status_code}")
                        
                        if booking_response.status_code == 200:
                            booking_result = booking_response.json()
                            
                            if booking_result.get('success'):
                                print("❌ UNEXPECTED: Booking succeeded despite user being banned!")
                                print(f"🚨 SECURITY ISSUE: Banned user was able to create booking")
                            else:
                                message = booking_result.get('message', 'No message')
                                print(f"✅ EXPECTED: Booking blocked: {message}")
                                
                                # Check if message mentions ban
                                if 'banned' in message.lower() or 'permanently banned' in message.lower():
                                    print("✅ Ban detection working: Booking blocked due to ban status")
                                else:
                                    print("⚠️  Booking blocked but ban reason unclear")
                        else:
                            print(f"📊 Booking response body: {booking_response.text}")
                    else:
                        print(f"❌ Profile check failed: {profile_response.status_code}")
                else:
                    print(f"❌ Profile check failed: {profile_data.get('error')}")
            else:
                print(f"❌ Login failed: {login_result.get('message')}")
        else:
            print(f"❌ Login failed with status: {login_response.status_code}")
            
    except Exception as e:
        print(f"❌ Test error: {e}")
    
    print("\n" + "=" * 50)
    print("🏁 TEST COMPLETED")

if __name__ == "__main__":
    test_automatic_logout()
