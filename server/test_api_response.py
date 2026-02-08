import requests
import json

# Test the API response
url = "https://intershifting-nakisha-nonspaciously.ngrok-free.dev/api/bookings?excludeUserRole=true"
headers = {
    'Authorization': 'Bearer fe234954-85da-4625-97b8-098f8e1d20d3',
    'Content-Type': 'application/json'
}

try:
    response = requests.get(url, headers=headers)
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        bookings = data.get('data', [])
        
        # Find bookings for 2026-02-23, Facility 1
        target_bookings = [
            booking for booking in bookings 
            if booking.get('booking_date') == '2026-02-23' and booking.get('facility_id') == 1
        ]
        
        print(f"\nFound {len(target_bookings)} bookings for 2026-02-23, Facility 1:")
        
        for i, booking in enumerate(target_bookings[:2]):
            print(f"\nBooking {i+1}:")
            print(f"  ID: {booking.get('id')}")
            print(f"  Available fields: {list(booking.keys())}")
            print(f"  full_name: {booking.get('full_name')}")
            print(f"  user_name: {booking.get('user_name')}")
            print(f"  user_email: {booking.get('user_email')}")
    else:
        print(f"Error: {response.text}")
        
except Exception as e:
    print(f"Exception: {e}")
