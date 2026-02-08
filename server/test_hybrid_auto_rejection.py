import requests
import json

def test_hybrid_auto_rejection():
    """Test the hybrid auto-rejection implementation"""
    
    headers = {
        'Authorization': 'Bearer fe234954-85da-4625-97b8-098f8e1d20d3',
        'Content-Type': 'application/json'
    }
    
    print("=== HYBRID AUTO-REJECTION TEST ===")
    
    # Test 1: Check existing bookings before official booking
    print("\n1. CHECKING EXISTING BOOKINGS...")
    check_url = "https://intershifting-nakisha-nonspaciously.ngrok-free.dev/api/bookings?excludeUserRole=true"
    
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
            for booking in sorted(target_bookings, key=lambda x: x.get('id')):
                print(f"  - ID: {booking.get('id')}, Status: {booking.get('status')}, Email: {booking.get('user_email')}, Time: {booking.get('start_time')}")
        else:
            print(f"Error checking bookings: {response.status_code}")
    except Exception as e:
        print(f"Exception checking bookings: {e}")
    
    # Test 2: Create official booking for entire day (should reject ALL resident bookings)
    print("\n2. TESTING OFFICIAL BOOKING FOR ENTIRE DAY...")
    
    official_booking_data = {
        'facility_id': 1,
        'user_email': 'captain@barangay.gov',  # Official user
        'date': '2026-02-23',
        'timeslot': 'ALL DAY',  # Officials book entire day
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
            print(f"\n🚫 Auto-rejected ALL Resident Bookings: {len(rejected_bookings)}")
            for i, booking in enumerate(rejected_bookings):
                print(f"  {i+1}. ID: {booking['booking_id']}, Name: {booking['resident_name']}, Email: {booking['resident_email']}, Timeslot: {booking['timeslot']}")
        else:
            print(f"❌ Error: {response.text}")
            
    except Exception as e:
        print(f"❌ Exception: {e}")
    
    # Test 3: Verify final state - should have 1 official booking and all resident bookings rejected
    print("\n3. VERIFYING FINAL STATE...")
    try:
        response = requests.get(check_url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            bookings = data.get('data', [])
            
            target_bookings = [
                booking for booking in bookings 
                if booking.get('booking_date') == '2026-02-23' and booking.get('facility_id') == 1
            ]
            
            print(f"Final booking status for 2026-02-23, Facility 1:")
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
    test_hybrid_auto_rejection()
