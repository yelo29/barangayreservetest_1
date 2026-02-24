import requests

# Test what the Flutter app does - fetch bookings with user data
url = "http://192.168.100.4:8000/api/bookings"
params = {
    "user_role": "resident",
    "user_email": "unresident@gmail.com"
}
headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer f37a14fc-aa76-4fc0-8431-0660410716b9"
}

try:
    response = requests.get(url, headers=headers, params=params)
    print(f"Status Code: {response.status_code}")
    data = response.json()
    if data.get('success'):
        print(f"Total bookings: {len(data.get('data', []))}")
        # Look for user's own booking to see profile data
        for booking in data.get('data', []):
            if booking.get('user_email') == 'unresident@gmail.com':
                print(f"Found user booking:")
                print(f"  - Full Name: {booking.get('full_name')}")
                print(f"  - Contact: {booking.get('contact_number')}")
                print(f"  - Address: {booking.get('contact_address')}")
                break
    else:
        print(f"Error: {data}")
except Exception as e:
    print(f"Error: {e}")
