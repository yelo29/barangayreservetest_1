import requests
import json

# Debug the login issue by testing different approaches
base_url = "https://intershifting-nakisha-nonspaciously.ngrok-free.dev"

print("Debugging login issue...")
print("=" * 50)

# Test 1: Check if the server is actually using our database
print("1. Testing if server recognizes our database accounts:")

accounts_to_test = [
    {"email": "official@barangay.com", "password": "password123"},
    {"email": "secretary@barangay.gov", "password": "admin123"},
    {"email": "secretary@barangay.gov", "password": "barangay123"},
    {"email": "captain@barangay.com", "password": "barangay123"},
]

for account in accounts_to_test:
    print(f"\nTesting: {account['email']} / {account['password']}")
    
    try:
        response = requests.post(
            f"{base_url}/api/auth/login",
            json=account,
            headers={'Content-Type': 'application/json'}
        )
        
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ SUCCESS: {data.get('message', 'Login successful')}")
            if 'user' in data:
                user = data['user']
                print(f"  User ID: {user.get('id')}")
                print(f"  Name: {user.get('full_name', user.get('fullName'))}")
                print(f"  Role: {user.get('role')}")
        else:
            print(f"❌ FAILED: {response.text}")
            
    except Exception as e:
        print(f"❌ ERROR: {e}")

print("\n" + "=" * 50)

# Test 2: Check if there's a different login endpoint
print("2. Testing alternative login endpoints:")

alternative_endpoints = [
    "/api/login",
    "/login",
    "/auth/login"
]

for endpoint in alternative_endpoints:
    print(f"\nTesting POST {endpoint}")
    
    try:
        response = requests.post(
            f"{base_url}{endpoint}",
            json={"email": "official@barangay.com", "password": "password123"},
            headers={'Content-Type': 'application/json'}
        )
        
        print(f"Status: {response.status_code}")
        if response.status_code != 404:
            print(f"Response: {response.text[:200]}...")
            
    except Exception as e:
        print(f"Error: {e}")

print("\n" + "=" * 50)

# Test 3: Check what the server actually returns for login
print("3. Checking server response details:")

try:
    response = requests.post(
        f"{base_url}/api/auth/login",
        json={"email": "official@barangay.com", "password": "password123"},
        headers={'Content-Type': 'application/json'}
    )
    
    print(f"Full response headers: {dict(response.headers)}")
    print(f"Full response body: {response.text}")
    
except Exception as e:
    print(f"Error: {e}")
