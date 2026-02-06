#!/usr/bin/env python3
import requests
import json

base_url = "http://localhost:5000"

def test_login_and_me():
    print("🧪 Testing login and /api/me endpoint...")
    
    # Test login
    login_data = {
        "email": "leo052904@gmail.com",
        "password": "zepol052904"
    }
    
    print("1. Testing login...")
    login_response = requests.post(f"{base_url}/api/auth/login", json=login_data)
    
    if login_response.status_code == 200:
        login_result = login_response.json()
        if login_result.get("success"):
            token = login_result.get("token")
            user_email = login_result.get("user", {}).get("email")
            print(f"✅ Login successful! Token: {token[:20]}...")
            print(f"   User: {user_email}")
            
            # Test /api/me endpoint
            print("\n2. Testing /api/me endpoint...")
            headers = {"Authorization": f"Bearer {token}"}
            me_response = requests.get(f"{base_url}/api/me?email={user_email}", headers=headers)
            
            if me_response.status_code == 200:
                me_result = me_response.json()
                if me_result.get("success"):
                    user_data = me_result.get("user", {})
                    print(f"✅ /api/me successful!")
                    print(f"   Name: {user_data.get('full_name')}")
                    print(f"   Role: {user_data.get('role')}")
                    print(f"   Verified: {user_data.get('verified')}")
                    print(f"   Discount: {user_data.get('discount_rate', 0) * 100}%")
                else:
                    print(f"❌ /api/me failed: {me_result.get('error')}")
            else:
                print(f"❌ /api/me HTTP error: {me_response.status_code}")
        else:
            print(f"❌ Login failed: {login_result.get('message')}")
    else:
        print(f"❌ Login HTTP error: {login_response.status_code}")

if __name__ == "__main__":
    test_login_and_me()
