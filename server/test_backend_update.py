import requests
import json

def test_backend_update():
    """Test if the backend is using the updated code"""
    
    headers = {
        'Authorization': 'Bearer fe234954-85da-4625-97b8-098f8e1d20d3',
        'Content-Type': 'application/json'
    }
    
    print("=== TESTING BACKEND UPDATE ===")
    
    # Create a simple resident booking
    print("\n1. Creating resident booking...")
    resident_booking_data = {
        'facility_id': 1,
        'user_email': 'resident01@gmail.com',
        'date': '2026-02-27',
        'timeslot': '10:00 AM - 12:00 PM',
        'purpose': 'Test backend update',
        'contact_number': '09123456789',
        'address': 'Test Address',
        'total_amount': 100
    }
    
    create_url = "https://intershifting-nakisha-nonspaciously.ngrok-free.dev/api/bookings"
    
    try:
        response = requests.post(create_url, headers=headers, json=resident_booking_data, timeout=10)
        print(f"Resident booking status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            resident_booking_id = result.get('booking_id')
            print(f"✅ Resident booking created: ID {resident_booking_id}")
            
            # Now create official booking to trigger auto-rejection
            print("\n2. Creating official booking...")
            official_booking_data = {
                'facility_id': 1,
                'user_email': 'captain@barangay.gov',
                'date': '2026-02-27',
                'timeslot': 'ALL DAY',
                'purpose': 'Official booking test',
                'contact_number': '09123456789',
                'address': 'Barangay Hall'
            }
            
            response = requests.post(create_url, headers=headers, json=official_booking_data, timeout=10)
            print(f"Official booking status: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                rejected_bookings = result.get('rejected_resident_bookings', [])
                
                if rejected_bookings:
                    booking = rejected_bookings[0]
                    timeslot = booking['timeslot']
                    print(f"📝 Rejected booking timeslot: '{timeslot}'")
                    
                    # Check if the timeslot format is correct
                    if timeslot.count(' - ') == 1:
                        print(f"✅ SUCCESS: Timeslot format is correct (no duplicate)")
                    else:
                        print(f"❌ ERROR: Timeslot still has duplicate format")
                        print(f"   Expected: '10:00 AM - 12:00 PM'")
                        print(f"   Got: '{timeslot}'")
                else:
                    print("❌ ERROR: No rejected bookings found")
            else:
                print(f"❌ Error creating official booking: {response.text}")
        else:
            print(f"❌ Error creating resident booking: {response.text}")
            
    except Exception as e:
        print(f"❌ Exception: {e}")

if __name__ == "__main__":
    test_backend_update()
