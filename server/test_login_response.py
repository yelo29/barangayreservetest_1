import requests
import json

# Test the login endpoint to see what data structure it returns
base_url = "https://intershifting-nakisha-nonspaciously.ngrok-free.dev"

# Test login with saloestillopez@gmail.com
login_data = {
    'email': 'saloestillopez@gmail.com',
    'password': 'salo3029'
}

print(f"Testing login for saloestillopez@gmail.com")
print(f"Login data: {login_data}")

try:
    response = requests.post(
        f"{base_url}/api/auth/login",
        json=login_data,
        headers={'Content-Type': 'application/json'}
    )
    
    print(f"Status Code: {response.status_code}")
    print(f"Response Headers: {dict(response.headers)}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"Response Data: {json.dumps(data, indent=2)}")
        
        # Check user data structure
        if 'user' in data:
            user = data['user']
            print(f"\nUser Data Structure:")
            print(f"  Keys: {list(user.keys())}")
            print(f"  ID: {user.get('id')}")
            print(f"  Email: {user.get('email')}")
            print(f"  Full Name: {user.get('full_name')}")
            print(f"  Verified: {user.get('verified')}")
            print(f"  Profile Photo URL: {user.get('profile_photo_url')}")
    else:
        print(f"Error: {response.text}")
        
except Exception as e:
    print(f"Exception: {e}")
