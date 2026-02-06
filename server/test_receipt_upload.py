import requests
import base64

# Test receipt upload with a simple 1x1 pixel PNG
test_receipt = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg=="

# Test booking data
booking_data = {
    "facility_id": "1",
    "user_email": "test@example.com", 
    "date": "2026-02-10",
    "timeslot": "10:00 AM - 12:00 PM",
    "purpose": "Test receipt upload",
    "receipt_base64": test_receipt,
    "contact_number": "09123456789",
    "address": "Test Address"
}

print("Testing booking creation with receipt...")
print(f"Receipt base64 length: {len(test_receipt)}")
print(f"Receipt starts with data:image: {test_receipt.startswith('data:image')}")

try:
    response = requests.post(
        "https://intershifting-nakisha-nonspaciously.ngrok-free.dev/api/bookings",
        json=booking_data,
        headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer 2c779452-f8ec-47ba-bb7d-81b487c54e45"
        }
    )
    
    print(f"Response status: {response.status_code}")
    print(f"Response body: {response.text}")
    
except Exception as e:
    print(f"Error: {e}")
