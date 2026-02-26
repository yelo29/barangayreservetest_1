import requests
import json

# Test verification lock system with local server
BASE_URL = "http://192.168.100.4:8000"

def test_login():
    """Test login functionality"""
    print("🧪 TESTING LOGIN FUNCTIONALITY")
    print("=" * 50)
    
    url = f"{BASE_URL}/api/auth/login"
    headers = {"Content-Type": "application/json"}
    
    # Test different user types
    test_users = [
        {
            "email": "unresident@gmail.com", 
            "password": "password123",
            "type": "Unverified Resident"
        },
        {
            "email": "verifiedresident@gmail.com", 
            "password": "password123", 
            "type": "Verified Resident"
        },
        {
            "email": "nonresident@gmail.com", 
            "password": "password123",
            "type": "Verified Non-Resident"
        }
    ]
    
    for user in test_users:
        print(f"\n🔍 Testing {user['type']}: {user['email']}")
        print("-" * 40)
        
        try:
            response = requests.post(url, headers=headers, json={
                "email": user["email"],
                "password": user["password"]
            })
            
            print(f"Status Code: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                if result.get('success'):
                    user_data = result.get('user', {})
                    print(f"✅ Login Successful")
                    print(f"   Name: {user_data.get('full_name', 'N/A')}")
                    print(f"   Role: {user_data.get('role', 'N/A')}")
                    print(f"   Verified: {user_data.get('verified', 'N/A')}")
                    print(f"   Verification Type: {user_data.get('verification_type', 'N/A')}")
                    print(f"   Discount Rate: {user_data.get('discount_rate', 'N/A')}")
                    
                    # Test verification status
                    test_verification_status(user_data.get('id'))
                else:
                    print(f"❌ Login Failed: {result.get('message', 'Unknown error')}")
            else:
                print(f"❌ HTTP Error: {response.status_code}")
                try:
                    error_data = response.json()
                    print(f"   Error: {error_data.get('message', 'Unknown error')}")
                except:
                    print(f"   Response: {response.text[:200]}...")
                    
        except requests.exceptions.ConnectionError:
            print(f"❌ Connection Error: Cannot connect to server at {BASE_URL}")
            print("   Make sure the server is running!")
        except Exception as e:
            print(f"❌ Error: {e}")

def test_verification_status(user_id):
    """Test verification status endpoint"""
    if not user_id:
        return
        
    print(f"\n🔍 Testing Verification Status for User ID: {user_id}")
    
    try:
        url = f"{BASE_URL}/api/verification-requests/status/{user_id}"
        response = requests.get(url)
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                print(f"✅ Status Check Successful")
                print(f"   Can Submit: {result.get('can_submit', 'N/A')}")
                print(f"   Lock Message: {result.get('lock_message', 'N/A')}")
                print(f"   Current Status: {result.get('current_status', 'N/A')}")
                print(f"   Verified: {result.get('verified', 'N/A')}")
                print(f"   Verification Type: {result.get('verification_type', 'N/A')}")
            else:
                print(f"❌ Status Check Failed: {result.get('message', 'Unknown error')}")
        else:
            print(f"❌ HTTP Error: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error checking verification status: {e}")

def test_server_health():
    """Test if server is running"""
    print("🏥 TESTING SERVER HEALTH")
    print("=" * 50)
    
    try:
        response = requests.get(f"{BASE_URL}/api/facilities", timeout=5)
        if response.status_code == 200:
            print("✅ Server is running and responsive")
            return True
        else:
            print(f"⚠️ Server responded with status: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Server is not running or not accessible")
        return False
    except Exception as e:
        print(f"❌ Error checking server health: {e}")
        return False

if __name__ == "__main__":
    print("🚀 VERIFICATION LOCK SYSTEM - LOGIN TESTS")
    print("=" * 60)
    
    # First check if server is running
    if test_server_health():
        # Run login tests
        test_login()
        
        print("\n" + "=" * 60)
        print("🏁 LOGIN TESTS COMPLETED")
        print("=" * 60)
    else:
        print("\n❌ Please start the server first:")
        print("   python server/server.py")
        print("=" * 60)
