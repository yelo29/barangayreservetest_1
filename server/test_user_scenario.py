import requests

def test_user_scenario():
    """Test the exact user scenario: Official updates -> Resident sees in Customer Service"""
    
    BASE_URL = "http://192.168.18.132:8000"
    
    print("🎯 TESTING EXACT USER SCENARIO")
    print("=" * 50)
    print("Scenario: Official updates profile -> Resident checks Customer Service")
    print()
    
    # Step 1: Official logs in and updates profile
    print("📝 STEP 1: Official updates profile...")
    print("  🏢 Logging in as captain@barangay.gov...")
    
    login_response = requests.post(f"{BASE_URL}/api/auth/login", 
        json={
            "email": "captain@barangay.gov",
            "password": "tatalaPunongBarangayadmin"
        }
    )
    
    if login_response.status_code == 200:
        token = login_response.json()['token']
        current_data = login_response.json()['user']
        
        print(f"  📋 Current profile: {current_data.get('full_name', 'Unknown')}")
        print(f"  📞 Current contact: {current_data.get('contact_number', 'Unknown')}")
        
        # Official updates profile with new information
        update_data = {
            "email": "captain@barangay.gov",
            "full_name": "Juan Dela Cruz",
            "contact_number": "09555-123-456",
            "address": "123 Barangay Hall, Manila"
        }
        
        print(f"  🔧 Updating profile to: {update_data['full_name']}")
        print(f"  📞 Updating contact to: {update_data['contact_number']}")
        
        update_response = requests.put(f"{BASE_URL}/api/users/profile",
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            },
            json=update_data
        )
        
        if update_response.status_code == 200:
            print("  ✅ Profile updated successfully!")
            
            # Step 2: Resident logs in and checks Customer Service
            print("\n📝 STEP 2: Resident checks Customer Service...")
            print("  👤 Logging in as resident...")
            
            # Login as resident (any resident account)
            resident_login = requests.post(f"{BASE_URL}/api/auth/login",
                json={
                    "email": "leo052904@gmail.com",
                    "password": "leo3029"
                }
            )
            
            if resident_login.status_code == 200:
                print("  ✅ Resident login successful!")
                
                # Check Customer Service (what resident sees in Account Settings)
                print("  🏢 Checking Customer Service container...")
                customer_response = requests.get(f"{BASE_URL}/api/officials")
                
                if customer_response.status_code == 200:
                    officials = customer_response.json()['data']
                    
                    print(f"  📋 Customer Service shows {len(officials)} officials:")
                    
                    captain_data = None
                    for official in officials:
                        name = official.get('full_name', 'Unknown')
                        email = official.get('email', 'Unknown')
                        contact = official.get('contact_number', 'Unknown')
                        
                        if 'captain@barangay.gov' in email:
                            captain_data = official
                            print(f"    🎯 CAPTAIN FOUND:")
                            print(f"      👨‍💼 Name: {name}")
                            print(f"      📞 Contact: {contact}")
                            print(f"      📧 Email: {email}")
                        else:
                            print(f"    🏢 {name} - Contact: {contact}")
                    
                    if captain_data:
                        expected_name = "Juan Dela Cruz"
                        expected_contact = "09555-123-456"
                        
                        actual_name = captain_data.get('full_name', '')
                        actual_contact = captain_data.get('contact_number', '')
                        
                        print(f"\n  🔍 VERIFICATION:")
                        print(f"    Expected Name: {expected_name}")
                        print(f"    Actual Name: {actual_name}")
                        print(f"    Expected Contact: {expected_contact}")
                        print(f"    Actual Contact: {actual_contact}")
                        
                        if actual_name == expected_name and actual_contact == expected_contact:
                            print("  ✅ SUCCESS: Resident sees updated official data!")
                            print("  🎉 Customer Service container shows correct information!")
                            print("\n  📋 SUMMARY:")
                            print("    ✅ Official can update profile")
                            print("    ✅ Updates persist to database")
                            print("    ✅ Customer Service reflects changes")
                            print("    ✅ Residents see updated information")
                        else:
                            print("  ❌ ISSUE: Resident doesn't see updated data")
                    else:
                        print("  ❌ ISSUE: Captain not found in Customer Service")
                else:
                    print("  ❌ Failed to get Customer Service data")
            else:
                print("  ❌ Failed to login as resident")
        else:
            print("  ❌ Failed to update official profile")
    else:
        print("  ❌ Failed to login as official")

if __name__ == "__main__":
    test_user_scenario()
