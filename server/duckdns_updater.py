#!/usr/bin/env python3
"""
DuckDNS Updater for Barangay Reserve Server
Automatically updates DuckDNS domain with your current IP address
"""

import requests
import time
import os
from config import Config

class DuckDNSUpdater:
    def __init__(self, domain=None, token=None):
        # Load from environment file first
        self._load_env()
        
        self.domain = domain or os.getenv('DUCKDNS_DOMAIN') or Config.DUCKDNS_DOMAIN
        self.token = token or os.getenv('DUCKDNS_TOKEN') or Config.DUCKDNS_TOKEN
        self.base_url = "https://duckdns.org/update"
        
    def _load_env(self):
        """Load environment variables from .env file"""
        try:
            if os.path.exists('.env'):
                with open('.env', 'r') as f:
                    for line in f:
                        if line.strip() and '=' in line:
                            key, value = line.strip().split('=', 1)
                            os.environ[key] = value
        except Exception as e:
            print(f"⚠️  Could not load .env file: {e}")
        
    def get_current_ip(self):
        """Get current public IP address"""
        try:
            response = requests.get('https://api.ipify.org', timeout=10)
            return response.text.strip()
        except Exception as e:
            print(f"❌ Error getting IP: {e}")
            return None
    
    def update_duckdns(self, ip=None):
        """Update DuckDNS with current or specified IP"""
        if not self.domain or not self.token:
            print("❌ DuckDNS domain or token not configured")
            return False
            
        if ip is None:
            ip = self.get_current_ip()
            if not ip:
                return False
        
        try:
            url = f"{self.base_url}?domains={self.domain}&token={self.token}&ip={ip}"
            response = requests.get(url, timeout=10)
            
            if response.text == 'ok':
                print(f"✅ DuckDNS updated successfully: {self.domain} -> {ip}")
                return True
            else:
                print(f"❌ DuckDNS update failed: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Error updating DuckDNS: {e}")
            return False
    
    def start_auto_update(self, interval=300):  # 5 minutes
        """Start automatic DuckDNS updates"""
        print(f"🔄 Starting DuckDNS auto-update every {interval} seconds")
        print(f"📡 Domain: {self.domain}")
        
        # Initial update
        self.update_duckdns()
        
        while True:
            time.sleep(interval)
            self.update_duckdns()

def setup_duckdns():
    """Interactive DuckDNS setup"""
    print("🦆 DuckDNS Setup for Barangay Reserve Server")
    print("=" * 50)
    
    domain = input("Enter your DuckDNS domain (e.g., mybarangay.duckdns.org): ").strip()
    token = input("Enter your DuckDNS token: ").strip()
    
    if not domain or not token:
        print("❌ Domain and token are required")
        return None
    
    # Save to environment file
    env_content = f"""
# DuckDNS Configuration
DUCKDNS_DOMAIN={domain}
DUCKDNS_TOKEN={token}
"""
    
    with open('.env', 'a') as f:
        f.write(env_content)
    
    print(f"✅ DuckDNS configuration saved to .env file")
    print(f"📡 Domain: {domain}")
    
    return DuckDNSUpdater(domain, token)

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "setup":
            updater = setup_duckdns()
            if updater:
                updater.update_duckdns()
                
        elif command == "update":
            updater = DuckDNSUpdater()
            updater.update_duckdns()
            
        elif command == "auto":
            updater = DuckDNSUpdater()
            updater.start_auto_update()
            
        else:
            print("Usage:")
            print("  python duckdns_updater.py setup    - Interactive setup")
            print("  python duckdns_updater.py update    - Update once")
            print("  python duckdns_updater.py auto     - Auto-update mode")
    else:
        updater = DuckDNSUpdater()
        if updater.domain and updater.token:
            updater.update_duckdns()
        else:
            print("❌ DuckDNS not configured. Run 'python duckdns_updater.py setup' first")
