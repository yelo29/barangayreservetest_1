import requests
import json

def create_test_resident():
    """Create a test resident booking for testing"""
    
    headers = {
        'Authorization': 'Bearer fe234954-85da-4625-97b8-098f8e1d20d3',
        'Content-Type': 'application/json'
    }
    
    print("=== CREATING TEST RESIDENT BOOKING ===")
    
    # Create a resident booking for 2026-02-15 (no existing bookings)
    resident_booking_data = {
        'facility_id': 1,
        'user_email': 'resident01@gmail.com',  # Resident user
        'date': '2026-02-15',
        'timeslot': '10:00 AM - 12:00 PM',
        'purpose': 'Test resident booking for auto-rejection',
        'contact_number': '09123456789',
        'address': 'Test Address',
        'total_amount': 100
    }
    
    create_url = "https://intershifting-nakisha-nonspaciously.ngrok-free.dev/api/bookings"
    
    try:
        response = requests.post(create_url, headers=headers, json=resident_booking_data, timeout=10)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Success: {result.get('success')}")
            print(f"📝 Message: {result.get('message')}")
            print(f"🆔 Booking ID: {result.get('booking_id')}")
            print(f"📊 Status: {result.get('status')}")
            
            if result.get('success'):
                print(f"\n🎯 Test resident booking created successfully!")
                print("Now you can test official booking on 2026-02-15")
            else:
                print(f"❌ Error: {result.get('message')}")
        else:
            print(f"❌ Error: {response.text}")
            
    except Exception as e:
        print(f"❌ Exception: {e}")

if __name__ == "__main__":
    create_test_resident()
