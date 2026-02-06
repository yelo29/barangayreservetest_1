import requests
import json

# Test getting current user data for jl052904@gmail.com
url = "https://intershifting-nakisha-nonspaciously.ngrok-free.dev/api/users/15"
headers = {
    "Content-Type": "application/json",
    "X-User-ID": "15",
    "X-User-Email": "jl052904@gmail.com"
}

try:
    response = requests.get(url, headers=headers)
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"Success: {result['success']}")
        if 'user' in result:
            user = result['user']
            print("All user fields:")
            for key, value in user.items():
                if key not in ['password', 'profile_photo_url']:  # Skip long fields
                    print(f"  {key}: {value}")
    else:
        print(f"Response: {response.text[:500]}")
        
except Exception as e:
    print(f"Error: {e}")
