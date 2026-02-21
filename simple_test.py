#!/usr/bin/env python3
"""
Simple test for profile update endpoints
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
        
        print(f"{method.upper()} {endpoint}: {response.status_code}")
        if response.text.strip():
            print(f"  Response: {response.text[:200]}...")
        return response.status_code
    except Exception as e:
        print(f"{method.upper()} {endpoint}: ERROR - {e}")
        return None

def main():
    print("🔍 TESTING PROFILE UPDATE ENDPOINTS")
    print("=" * 40)
    
    test_token = "7219f806-1881-4475-954c-1697cf3e551b"
    
    # Test the specific endpoints we need
    print("Testing PUT /api/users/profile:")
    test_endpoint("PUT", "/users/profile", 
                  data={"fullName": "Test User", "contactNumber": "0987654321"}, 
                  token=test_token)
    
    print("\nTesting POST /api/users/profile-photo:")
    files = {"profile_photo": ("test.jpg", b"fake image data", "image/jpeg")}
    test_endpoint("POST", "/users/profile-photo", files=files, token=test_token)
    
    print("\nTesting GET /api/users/profile (should fail with 405):")
    test_endpoint("GET", "/users/profile", token=test_token)

if __name__ == "__main__":
    main()
