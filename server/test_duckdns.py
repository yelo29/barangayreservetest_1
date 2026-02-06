#!/usr/bin/env python3
import requests
import json

def test_duckdns():
    duckdns_url = "http://barangay-reserve.duckdns.org:8080/api/login"
    local_url = "http://192.168.100.4:8080/api/login"
    
    data = {
        "email": "leo052904@gmail.com",
        "password": "zepol052904"
    }
    
    print("🦆 Testing DuckDNS vs Local Connection")
    print("=" * 50)
    
    # Test 1: Local URL
    print("\n1. Testing Local URL:")
    print(f"   📡 {local_url}")
    try:
        response = requests.post(local_url, json=data, timeout=10)
        print(f"   ✅ Status: {response.status_code}")
        if response.status_code == 200:
            print("   🎉 Local connection works!")
        else:
            print(f"   ❌ Error: {response.text}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 2: DuckDNS URL
    print("\n2. Testing DuckDNS URL:")
    print(f"   📡 {duckdns_url}")
    try:
        response = requests.post(duckdns_url, json=data, timeout=10)
        print(f"   ✅ Status: {response.status_code}")
        if response.status_code == 200:
            print("   🎉 DuckDNS connection works!")
        else:
            print(f"   ❌ Error: {response.text}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 3: Check if DuckDNS resolves
    print("\n3. Testing DuckDNS Resolution:")
    try:
        import socket
        ip = socket.gethostbyname('barangay-reserve.duckdns.org')
        print(f"   ✅ DuckDNS resolves to: {ip}")
        print(f"   📍 Your local IP: 192.168.100.4")
        if ip == "192.168.100.4":
            print("   🎯 DuckDNS points to your local IP!")
        else:
            print(f"   ⚠️  DuckDNS points to different IP: {ip}")
    except Exception as e:
        print(f"   ❌ DuckDNS resolution failed: {e}")

if __name__ == "__main__":
    test_duckdns()
