import requests
import json

def test_fixed_auto_rejection():
    """Test the fixed auto-rejection implementation"""
    
    headers = {
        'Authorization': 'Bearer fe234954-85da-4625-97b8-098f8e1d20d3',
        'Content-Type': 'application/json'
    }
    
    print("=== TESTING FIXED AUTO-REJECTION ===")
    
    # Test 1: Create official booking for 2026-02-20 (should reject resident booking ID 38)
    print("\n1. TESTING OFFICIAL BOOKING FOR 2026-02-20...")
    
    official_booking_data = {
        'facility_id': 1,
        'user_email': 'captain@barangay.gov',  # Official user
        'date': '2026-02-20',
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
            print(f"\n🚫 Auto-rejected Resident Bookings: {len(rejected_bookings)}")
            for i, booking in enumerate(rejected_bookings):
                print(f"  {i+1}. ID: {booking['booking_id']}, Name: {booking['resident_name']}, Email: {booking['resident_email']}, Timeslot: {booking['timeslot']}")
                
                # Check if timeslot shows actual resident time (not "ALL DAY")
                if booking['timeslot'] == 'ALL DAY':
                    print(f"    ❌ ERROR: Timeslot should show resident's actual time, not 'ALL DAY'")
                else:
                    print(f"    ✅ CORRECT: Shows resident's actual time slot")
                    
        else:
            print(f"❌ Error: {response.text}")
            
    except Exception as e:
        print(f"❌ Exception: {e}")
    
    # Test 2: Verify the rejected booking in database
    print("\n2. VERIFYING REJECTED BOOKING IN DATABASE...")
    try:
        check_url = "https://intershifting-nakisha-nonspaciously.ngrok-free.dev/api/bookings"
        response = requests.get(check_url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            bookings = data.get('data', [])
            
            # Find booking ID 38
            target_booking = None
            for booking in bookings:
                if booking.get('id') == 38:
                    target_booking = booking
                    break
            
            if target_booking:
                print(f"✅ Found booking ID {target_booking.get('id')}")
                print(f"📝 Status: {target_booking.get('status')}")
                print(f"⏰ Time: {target_booking.get('start_time')} - {target_booking.get('end_time')}")
                
                rejection_reason = target_booking.get('rejection_reason', 'Not found')
                print(f"💬 Rejection Reason: {rejection_reason[:100]}..." if len(rejection_reason) > 100 else f"💬 Rejection Reason: {rejection_reason}")
                
                if target_booking.get('status') == 'rejected':
                    print(f"✅ SUCCESS: Booking correctly rejected")
                else:
                    print(f"❌ ERROR: Booking should be rejected but status is {target_booking.get('status')}")
            else:
                print("❌ Could not find booking ID 38")
        else:
            print(f"❌ Error verifying: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Exception verifying: {e}")

if __name__ == "__main__":
    test_fixed_auto_rejection()
