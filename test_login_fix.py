import requests
import json

# Test login with mamamo@gmail.com (has password 123456)
url = 'http://192.168.100.4:8000/api/auth/login'
headers = {'Content-Type': 'application/json'}
data = {
    'email': 'mamamo@gmail.com',
    'password': '123456'  # Correct password for this user
}

print('🔍 Testing login with mamamo@gmail.com')
try:
    response = requests.post(url, headers=headers, json=data, timeout=5)
    print(f'Status Code: {response.status_code}')
    if response.status_code == 200:
        result = response.json()
        print('Success:', result.get('success'))
        print('Message:', result.get('message'))
        if result.get('user'):
            user = result['user']
            print('User ID:', user.get('id'))
            print('Verified:', user.get('verified'))
            print('Role:', user.get('role'))
            print('Login successful! 🎉')
    else:
        print('Error:', response.text)
except Exception as e:
    print('Login test error:', e)
