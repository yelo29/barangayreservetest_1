import requests
import json

# Test login functionality only
BASE_URL = "http://192.168.100.4:8000"

def test_login_only():
    """Test login functionality without verification status"""
    print("🧪 TESTING LOGIN ONLY")
    print("=" * 50)
    
    url = f"{BASE_URL}/api/auth/login"
    headers = {"Content-Type": "application/json"}
    
    # Test with sample user
    test_user = {
        "email": "resident@barangay.com", 
        "password": "password123"
    }
    
    print(f"🔍 Testing login with: {test_user['email']}")
    print("-" * 40)
    
    try:
        response = requests.post(url, headers=headers, json=test_user)
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text[:500]}...")
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                user_data = result.get('user', {})
                print(f"✅ Login Successful")
                print(f"   Name: {user_data.get('full_name', 'N/A')}")
                print(f"   Role: {user_data.get('role', 'N/A')}")
                print(f"   Verified: {user_data.get('verified', 'N/A')}")
                print(f"   User ID: {user_data.get('id', 'N/A')}")
                return True
            else:
                print(f"❌ Login Failed: {result.get('message', 'Unknown error')}")
                return False
        else:
            print(f"❌ HTTP Error: {response.status_code}")
            return False
                
    except requests.exceptions.ConnectionError:
        print(f"❌ Connection Error: Cannot connect to server at {BASE_URL}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    print("🚀 LOGIN ONLY TEST")
    print("=" * 60)
    
    success = test_login_only()
    
    print("\n" + "=" * 60)
    if success:
        print("🏁 LOGIN TEST COMPLETED SUCCESSFULLY")
    else:
        print("❌ LOGIN TEST FAILED")
    print("=" * 60)
