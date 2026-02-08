import requests
import json

def test_final_flow():
    """Test the complete auto-rejection flow with fresh resident booking"""
    
    headers = {
        'Authorization': 'Bearer fe234954-85da-4625-97b8-098f8e1d20d3',
        'Content-Type': 'application/json'
    }
    
    print("=== TESTING FINAL AUTO-REJECTION FLOW ===")
    print("Date: 2026-02-15 (fresh resident booking created)")
    
    # Test 1: Check resident booking
    print("\n1. CHECKING RESIDENT BOOKING...")
    check_url = "https://intershifting-nakisha-nonspaciously.ngrok-free.dev/api/bookings?excludeUserRole=true"
    
    try:
        response = requests.get(check_url, headers=headers, timeout=10)
        if response.status_code == 200:
            data = response.json()
            bookings = data.get('data', [])
            
            target_bookings = [
                booking for booking in bookings 
                if booking.get('booking_date') == '2026-02-15' and booking.get('facility_id') == 1
            ]
            
            print(f"Found {len(target_bookings)} bookings for 2026-02-15, Facility 1:")
            for booking in target_bookings:
                print(f"  - ID: {booking.get('id')}, Status: {booking.get('status')}, Email: {booking.get('user_email')}, Time: {booking.get('start_time')}")
    except Exception as e:
        print(f"Exception checking bookings: {e}")
    
    # Test 2: Create official booking
    print("\n2. CREATING OFFICIAL BOOKING...")
    
    official_booking_data = {
        'facility_id': 1,
        'user_email': 'captain@barangay.gov',
        'date': '2026-02-15',
        'timeslot': 'ALL DAY',
        'purpose': 'Official barangay council meeting - entire day booking',
        'contact_number': '09123456789',
        'address': 'Barangay Hall'
    }
    
    create_url = "https://intershifting-nakisha-nonspaciously.ngrok-free.dev/api/bookings"
    
    try:
        response = requests.post(create_url, headers=headers, json=official_booking_data, timeout=10)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Success: {result.get('success')}")
            print(f"📝 Message: {result.get('message')}")
            print(f"🆔 Booking ID: {result.get('booking_id')}")
            print(f"📊 Status: {result.get('status')}")
            
            rejected_bookings = result.get('rejected_resident_bookings', [])
            print(f"\n🚫 Auto-rejected Resident Bookings: {len(rejected_bookings)}")
            for i, booking in enumerate(rejected_bookings):
                print(f"  {i+1}. ID: {booking['booking_id']}, Name: {booking['resident_name']}, Email: {booking['resident_email']}, Timeslot: {booking['timeslot']}")
                
                # Check if timeslot shows actual resident time (not "ALL DAY")
                if booking['timeslot'] and booking['timeslot'] != 'ALL DAY':
                    print(f"    ✅ CORRECT: Shows resident's actual time slot")
                else:
                    print(f"    ❌ ERROR: Timeslot issue - {booking['timeslot']}")
                    
        else:
            print(f"❌ Error: {response.text}")
            
    except Exception as e:
        print(f"❌ Exception: {e}")
    
    # Test 3: Verify final state
    print("\n3. VERIFYING FINAL STATE...")
    try:
        response = requests.get(check_url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            bookings = data.get('data', [])
            
            target_bookings = [
                booking for booking in bookings 
                if booking.get('booking_date') == '2026-02-15' and booking.get('facility_id') == 1
            ]
            
            print(f"Final booking status for 2026-02-15, Facility 1:")
            for booking in sorted(target_bookings, key=lambda x: x.get('id')):
                status = booking.get('status')
                email = booking.get('user_email')
                time = booking.get('start_time')
                
                if email == 'captain@barangay.gov':
                    print(f"  🏆 OFFICIAL: ID: {booking.get('id')}, Status: {status}, Time: {time}")
                else:
                    print(f"  👁 RESIDENT: ID: {booking.get('id')}, Status: {status}, Time: {time}")
                    
    except Exception as e:
        print(f"❌ Exception final check: {e}")

if __name__ == "__main__":
    test_final_flow()
