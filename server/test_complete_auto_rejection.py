import requests
import json

def test_complete_auto_rejection():
    """Test the complete auto-rejection workflow"""
    
    headers = {
        'Authorization': 'Bearer fe234954-85da-4625-97b8-098f8e1d20d3',
        'Content-Type': 'application/json'
    }
    
    print("=== COMPLETE AUTO-REJECTION TEST ===")
    
    # Test 1: Check existing bookings
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
            for booking in target_bookings:
                print(f"  - ID: {booking.get('id')}, Status: {booking.get('status')}, Email: {booking.get('user_email')}, Time: {booking.get('start_time')}")
        else:
            print(f"Error checking bookings: {response.status_code}")
    except Exception as e:
        print(f"Exception checking bookings: {e}")
    
    # Test 2: Create official booking for 8:00 AM - 10:00 AM (should auto-reject booking ID 40)
    print("\n2. TESTING OFFICIAL BOOKING FOR 8:00 AM - 10:00 AM...")
    
    official_booking_data = {
        'facility_id': 1,
        'user_email': 'captain@barangay.gov',  # Official user
        'date': '2026-02-23',
        'timeslot': '8:00 AM - 10:00 AM',
        'purpose': 'Official barangay council meeting',
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
        else:
            print(f"❌ Error: {response.text}")
            
    except Exception as e:
        print(f"❌ Exception: {e}")
    
    # Test 3: Verify the rejected booking has apology message
    print("\n3. VERIFYING APOLOGY MESSAGE...")
    try:
        # Get the specific rejected booking to check the apology message
        check_url = "https://intershifting-nakisha-nonspaciously.ngrok-free.dev/api/bookings"
        response = requests.get(check_url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            bookings = data.get('data', [])
            
            # Find the rejected booking
            rejected_booking = None
            for booking in bookings:
                if (booking.get('id') == 40 and booking.get('status') == 'rejected'):
                    rejected_booking = booking
                    break
            
            if rejected_booking:
                print(f"✅ Found rejected booking ID {rejected_booking.get('id')}")
                print(f"📝 Status: {rejected_booking.get('status')}")
                rejection_reason = rejected_booking.get('rejection_reason', 'Not found')
                print(f"💬 Rejection Reason: {rejection_reason[:100]}..." if len(rejection_reason) > 100 else f"💬 Rejection Reason: {rejection_reason}")
                
                # Check if apology message contains expected content
                expected_phrases = ['apologize', 'official barangay business', 'refund', 'Barangay Management']
                found_phrases = [phrase for phrase in expected_phrases if phrase.lower() in rejection_reason.lower()]
                print(f"✅ Found expected phrases: {found_phrases}")
            else:
                print("❌ Could not find rejected booking with apology message")
        else:
            print(f"❌ Error verifying apology: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Exception verifying apology: {e}")
    
    # Test 4: Check final booking status
    print("\n4. FINAL BOOKING STATUS CHECK...")
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
                print(f"  - ID: {booking.get('id')}, Status: {booking.get('status')}, Email: {booking.get('user_email')}, Time: {booking.get('start_time')}")
                
    except Exception as e:
        print(f"❌ Exception final check: {e}")

if __name__ == "__main__":
    test_complete_auto_rejection()
