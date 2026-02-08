#!/usr/bin/env python3
import requests
import json

def test_api():
    url = "http://192.168.18.132:5000/api/bookings"
    
    try:
        print(f"Testing API: {url}")
        response = requests.get(url)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Success: {data.get('success')}")
            print(f"Data length: {len(data.get('data', []))}")
            
            # Print first few bookings
            bookings = data.get('data', [])
            for i, booking in enumerate(bookings[:3]):
                print(f"  Booking {i+1}: {booking.get('booking_date')} - {booking.get('user_email')} - {booking.get('status')}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    test_api()
