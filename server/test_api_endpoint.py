import requests
import json

# Test the API endpoint that's being called by the app
base_url = "https://intershifting-nakisha-nonspaciously.ngrok-free.dev"
user_id = "cg0Dya4g2oMBYna2gInAdliuUKv2"  # Firebase UID

# Test the endpoint that the app is calling
url = f"{base_url}/api/users/{user_id}"
print(f"Testing API endpoint: {url}")

try:
    response = requests.get(url)
    print(f"Status Code: {response.status_code}")
    print(f"Response Headers: {dict(response.headers)}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"Response Data: {json.dumps(data, indent=2)}")
        
        # Check if profile_photo_url is in the response
        if 'user' in data:
            user_data = data['user']
            print(f"\nUser data keys: {list(user_data.keys())}")
            if 'profile_photo_url' in user_data:
                print(f"Profile photo URL found: {user_data['profile_photo_url'][:100]}...")
            else:
                print("Profile photo URL NOT found in user data")
    else:
        print(f"Error response: {response.text}")
        
except Exception as e:
    print(f"Error: {e}")

print("\n" + "="*50 + "\n")

# Test with numeric ID (ID 14 for saloestillopez@gmail.com)
numeric_id = "14"
url_numeric = f"{base_url}/api/users/{numeric_id}"
print(f"Testing with numeric ID: {url_numeric}")

try:
    response = requests.get(url_numeric)
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"Response Data: {json.dumps(data, indent=2)}")
        
        # Check if profile_photo_url is in the response
        if 'user' in data:
            user_data = data['user']
            print(f"\nUser data keys: {list(user_data.keys())}")
            if 'profile_photo_url' in user_data:
                print(f"Profile photo URL found: {user_data['profile_photo_url'][:100]}...")
            else:
                print("Profile photo URL NOT found in user data")
    else:
        print(f"Error response: {response.text}")
        
except Exception as e:
    print(f"Error: {e}")
