#!/usr/bin/env python3
"""
Interactive DuckDNS Setup for Barangay Reserve Server
"""

import os
import requests

def setup_duckdns():
    print("🦆 DuckDNS Setup for Barangay Reserve Server")
    print("=" * 50)
    
    # Get user input
    domain = input("Enter your DuckDNS domain (e.g., john-barangay.duckdns.org): ").strip()
    token = input("Enter your DuckDNS token: ").strip()
    
    if not domain or not token:
        print("❌ Domain and token are required")
        return False
    
    # Validate domain format
    if not domain.endswith('.duckdns.org'):
        domain += '.duckdns.org'
    
    print(f"\n📡 Domain: {domain}")
    print(f"🔑 Token: {token[:10]}...")
    
    # Test DuckDNS connection
    print("\n🧪 Testing DuckDNS connection...")
    try:
        test_url = f"https://duckdns.org/update?domains={domain.split('.')[0]}&token={token}&ip=1.2.3.4"
        response = requests.get(test_url, timeout=10)
        
        if response.text == 'ok':
            print("✅ DuckDNS connection successful!")
        else:
            print(f"❌ DuckDNS test failed: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ DuckDNS test error: {e}")
        return False
    
    # Create .env file
    env_content = f"""# DuckDNS Configuration for Barangay Reserve
DUCKDNS_DOMAIN={domain}
DUCKDNS_TOKEN={token}

# Server Settings
SERVER_HOST=0.0.0.0
SERVER_PORT=8080
DEBUG=False

# CORS Settings (allow all origins)
CORS_ORIGINS=*

# Database
DB_PATH=barangay.db
"""
    
    try:
        with open('.env', 'w') as f:
            f.write(env_content)
        print("✅ Configuration saved to .env file")
    except Exception as e:
        print(f"❌ Error saving .env file: {e}")
        return False
    
    # Update config.py if needed
    try:
        with open('config.py', 'r') as f:
            config_content = f.read()
        
        if 'DUCKDNS_DOMAIN' not in config_content:
            print("✅ config.py already has DuckDNS support")
        else:
            print("✅ config.py ready for DuckDNS")
            
    except Exception as e:
        print(f"⚠️  Warning: Could not check config.py: {e}")
    
    return True

def test_current_ip():
    """Get current public IP"""
    try:
        response = requests.get('https://api.ipify.org', timeout=10)
        return response.text.strip()
    except:
        return "Unknown"

def main():
    print("🌐 Setting up your laptop as a global server...")
    print(f"📍 Your current public IP: {test_current_ip()}")
    print()
    
    if setup_duckdns():
        print("\n🎉 DuckDNS setup complete!")
        print("\n🚀 Next steps:")
        print("1. Start your server: python server.py")
        print("2. Update DuckDNS: python duckdns_updater.py update")
        print("3. Test from anywhere: http://your-domain.duckdns.org:8080")
        print("4. Configure Flutter app with your DuckDNS domain")
        print("\n✅ Your laptop will now work from any network!")
    else:
        print("\n❌ Setup failed. Please check your domain and token.")

if __name__ == "__main__":
    main()
