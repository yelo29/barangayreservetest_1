#!/usr/bin/env python3
"""
Test ngrok connection from different network scenarios
"""

import requests
import time

def test_ngrok_connection():
    url = "https://unstanding-unmenaced-pete.ngrok-free.dev/api/me?email=test@example.com"
    
    print("🌐 Testing Ngrok Connection")
    print("=" * 40)
    print(f"📡 URL: {url}")
    print()
    
    # Test with longer timeout for mobile data
    try:
        print("🔄 Testing connection (30s timeout)...")
        start_time = time.time()
        
        response = requests.get(url, timeout=30)
        
        end_time = time.time()
        duration = end_time - start_time
        
        print(f"✅ Status Code: {response.status_code}")
        print(f"⏱️ Response Time: {duration:.2f} seconds")
        print(f"📄 Response: {response.text}")
        
        if response.status_code == 200:
            print("🎉 Ngrok connection working!")
            if duration > 10:
                print("⚠️ Slow response - might cause app timeout")
        else:
            print(f"❌ Error: {response.status_code}")
            
    except requests.exceptions.Timeout:
        print("❌ Request timed out (30s) - ngrok too slow for mobile data")
    except requests.exceptions.ConnectionError:
        print("❌ Connection failed - ngrok might be down")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_ngrok_connection()
