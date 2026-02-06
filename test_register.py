import requests
import json

# Test registration endpoint
url = "https://intershifting-nakisha-nonspaciously.ngrok-free.dev/api/auth/register"
headers = {"Content-Type": "application/json"}
data = {
    "name": "Sally Estil Lopez",
    "email": "rubyjenlvr797@gmail.com", 
    "password": "test123",
    "role": "resident"
}

try:
    response = requests.post(url, headers=headers, json=data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"Error: {e}")
