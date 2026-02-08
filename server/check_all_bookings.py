import requests
import json

def check_all_bookings():
    """Check all bookings to find the rejected one"""
    
    headers = {
        'Authorization': 'Bearer fe234954-85da-4625-97b8-098f8e1d20d3',
        'Content-Type': 'application/json'
    }
    
    print("=== CHECKING ALL BOOKINGS ===")
    
    # Get all bookings
    check_url = "https://intershifting-nakisha-nonspaciously.ngrok-free.dev/api/bookings"
    response = requests.get(check_url, headers=headers, timeout=10)
    
    if response.status_code == 200:
        data = response.json()
        bookings = data.get('data', [])
        
        print(f"Total bookings found: {len(bookings)}")
        
        # Find all bookings for 2026-02-23, Facility 1
        target_bookings = [
            booking for booking in bookings 
            if booking.get('booking_date') == '2026-02-23' and booking.get('facility_id') == 1
        ]
        
        print(f"\nBookings for 2026-02-23, Facility 1:")
        for booking in sorted(target_bookings, key=lambda x: x.get('id')):
            print(f"  - ID: {booking.get('id')}, Status: {booking.get('status')}, Email: {booking.get('user_email')}, Time: {booking.get('start_time')}")
            
            # Check if this is a rejected booking
            if booking.get('status') == 'rejected':
                print(f"    🚫 Rejected booking found!")
                rejection_reason = booking.get('rejection_reason')
                if rejection_reason:
                    print(f"    💬 Rejection Reason: {rejection_reason[:100]}...")
                else:
                    print(f"    ❌ No rejection_reason field")
                    
                # Check all fields for this booking
                print(f"    📋 Fields: {list(booking.keys())}")
    else:
        print(f"❌ Error: {response.status_code}")

if __name__ == "__main__":
    check_all_bookings()
