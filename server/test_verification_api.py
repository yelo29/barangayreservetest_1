#!/usr/bin/env python3
"""
Test the verification requests API endpoint
"""

import requests
import json

def test_verification_api():
    try:
        # Test the GET endpoint for verification requests
        url = "http://192.168.100.4:8000/api/verification-requests"
        
        print(f"🔍 Testing GET {url}")
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer 0b1b3562-dabb-4c7d-a34c-75a0710bc76a"
        }
        
        response = requests.get(url, headers=headers)
        
        print(f"📊 Response status: {response.status_code}")
        print(f"📊 Response headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Response JSON structure:")
            print(f"   - Success: {data.get('success')}")
            print(f"   - Data type: {type(data.get('data'))}")
            print(f"   - Data length: {len(data.get('data', []))}")
            
            if data.get('data'):
                print(f"   - First item type: {type(data['data'][0])}")
                print(f"   - First item keys: {list(data['data'][0].keys()) if isinstance(data['data'][0], dict) else 'Not a dict'}")
                print(f"   - First item: {data['data'][0]}")
                
        else:
            print(f"❌ Error response: {response.text}")
            
    except Exception as e:
        print(f"❌ Test failed: {e}")

if __name__ == "__main__":
    test_verification_api()
