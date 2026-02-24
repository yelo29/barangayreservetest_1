import requests

# Get user profile to verify address update
url = "http://192.168.100.4:8000/api/users/profile/unresident@gmail.com"
headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer f37a14fc-aa76-4fc0-8431-0660410716b9"
}

try:
    response = requests.get(url, headers=headers)
    print(f"Status Code: {response.status_code}")
    data = response.json()
    if data.get('success'):
        user = data.get('user', {})
        print(f"Full Name: {user.get('full_name')}")
        print(f"Contact: {user.get('contact_number')}")
        print(f"Address: {user.get('address')}")
        print(f"Email: {user.get('email')}")
    else:
        print(f"Error: {data}")
except Exception as e:
    print(f"Error: {e}")
