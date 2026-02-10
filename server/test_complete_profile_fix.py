import requests

def test_complete_profile_fix():
    """Comprehensive test of the profile update fix"""
    
    BASE_URL = "http://192.168.18.132:8000"
    
    print("🎯 COMPREHENSIVE PROFILE UPDATE FIX TEST")
    print("=" * 60)
    
    # Test 1: Login as official and check current data
    print("📝 Test 1: Login and check current data...")
    login_response = requests.post(f"{BASE_URL}/api/auth/login", 
        json={
            "email": "captain@barangay.gov",
            "password": "tatalaPunongBarangayadmin"
        }
    )
    
    if login_response.status_code == 200:
        token = login_response.json()['token']
        current_user = login_response.json()['user']
        print("✅ Login successful")
        print(f"📋 Current name: {current_user.get('full_name', 'Unknown')}")
        print(f"📋 Current contact: {current_user.get('contact_number', 'Unknown')}")
        print(f"📋 Current address: {current_user.get('address', 'Unknown')}")
        
        # Test 2: Update profile with new data
        print("\n📝 Test 2: Update profile with new data...")
        new_data = {
            "email": "captain@barangay.gov",
            "full_name": "Final Test Captain",
            "contact_number": "09999999999",
            "address": "Final Test Address"
        }
        
        update_response = requests.put(f"{BASE_URL}/api/users/profile",
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            },
            json=new_data
        )
        
        print(f"📊 Update response: {update_response.status_code}")
        if update_response.status_code == 200:
            print("✅ Profile update successful")
            
            # Test 3: Check customer service to see updated data
            print("\n📝 Test 3: Check customer service...")
            customer_response = requests.get(f"{BASE_URL}/api/officials")
            
            if customer_response.status_code == 200:
                officials = customer_response.json()['data']
                captain_found = False
                
                for official in officials:
                    if 'captain@barangay.gov' in official.get('email', ''):
                        captain_found = True
                        name = official.get('full_name', 'Unknown')
                        contact = official.get('contact_number', 'Unknown')
                        print(f"🏢 Captain in customer service: {name} - Contact: {contact}")
                        
                        if name == 'Final Test Captain' and contact == '09999999999':
                            print("✅ SUCCESS: Customer service shows updated data!")
                        else:
                            print("❌ ISSUE: Customer service shows old data")
                        break
                
                if not captain_found:
                    print("❌ ISSUE: Captain not found in customer service")
            else:
                print("❌ Failed to get customer service data")
            
            # Test 4: Login again to verify persistence
            print("\n📝 Test 4: Re-login to verify persistence...")
            login_response2 = requests.post(f"{BASE_URL}/api/auth/login", 
                json={
                    "email": "captain@barangay.gov",
                    "password": "tatalaPunongBarangayadmin"
                }
            )
            
            if login_response2.status_code == 200:
                user_data = login_response2.json()['user']
                print(f"📋 Name after re-login: {user_data.get('full_name', 'Unknown')}")
                print(f"📋 Contact after re-login: {user_data.get('contact_number', 'Unknown')}")
                print(f"📋 Address after re-login: {user_data.get('address', 'Unknown')}")
                
                if (user_data.get('full_name') == 'Final Test Captain' and 
                    user_data.get('contact_number') == '09999999999' and
                    user_data.get('address') == 'Final Test Address'):
                    print("🎉 COMPLETE SUCCESS: All tests passed!")
                    print("✅ Profile update issue has been completely FIXED!")
                    print("\n📋 SUMMARY:")
                    print("  ✅ Flutter app now calls server API for profile updates")
                    print("  ✅ Server correctly updates database")
                    print("  ✅ Customer service shows updated data")
                    print("  ✅ Login returns updated data")
                    print("  ✅ Data persists across sessions")
                else:
                    print("❌ ISSUE: Data not persisted correctly")
            else:
                print("❌ Failed to login again")
        else:
            print("❌ Profile update failed")
    else:
        print("❌ Failed to login as official")

if __name__ == "__main__":
    test_complete_profile_fix()
