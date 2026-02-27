#!/usr/bin/env python3
"""
Test script for verification request API
"""

import requests
import json

def test_verification_request():
    base_url = "http://192.168.18.12:8000"
    
    # Test data for verification request
    verification_data = {
        "residentId": 1,
        "verificationType": "resident",
        "fullName": "Test User",
        "contactNumber": "1234567890",
        "address": "Test Address",
        "userPhotoUrl": "data:image/jpeg;base64,testphoto",
        "validIdUrl": "data:image/jpeg;base64,testid",
        "status": "pending",
        "submittedAt": "2026-02-26T12:00:00.000Z"
    }
    
    print("Creating verification request...")
    try:
        response = requests.post(
            f"{base_url}/api/verification-requests",
            json=verification_data,
            headers={"Content-Type": "application/json"}
        )
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                print("✓ Verification request created successfully!")
                
                # Test duplicate request
                print("\nTesting duplicate request...")
                response2 = requests.post(
                    f"{base_url}/api/verification-requests",
                    json=verification_data,
                    headers={"Content-Type": "application/json"}
                )
                print(f"Status: {response2.status_code}")
                print(f"Response: {response2.text}")
                
                if response2.status_code == 409:
                    print("✓ Duplicate request correctly rejected!")
                else:
                    print("✗ Duplicate request should have been rejected")
            else:
                print("✗ Failed to create verification request")
        
    except Exception as e:
        print(f"Error: {e}")
    
    # Test verification status after creating request
    print("\nChecking verification status...")
    try:
        response = requests.get(f"{base_url}/api/verification/status")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            result = response.json()
            if result.get('hasPendingRequest'):
                print("✓ Pending request detected!")
            else:
                print("✗ No pending request found")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_verification_request()
