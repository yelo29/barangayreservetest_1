import requests
import json

# Test the email-based endpoint
base_url = "https://intershifting-nakisha-nonspaciously.ngrok-free.dev"
email = "saloestillopez@gmail.com"

# Test the /api/me endpoint with email parameter
url = f"{base_url}/api/me?email={email}"
print(f"Testing email-based endpoint: {url}")

try:
    response = requests.get(url)
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
