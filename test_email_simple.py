#!/usr/bin/env python3
import requests

base_url = 'http://192.168.18.12:8000'
test_email = 'captain@barangay.gov'

try:
    response = requests.get(f'{base_url}/api/users/profile/{test_email}')
    print(f'Status: {response.status_code}')
    
    if response.status_code == 200:
        data = response.json()
        if data.get('success'):
            user = data.get('user', {})
            print('User found:')
            print(f'  - ID: {user.get("id")}')
            print(f'  - Email: {user.get("email")}')
            print(f'  - Full Name: {user.get("full_name")}')
            print(f'  - Contact: {user.get("contact_number")}')
            print(f'  - Address: {user.get("address")}')
            print(f'  - Verified: {user.get("verified")}')
            
            if user.get('email'):
                print('SUCCESS: Email field is present in backend response')
            else:
                print('ERROR: Email field is missing from backend response')
        else:
            print(f'API returned error: {data.get("message")}')
    else:
        print(f'HTTP Error: {response.status_code}')
        print(f'Response: {response.text}')
        
except Exception as e:
    print(f'Error: {e}')
