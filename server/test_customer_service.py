import requests

def test_customer_service():
    """Test the customer service endpoint"""
    
    BASE_URL = "http://192.168.18.132:8000"
    
    print("🧪 TESTING CUSTOMER SERVICE ENDPOINT")
    print("=" * 50)
    
    try:
        response = requests.get(f"{BASE_URL}/api/officials")
        print(f"📊 Response status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"📊 Success: {data.get('success')}")
            
            if 'data' in data:
                officials = data['data']
                print(f"📋 Total officials returned: {len(officials)}")
                
                for official in officials:
                    name = official.get('full_name', 'Unknown')
                    email = official.get('email', 'Unknown')
                    role = official.get('role', 'Unknown')
                    print(f"  📋 {name} ({email}) - {role}")
                    
                    # Check if Salo E. Lopez appears
                    if 'Salo E. Lopez' in name:
                        print("  ✅ Found Salo E. Lopez in customer service!")
        else:
            print("❌ Failed to get officials data")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_customer_service()
