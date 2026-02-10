import requests
import json

def test_feb_15_auto_rejection():
    """Test auto-rejection on Feb 15th (has resident booking)"""
    
    BASE_URL = "http://192.168.18.132:8000"
    
    print("🧪 TESTING AUTO-REJECTION ON FEB 15TH")
    print("=" * 50)
    
    # Login as official
    print("\n📝 Step 1: Login as official...")
    official_login = requests.post(f"{BASE_URL}/api/auth/login", json={
        "email": "captain@barangay.gov",
        "password": "tatalaPunongBarangayadmin"
    })
    
    if official_login.status_code != 200:
        print("❌ Official login failed")
        return False
    
    official_token = official_login.json()['token']
    print("✅ Official login successful")
    
    # Check what resident booking exists on Feb 15th
    print("\n📝 Step 2: Check existing bookings on Feb 15th...")
    
    # Create overlapping official booking
    print("\n📝 Step 3: Create overlapping official booking on Feb 15th...")
    official_booking = requests.post(f"{BASE_URL}/api/bookings",
        headers={"Authorization": f"Bearer {official_token}"},
        json={
            "facility_id": 5,  # Test Facility (has resident booking on Feb 15)
            "user_email": "captain@barangay.gov",
            "date": "2026-02-15",  # Date with resident booking
            "timeslot": "10:00 AM - 12:00 PM",  # Same time as resident booking
            "total_amount": 0,
            "full_name": "Barangay Official",
            "contact_number": "09123456789",
            "address": "Barangay Hall",
            "purpose": "Test auto-rejection Feb 15",
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
    test_feb_15_auto_rejection()
