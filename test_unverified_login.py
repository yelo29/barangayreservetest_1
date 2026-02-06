import requests
import json

# Test login with unverified user
url = "https://intershifting-nakisha-nonspaciously.ngrok-free.dev/api/auth/login"
headers = {"Content-Type": "application/json"}
data = {
    "email": "rubyjenlvr797@gmail.com",
    "password": "test123"
}

try:
    response = requests.post(url, headers=headers, json=data)
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"Success: {result['success']}")
        if 'user' in result:
            user = result['user']
            print(f"User ID: {user.get('id')}")
            print(f"Email: {user.get('email')}")
            print(f"Name: {user.get('full_name')}")
            print(f"Role: {user.get('role')}")
            print(f"Verified: {user.get('verified')}")
            print(f"Discount Rate: {user.get('discount_rate')}")
            print(f"Is Authenticated: {user.get('is_authenticated')}")
    else:
        print(f"Response: {response.text}")
        
except Exception as e:
    print(f"Error: {e}")
