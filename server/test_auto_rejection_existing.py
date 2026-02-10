import requests
import json

def test_auto_rejection_existing():
    """Test auto-rejection with existing resident booking on Feb 23"""
    
    BASE_URL = "http://192.168.18.132:8000"
    
    print("🧪 TESTING AUTO-REJECTION WITH EXISTING BOOKING")
    print("=" * 50)
    
    # Step 1: Login as official
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
    
    # Step 2: Create overlapping official booking on Feb 23
    print("\n📝 Step 2: Create overlapping official booking on Feb 23...")
    official_booking = requests.post(f"{BASE_URL}/api/bookings",
        headers={"Authorization": f"Bearer {official_token}"},
        json={
            "facility_id": 1,  # Community Hall
            "user_email": "captain@barangay.gov",
            "date": "2026-02-23",  # Date with existing resident booking
            "timeslot": "6:00 AM - 8:00 AM",  # Exact same time as resident booking
            "total_amount": 0,
            "full_name": "Barangay Official",
            "contact_number": "09123456789",
            "address": "Barangay Hall",
            "purpose": "Test auto-rejection existing booking",
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
    test_auto_rejection_existing()
