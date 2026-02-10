import requests

def test_fixed_profile_update():
    """Test the fixed profile update process"""
    
    BASE_URL = "http://192.168.18.132:8000"
    
    print("🧪 TESTING FIXED PROFILE UPDATE")
    print("=" * 50)
    
    # Login as official
    print("📝 Step 1: Login as official...")
    login_response = requests.post(f"{BASE_URL}/api/auth/login", 
        json={
            "email": "captain@barangay.gov",
            "password": "tatalaPunongBarangayadmin"
        }
    )
    
    if login_response.status_code == 200:
        token = login_response.json()['token']
        current_user = login_response.json()['user']
        print("✅ Official login successful")
        print(f"📋 Current name: {current_user.get('full_name', 'Unknown')}")
        print(f"📋 Current contact: {current_user.get('contact_number', 'Unknown')}")
        
        # Test profile update with new data
        print("\n📝 Step 2: Update official profile...")
        update_data = {
            "email": "captain@barangay.gov",
            "full_name": "Fixed Captain Name",
            "contact_number": "09888888888",
            "address": "Fixed Test Address"
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
            
            # Test login again to verify persistence
            print("\n📝 Step 3: Login again to verify persistence...")
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
                
                if (user_data.get('full_name') == 'Fixed Captain Name' and 
                    user_data.get('contact_number') == '09888888888'):
                    print("✅ SUCCESS: Profile update persisted correctly!")
                    print("🎉 The official profile update issue has been FIXED!")
                else:
                    print("❌ ISSUE: Profile update not persisted")
            else:
                print("❌ Failed to login again")
        else:
            print("❌ Profile update failed")
    else:
        print("❌ Failed to login as official")

if __name__ == "__main__":
    test_fixed_profile_update()
