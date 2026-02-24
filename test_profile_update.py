import requests
import json

# Test profile update
url = "http://192.168.100.4:8000/api/users/profile"
headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer f37a14fc-aa76-4fc0-8431-0660410716b9"
}
data = {
    "email": "unresident@gmail.com",
    "full_name": "UnResident Updated",
    "contact_number": "09656692463",
    "address": "Test Address Updated"
}

try:
    response = requests.put(url, headers=headers, json=data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"Error: {e}")
