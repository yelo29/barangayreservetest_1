import requests
import json

# Test the profile endpoint that should work
base_url = "https://intershifting-nakisha-nonspaciously.ngrok-free.dev"

# Test with different emails
emails_to_test = [
    "leo052904@gmail.com",
    "saloestillopez@gmail.com", 
    "official@barangay.com",
    "secretary@barangay.gov"
]

for email in emails_to_test:
    print(f"Testing /api/users/profile/{email}")
    try:
        response = requests.get(f"{base_url}/api/users/profile/{email}")
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Success: {json.dumps(data, indent=2)}")
        else:
            print(f"❌ Error: {response.text}")
    except Exception as e:
        print(f"❌ Exception: {e}")
    
    print("-" * 50)
