import requests
import base64

# Test receipt upload with a simple 1x1 pixel PNG
test_receipt = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg=="

# Test booking data with real user
booking_data = {
    "facility_id": "1",
    "user_email": "leo052904@gmail.com",  # Real user ID 14
    "date": "2026-02-10",
    "timeslot": "10:00 AM - 12:00 PM",
    "purpose": "Test receipt upload with fix",
    "receipt_base64": test_receipt,
    "contact_number": "09656692463",
    "address": "Test Address"
}

print("Testing booking creation with receipt using real user...")
print(f"Receipt base64 length: {len(test_receipt)}")
print(f"Receipt starts with data:image: {test_receipt.startswith('data:image')}")

try:
    response = requests.post(
        "https://intershifting-nakisha-nonspaciously.ngrok-free.dev/api/bookings",
        json=booking_data,
        headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer 2c779452-f8ec-47ba-bb7d-81b487c54e45"
        }
    )
    
    print(f"Response status: {response.status_code}")
    print(f"Response body: {response.text}")
    
    if response.status_code == 200:
        print("✅ Booking created successfully! Checking database...")
        
        # Check if receipt was saved
        import sqlite3
        conn = sqlite3.connect('barangay.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, booking_reference, receipt_base64 
            FROM bookings 
            ORDER BY id DESC 
            LIMIT 1
        ''')
        
        result = cursor.fetchone()
        if result:
            booking_id, booking_ref, receipt_base64 = result
            has_receipt = receipt_base64 is not None and receipt_base64 != ''
            print(f"Latest booking:")
            print(f"  ID: {booking_id}")
            print(f"  Reference: {booking_ref}")
            print(f"  Has Receipt: {has_receipt}")
            print(f"  Receipt Length: {len(receipt_base64) if receipt_base64 else 0}")
        
        conn.close()
    
except Exception as e:
    print(f"Error: {e}")
