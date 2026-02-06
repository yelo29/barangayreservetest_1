import requests
import json

# Test facilities endpoint with correct URL
url = "https://intershifting-nakisha-nonspaciously.ngrok-free.dev/api/facilities"
headers = {
    "Content-Type": "application/json",
    "X-User-ID": "5",
    "X-User-Email": "leo052904@gmail.com"
}

try:
    response = requests.get(url, headers=headers)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"Type: {type(data)}")
        print(f"Length: {len(data) if isinstance(data, list) else 'Not a list'}")
        
except Exception as e:
    print(f"Error: {e}")
