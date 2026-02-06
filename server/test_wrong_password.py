import requests
import json

# Test with wrong password (residen01)
url = "https://intershifting-nakisha-nonspaciously.ngrok-free.dev/api/auth/login"
data = {
    "email": "resident01@gmail.com",
    "password": "residen01"  # Missing 't'
}

try:
    response = requests.post(url, json=data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"Error: {e}")
