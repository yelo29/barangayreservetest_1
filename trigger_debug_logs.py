import requests

print('=== TESTING REGISTRATION TO TRIGGER DEBUG LOGS ===')

# Test registration with name field
reg_data = {
    'name': 'DebugUser2',
    'email': 'debuguser2@gmail.com',
    'password': 'password123',
    'role': 'resident',
    'contact_number': '1234567890',
    'address': 'Debug Address 2'
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
