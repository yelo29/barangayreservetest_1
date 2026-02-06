import requests
import json

base_url = "https://intershifting-nakisha-nonspaciously.ngrok-free.dev"

def test_facilities():
    """Test facilities endpoint"""
    url = f"{base_url}/api/facilities"
    
    try:
        response = requests.get(url)
        print(f"\n=== Facilities Endpoint Test ===")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text[:200]}...")
        
        if response.status_code == 200:
            result = response.json()
            print(f"Type: {type(result)}")
            if isinstance(result, dict):
                print(f"✅ Proper format: {list(result.keys())}")
                facilities = result.get('data', [])
                print(f"Facilities count: {len(facilities)}")
            else:
                print(f"❌ Wrong format: expecting dict, got {type(result)}")
        else:
            print(f"❌ Error: {response.text}")
    except Exception as e:
        print(f"❌ Error: {e}")

def test_bookings():
    """Test bookings endpoint"""
    url = f"{base_url}/api/bookings"
    
    try:
        response = requests.get(url)
        print(f"\n=== Bookings Endpoint Test ===")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text[:200]}...")
        
        if response.status_code == 200:
            result = response.json()
            print(f"Type: {type(result)}")
            if isinstance(result, dict):
                print(f"✅ Proper format: {list(result.keys())}")
                bookings = result.get('data', [])
                print(f"Bookings count: {len(bookings)}")
            else:
                print(f"❌ Wrong format: expecting dict, got {type(result)}")
        else:
            print(f"❌ Error: {response.text}")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    print("🔍 ENDPOINT FORMAT TESTING")
    print("=" * 40)
    test_facilities()
    test_bookings()
