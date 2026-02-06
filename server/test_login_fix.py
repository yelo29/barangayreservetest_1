#!/usr/bin/env python3
"""
Test the login endpoint to verify the get_db() fix
"""

import requests
import json

def test_login():
    try:
        url = "https://intershifting-nakisha-nonspaciously.ngrok-free.dev/api/auth/login"
        
        login_data = {
            'email': 'leo052904@gmail.com',
            'password': 'leo3029'
        }
        
        print(f"🔍 Testing login to {url}")
        print(f"📊 Login data: {login_data}")
        
        response = requests.post(url, json=login_data)
        
        print(f"📊 Response status: {response.status_code}")
        print(f"📊 Response body: {response.text}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Login successful!")
            print(f"   - Success: {data.get('success')}")
            print(f"   - Token: {data.get('token', 'N/A')[:20]}...")
            if data.get('user'):
                print(f"   - User: {data['user'].get('full_name', 'N/A')}")
                print(f"   - Role: {data['user'].get('role', 'N/A')}")
        else:
            print(f"❌ Login failed with status {response.status_code}")
            
    except Exception as e:
        print(f"❌ Test failed: {e}")

if __name__ == "__main__":
    test_login()
