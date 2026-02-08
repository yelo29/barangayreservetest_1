import json

try:
    with open('users.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    print('=== USERS.JSON CONTENT ===')
    print(f'Total users: {len(data)}')
    for email, user_data in data.items():
        print(f'Email: {email}, Name: {user_data.get("full_name", "N/A")}, Role: {user_data.get("role", "N/A")}')
        if 'leo052904@gmail.com' in email:
            print(f'  🎯 FOUND LEO USER: {email}')
except Exception as e:
    print(f'Error reading users.json: {e}')
