import requests
import json

def test_auto_rejection_fix():
    """Test that official bookings auto-reject BOTH pending AND approved resident bookings"""
    
    BASE_URL = "http://192.168.18.132:8000"
    
    print("🧪 TESTING AUTO-REJECTION FIX FOR APPROVED BOOKINGS")
    print("=" * 60)
    
    # Step 1: Login as resident
    print("\n📝 Step 1: Login as resident...")
    resident_login = requests.post(f"{BASE_URL}/api/auth/login", json={
        "email": "saloestillopez@gmail.com",
        "password": "salo3029"
    })
    
    if resident_login.status_code != 200:
        print("❌ Resident login failed")
        return False
    
    resident_token = resident_login.json()['token']
    print("✅ Resident login successful")
    
    # Step 2: Create a resident booking
    print("\n📝 Step 2: Create resident booking...")
    resident_booking = requests.post(f"{BASE_URL}/api/bookings", 
        headers={"Authorization": f"Bearer {resident_token}"},
        json={
            "facility_id": 5,  # Test Facility
            "user_email": "saloestillopez@gmail.com",
            "date": "2026-03-01",
            "timeslot": "8:00 PM - 10:00 PM",
            "total_amount": 100,
            "full_name": "Salo E. Lopez",
            "contact_number": "09656692463",
            "address": "Pasig",
            "purpose": "Test auto-rejection fix"
        }
    )
    
    if resident_booking.status_code != 200:
        print(f"❌ Resident booking failed: {resident_booking.text}")
        return False
    
    resident_booking_id = resident_booking.json()['booking_id']
    print(f"✅ Resident booking created: {resident_booking_id}")
    
    # Step 3: Login as official and approve the resident booking
    print("\n📝 Step 3: Login as official...")
    official_login = requests.post(f"{BASE_URL}/api/auth/login", json={
        "email": "captain@barangay.gov",
        "password": "tatalaPunongBarangayadmin"
    })
    
    if official_login.status_code != 200:
        print("❌ Official login failed")
        return False
    
    official_token = official_login.json()['token']
    print("✅ Official login successful")
    
    # Step 4: Approve the resident booking
    print("\n📝 Step 4: Approve resident booking...")
    approve_response = requests.put(f"{BASE_URL}/api/bookings/{resident_booking_id}/status",
        headers={"Authorization": f"Bearer {official_token}"},
        json={"status": "approved"}
    )
    
    if approve_response.status_code != 200:
        print(f"❌ Approval failed: {approve_response.text}")
        return False
    
    print("✅ Resident booking approved")
    
    # Step 5: Create an official booking on the same date
    print("\n📝 Step 5: Create overlapping official booking...")
    official_booking = requests.post(f"{BASE_URL}/api/bookings",
        headers={"Authorization": f"Bearer {official_token}"},
        json={
            "facility_id": 5,  # Same facility
            "user_email": "captain@barangay.gov",
            "date": "2026-03-01",  # Same date
            "timeslot": "ALL DAY",  # This should trigger auto-rejection for ALL resident bookings
            "total_amount": 0,
            "full_name": "Barangay Official",
            "contact_number": "09123456789",
            "address": "Barangay Hall",
            "purpose": "Official barangay business",
            "user_role": "official"
        }
    )
    
    if official_booking.status_code != 200:
        print(f"❌ Official booking failed: {official_booking.text}")
        return False
    
    print("✅ Official booking created")
    
    # Step 6: Check if resident booking was auto-rejected
    print("\n📝 Step 6: Check resident booking status...")
    check_response = requests.get(f"{BASE_URL}/api/bookings?user_role=resident&user_email=saloestillopez@gmail.com",
        headers={"Authorization": f"Bearer {resident_token}"}
    )
    
    if check_response.status_code != 200:
        print(f"❌ Failed to check booking status: {check_response.text}")
        return False
    
    try:
        bookings_data = check_response.json()
        print(f"🔍 DEBUG: Response type: {type(bookings_data)}")
        print(f"🔍 DEBUG: Response keys: {bookings_data.keys() if isinstance(bookings_data, dict) else 'Not a dict'}")
        # Handle both list and dict responses
        if isinstance(bookings_data, dict) and 'bookings' in bookings_data:
            bookings = bookings_data['bookings']
        elif isinstance(bookings_data, list):
            bookings = bookings_data
        elif isinstance(bookings_data, dict):
            # If it's a dict but no 'bookings' key, check if it has booking data directly
            bookings = [bookings_data] if 'id' in bookings_data else []
        else:
            print(f"❌ Unexpected response format: {type(bookings_data)}")
            return False
    except Exception as e:
        print(f"❌ Failed to parse bookings response: {e}")
        print(f"Response text: {check_response.text}")
        return False
    target_booking = None
    for booking in bookings:
        if booking['id'] == resident_booking_id:
            target_booking = booking
            break
    
    if not target_booking:
        print("❌ Could not find the resident booking")
        return False
    
    print(f"📊 Resident booking status: {target_booking['status']}")
    print(f"📊 Rejection reason: {target_booking.get('rejection_reason', 'None')}")
    
    # Step 7: Verify the fix
    if target_booking['status'] == 'rejected' and target_booking.get('rejection_reason'):
        print("✅ SUCCESS: Approved resident booking was auto-rejected with apology!")
        print(f"📝 Rejection reason: {target_booking['rejection_reason']}")
        return True
    else:
        print("❌ FAILURE: Approved resident booking was NOT auto-rejected")
        return False

if __name__ == "__main__":
    success = test_auto_rejection_fix()
    if success:
        print("\n🎉 AUTO-REJECTION FIX VERIFICATION: PASSED")
    else:
        print("\n💥 AUTO-REJECTION FIX VERIFICATION: FAILED")
