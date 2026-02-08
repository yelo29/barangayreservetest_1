import requests
import json

def test_final_compilation():
    """Test the final compilation fixes"""
    
    headers = {
        'Authorization': 'Bearer fe234954-85da-4625-97b8-098f8e1d20d3',
        'Content-Type': 'application/json'
    }
    
    print("=== TESTING FINAL COMPILATION FIXES ===")
    print("Testing: Complete flow with fixed UI and backend")
    
    # Test the complete flow one more time
    print("\n1. Creating resident booking...")
    resident_booking_data = {
        'facility_id': 1,
        'user_email': 'resident01@gmail.com',
        'date': '2026-02-24',
        'timeslot': '3:00 PM - 5:00 PM',
        'purpose': 'Final compilation test',
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
            print(f"✅ Resident booking created: ID {result.get('booking_id')}")
            
            # Create official booking
            print("\n2. Creating official booking...")
            official_booking_data = {
                'facility_id': 1,
                'user_email': 'captain@barangay.gov',
                'date': '2026-02-24',
                'timeslot': 'ALL DAY',
                'purpose': 'Final official test',
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
                    print(f"✅ SUCCESS: Complete flow working!")
                    print(f"   - Official booking ID: {result.get('booking_id')}")
                    print(f"   - Rejected resident ID: {booking['booking_id']}")
                    print(f"   - Timeslot format: '{timeslot}'")
                    print(f"   - Message: {result.get('message')}")
                    
                    # Verify timeslot format
                    if timeslot.count(' - ') == 1 and len(timeslot.split(' - ')) == 2:
                        print(f"✅ TIMESLOT FIX: Format is correct")
                    else:
                        print(f"❌ TIMESLOT ERROR: Format still broken")
                else:
                    print("❌ ERROR: No rejected bookings found")
            else:
                print(f"❌ Error creating official booking: {response.text}")
        else:
            print(f"❌ Error creating resident booking: {response.text}")
            
    except Exception as e:
        print(f"❌ Exception: {e}")

if __name__ == "__main__":
    test_final_compilation()
