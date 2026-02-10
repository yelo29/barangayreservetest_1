import requests

def test_official_profile_update():
    """Test official profile update to see what data is sent"""
    
    BASE_URL = "http://192.168.18.132:8000"
    
    print("🧪 TESTING OFFICIAL PROFILE UPDATE")
    print("=" * 50)
    
    # First login as official
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
        
        # Test profile update with new data
        print("\n📝 Step 2: Update official profile...")
        update_data = {
            "email": "captain@barangay.gov",
            "full_name": "Updated Captain Name",
            "contact_number": "09123456789",
            "address": "Updated Address"
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
            
            # Check customer service to see if data is updated
            print("\n📝 Step 3: Check customer service...")
            customer_response = requests.get(f"{BASE_URL}/api/officials")
            
            if customer_response.status_code == 200:
                data = customer_response.json()
                officials = data['data']
                
                print(f"📋 Customer service shows {len(officials)} officials:")
                for official in officials:
                    name = official.get('full_name', 'Unknown')
                    email = official.get('email', 'Unknown')
                    contact = official.get('contact_number', 'None')
                    print(f"  🏢 {name} ({email}) - Contact: {contact}")
                    
                    # Check if captain shows updated data
                    if 'captain@barangay.gov' in email:
                        if 'Updated Captain Name' in name and '09123456789' in str(contact):
                            print("  ✅ SUCCESS: Captain shows updated data!")
                        else:
                            print("  ❌ ISSUE: Captain still shows old data")
        else:
            print("❌ Failed to get customer service data")
    else:
        print("❌ Failed to login as official")

if __name__ == "__main__":
    test_official_profile_update()
