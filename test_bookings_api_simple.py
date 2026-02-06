import requests
import json

# Test getting bookings for jl052904@gmail.com
url = "https://intershifting-nakisha-nonspaciously.ngrok-free.dev/api/bookings?user_email=jl052904@gmail.com&user_role=resident"
headers = {
    "Content-Type": "application/json",
    "X-User-ID": "15",
    "X-User-Email": "jl052904@gmail.com"
}

try:
    response = requests.get(url, headers=headers)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text[:1000]}")
        
except Exception as e:
    print(f"Error: {e}")
