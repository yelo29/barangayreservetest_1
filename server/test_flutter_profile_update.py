import requests
import json

def test_flutter_profile_update():
    """Test profile update exactly as Flutter should do it"""
    
    BASE_URL = "http://192.168.18.132:8000"
    
    print("🧪 TESTING FLUTTER PROFILE UPDATE")
    print("=" * 50)
    
    # Login as official first
    print("📝 Step 1: Login as official...")
    login_response = requests.post(f"{BASE_URL}/api/auth/login", 
        json={
            "email": "captain@barangay.gov",
            "password": "tatalaPunongBarangayadmin"
        }
    )
    
    if login_response.status_code == 200:
        token = login_response.json()['token']
        print("✅ Official login successful")
        
        # Test profile update with different data
        print("\n📝 Step 2: Update official profile...")
        update_data = {
            "email": "captain@barangay.gov",
            "full_name": "Flutter Test Name",
            "contact_number": "09999999999",
            "address": "Flutter Test Address"
        }
        
        print(f"🔍 Sending update data: {update_data}")
        
        update_response = requests.put(f"{BASE_URL}/api/users/profile",
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            },
            json=update_data
        )
        
        print(f"📊 Update response status: {update_response.status_code}")
        print(f"📊 Update response body: {update_response.text}")
        
        if update_response.status_code == 200:
            print("✅ Profile update successful")
            
            # Test login again to see if data persists
            print("\n📝 Step 3: Login again to check persistence...")
            login_response2 = requests.post(f"{BASE_URL}/api/auth/login", 
                json={
                    "email": "captain@barangay.gov",
                    "password": "tatalaPunongBarangayadmin"
                }
            )
            
            if login_response2.status_code == 200:
                user_data = login_response2.json()['user']
                print(f"📋 User data after re-login:")
                print(f"  👨‍💼 Name: {user_data.get('full_name', 'Unknown')}")
                print(f"  📞 Contact: {user_data.get('contact_number', 'Unknown')}")
                print(f"  🏠 Address: {user_data.get('address', 'Unknown')}")
                
                if (user_data.get('full_name') == 'Flutter Test Name' and 
                    user_data.get('contact_number') == '09999999999'):
                    print("✅ SUCCESS: Profile update persisted correctly!")
                else:
                    print("❌ ISSUE: Profile update not persisted")
            else:
                print("❌ Failed to login again")
        else:
            print("❌ Profile update failed")
    else:
        print("❌ Failed to login as official")

if __name__ == "__main__":
    test_flutter_profile_update()
