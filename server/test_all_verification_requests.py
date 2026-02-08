import requests
import json

def test_verification_api():
    try:
        url = "http://192.168.100.4:8000/api/verification-requests"
        
        # Test without authentication first
        print("Testing without authentication:")
        response = requests.get(url)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                requests_data = data.get('data', [])
                print(f"Total requests: {len(requests_data)}")
                
                # Count by status
                pending = [r for r in requests_data if r.get('status') == 'pending']
                approved = [r for r in requests_data if r.get('status') == 'approved']
                rejected = [r for r in requests_data if r.get('status') == 'rejected']
                
                print(f"Pending: {len(pending)}")
                print(f"Approved: {len(approved)}")
                print(f"Rejected: {len(rejected)}")
                
                print("\nAll requests:")
                for req in requests_data:
                    print(f"  ID: {req.get('id')}, Name: {req.get('fullName')}, Status: {req.get('status')}")
                
            else:
                print(f"API Error: {data}")
        else:
            print(f"HTTP Error: {response.text}")
            
        # Test with authentication
        print("\n" + "="*50)
        print("Testing with authentication:")
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer c44fcde2-94d4-40ef-aba5-48e590f1db5c"
        }
        
        response = requests.get(url, headers=headers)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                requests_data = data.get('data', [])
                print(f"Total requests: {len(requests_data)}")
            else:
                print(f"API Error: {data}")
        else:
            print(f"HTTP Error: {response.text}")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_verification_api()
