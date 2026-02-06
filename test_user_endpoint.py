import requests
import json

# Test the new user endpoint
url = "https://intershifting-nakisha-nonspaciously.ngrok-free.dev/api/users/16"
headers = {"Content-Type": "application/json"}

try:
    response = requests.get(url, headers=headers)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"Error: {e}")
