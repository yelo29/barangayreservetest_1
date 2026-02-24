#!/usr/bin/env python3
"""
Test Data Isolation Fix
"""

import requests
import json

def test_data_isolation():
    """Test that facility filtering works correctly"""
    base_url = "http://192.168.18.132:8000"
    
    print("🧪 TESTING DATA ISOLATION FIX")
    print("=" * 50)
    
    # Test 1: Get all bookings (should be many)
    print("\n📋 Test 1: All bookings (no facility filter)")
    response = requests.get(f"{base_url}/api/bookings?user_role=resident&user_email=leo052904@gmail.com")
    
    if response.status_code == 200:
        data = response.json()
        all_bookings = data.get('data', [])
        print(f"  ✅ Total bookings: {len(all_bookings)}")
    else:
        print(f"  ❌ Error: {response.status_code}")
        return
    
    # Test 2: Get Basketball Court bookings only (should be 1)
    print("\n🏀 Test 2: Basketball Court bookings (facility_id=10)")
    response = requests.get(f"{base_url}/api/bookings?facility_id=10&user_role=resident&user_email=leo052904@gmail.com")
    
    if response.status_code == 200:
        data = response.json()
        basketball_bookings = data.get('data', [])
        print(f"  ✅ Basketball Court bookings: {len(basketball_bookings)}")
        
        for booking in basketball_bookings:
            facility_name = booking.get('facility_name', 'Unknown')
            date = booking.get('booking_date', 'Unknown')
            status = booking.get('status', 'Unknown')
            email = booking.get('user_email', 'Unknown')
            print(f"    - {facility_name}: {date} - {status} - {email}")
    else:
        print(f"  ❌ Error: {response.status_code}")
    
    # Test 3: Get Community Hall bookings only (should be many)
    print("\n🏛️ Test 3: Community Hall bookings (facility_id=1)")
    response = requests.get(f"{base_url}/api/bookings?facility_id=1&user_role=resident&user_email=leo052904@gmail.com")
    
    if response.status_code == 200:
        data = response.json()
        hall_bookings = data.get('data', [])
        print(f"  ✅ Community Hall bookings: {len(hall_bookings)}")
    else:
        print(f"  ❌ Error: {response.status_code}")
    
    # Test 4: Test date filtering with facility
    print("\n📅 Test 4: Basketball Court on 2026-03-06 (specific date)")
    response = requests.get(f"{base_url}/api/bookings?facility_id=10&date=2026-03-06&user_role=resident&user_email=leo052904@gmail.com")
    
    if response.status_code == 200:
        data = response.json()
        specific_bookings = data.get('data', [])
        print(f"  ✅ Basketball Court on 2026-03-06: {len(specific_bookings)}")
        
        for booking in specific_bookings:
            facility_name = booking.get('facility_name', 'Unknown')
            date = booking.get('booking_date', 'Unknown')
            status = booking.get('status', 'Unknown')
            email = booking.get('user_email', 'Unknown')
            print(f"    - {facility_name}: {date} - {status} - {email}")
    else:
        print(f"  ❌ Error: {response.status_code}")
    
    print("\n✅ Data isolation test completed!")
    print("📊 Summary:")
    print(f"  - All bookings: {len(all_bookings)}")
    print(f"  - Basketball Court only: {len(basketball_bookings)}")
    print(f"  - Community Hall only: {len(hall_bookings)}")
    print(f"  - Basketball Court on specific date: {len(specific_bookings)}")
    
    # Verify isolation is working
    if len(basketball_bookings) < len(all_bookings):
        print("  ✅ Data isolation is WORKING!")
    else:
        print("  ❌ Data isolation is NOT working!")

if __name__ == "__main__":
    test_data_isolation()
