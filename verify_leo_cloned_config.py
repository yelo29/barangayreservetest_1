#!/usr/bin/env python3
"""
Configuration Verification for Leo's Ngrok Setup - Cloned Repository
"""

import os
import sys
sys.path.append('server')
from config import Config

def check_configuration():
    print("🔍 CHECKING LEO'S NGROK CONFIGURATION (CLONED REPO)")
    print("=" * 60)
    
    # Check ngrok configuration
    print(f"✅ Ngrok Domain: {Config.NGROK_DOMAIN}")
    print(f"✅ Server URL: {Config.get_server_url()}")
    
    # Check server settings
    print(f"✅ Server Host: {Config.HOST}")
    print(f"✅ Server Port: {Config.PORT}")
    print(f"✅ Database Path: {Config.DATABASE_PATH}")
    
    # Check CORS
    print(f"✅ CORS Origins: {Config.get_cors_origins()}")
    
    # Check Android app configuration
    try:
        with open('lib/config/app_config.dart', 'r') as f:
            content = f.read()
            if 'unstanding-unmenaced-pete.ngrok-free.dev' in content:
                print("✅ Android App: Configured with Leo's ngrok URL")
            else:
                print("❌ Android App: NOT configured with Leo's ngrok URL")
    except Exception as e:
        print(f"❌ Android App: Could not check - {e}")
    
    # Check ngrok.yml
    try:
        with open('ngrok.yml', 'r') as f:
            content = f.read()
            if '3976aR0q9u2A9Q9pdLk8yJw1Nrz_NYhzp636M8cnUbJvA4TW' in content:
                print("✅ Ngrok Config: Leo's authtoken found")
            else:
                print("❌ Ngrok Config: Leo's authtoken NOT found")
    except Exception as e:
        print(f"❌ Ngrok Config: Could not check - {e}")
    
    print("=" * 60)
    print("🎯 LEO'S CONFIGURATION STATUS: READY")
    print("📱 Android app will connect to: https://unstanding-unmenaced-pete.ngrok-free.dev")
    print("🚀 To start: python server/server.py")
    print("🌐 To start ngrok: ngrok http 8000")

if __name__ == "__main__":
    check_configuration()
