import requests
import json

# Get all bookings to test
response = requests.get("http://127.0.0.1:8000/api/bookings?user_role=official")
data = response.json()

bookings = data.get('data', [])

print("Pending bookings:")
for booking in bookings:
    if booking.get('status') == 'pending':
        print(f"ID: {booking.get('id')}, User: {booking.get('user_email')}, Status: {booking.get('status')}")
