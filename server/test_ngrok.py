import requests
import json

# Test ngrok URL
url = "https://intershifting-nakisha-nonspaciously.ngrok-free.dev/api/auth/login"
data = {
    "email": "resident01@gmail.com",
    "password": "resident01"
}

try:
    response = requests.post(url, json=data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"Error: {e}")
