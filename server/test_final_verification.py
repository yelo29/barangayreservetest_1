import requests
from datetime import datetime

def test_final_verification():
    """Final verification that official profile updates work for residents"""
    
    BASE_URL = "http://192.168.18.132:8000"
    
    print("🎯 FINAL VERIFICATION TEST")
    print("=" * 50)
    print("Testing: Official updates profile → Resident sees in Customer Service")
    print()
    
    # Test the current state first
    print("📋 Step 1: Check current Customer Service state...")
    response = requests.get(f"{BASE_URL}/api/officials")
    
    if response.status_code == 200:
        officials = response.json()['data']
        captain = None
        for official in officials:
            if 'captain@barangay.gov' in official.get('email', ''):
                captain = official
                break
        
        if captain:
            current_name = captain.get('full_name', 'Unknown')
            current_contact = captain.get('contact_number', 'Unknown')
            print(f"  Current Captain: {current_name} - Contact: {current_contact}")
        
        # Step 2: Update with new data
        print("\n📝 Step 2: Official updates profile...")
        new_name = f"Updated Captain {int(datetime.now().timestamp())}"
        new_contact = f"09{int(datetime.now().timestamp()) % 100000:05d}"
        
        # Login as official
        login_response = requests.post(f"{BASE_URL}/api/auth/login",
            json={
                "email": "captain@barangay.gov",
                "password": "tatalaPunongBarangayadmin"
            }
        )
        
        if login_response.status_code == 200:
            token = login_response.json()['token']
            
            # Update profile
            update_data = {
                "email": "captain@barangay.gov",
                "full_name": new_name,
                "contact_number": new_contact,
            }
            
            update_response = requests.put(f"{BASE_URL}/api/users/profile",
                headers={
                    "Authorization": f"Bearer {token}",
                    "Content-Type": "application/json"
                },
                json=update_data
            )
            
            if update_response.status_code == 200:
                print(f"  ✅ Profile updated: {new_name}")
                print(f"  ✅ Contact updated: {new_contact}")
                
                # Step 3: Check Customer Service again
                print("\n📝 Step 3: Resident checks updated Customer Service...")
                customer_response = requests.get(f"{BASE_URL}/api/officials")
                
                if customer_response.status_code == 200:
                    updated_officials = customer_response.json()['data']
                    updated_captain = None
                    
                    for official in updated_officials:
                        if 'captain@barangay.gov' in official.get('email', ''):
                            updated_captain = official
                            break
                    
                    if updated_captain:
                        updated_name = updated_captain.get('full_name', 'Unknown')
                        updated_contact = updated_captain.get('contact_number', 'Unknown')
                        
                        print(f"  🏢 Updated Captain: {updated_name}")
                        print(f"  📞 Updated Contact: {updated_contact}")
                        
                        # Verification
                        if (updated_name == new_name and updated_contact == new_contact):
                            print("\n🎉 SUCCESS: RESIDENT SEES UPDATED OFFICIAL DATA!")
                            print("✅ Official profile updates work correctly!")
                            print("✅ Customer Service shows updated information!")
                            print("✅ The issue has been completely RESOLVED!")
                        else:
                            print("\n❌ ISSUE: Data not updated in Customer Service")
                    else:
                        print("❌ Failed to get updated Customer Service")
                else:
                    print("❌ Profile update failed")
            else:
                print("❌ Failed to login as official")
        else:
            print("❌ Failed to get current Customer Service state")
    else:
        print("❌ Failed to connect to server")

if __name__ == "__main__":
    test_final_verification()
