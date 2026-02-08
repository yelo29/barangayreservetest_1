import requests
import json

def test_timeslot_display():
    """Test that time slots display correctly for officials"""
    
    headers = {
        'Authorization': 'Bearer fe234954-85da-4625-97b8-098f8e1d20d3',
        'Content-Type': 'application/json'
    }
    
    print("=== TESTING TIME SLOT DISPLAY FOR OFFICIALS ===")
    
    # Test the available timeslots endpoint for a date with resident bookings
    test_date = '2026-02-11'  # Date from logs that has resident booking
    facility_id = '3'  # Swimming Pool from logs
    
    url = f"https://intershifting-nakisha-nonspaciously.ngrok-free.dev/api/available-timeslots?facility_id={facility_id}&date={test_date}&user_email=captain@barangay.gov"
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Success: {data['success']}")
            
            default_slots = data.get('default_timeslots', [])
            print(f"📅 Default time slots: {len(default_slots)}")
            
            # Print full response for debugging
            print(f"🔍 Full response keys: {list(data.keys())}")
            for key in data.keys():
                if key != 'data':  # Skip large data field
                    print(f"  {key}: {data[key]}")
            
            if default_slots:
                print("🕐 Time slots available:")
                for i, slot in enumerate(default_slots[:5]):  # Show first 5
                    print(f"  {i+1}. {slot}")
            else:
                print("❌ No time slots found")
                
        else:
            print(f"❌ Error: {response.text}")
            
    except Exception as e:
        print(f"❌ Exception: {e}")

if __name__ == "__main__":
    test_timeslot_display()
