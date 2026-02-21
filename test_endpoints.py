#!/usr/bin/env python3
"""
Test specific endpoints for profile updates
"""

import requests
import json

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
        elif method.upper() == 'DELETE':
            response = requests.delete(f"{API_BASE}{endpoint}", headers=headers, timeout=5)
        
        print(f"{method.upper()} {endpoint}: {response.status_code}")
        if response.text.strip():
            print(f"  Response: {response.text[:200]}...")
        return response.status_code, response.text
    except Exception as e:
        print(f"{method.upper()} {endpoint}: ERROR - {e}")
        return None, str(e)

def main():
    print("🔍 TESTING SPECIFIC ENDPOINTS")
    print("=" * 40)
    
    test_token = "7219f806-1881-4475-954c-1697cf3e551b"
    
    # Test endpoints we need
    endpoints_to_test = [
        # Profile update endpoints
        ("GET", "/users/profile", None, None, test_token),
        ("PUT", "/users/profile", {"fullName": "Test User"}, None, test_token),
        
        # Profile photo upload
        ("POST", "/users/profile-photo", None, {"profile_photo": ("test.jpg", b"fake data", "image/jpeg")}, test_token),
        
        # Auth endpoints
        ("POST", "/auth/login", {"email": "test@test.com", "password": "test"}, None, None),
        ("POST", "/auth/register", {"email": "test2@test.com", "password": "test", "fullName": "Test User"}, None, None),
        
        # Verification endpoints
        ("GET", "/users/verification-status/test", None, None, test_token),
        ("POST", "/users/verification-request", {"residentId": "1", "fullName": "Test User"}, None, test_token),
        
        # Facilities
        ("GET", "/facilities", None, None, test_token),
        ("POST", "/facilities", {"name": "Test Facility"}, None, test_token),
    ]
    
    results = []
    for method, endpoint, data, files, token in endpoints_to_test:
        status_code, response_text = test_endpoint(method, endpoint, data, files, token)
        results.append((method, endpoint, status_code))
    
    print("\n" + "=" * 40)
    print("📊 ENDPOINT TEST RESULTS")
    print("=" * 40)
    
    for method, endpoint, status_code in results:
        status_icon = "✅" if status_code == 200 else "❌" if status_code and status_code >= 400 else "⚠️"
        print(f"{status_icon} {method:8} {endpoint:20} - {status_code or 'ERROR'}")
    
    # Check specifically for our needed endpoints
    needed_endpoints = [
        ("PUT", "/users/profile"),
        ("POST", "/users/profile-photo"),
    ]
    
    print(f"\n🎯 NEEDED ENDPOINTS FOR PROFILE UPDATES:")
    all_good = True
    for needed_method, needed_endpoint in needed_endpoints:
        found = False
        for test_method, test_endpoint, status_code in results:
            if test_method == needed_method and test_endpoint == needed_endpoint:
                found = True
                if status_code == 200:
                    print(f"✅ {needed_method} {needed_endpoint} - WORKING")
                else:
                    print(f"❌ {needed_method} {needed_endpoint} - FAILED ({status_code})")
                    all_good = False
                break
        if not found:
            print(f"❌ {needed_method} {needed_endpoint} - NOT FOUND")
            all_good = False
    
    if all_good:
        print("\n🎉 ALL NEEDED ENDPOINTS ARE WORKING!")
    else:
        print("\n⚠️  SOME NEEDED ENDPOINTS ARE MISSING OR BROKEN")
        print("💡 The server needs to implement these endpoints properly.")

if __name__ == "__main__":
    main()
