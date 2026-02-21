#!/usr/bin/env python3
"""
Test script to validate server endpoint implementations
"""

import requests
import json
import os

BASE_URL = "http://192.168.100.4:8000"
API_BASE = f"{BASE_URL}/api"

def test_endpoint(method, endpoint, data=None, files=None, token=None):
    """Test a specific endpoint"""
    headers = {}
    if token:
        headers['Authorization'] = f'Bearer {token}'
    if not files:
        headers['Content-Type'] = 'application/json'
        headers['Accept'] = 'application/json'
    
    try:
        if method.upper() == 'GET':
            response = requests.get(f"{API_BASE}{endpoint}", headers=headers, timeout=5)
        elif method.upper() == 'POST':
            if files:
                response = requests.post(f"{API_BASE}{endpoint}", files=files, headers=headers, timeout=10)
            else:
                response = requests.post(f"{API_BASE}{endpoint}", json=data, headers=headers, timeout=10)
        elif method.upper() == 'PUT':
            response = requests.put(f"{API_BASE}{endpoint}", json=data, headers=headers, timeout=10)
        
        print(f"{method.upper()} {endpoint}: {response.status_code}")
        if response.text.strip():
            try:
                json_response = response.json()
                print(f"  JSON: {json_response}")
                return response.status_code, json_response
            except:
                print(f"  Response: {response.text[:200]}...")
                return response.status_code, response.text
        return response.status_code, None
    except Exception as e:
        print(f"{method.upper()} {endpoint}: ERROR - {e}")
        return None, None

def main():
    print("🧪 TESTING SERVER ENDPOINT IMPLEMENTATIONS")
    print("=" * 50)
    
    test_token = "7219f806-1881-4475-954c-1697cf3e551b"
    
    # Test 1: Profile photo upload
    print("📸 Testing Profile Photo Upload:")
    files = {"profile_photo": ("test.jpg", b"fake image data", "image/jpeg")}
    status, response = test_endpoint("POST", "/users/profile-photo", files=files, token=test_token)
    
    if status == 200:
        print("✅ Profile photo upload endpoint working!")
    elif status == 404:
        print("❌ Profile photo endpoint not implemented yet")
    elif status == 500:
        print("❌ Profile photo endpoint has server error")
    
    # Test 2: Profile update
    print("\n📝 Testing Profile Update:")
    profile_data = {
        "fullName": "Test User Updated",
        "contactNumber": "0987654321", 
        "address": "123 Updated Street, Test City"
    }
    status, response = test_endpoint("PUT", "/users/profile", data=profile_data, token=test_token)
    
    if status == 200 and response and response.get('success'):
        print("✅ Profile update endpoint working!")
    elif status == 500:
        print("❌ Profile update endpoint has server error")
        if response:
            print(f"   Error: {response.get('message', 'Unknown error')}")
    elif status == 404:
        print("❌ Profile update endpoint not implemented yet")
    
    # Test 3: Profile retrieval
    print("\n👤 Testing Profile Retrieval:")
    status, response = test_endpoint("GET", "/users/profile", token=test_token)
    
    if status == 200 and response and response.get('success'):
        print("✅ Profile retrieval endpoint working!")
        user_data = response.get('data', {})
        print(f"   User: {user_data.get('fullName', 'Unknown')}")
        print(f"   Email: {user_data.get('email', 'Unknown')}")
    elif status == 405:
        print("⚠️  Profile retrieval only supports PUT/POST, not GET")
    elif status == 404:
        print("❌ Profile retrieval endpoint not implemented yet")
    
    print("\n" + "=" * 50)
    print("📊 TEST SUMMARY:")
    
    # Check if all endpoints are working
    endpoints_working = []
    
    # Re-test to get current status
    photo_status, _ = test_endpoint("POST", "/users/profile-photo", files=files, token=test_token)
    if photo_status == 200:
        endpoints_working.append("Profile Photo Upload")
    
    update_status, _ = test_endpoint("PUT", "/users/profile", data=profile_data, token=test_token)
    if update_status == 200:
        endpoints_working.append("Profile Update")
    
    get_status, _ = test_endpoint("GET", "/users/profile", token=test_token)
    if get_status == 200:
        endpoints_working.append("Profile Retrieval")
    
    print(f"✅ Working: {', '.join(endpoints_working) if endpoints_working else 'None'}")
    print(f"❌ Missing: {len(['Profile Photo Upload', 'Profile Update', 'Profile Retrieval']) - len(endpoints_working)} endpoints")
    
    if len(endpoints_working) == 3:
        print("\n🎉 ALL ENDPOINTS WORKING! The Flutter app should work perfectly!")
    elif len(endpoints_working) > 0:
        print(f"\n⚠️  {len(endpoints_working)}/3 endpoints working. Partial functionality available.")
    else:
        print("\n❌ No endpoints working. Server implementation needed.")

if __name__ == "__main__":
    main()
