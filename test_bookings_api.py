import requests
import json

# Test getting bookings for jl052904@gmail.com
url = "https://intershifting-nakisha-nonspaciously.ngrok-free.dev/api/bookings?user_email=jl052904@gmail.com&user_role=resident"
headers = {
    "Content-Type": "application/json",
    "X-User-ID": "15",
    "X-User-Email": "jl052904@gmail.com"
}

try:
    response = requests.get(url, headers=headers)
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"Success: {result['success']}")
        if 'bookings' in result:
            bookings = result['bookings']
            print(f"Found {len(bookings)} bookings:")
            for booking in bookings:
                print(f"  - ID: {booking.get('id')}, Facility: {booking.get('facility_id')}, Date: {booking.get('date')}, Status: {booking.get('status')}")
        else:
            print("No bookings field in response")
    else:
        print(f"Response: {response.text[:500]}")
        
except Exception as e:
    print(f"Error: {e}")
