import requests
import json

# Test user profile API
response = requests.get("http://127.0.0.1:8000/api/users/profile/leo052904@gmail.com")
print("Profile API Response:")
print(json.dumps(response.json(), indent=2))

# Test creating a booking
booking_data = {
    "facility_id": 1,
    "user_email": "test@example.com", 
    "date": "2026-02-20",
    "timeslot": "2:00 PM - 4:00 PM",
    "total_amount": 1000,
    "status": "pending",
    "full_name": "Test User",
    "contact_number": "123456789",
    "address": "Test Address", 
    "purpose": "Test booking"
}

response = requests.post("http://127.0.0.1:8000/api/bookings", json=booking_data)
print("\nCreate Booking Response:")
print(json.dumps(response.json(), indent=2))
