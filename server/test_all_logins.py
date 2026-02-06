#!/usr/bin/env python3
import requests
import json

base_url = "http://localhost:5000"

test_users = [
    {"email": "captain@barangay.gov", "password": "tatalaPunongBarangayadmin", "role": "official"},
    {"email": "secretary@barangay.gov", "password": "tatalaSecretaryadmin", "role": "official"},
    {"email": "administrator@barangay.gov", "password": "tatalaAdministratoradmin", "role": "official"},
    {"email": "kagawad1@barangay.gov", "password": "tatalaKagawad1admin", "role": "official"},
    {"email": "planning@barangay.gov", "password": "tatalaPlanningOfficeradmin", "role": "official"},
    {"email": "utility@barangay.gov", "password": "tatalaUtilityadmin", "role": "official"}
]

print("🧪 Testing all user logins...")
print("=" * 50)

for user in test_users:
    try:
        response = requests.post(f"{base_url}/api/auth/login", json={
            "email": user["email"],
            "password": user["password"]
        })
        
        if response.status_code == 200:
            data = response.json()
            if data.get("success"):
                user_data = data.get("user", {})
                print(f"✅ {user['email']} - {user_data.get('role', 'unknown').upper()}")
                print(f"   Name: {user_data.get('full_name', 'N/A')}")
                print(f"   Verified: {user_data.get('verified', False)}")
                print(f"   Discount: {user_data.get('discount_rate', 0) * 100}%")
            else:
                print(f"❌ {user['email']} - Login failed: {data.get('message', 'Unknown error')}")
        else:
            print(f"❌ {user['email']} - HTTP {response.status_code}: {response.text}")
            
    except Exception as e:
        print(f"❌ {user['email']} - Exception: {e}")
    
    print("-" * 30)

print("🎯 Login testing complete!")
