#!/usr/bin/env python3
"""
Test Verification Requests Endpoint
Check if verification requests are being created and fetched correctly
"""

import requests
import json

def test_verification_requests():
    base_url = "http://192.168.18.12:8000"
    
    print("Testing Verification Requests Endpoint")
    print("=" * 50)
    
    # Test 1: Check server health
    try:
        response = requests.get(f"{base_url}/health", timeout=5)
        print(f"[{'PASS' if response.status_code == 200 else 'FAIL'}] Server Health: {response.status_code}")
    except Exception as e:
        print(f"[FAIL] Server Health: {str(e)}")
        return
    
    # Test 2: Try to login as official
    token = None
    try:
        login_data = {"email": "testofficial@example.com", "password": "official123456"}
        response = requests.post(f"{base_url}/api/auth/login", json=login_data, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get('success') and data.get('token'):
                token = data['token']
                print(f"[PASS] Official Login: Token received")
            else:
                print(f"[FAIL] Official Login: No token in response")
        else:
            print(f"[FAIL] Official Login: Status {response.status_code}")
    except Exception as e:
        print(f"[FAIL] Official Login: {str(e)}")
    
    if not token:
        print("[WARN] Using test token for endpoint validation")
        token = "test_token_for_validation"
    
    headers = {'Authorization': f'Bearer {token}'}
    
    # Test 3: Fetch verification requests
    try:
        response = requests.get(f"{base_url}/api/verification-requests", headers=headers, timeout=10)
        print(f"[{'PASS' if response.status_code == 200 else 'FAIL'}] Fetch Verification Requests: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                requests_data = data.get('data', [])
                print(f"[INFO] Found {len(requests_data)} verification requests")
                for i, req in enumerate(requests_data[:3]):  # Show first 3
                    print(f"[INFO] Request {i+1}: ID={req.get('id')}, Status={req.get('status')}, Email={req.get('email')}")
            else:
                print(f"[FAIL] API returned success=False: {data.get('message', 'No message')}")
        else:
            print(f"[FAIL] HTTP Error: {response.text}")
    except Exception as e:
        print(f"[FAIL] Fetch Verification Requests: {str(e)}")
    
    # Test 4: Create a test verification request
    try:
        test_request = {
            "verification_type": "resident",
            "residential_address": "123 Test Street, Test City",
            "user_photo_base64": "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg==",
            "valid_id_base64": "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg=="
        }
        
        response = requests.post(f"{base_url}/api/verification-requests", json=test_request, headers=headers, timeout=10)
        print(f"[{'PASS' if response.status_code == 200 else 'FAIL'}] Create Verification Request: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"[INFO] Creation response: {data.get('message', 'No message')}")
        else:
            print(f"[FAIL] Creation failed: {response.text}")
    except Exception as e:
        print(f"[FAIL] Create Verification Request: {str(e)}")
    
    print("\nVerification Requests Testing Complete!")

if __name__ == "__main__":
    test_verification_requests()
