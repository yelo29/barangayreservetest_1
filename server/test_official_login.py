import requests
import json

# Test the official login with correct password
base_url = "https://intershifting-nakisha-nonspaciously.ngrok-free.dev"

# Test login with secretary@barangay.gov using the correct password
login_data = {
    'email': 'secretary@barangay.gov',
    'password': 'tatalaadminkalihim'
}

print(f"Testing official login for secretary@barangay.gov")
print(f"Using password: {login_data['password']}")

try:
    response = requests.post(
        f"{base_url}/api/auth/login",
        json=login_data,
        headers={'Content-Type': 'application/json'}
    )
    
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"Response Data: {json.dumps(data, indent=2)}")
        
        if data['success'] == True:
            print("✅ Official login successful!")
            user = data['user']
            print(f"  User ID: {user.get('id')}")
            print(f"  Email: {user.get('email')}")
            print(f"  Name: {user.get('full_name')}")
            print(f"  Role: {user.get('role')}")
            print(f"  Verified: {user.get('verified')}")
        else:
            print(f"❌ Login failed: {data.get('message')}")
    else:
        print(f"❌ HTTP Error: {response.status_code}")
        print(f"Error response: {response.text}")
        
except Exception as e:
    print(f"Exception: {e}")

print("\n" + "="*50 + "\n")

# Test with a simple password that might be expected
simple_login_data = {
    'email': 'secretary@barangay.gov',
    'password': 'admin123'
}

print(f"Testing with simple password: {simple_login_data['password']}")

try:
    response = requests.post(
        f"{base_url}/api/auth/login",
        json=simple_login_data,
        headers={'Content-Type': 'application/json'}
    )
    
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"Response: {json.dumps(data, indent=2)}")
    else:
        print(f"❌ Simple password failed: {response.text}")
        
except Exception as e:
    print(f"Exception: {e}")
