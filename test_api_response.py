import requests

# Test the actual API response
base_url = 'http://192.168.100.4:8000'
email = 'residentresident@gmail.com'

print('🔍 TESTING ACTUAL API RESPONSE')
print('=' * 50)

try:
    response = requests.get(f'{base_url}/api/users/profile/{email}', timeout=5)
    print(f'Status Code: {response.status_code}')
    
    if response.status_code == 200:
        data = response.json()
        print(f'✅ Raw JSON Response:')
        print(f'{data}')
        
        if data.get('success') and data.get('user'):
            user_data = data['user']
            print(f'\n✅ User Data:')
            print(f'  - ID: {user_data.get("id")}')
            print(f'  - Email: {user_data.get("email")}')
            print(f'  - Full Name: {user_data.get("full_name")}')
            print(f'  - Role: {user_data.get("role")}')
            print(f'  - Verified: {user_data.get("verified")} (type: {type(user_data.get("verified"))})')
            print(f'  - Verification Type: {user_data.get("verification_type")} (type: {type(user_data.get("verification_type"))})')
            print(f'  - Discount Rate: {user_data.get("discount_rate")} (type: {type(user_data.get("discount_rate"))})')
        else:
            print(f'❌ Invalid response structure: {data}')
    else:
        print(f'❌ API Error: {response.status_code}')
        print(f'Response: {response.text}')
        
except Exception as e:
    print(f'❌ Error: {e}')
