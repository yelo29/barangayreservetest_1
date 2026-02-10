import requests
import json

# Test rejecting booking 91 with fake receipt violation
booking_id = 91
rejection_data = {
    "status": "rejected",
    "rejection_reason": "Your payment receipt is fake or shown no payment in our payment history/records, ⚠️ know that this violation will be recorded and you will only have three chances before getting your account banned!",
    "rejection_type": "fake_receipt"
}

response = requests.put(f"http://127.0.0.1:8000/api/bookings/{booking_id}/status", json=rejection_data)
print("Reject Booking Response:")
print(json.dumps(response.json(), indent=2))

# Check user profile after rejection to see if violations increased
profile_response = requests.get("http://127.0.0.1:8000/api/users/profile/leo052904@gmail.com")
print("\nUser Profile After Rejection:")
print(json.dumps(profile_response.json(), indent=2))
