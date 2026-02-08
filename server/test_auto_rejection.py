import requests
import json

# Test the auto-rejection logic
def test_auto_rejection():
    # First, let's check existing bookings for 2026-02-23, Facility 1
    check_url = "https://intershifting-nakisha-nonspaciously.ngrok-free.dev/api/bookings?excludeUserRole=true"
    headers = {
        'Authorization': 'Bearer fe234954-85da-4625-97b8-098f8e1d20d3',
        'Content-Type': 'application/json'
    }
    
    print("=== CHECKING EXISTING BOOKINGS ===")
    try:
        response = requests.get(check_url, headers=headers, timeout=10)
        if response.status_code == 200:
            data = response.json()
            bookings = data.get('data', [])
            
            # Find bookings for 2026-02-23, Facility 1
            target_bookings = [
                booking for booking in bookings 
                if booking.get('booking_date') == '2026-02-23' and booking.get('facility_id') == 1
            ]
            
            print(f"Found {len(target_bookings)} existing bookings for 2026-02-23, Facility 1:")
            for booking in target_bookings:
                print(f"  - ID: {booking.get('id')}, Status: {booking.get('status')}, Email: {booking.get('user_email')}")
        else:
            print(f"Error checking bookings: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"Exception checking bookings: {e}")
    
    # Now test creating an official booking that should trigger auto-rejection
    print("\n=== TESTING OFFICIAL BOOKING AUTO-REJECTION ===")
    
    official_booking_data = {
        'facility_id': 1,
        'user_email': 'captain@barangay.gov',  # Official user
        'date': '2026-02-23',
        'timeslot': '6:00 AM - 8:00 AM',
        'purpose': 'Official barangay meeting',
        'contact_number': '09123456789',
        'address': 'Barangay Hall'
    }
    
    create_url = "https://intershifting-nakisha-nonspaciously.ngrok-free.dev/api/bookings"
    
    try:
        response = requests.post(create_url, headers=headers, json=official_booking_data, timeout=10)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"Success: {result.get('success')}")
            print(f"Message: {result.get('message')}")
            print(f"Booking ID: {result.get('booking_id')}")
            print(f"Status: {result.get('status')}")
            
            rejected_bookings = result.get('rejected_resident_bookings', [])
            print(f"\nRejected Resident Bookings: {len(rejected_bookings)}")
            for i, booking in enumerate(rejected_bookings):
                print(f"  {i+1}. ID: {booking['booking_id']}, Name: {booking['resident_name']}, Email: {booking['resident_email']}, Timeslot: {booking['timeslot']}")
        else:
            print(f"Error: {response.text}")
            
    except Exception as e:
        print(f"Exception: {e}")

if __name__ == "__main__":
    test_auto_rejection()
