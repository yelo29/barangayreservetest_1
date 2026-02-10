import requests
import json

def test_debug_auto_rejection():
    """Test auto-rejection with debug output"""
    
    BASE_URL = "http://192.168.18.132:8000"
    
    print("🧪 TESTING AUTO-REJECTION WITH DEBUG")
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
    
    # Create official booking on a date with NO existing bookings to see debug
    print("\n📝 Step 2: Create official booking on new date...")
    official_booking = requests.post(f"{BASE_URL}/api/bookings",
        headers={"Authorization": f"Bearer {official_token}"},
        json={
            "facility_id": 1,  # Community Hall
            "user_email": "captain@barangay.gov",
            "date": "2026-03-10",  # New date
            "timeslot": "2:00 PM - 4:00 PM",  # Different time slot
            "total_amount": 0,
            "full_name": "Barangay Official",
            "contact_number": "09123456789",
            "address": "Barangay Hall",
            "purpose": "Test debug auto-rejection",
            "user_role": "official"
        }
    )
    
    print(f"📊 Official booking response status: {official_booking.status_code}")
    print(f"📊 Official booking response: {official_booking.text}")
    
    return official_booking.status_code == 200

if __name__ == "__main__":
    test_debug_auto_rejection()
