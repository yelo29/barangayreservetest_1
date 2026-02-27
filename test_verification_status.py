#!/usr/bin/env python3
"""
Test script for verification status API
"""

import requests
import json

# Test the verification status endpoint
def test_verification_status():
    base_url = "http://192.168.18.12:8000"
    
    # Test without authentication (should fail)
    print("Testing verification status endpoint without auth...")
    try:
        response = requests.get(f"{base_url}/api/verification/status")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Test with dummy auth token
    print("\nTesting with dummy auth token...")
    try:
        headers = {"Authorization": "Bearer dummy-token"}
        response = requests.get(f"{base_url}/api/verification/status", headers=headers)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_verification_status()
