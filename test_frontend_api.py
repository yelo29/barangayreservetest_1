#!/usr/bin/env python3
"""
Test frontend API calls (simulating Flutter behavior)
"""

import requests
import json

def test_frontend_api():
    base_url = "http://192.168.18.12:8000"
    
    # Simulate checking verification status (like Flutter would)
    print("=== Testing Frontend API Simulation ===")
    
    # 1. Check verification status
    print("\n1. Checking verification status...")
    try:
        response = requests.get(f"{base_url}/api/verification/status")
        result = response.json()
        
        print(f"Status: {response.status_code}")
        print(f"Has Pending Request: {result.get('hasPendingRequest')}")
        
        if result.get('hasPendingRequest'):
            pending = result.get('pendingRequest')
            print(f"Pending Request ID: {pending.get('id')}")
            print(f"Verification Type: {pending.get('verificationType')}")
            print(f"Status: {pending.get('status')}")
            
            # This would trigger form locking in Flutter
            print("\n-> Flutter should: LOCK all form fields")
            print("-> Flutter should: Show 'Verification Request Pending!' message")
            print("-> Flutter should: Disable submit button")
        else:
            print("\n-> Flutter should: ENABLE all form fields")
            print("-> Flutter should: Show normal verification form")
        
    except Exception as e:
        print(f"Error: {e}")
    
    # 2. Test creating a new request (if no pending)
    if not result.get('hasPendingRequest'):
        print("\n2. Creating new verification request...")
        verification_data = {
            "residentId": 2,  # Different user ID
            "verificationType": "non-resident",
            "fullName": "Another User",
            "contactNumber": "0987654321",
            "address": "Another Address",
            "userPhotoUrl": "data:image/jpeg;base64,anotherphoto",
            "validIdUrl": "data:image/jpeg;base64,anotherid",
            "status": "pending",
            "submittedAt": "2026-02-26T12:05:00.000Z"
        }
        
        try:
            response = requests.post(
                f"{base_url}/api/verification-requests",
                json=verification_data,
                headers={"Content-Type": "application/json"}
            )
            result = response.json()
            
            print(f"Status: {response.status_code}")
            print(f"Success: {result.get('success')}")
            print(f"Message: {result.get('message')}")
            
            if result.get('success'):
                print("\n-> Flutter should: Show success message")
                print("-> Flutter should: Navigate back to profile")
                print("-> Flutter should: Refresh user data")
            
        except Exception as e:
            print(f"Error: {e}")
    
    # 3. Test duplicate request attempt
    print("\n3. Testing duplicate request attempt...")
    duplicate_data = {
        "residentId": 2,  # Same user as above
        "verificationType": "resident",
        "fullName": "Duplicate User",
        "contactNumber": "1111111111",
        "address": "Duplicate Address",
        "userPhotoUrl": "data:image/jpeg;base64,duplicatephoto",
        "validIdUrl": "data:image/jpeg;base64,duplicateid",
        "status": "pending",
        "submittedAt": "2026-02-26T12:10:00.000Z"
    }
    
    try:
        response = requests.post(
            f"{base_url}/api/verification-requests",
            json=duplicate_data,
            headers={"Content-Type": "application/json"}
        )
        result = response.json()
        
        print(f"Status: {response.status_code}")
        print(f"Success: {result.get('success')}")
        print(f"Error Type: {result.get('error_type')}")
        print(f"Message: {result.get('message')}")
        
        if response.status_code == 409 and result.get('error_type') == 'duplicate_request':
            print("\n-> Flutter should: Show duplicate request warning")
            print("-> Flutter should: Update pending status")
            print("-> Flutter should: Lock form fields")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_frontend_api()
