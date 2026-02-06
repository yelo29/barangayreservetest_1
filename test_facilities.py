import requests
import json

# Test facilities endpoint
url = "https://intershifting-nakisha-nonspaciously.ngrok-free.dev/api/facilities"
headers = {"Content-Type": "application/json"}

try:
    response = requests.get(url, headers=headers)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"Error: {e}")
