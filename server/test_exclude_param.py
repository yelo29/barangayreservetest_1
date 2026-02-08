#!/usr/bin/env python3
import requests
import json

def test_api():
    base_url = "http://192.168.18.132:5000/api/bookings"
    
    # Test with excludeUserRole parameter
    url_with_exclude = f"{base_url}?excludeUserRole=true"
    
    try:
        print(f"Testing API with excludeUserRole: {url_with_exclude}")
        response = requests.get(url_with_exclude)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Success: {data.get('success')}")
            print(f"Data length: {len(data.get('data', []))}")
            
            # Print first few bookings
            bookings = data.get('data', [])
            print(f"First 5 bookings:")
            for i, booking in enumerate(bookings[:5]):
                print(f"  Booking {i+1}: Date={booking.get('booking_date')}, Facility={booking.get('facility_id')}, Email={booking.get('user_email')}, Status={booking.get('status')}, Role={booking.get('user_role', 'N/A')}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    test_api()
