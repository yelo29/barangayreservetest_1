#!/usr/bin/env python3
"""
Comprehensive test for all profile update endpoints
Tests server implementation step by step
"""

import requests
import json
import os
import time

BASE_URL = "http://192.168.100.4:8000"
API_BASE = f"{BASE_URL}/api"

def test_endpoint(method, endpoint, data=None, files=None, token=None, expected_status=200):
    """Test a specific endpoint with detailed logging"""
    print(f"🧪 Testing {method.upper()} {endpoint}...")
    
    headers = {}
    if token:
        headers['Authorization'] = f'Bearer {token}'
    if not files:
        headers['Content-Type'] = 'application/json'
        headers['Accept'] = 'application/json'
    
    try:
        if method.upper() == 'GET':
            response = requests.get(f"{API_BASE}{endpoint}", headers=headers, timeout=10)
        elif method.upper() == 'POST':
            if files:
                response = requests.post(f"{API_BASE}{endpoint}", files=files, headers=headers, timeout=10)
            else:
                response = requests.post(f"{API_BASE}{endpoint}", json=data, headers=headers, timeout=10)
        elif method.upper() == 'PUT':
            response = requests.put(f"{API_BASE}{endpoint}", json=data, headers=headers, timeout=10)
        
        print(f"📥 Status: {response.status_code}")
        
        # Check if status matches expectation
        if response.status_code == expected_status:
            print(f"✅ {method.upper()} {endpoint} - SUCCESS")
            try:
                json_response = response.json()
                print(f"📥 Response: {json_response}")
                return True, json_response
            except:
                print(f"✅ {method.upper()} {endpoint} - SUCCESS (no JSON)")
                return True, {"success": True}
        else:
            print(f"❌ {method.upper()} {endpoint} - FAILED (expected {expected_status}, got {response.status_code})")
            try:
                error_response = response.json()
                print(f"❌ Error Response: {error_response}")
                return False, error_response
            except:
                print(f"❌ {method.upper()} {endpoint} - FAILED (expected {expected_status}, got {response.status_code})")
                print(f"❌ Raw Response: {response.text[:200]}...")
                return False, {"error": f"HTTP {response.status_code}"}
                
    except Exception as e:
        print(f"❌ {method.upper()} {endpoint}: ERROR - {e}")
        return False, {"error": str(e)}
        
    except requests.exceptions.RequestException as e:
        print(f"❌ {method.upper()} {endpoint}: NETWORK ERROR - {e}")
        return False, {"error": f"Network error: {e}"}

def test_profile_photo_upload():
    """Test profile photo upload with a real image file"""
    print("\n📸 Testing Profile Photo Upload (with real file)...")
    
    # Create a small test image file
    test_image_path = "test_upload.jpg"
    with open(test_image_path, 'wb') as f:
        f.write(b"fake image data for testing profile photo upload")
    
    test_token = "7219f806-1881-4475-954c-1697cf3e551b"
    
    files = {"profile_photo": (test_image_path, open(test_image_path, 'rb'), "image/jpeg")}
    
    success, response = test_endpoint("POST", "/users/profile-photo", files=files, token=test_token)
    
    if success:
        print("✅ Profile photo upload endpoint working with real file!")
    else:
        print(f"❌ Profile photo upload failed: {response}")
    
    # Clean up
    if os.path.exists(test_image_path):
        os.remove(test_image_path)

def test_profile_update():
    """Test profile update with complete data"""
    print("\n📝 Testing Profile Update (complete data)...")
    
    test_token = "7219f806-1881-4475-954c-1697cf3e551b"
    
    profile_data = {
        "fullName": "Test User Updated",
        "contactNumber": "0987654321",
        "address": "123 Updated Street, Test City"
    }
    
    success, response = test_endpoint("PUT", "/users/profile", data=profile_data, token=test_token)
    
    if success:
        print("✅ Profile update endpoint working!")
        return True
    else:
        print(f"❌ Profile update failed: {response}")
            return False

def test_profile_get():
    """Test profile retrieval with email parameter"""
    print("\n👤 Testing Profile Retrieval (with email)...")
    
    test_token = "7219f806-1881-4475-954c-1697cf3e551b"
    test_email = "resident01@gmail.com"
    
    success, response = test_endpoint("GET", f"/users/profile/{test_email}", token=test_token)
    
    if success:
        print("✅ Profile retrieval with email working!")
        return True
    else:
        print(f"❌ Profile retrieval failed: {response}")
            return False

