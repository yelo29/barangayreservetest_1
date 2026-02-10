import requests

def test_resident_customer_service_update():
    """Test that resident sees updated official profile in Customer Service"""
    
    BASE_URL = "http://192.168.18.132:8000"
    
    print("🧪 TESTING RESIDENT CUSTOMER SERVICE UPDATE VISIBILITY")
    print("=" * 60)
    
    # Step 1: Login as official and update profile
    print("📝 Step 1: Official login and profile update...")
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
        
        # Update profile with new data
        new_data = {
            "email": "captain@barangay.gov",
            "full_name": "Resident Visible Captain",
            "contact_number": "09777777777",
            "address": "Resident Visible Address"
        }
        
        print(f"🔍 Updating profile: {new_data['full_name']} -> {new_data['contact_number']}")
        
        update_response = requests.put(f"{BASE_URL}/api/users/profile",
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            },
            json=new_data
        )
        
        if update_response.status_code == 200:
            print("✅ Official profile updated successfully")
            
            # Step 2: Check customer service as resident would see it
            print("\n📝 Step 2: Check Customer Service (Resident View)...")
            customer_response = requests.get(f"{BASE_URL}/api/officials")
            
            if customer_response.status_code == 200:
                officials = customer_response.json()['data']
                print(f"📋 Customer Service shows {len(officials)} officials:")
                
                captain_found = False
                for official in officials:
                    name = official.get('full_name', 'Unknown')
                    email = official.get('email', 'Unknown')
                    contact = official.get('contact_number', 'Unknown')
                    print(f"  🏢 {name} ({email}) - Contact: {contact}")
                    
                    if 'captain@barangay.gov' in email:
                        captain_found = True
                        print(f"\n🎯 CAPTAIN FOUND IN CUSTOMER SERVICE:")
                        print(f"  👨‍💼 Name: {name}")
                        print(f"  📞 Contact: {contact}")
                        
                        if name == 'Resident Visible Captain' and contact == '09777777777':
                            print("✅ SUCCESS: Resident sees updated official data!")
                            print("🎉 Customer Service container shows correct updated information!")
                        else:
                            print("❌ ISSUE: Resident sees old official data")
                            print(f"   Expected: Resident Visible Captain, 09777777777")
                            print(f"   Actual: {name}, {contact}")
                        break
                
                if not captain_found:
                    print("❌ ISSUE: Captain not found in Customer Service")
            else:
                print("❌ Failed to get Customer Service data")
        else:
            print("❌ Failed to update official profile")
    else:
        print("❌ Failed to login as official")

if __name__ == "__main__":
    test_resident_customer_service_update()
