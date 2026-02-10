import requests
import json

def test_all_day_auto_rejection():
    """Test ALL DAY auto-rejection on Feb 23rd"""
    
    BASE_URL = "http://192.168.18.132:8000"
    
    print("🧪 TESTING ALL DAY AUTO-REJECTION ON FEB 23RD")
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
    
    # Create ALL DAY official booking on Feb 23rd
    print("\n📝 Step 2: Create ALL DAY official booking on Feb 23rd...")
    official_booking = requests.post(f"{BASE_URL}/api/bookings",
        headers={"Authorization": f"Bearer {official_token}"},
        json={
            "facility_id": 1,  # Community Hall
            "user_email": "captain@barangay.gov",
            "date": "2026-02-23",  # Date with resident booking
            "timeslot": "ALL DAY",  # This should reject ALL resident bookings
            "total_amount": 0,
            "full_name": "Barangay Official",
            "contact_number": "09123456789",
            "address": "Barangay Hall",
            "purpose": "Test ALL DAY auto-rejection",
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
    test_all_day_auto_rejection()