def test_profile_get_no_params():
    """Test profile retrieval without email parameter (should fail)"""
    print("\n🔍 Testing Profile Retrieval (no params - should fail)...")
    
    test_token = "7219f806-1881-4475-954c-1697cf3e551b"
    
    success, response = test_endpoint("GET", "/users/profile", token=test_token)
    
    if success:
        print("❌ Profile retrieval without params should have failed but succeeded!")
        return False
    else:
        print("✅ Profile retrieval without params correctly failed")
            return True

def test_endpoints():
    """Test all endpoints systematically"""
    print("🧪 COMPREHENSIVE ENDPOINT TESTING")
    print("=" * 60)
    
    test_token = "7219f806-1881-4475-954c-1697cf3e551b"
    
    results = []
    
    # Test endpoints in logical order
    endpoints = [
        ("GET", "/api/health", None, None, test_token, 200),
        ("GET", "/api/users/profile", None, None, test_token, 200),
        ("GET", f"/api/users/profile/resident01@gmail.com", None, None, test_token, 200),
        ("GET", "/api/users/profile", None, None, test_token, 405), # Should fail - no email param
        ("PUT", "/api/users/profile", {"fullName": "Test"}, None, test_token, 200),
        ("POST", "/api/users/profile-photo", None, {"profile_photo": ("test.jpg", b"fake data")}, test_token, 200),
        ("POST", "/api/users/profile-photo", {"profile_photo": ("test.jpg", b"fake image data")}, test_token, 200),
        ("POST", "/api/users/profile-photo", {"profile_photo": ("test.jpg", b"fake data")}, test_token, 500), # Should fail - server error
        ("POST", "/api/users/profile-photo", {"profile_photo": ("test.jpg", b"fake data")}, test_token, 404), # Should fail - endpoint not implemented
    ]
    
    for method, endpoint, data, files, token, expected_status in endpoints:
        print(f"\n🧪 Testing {method.upper()} {endpoint}...")
        success, response = test_endpoint(method, endpoint, data, files, token, expected_status)
        status_icon = "✅" if success else "❌"
        print(f"{status_icon} {method.upper()} {endpoint}: {response.status_code if response else 'ERROR'}")
        
        results.append({
            'method': method.upper(),
            'endpoint': endpoint,
            'success': success,
            'status_code': response.status_code if response else None,
            'expected': expected_status
        })
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 TEST RESULTS SUMMARY")
    print("=" * 60)
    
    success_count = sum(1 for r in results if r['success'])
    total_tests = len(results)
    
    print(f"✅ SUCCESS: {success_count}/{total_tests}")
    print(f"❌ FAILED: {total_tests - success_count}")
    
    if success_count == len(results):
        print("\n🎉 ALL ENDPOINTS WORKING PERFECTLY!")
        return True
    else:
        print(f"\n⚠️  {total_tests - success_count} ENDPOINTS HAVE ISSUES")
        
        # Show failed endpoints
        failed = [r for r in results if not r['success']]
        if failed:
            print("\n❌ FAILED ENDPOINTS:")
            for f in failed:
                print(f"  - {f['method']} {f['endpoint']} (Status: {f['status_code']}, Expected: {f['expected']})")
        
        return False

def main():
    print("🧪 COMPREHENSIVE PROFILE UPDATE TESTING")
    print("=" * 60)
    print(f"📅 Test started at: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🌐 Testing server: {BASE_URL}")
    print("=" * 60)
    
    # Test server connectivity first
    print("🔍 Step 1: Testing server connectivity...")
    try:
        response = requests.get(BASE_URL, timeout=5)
        if response.status_code == 200:
            print("✅ Server is running and accessible")
        else:
            print(f"❌ Server responded with {response.status_code}")
            return
    except Exception as e:
        print(f"❌ Server connectivity error: {e}")
            return
    
    # Run comprehensive endpoint tests
    print("\n🧪 Step 2: Testing all endpoints...")
    success = test_endpoints()
    
    if success:
        print("\n🎉 ALL TESTS PASSED! The Flutter app should work perfectly!")
        print("\n📱 Ready for Flutter app testing!")
    else:
        print("\n⚠️ SOME TESTS FAILED. Server implementation needs fixes.")
        print("\n💡 Check server_implementation_guide.md for detailed steps.")

if __name__ == "__main__":
    main()
