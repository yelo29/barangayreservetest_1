import requests
import json

def test_auto_rejection_new():
    """Test auto-rejection with a new resident booking"""
    
    BASE_URL = "http://192.168.18.132:8000"
    
    print("🧪 TESTING AUTO-REJECTION WITH NEW BOOKING")
    print("=" * 50)
    
    # Step 1: Login as resident
    print("\n📝 Step 1: Login as resident...")
    resident_login = requests.post(f"{BASE_URL}/api/auth/login", json={
        "email": "leo052904@gmail.com",
        "password": "leo123",
    })
    
    if resident_login.status_code != 200:
        print("❌ Resident login failed")
        return False
    
    resident_token = resident_login.json()['token']
    print("✅ Resident login successful")
    
    # Step 2: Create a new resident booking
    print("\n📝 Step 2: Create new resident booking...")
    resident_booking = requests.post(f"{BASE_URL}/api/bookings", 
        headers={"Authorization": f"Bearer {resident_token}"},
        json={
            "facility_id": 1,  # Community Hall
            "user_email": "leo052904@gmail.com",
            "date": "2026-03-05",  # Future date
            "timeslot": "10:00 AM - 12:00 PM",
            "total_amount": 1000,
            "full_name": "John Leo L. Lopez",
            "contact_number": "09656692463",
            "address": "Mountain",
            "purpose": "Test auto-rejection new booking"
        }
    )
    
    if resident_booking.status_code != 200:
        print(f"❌ Resident booking failed: {resident_booking.text}")
        return False
    
    resident_booking_id = resident_booking.json()['booking_id']
    print(f"✅ Resident booking created: {resident_booking_id}")
    
    # Step 3: Login as official
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
    
    # Step 4: Create overlapping official booking
    print("\n📝 Step 4: Create overlapping official booking...")
    official_booking = requests.post(f"{BASE_URL}/api/bookings",
        headers={"Authorization": f"Bearer {official_token}"},
        json={
            "facility_id": 1,  # Same facility
            "user_email": "captain@barangay.gov",
            "date": "2026-03-05",  # Same date
            "timeslot": "ALL DAY",  # This should trigger auto-rejection
            "total_amount": 0,
            "full_name": "Barangay Official",
            "contact_number": "09123456789",
            "address": "Barangay Hall",
            "purpose": "Test auto-rejection new booking",
            "user_role": "official"
        }
    )
    
    print(f"📊 Official booking response status: {official_booking.status_code}")
    print(f"📊 Official booking response: {official_booking.text}")
    
    if official_booking.status_code == 200:
        response_data = official_booking.json()
        if 'rejected_resident_bookings' in response_data and response_data['rejected_resident_bookings']:
            print("✅ Auto-rejection worked!")
            return True
        else:
            print("❌ Auto-rejection failed - no rejected bookings")
            return False
    else:
        print("❌ Official booking failed")
        return False

if __name__ == "__main__":
    test_auto_rejection_new()
