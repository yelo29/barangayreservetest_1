#!/usr/bin/env python3
"""
Test server endpoints to verify they work
"""

import requests
import json

def test_server():
    base_url = "http://192.168.100.4:8080"
    
    print("🧪 Testing Server Endpoints")
    print("=" * 40)
    print(f"📡 Server URL: {base_url}")
    print()
    
    # Test 1: Basic API test
    print("1. Testing basic API...")
    try:
        response = requests.get(f"{base_url}/api/me?email=test@example.com", timeout=5)
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.text}")
    except Exception as e:
        print(f"   Error: {e}")
    
    print()
    
    # Test 2: Login endpoint
    print("2. Testing login endpoint...")
    try:
        login_data = {
            "email": "leo052904@gmail.com",
            "password": "password123"  # Common test password
        }
        response = requests.post(f"{base_url}/api/login", json=login_data, timeout=5)
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.text}")
    except Exception as e:
        print(f"   Error: {e}")
    
    print()
    
    # Test 3: Check if user exists
    print("3. Checking if user exists...")
    try:
        response = requests.get(f"{base_url}/api/me?email=leo052904@gmail.com", timeout=5)
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.text}")
    except Exception as e:
        print(f"   Error: {e}")

if __name__ == "__main__":
    test_server()
