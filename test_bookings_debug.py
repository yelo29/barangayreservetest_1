import requests
import json

# Test bookings endpoint for official
url = "https://intershifting-nakisha-nonspaciously.ngrok-free.dev/api/bookings"
headers = {
    "Content-Type": "application/json",
    "X-User-ID": "11",
    "X-User-Email": "secretary@barangay.gov"
}

try:
    response = requests.get(url, headers=headers)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"Type: {type(data)}")
        print(f"Length: {len(data) if isinstance(data, list) else 'Not a list'}")
        
except Exception as e:
    print(f"Error: {e}")

print("\n" + "="*50)

# Test bookings endpoint for resident
url2 = "https://intershifting-nakisha-nonspaciously.ngrok-free.dev/api/bookings?user_email=leo052904@gmail.com&user_role=resident"
headers2 = {
    "Content-Type": "application/json",
    "X-User-ID": "5",
    "X-User-Email": "leo052904@gmail.com"
}

try:
    response2 = requests.get(url2, headers=headers2)
    print(f"Status Code: {response2.status_code}")
    print(f"Response: {response2.text}")
    
    if response2.status_code == 200:
        data2 = response2.json()
        print(f"Type: {type(data2)}")
        print(f"Length: {len(data2) if isinstance(data2, list) else 'Not a list'}")
        
except Exception as e:
    print(f"Error: {e}")
