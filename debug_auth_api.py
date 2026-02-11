#!/usr/bin/env python3
"""
Debug script to see the exact API response structure for verification requests
"""

import requests
import json

def debug_verification_requests():
    base_url = "http://192.168.18.12:8000"
    
    print("Debugging Verification Requests API Response")
    print("=" * 50)
    
    # Try to get verification requests
    try:
        response = requests.get(f"{base_url}/api/verification-requests", timeout=10)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Response structure:")
            print(json.dumps(data, indent=2))
            
            if data.get('success') and data.get('data'):
                requests_data = data['data']
                print(f"\nFound {len(requests_data)} requests")
                
                for i, req in enumerate(requests_data[:2]):  # Show first 2
                    print(f"\n--- Request {i+1} ---")
                    print(f"Fields: {list(req.keys())}")
                    for key, value in req.items():
                        print(f"  {key}: {value} ({type(value).__name__})")
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"Exception: {e}")

if __name__ == "__main__":
    debug_verification_requests()
