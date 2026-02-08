import requests
import json

def test_resident_booking_api():
    """Test the resident booking API to check if rejection_reason is included"""
    
    base_url = "https://intershifting-nakisha-nonspaciously.ngrok-free.dev"
    
    # Test fetching bookings for resident01@gmail.com
    print("=== TESTING RESIDENT BOOKING API ===")
    
    # First login to get token
    login_data = {
        "email": "resident01@gmail.com",
        "password": "resident01"
    }
    
    try:
        # Login
        print("🔍 Logging in as resident01@gmail.com...")
        login_response = requests.post(f"{base_url}/api/auth/login", json=login_data)
        
        if login_response.status_code != 200:
            print(f"❌ Login failed: {login_response.status_code}")
            print(f"Response: {login_response.text}")
            return
            
        login_data = login_response.json()
        token = login_data.get('token')
        print(f"✅ Login successful, token: {token[:20]}...")
        
        # Fetch bookings
        headers = {"Authorization": f"Bearer {token}"}
        bookings_url = f"{base_url}/api/bookings?user_role=resident&user_email=resident01%40gmail.com"
        
        print(f"🔍 Fetching bookings from: {bookings_url}")
        bookings_response = requests.get(bookings_url, headers=headers)
        
        if bookings_response.status_code != 200:
            print(f"❌ Failed to fetch bookings: {bookings_response.status_code}")
            print(f"Response: {bookings_response.text}")
            return
            
        bookings_data = bookings_response.json()
        print(f"✅ Bookings fetched successfully")
        
        # Look for the specific booking (ID 65 - the one that was auto-rejected)
        bookings = bookings_data.get('data', [])
        print(f"📊 Found {len(bookings)} total bookings")
        
        # Find booking ID 65
        target_booking = None
        for booking in bookings:
            if booking.get('id') == 65:
                target_booking = booking
                break
        
        if target_booking:
            print(f"\n🎯 FOUND TARGET BOOKING (ID 65):")
            print(f"📅 Date: {target_booking.get('booking_date')}")
            print(f"🏢 Facility: {target_booking.get('facility_name')} (ID: {target_booking.get('facility_id')})")
            print(f"⏰ Time: {target_booking.get('start_time')} - {target_booking.get('end_time')}")
            print(f"📊 Status: {target_booking.get('status')}")
            print(f"💬 Rejection Reason: '{target_booking.get('rejection_reason')}'")
            print(f"🎯 Purpose: {target_booking.get('purpose')}")
            print(f"👤 Email: {target_booking.get('user_email')}")
            print(f"🆔 ID: {target_booking.get('id')}")
            
            # Check all fields
            print(f"\n🔍 ALL FIELDS IN BOOKING:")
            for key, value in target_booking.items():
                if 'rejection' in key.lower() or key == 'status':
                    print(f"  {key}: {value}")
        else:
            print(f"❌ Booking ID 65 not found in the response")
            
            # Show all rejected bookings
            print(f"\n🔍 ALL REJECTED BOOKINGS:")
            rejected_count = 0
            for booking in bookings:
                if booking.get('status') == 'rejected':
                    rejected_count += 1
                    print(f"  ID {booking.get('id')}: {booking.get('booking_date')} - {booking.get('facility_name')} - rejection_reason: '{booking.get('rejection_reason')}'")
            
            print(f"📊 Total rejected bookings: {rejected_count}")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_resident_booking_api()
