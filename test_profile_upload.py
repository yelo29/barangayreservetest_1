#!/usr/bin/env python3
"""
Test script for profile photo upload functionality
Tests the new profile photo upload endpoint we implemented
"""

import requests
import json
import os
from datetime import datetime

# Configuration
BASE_URL = "http://192.168.100.4:8000"
API_BASE = f"{BASE_URL}/api"

def test_server_connectivity():
    """Test basic server connectivity"""
    print("🔍 Testing server connectivity...")
    try:
        # Try the base URL first
        response = requests.get(BASE_URL, timeout=5)
        print(f"📥 Base URL check status: {response.status_code}")
        if response.status_code == 200:
            print("✅ Server is running and accessible")
            return True
        else:
            print("⚠️  Server responded but not with 200")
            # Still try to proceed with other tests
            return True
    except requests.exceptions.RequestException as e:
        print(f"❌ Server connectivity error: {e}")
        return False

def test_authentication():
    """Test authentication with a sample token"""
    print("\n🔐 Testing authentication...")
    
    # Test with the token from logs
    test_token = "7219f806-1881-4475-954c-1697cf3e551b"
    
    headers = {
        'Authorization': f'Bearer {test_token}',
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    
    try:
        response = requests.get(f"{API_BASE}/users/profile", headers=headers, timeout=5)
        print(f"📥 Auth test status: {response.status_code}")
        print(f"📥 Auth response: {response.text}")
        return response.status_code == 200
    except requests.exceptions.RequestException as e:
        print(f"❌ Authentication test error: {e}")
        return False

def test_profile_photo_endpoint():
    """Test the profile photo upload endpoint"""
    print("\n📤 Testing profile photo upload endpoint...")
    
    test_token = "7219f806-1881-4475-954c-1697cf3e551b"
    
    # Test with a small text file as "image"
    test_data = {
        'profile_photo': ('test.jpg', b'fake image data for testing', 'image/jpeg')
    }
    
    headers = {
        'Authorization': f'Bearer {test_token}',
        # Don't set Content-Type for multipart requests
    }
    
    try:
        response = requests.post(
            f"{API_BASE}/users/profile-photo",
            files=test_data,
            headers=headers,
            timeout=10
        )
        print(f"📥 Upload test status: {response.status_code}")
        print(f"📥 Upload response: {response.text}")
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print("✅ Profile photo upload endpoint works!")
                return True
            else:
                print(f"❌ Upload failed: {data.get('message', 'Unknown error')}")
                return False
        else:
            print(f"❌ Server error: HTTP {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Upload test error: {e}")
        return False

def test_profile_update_endpoint():
    """Test the profile update endpoint"""
    print("\n📝 Testing profile update endpoint...")
    
    test_token = "7219f806-1881-4475-954c-1697cf3e551b"
    
    profile_data = {
        'fullName': 'Test User Updated',
        'contactNumber': '0987654321',
        'address': '123 Updated Street, Test City'
    }
    
    headers = {
        'Authorization': f'Bearer {test_token}',
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    
    try:
        response = requests.put(
            f"{API_BASE}/users/profile",
            json=profile_data,
            headers=headers,
            timeout=10
        )
        print(f"📥 Profile update status: {response.status_code}")
        print(f"📥 Profile update response: {response.text}")
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print("✅ Profile update endpoint works!")
                return True
            else:
                print(f"❌ Update failed: {data.get('message', 'Unknown error')}")
                return False
        else:
            print(f"❌ Server error: HTTP {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Profile update test error: {e}")
        return False

def list_available_endpoints():
    """List all available endpoints on the server"""
    print("\n📋 Checking available endpoints...")
    
    common_endpoints = [
        "/api/health",
        "/api/users/profile",
        "/api/users/profile-photo",
        "/api/users/verification-status/test",
        "/api/facilities",
        "/api/auth/login",
        "/api/auth/register"
    ]
    
    for endpoint in common_endpoints:
        try:
            response = requests.get(f"{BASE_URL}{endpoint}", timeout=3)
            print(f"  {endpoint}: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"  {endpoint}: ERROR - {e}")

def main():
    """Run all tests"""
    print("🧪 TESTING PROFILE UPDATES FUNCTIONALITY")
    print("=" * 50)
    print(f"📅 Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🌐 Testing server: {BASE_URL}")
    print("=" * 50)
    
    # Test basic connectivity
    if not test_server_connectivity():
        print("\n❌ Server is not accessible. Please check:")
        print("  1. Server is running (python app.py)")
        print("  2. Server IP is correct (192.168.100.4:8000)")
        print("  3. No firewall blocking the connection")
        return
    
    # Test authentication
    if not test_authentication():
        print("\n❌ Authentication failed. Please check:")
        print("  1. Token is valid and not expired")
        print("  2. User exists in database")
        print("  3. Auth endpoint is working")
        return
    
    # Test profile photo upload
    upload_success = test_profile_photo_endpoint()
    
    # Test profile update
    update_success = test_profile_update_endpoint()
    
    # List available endpoints
    list_available_endpoints()
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 TEST SUMMARY")
    print("=" * 50)
    print(f"📤 Profile Photo Upload: {'✅ SUCCESS' if upload_success else '❌ FAILED'}")
    print(f"📝 Profile Update: {'✅ SUCCESS' if update_success else '❌ FAILED'}")
    
    if upload_success and update_success:
        print("\n🎉 ALL TESTS PASSED! The profile updates should work in the app.")
    else:
        print("\n⚠️  SOME TESTS FAILED. Check the server implementation.")
        print("💡 Make sure the server has the correct endpoints implemented.")

if __name__ == "__main__":
    main()
