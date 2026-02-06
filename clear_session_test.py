import requests
import json

# Test logout to clear session
url = "https://intershifting-nakisha-nonspaciously.ngrok-free.dev/api/auth/logout"
headers = {
    "Content-Type": "application/json",
    "X-User-ID": "5",
    "X-User-Email": "leo052904@gmail.com"
}

try:
    response = requests.post(url, headers=headers)
    print(f"Logout Status Code: {response.status_code}")
    print(f"Logout Response: {response.text}")
except Exception as e:
    print(f"Error: {e}")
