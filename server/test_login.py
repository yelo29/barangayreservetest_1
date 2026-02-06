import requests
import json

# Test login endpoint
url = "http://localhost:5000/api/auth/login"
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
