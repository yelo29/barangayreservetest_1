#!/usr/bin/env python3
import requests

print("Testing server connection...")
try:
    response = requests.get("http://192.168.100.4:8080/api/me?email=leo052904@gmail.com", timeout=5)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"Error: {e}")
