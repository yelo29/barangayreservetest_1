import requests

# Test unresident@gmail.com
response = requests.get('http://192.168.100.4:8000/api/users/profile/unresident@gmail.com')
if response.status_code == 200:
    data = response.json()
    user = data['user']
    print('=== unresident@gmail.com ===')
    print(f'Verified: {user.get("verified")}')
    print(f'Verification Type: {user.get("verification_type")}')
    print(f'Discount Rate: {user.get("discount_rate")}')
    print(f'Full Name: {user.get("full_name")}')
    print(f'Email: {user.get("email")}')
else:
    print(f'Error: {response.status_code}')

# Test diddy@gmail.com
response = requests.get('http://192.168.100.4:8000/api/users/profile/diddy@gmail.com')
if response.status_code == 200:
    data = response.json()
    user = data['user']
    print('\n=== diddy@gmail.com ===')
    print(f'Verified: {user.get("verified")}')
    print(f'Verification Type: {user.get("verification_type")}')
    print(f'Discount Rate: {user.get("discount_rate")}')
    print(f'Full Name: {user.get("full_name")}')
    print(f'Email: {user.get("email")}')
else:
    print(f'Error: {response.status_code}')
