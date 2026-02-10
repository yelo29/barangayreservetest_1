import requests

def test_timeslot_lock_logic():
    """Test the new timeslot lock logic for residents"""
    
    BASE_URL = "http://192.168.18.132:8000"
    
    print("🧪 TESTING TIMESLOT LOCK LOGIC")
    print("=" * 50)
    
    # Step 1: Create first resident booking
    print("📝 Step 1: Create booking for Resident A...")
    
    # Login as resident
    login_response = requests.post(f"{BASE_URL}/api/auth/login",
        json={
            "email": "leo052904@gmail.com", 
            "password": "leo3029"
        }
    )
    
    if login_response.status_code == 200:
        token = login_response.json()['token']
        
        # Create booking for March 10, 6-8 AM
        booking_data = {
            "facility_id": 5,
            "user_email": "leo052904@gmail.com",
            "date": "2026-03-10",
            "timeslot": "6:00 AM - 8:00 AM",
            "purpose": "Resident A Test Booking",
            "total_amount": 100,
            "full_name": "Resident A",
            "contact_number": "09111111111",
            "address": "Test Address",
            "receipt_base64": "",
            "valid_id_base64": "",
            "user_role": "resident",
            "status": "pending"
        }
        
        create_response = requests.post(f"{BASE_URL}/api/bookings",
            headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
            json=booking_data
        )
        
        if create_response.status_code == 200:
            print("✅ Resident A booking created successfully")
        else:
            print(f"❌ Failed to create Resident A booking: {create_response.text}")
    
    # Step 2: Check available timeslots for different user
    print("\n📝 Step 2: Check timeslots for different user (should show locked)...")
    
    # Check available timeslots for different user
    timeslot_response = requests.get(
        f"{BASE_URL}/api/available-timeslots?facility_id=5&date=2026-03-10&user_email=saloestillopez@gmail.com",
        headers={"Content-Type": "application/json"}
    )
    
    if timeslot_response.status_code == 200:
        timeslot_data = timeslot_response.json()
        print(f"📊 Available timeslots for different user: {timeslot_data}")
        
        # Check if 6:00 AM - 8:00 AM is properly locked
        user_booked_timeslots = timeslot_data.get('user_booked_timeslots', [])
        competitive_timeslots = timeslot_data.get('competitive_timeslots', [])
        
        target_timeslot = "6:00 AM - 8:00 AM"
        
        if target_timeslot in user_booked_timeslots:
            print("✅ SUCCESS: Target timeslot is in user_booked_timeslots (properly locked)")
        elif target_timeslot in competitive_timeslots:
            print("⚠️ WARNING: Target timeslot is in competitive_timeslots (should be in user_booked_timeslots)")
        else:
            print("❌ ISSUE: Target timeslot is still available")
    else:
        print(f"❌ Failed to get timeslots: {timeslot_response.text}")

if __name__ == "__main__":
    test_timeslot_lock_logic()
