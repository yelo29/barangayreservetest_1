import requests

print('=== TESTING REGISTRATION WITH FULL DEBUG ===')

# Test registration with name field
reg_data = {
    'name': 'FinalTestUser',
    'email': 'finaltest@gmail.com',
    'password': 'password123',
    'role': 'resident',
    'contact_number': '0987654321',
    'address': 'Final Test Address'
}

print('Sending registration request...')
reg_response = requests.post('http://192.168.100.4:8000/api/auth/register', json=reg_data)

print(f'Status Code: {reg_response.status_code}')
if reg_response.status_code == 200:
    reg_result = reg_response.json()
    print('Registration Response:')
    print(f'  - Success: {reg_result.get("success")}')
    print(f'  - Message: {reg_result.get("message")}')
    if 'user' in reg_result:
        user = reg_result['user']
        print(f'  - User Full Name: "{user.get("full_name")}"')
        print(f'  - User Email: {user.get("email")}')
        print(f'  - User ID: {user.get("id")}')
else:
    print(f'Error: {reg_response.text}')

print('\nCheck server logs for debug output...')
