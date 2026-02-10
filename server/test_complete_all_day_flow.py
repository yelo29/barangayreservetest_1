import sqlite3
import requests
import json

def test_complete_all_day_flow():
    """Test complete ALL DAY auto-rejection flow"""
    
    BASE_URL = "http://192.168.18.132:8000"
    
    print("🧪 TESTING COMPLETE ALL DAY AUTO-REJECTION FLOW")
    print("=" * 50)
    
    # Step 1: Create a resident booking manually in database
    print("\n📝 Step 1: Create resident booking manually...")
    conn = sqlite3.connect('barangay.db')
    cursor = conn.cursor()
    
    # Get user ID for saloestillopez@gmail.com
    cursor.execute('SELECT id FROM users WHERE email = ?', ('saloestillopez@gmail.com',))
    user_result = cursor.fetchone()
    if not user_result:
        print("❌ Resident user not found")
        return False
    
    user_id = user_result[0]
    
    # Create resident booking
    cursor.execute('''
        INSERT INTO bookings (
            facility_id, user_id, booking_date, start_time, end_time, status,
            purpose, total_amount, base_rate, downpayment_amount, booking_reference,
            time_slot_id, duration_hours, created_at, updated_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
    ''', (
        1,  # Community Hall
        user_id,
        '2026-04-04',  # Future date
        '10:00 AM - 12:00 PM',
        '10:00 AM - 12:00 PM',
        'approved',  # Set as approved to test approved booking auto-rejection
        'Test ALL DAY auto-rejection',
        1000,
        1000,
        500,
        f'BR20260409180000{user_id}',  # Generate booking reference
        164,  # time_slot_id for 10:00 AM - 12:00 PM
        2.0   # duration_hours (2 hours)
    ))
    
    resident_booking_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    print(f"✅ Created resident booking: {resident_booking_id}")
    
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
    
    # Step 3: Create ALL DAY official booking
    print("\n📝 Step 3: Create ALL DAY official booking...")
    official_booking = requests.post(f"{BASE_URL}/api/bookings",
        headers={"Authorization": f"Bearer {official_token}"},
        json={
            "facility_id": 1,  # Community Hall
            "user_email": "captain@barangay.gov",
            "date": "2026-04-04",  # Same date as resident booking
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
            
            # Verify the resident booking was actually rejected
            conn = sqlite3.connect('barangay.db')
            cursor = conn.cursor()
            cursor.execute('SELECT status, rejection_reason FROM bookings WHERE id = ?', (resident_booking_id,))
            result = cursor.fetchone()
            if result:
                status, rejection_reason = result
                print(f"🔍 Resident booking status: {status}")
                print(f"🔍 Rejection reason: {rejection_reason if rejection_reason else 'None'}")
                if status == 'rejected' and rejection_reason:
                    print("✅ SUCCESS: ALL DAY auto-rejection is working!")
                    return True
                else:
                    print("❌ FAILURE: Booking was not properly rejected")
                    return False
            conn.close()
        else:
            print("❌ Auto-rejection failed - no rejected bookings")
            return False
    else:
        print("❌ Official booking failed")
        return False

if __name__ == "__main__":
    test_complete_all_day_flow()
