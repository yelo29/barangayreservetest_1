#!/usr/bin/env python3
"""
Debug script to check what URL the app is actually trying to reach
"""

import requests
import json

def test_login_debug():
    # Test the exact same login request the app would make
    url = "http://192.168.100.4:8080/api/login"
    data = {
        "email": "leo052904@gmail.com",
        "password": "zepol052904"
    }
    
    print("🔍 Debug Login Connection")
    print("=" * 40)
    print(f"📡 URL: {url}")
    print(f"📧 Email: {data['email']}")
    print(f"🔑 Password: {data['password']}")
    print()
    
    try:
        print("🔄 Sending login request...")
        response = requests.post(url, json=data, timeout=5)
        print(f"✅ Status Code: {response.status_code}")
        print(f"📄 Response: {response.text}")
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                print("🎉 Login successful!")
                print(f"👤 User: {result.get('user', {})}")
            else:
                print(f"❌ Login failed: {result.get('error', 'Unknown error')}")
        else:
            print(f"❌ HTTP Error: {response.status_code}")
            
    except requests.exceptions.Timeout:
        print("❌ Request timed out - this is likely the app's problem!")
    except requests.exceptions.ConnectionError:
        print("❌ Connection failed - server unreachable")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_login_debug()
