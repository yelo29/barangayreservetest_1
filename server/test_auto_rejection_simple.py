import requests
import json

def test_auto_rejection_simple():
    """Simple test to trigger auto-rejection with debug logs"""
    
    BASE_URL = "http://192.168.18.132:8000"
    
    print("🧪 SIMPLE AUTO-REJECTION TEST")
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
    
    # Step 2: Create an official booking on a date with existing resident bookings
    print("\n📝 Step 2: Create official booking on date with resident bookings...")
    official_booking = requests.post(f"{BASE_URL}/api/bookings",
        headers={"Authorization": f"Bearer {official_token}"},
        json={
            "facility_id": 5,  # Test Facility
            "user_email": "captain@barangay.gov",
            "date": "2026-02-15",  # Date with resident bookings but no official bookings
            "timeslot": "ALL DAY",
            "total_amount": 0,
            "full_name": "Barangay Official",
            "contact_number": "09123456789",
            "address": "Barangay Hall",
            "purpose": "Test auto-rejection trigger",
            "user_role": "official"
        }
    )
    
    print(f"📊 Official booking response status: {official_booking.status_code}")
    print(f"📊 Official booking response: {official_booking.text}")
    
    if official_booking.status_code == 200:
        print("✅ Official booking created - should have triggered auto-rejection")
        return True
    else:
        print("❌ Official booking failed")
        return False

if __name__ == "__main__":
    test_auto_rejection_simple()
