import requests

def check_current_customer_service():
    """Check current Customer Service state"""
    
    BASE_URL = "http://192.168.18.132:8000"
    
    print("🔍 CURRENT CUSTOMER SERVICE STATE")
    print("=" * 40)
    
    response = requests.get(f"{BASE_URL}/api/officials")
    
    if response.status_code == 200:
        officials = response.json()['data']
        print(f"📋 Customer Service currently shows {len(officials)} officials:\n")
        
        for official in officials:
            name = official.get('full_name', 'Unknown')
            email = official.get('email', 'Unknown')
            contact = official.get('contact_number', 'None')
            status = "✅ HAS CONTACT" if contact and contact != 'None' else "❌ NO CONTACT"
            print(f"  🏢 {name}")
            print(f"     📧 {email}")
            print(f"     📞 {contact}")
            print(f"     {status}\n")
    else:
        print(f"❌ Failed to get Customer Service: {response.status_code}")

if __name__ == "__main__":
    check_current_customer_service()
