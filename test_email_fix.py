#!/usr/bin/env python3
"""
Test script to verify email fetching from backend profile endpoint
"""

import requests
import json

def test_email_fetching():
    base_url = "http://192.168.18.12:8000"
    
    # Test the profile endpoint with a sample email
    test_email = "test@example.com"
    print(f"Testing profile endpoint for email: {test_email}")
    
    try:
        response = requests.get(f"{base_url}/api/users/profile/{test_email}")
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                user = data.get('user', {})
                print(f"✓ User found:")
                print(f"  - ID: {user.get('id')}")
                print(f"  - Email: {user.get('email')}")
                print(f"  - Full Name: {user.get('full_name')}")
                print(f"  - Contact: {user.get('contact_number')}")
                print(f"  - Address: {user.get('address')}")
                print(f"  - Verified: {user.get('verified')}")
                print(f"  - Verification Type: {user.get('verification_type')}")
                
                # Check if email field is present
                if user.get('email'):
                    print("✓ Email field is present in backend response")
                else:
                    print("✗ Email field is missing from backend response")
            else:
                print(f"✗ API returned error: {data.get('message')}")
        else:
            print(f"✗ HTTP Error: {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"✗ Error: {e}")

if __name__ == "__main__":
    test_email_fetching()
