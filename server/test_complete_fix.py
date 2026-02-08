import requests
import json

def test_complete_fix():
    """Test the complete fix for UI overflow and resident booking updates"""
    
    headers = {
        'Authorization': 'Bearer fe234954-85da-4625-97b8-098f8e1d20d3',
        'Content-Type': 'application/json'
    }
    
    print("=== TESTING COMPLETE FIX ===")
    print("Testing: UI overflow fix + resident booking update")
    
    # Test 1: Create a new resident booking for testing
    print("\n1. CREATING TEST RESIDENT BOOKING...")
    resident_booking_data = {
        'facility_id': 1,
        'user_email': 'resident01@gmail.com',
        'date': '2026-02-26',  # New date for testing
        'timeslot': '2:00 PM - 4:00 PM',
        'purpose': 'Test booking for UI overflow fix',
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
            print(f"✅ Resident booking created: ID {result.get('booking_id')}")
        else:
            print(f"❌ Error creating resident booking: {response.text}")
            return
    except Exception as e:
        print(f"❌ Exception: {e}")
        return
    
    # Test 2: Create official booking to auto-reject
    print("\n2. CREATING OFFICIAL BOOKING...")
    
    official_booking_data = {
        'facility_id': 1,
        'user_email': 'captain@barangay.gov',
        'date': '2026-02-26',
        'timeslot': 'ALL DAY',
        'purpose': 'Official barangay council meeting - entire day booking',
        'contact_number': '09123456789',
        'address': 'Barangay Hall'
    }
    
    try:
        response = requests.post(create_url, headers=headers, json=official_booking_data, timeout=10)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Official booking created: ID {result.get('booking_id')}")
            print(f"📝 Message: {result.get('message')}")
            
            rejected_bookings = result.get('rejected_resident_bookings', [])
            print(f"\n🚫 Auto-rejected Resident Bookings: {len(rejected_bookings)}")
            
            for i, booking in enumerate(rejected_bookings):
                timeslot = booking['timeslot']
                print(f"  {i+1}. ID: {booking['booking_id']}, Name: {booking['resident_name']}")
                print(f"      Email: {booking['resident_email']}")
                print(f"      Timeslot: '{timeslot}'")
                
                # Check if timeslot is fixed (no duplicate)
                if ' - ' in timeslot and timeslot.count(' - ') == 1:
                    print(f"      ✅ FIXED: Timeslot format is correct")
                else:
                    print(f"      ❌ ERROR: Timeslot still has duplicate format")
                    
        else:
            print(f"❌ Error creating official booking: {response.text}")
            
    except Exception as e:
        print(f"❌ Exception: {e}")
    
    # Test 3: Verify resident booking has apology message
    print("\n3. VERIFYING APOLOGY MESSAGE...")
    try:
        check_url = "https://intershifting-nakisha-nonspaciously.ngrok-free.dev/api/bookings"
        response = requests.get(check_url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            bookings = data.get('data', [])
            
            # Find the resident booking we just rejected
            resident_booking = None
            for booking in bookings:
                if (booking.get('booking_date') == '2026-02-26' and 
                    booking.get('facility_id') == 1 and 
                    booking.get('user_email') == 'resident01@gmail.com'):
                    resident_booking = booking
                    break
            
            if resident_booking:
                print(f"✅ Found resident booking: ID {resident_booking.get('id')}")
                print(f"📊 Status: {resident_booking.get('status')}")
                
                rejection_reason = resident_booking.get('rejection_reason', '')
                if rejection_reason:
                    print(f"💬 Rejection Reason: {rejection_reason[:50]}...")
                    if 'apologize' in rejection_reason.lower():
                        print(f"✅ FIXED: Apology message is present")
                    else:
                        print(f"❌ ERROR: No apology message found")
                else:
                    print(f"❌ ERROR: No rejection reason found")
            else:
                print("❌ ERROR: Could not find resident booking")
        else:
            print(f"❌ Error verifying: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Exception verifying: {e}")

if __name__ == "__main__":
    test_complete_fix()
