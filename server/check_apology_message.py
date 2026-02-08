import requests
import json

def check_apology_message():
    """Check the apology message for rejected booking"""
    
    headers = {
        'Authorization': 'Bearer fe234954-85da-4625-97b8-098f8e1d20d3',
        'Content-Type': 'application/json'
    }
    
    print("=== CHECKING APOLOGY MESSAGE ===")
    
    # Get all bookings
    check_url = "https://intershifting-nakisha-nonspaciously.ngrok-free.dev/api/bookings"
    response = requests.get(check_url, headers=headers, timeout=10)
    
    if response.status_code == 200:
        data = response.json()
        bookings = data.get('data', [])
        
        # Find booking ID 40 (should be rejected)
        target_booking = None
        for booking in bookings:
            if booking.get('id') == 40:
                target_booking = booking
                break
        
        if target_booking:
            print(f"✅ Found booking ID {target_booking.get('id')}")
            print(f"📝 Status: {target_booking.get('status')}")
            print(f"📧 Email: {target_booking.get('user_email')}")
            print(f"⏰ Time: {target_booking.get('start_time')}")
            
            # Check all available fields
            print(f"\n📋 Available fields: {list(target_booking.keys())}")
            
            # Check rejection_reason field
            rejection_reason = target_booking.get('rejection_reason')
            if rejection_reason:
                print(f"\n💬 Rejection Reason:")
                print(rejection_reason)
            else:
                print(f"\n❌ No rejection_reason field found")
                
                # Check if there are any other fields that might contain the apology
                for key, value in target_booking.items():
                    if 'reason' in key.lower() or 'apology' in key.lower() or 'reject' in key.lower():
                        print(f"🔍 Found potential field '{key}': {value}")
        else:
            print("❌ Could not find booking ID 40")
    else:
        print(f"❌ Error: {response.status_code}")

if __name__ == "__main__":
    check_apology_message()
