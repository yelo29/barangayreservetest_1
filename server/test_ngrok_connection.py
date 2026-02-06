#!/usr/bin/env python3
"""
Test the exact same request the app is making
"""

import requests

def test_ngrok_endpoint():
    # Test the exact endpoint the app is testing
    url = "https://unstanding-unmenaced-pete.ngrok-free.dev/api/me?email=test@example.com"
    
    print("🔍 Testing Ngrok Endpoint")
    print("=" * 40)
    print(f"📡 URL: {url}")
    print()
    
    try:
        print("🔄 Sending request...")
        response = requests.get(url, timeout=10)
        print(f"✅ Status Code: {response.status_code}")
        print(f"📄 Response: {response.text}")
        
        if response.status_code == 200:
            print("🎉 Ngrok endpoint working!")
        else:
            print(f"❌ Error: {response.status_code}")
            
    except requests.exceptions.Timeout:
        print("❌ Request timed out")
    except requests.exceptions.ConnectionError:
        print("❌ Connection failed - is ngrok running?")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_ngrok_endpoint()
