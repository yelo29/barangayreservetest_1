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
            print(f"User ID: {user.get('id')}")
            print(f"Email: {user.get('email')}")
            print(f"Name: {user.get('full_name')}")
            print(f"Role: {user.get('role')}")
            print(f"Verified: {user.get('verified')}")
            print(f"Discount Rate: {user.get('discount_rate')}")
            print(f"Contact Number: {user.get('contact_number')}")
            print(f"Profile Photo URL: {user.get('profile_photo_url')}")
            print(f"Is Authenticated: {user.get('is_authenticated')}")
    else:
        print(f"Response: {response.text}")
        
except Exception as e:
    print(f"Error: {e}")
