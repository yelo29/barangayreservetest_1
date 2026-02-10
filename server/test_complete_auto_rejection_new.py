import requests
import json

def test_complete_auto_rejection():
    """Test complete auto-rejection flow"""
    
    BASE_URL = "http://192.168.18.132:8000"
    
    print("🧪 TESTING COMPLETE AUTO-REJECTION FLOW")
    print("=" * 50)
    
    # Step 1: Login as resident and create a booking
    print("\n📝 Step 1: Create resident booking...")
    resident_login = requests.post(f"{BASE_URL}/api/auth/login", json={
        "email": "saloestillopez@gmail.com",  # Use different resident
        "password": "password123"
    })
    
    if resident_login.status_code != 200:
        print("❌ Resident login failed")
        return False
    
    resident_token = resident_login.json()['token']
    
    # Create resident booking
    resident_booking = requests.post(f"{BASE_URL}/api/bookings", 
        headers={"Authorization": f"Bearer {resident_token}"},
        json={
            "facility_id": 1,  # Community Hall
            "user_email": "saloestillopez@gmail.com",
            "date": "2026-03-15",  # Future date
            "timeslot": "2:00 PM - 4:00 PM",
            "total_amount": 1000,
            "full_name": "Salo E. Lopez",
            "contact_number": "09656692463",
            "address": "Pasig",
            "purpose": "Test auto-rejection complete flow"
        }
    )
    
    if resident_booking.status_code != 200:
        print(f"❌ Resident booking failed: {resident_booking.text}")
        return False
    
    resident_booking_id = resident_booking.json()['booking_id']
    print(f"✅ Resident booking created: {resident_booking_id}")
    
    # Step 2: Login as official
    print("\n📝 Step 2: Login as official...")
    official_login = requests.post(f"{BASE_URL}/api/auth/login", json={
        "email": "captain@barangay.gov",
        "password": "tatalaPunongBarangayadmin"
    })
    
    if official_login.status_code != 200:
        print("❌ Official login failed")
        return False
    
    official_token = official_login.json()['token']
    print("✅ Official login successful")
    
    # Step 3: Create overlapping official booking
    print("\n📝 Step 3: Create overlapping official booking...")
    official_booking = requests.post(f"{BASE_URL}/api/bookings",
        headers={"Authorization": f"Bearer {official_token}"},
        json={
            "facility_id": 1,  # Same facility
            "user_email": "captain@barangay.gov",
            "date": "2026-03-15",  # Same date
            "timeslot": "2:00 PM - 4:00 PM",  # Same time slot
            "total_amount": 0,
            "full_name": "Barangay Official",
            "contact_number": "09123456789",
            "address": "Barangay Hall",
            "purpose": "Test auto-rejection complete flow",
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
    test_complete_auto_rejection()
