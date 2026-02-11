#!/usr/bin/env python3
"""
Check the status field values in verification requests
"""

import requests
import json

def check_status():
    base_url = "http://192.168.18.12:8000"
    
    try:
        response = requests.get(f"{base_url}/api/verification-requests", timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            
            if data.get('success') and data.get('data'):
                requests_data = data['data']
                print(f"Found {len(requests_data)} requests")
                
                pending = []
                approved = []
                rejected = []
                
                for req in requests_data:
                    status = req.get('status', 'unknown')
                    print(f"Request ID {req.get('id')}: status = '{status}' (type: {type(status).__name__})")
                    
                    if status == 'pending':
                        pending.append(req)
                    elif status == 'approved':
                        approved.append(req)
                    elif status == 'rejected':
                        rejected.append(req)
                
                print(f"\nStatus breakdown:")
                print(f"Pending: {len(pending)}")
                print(f"Approved: {len(approved)}")
                print(f"Rejected: {len(rejected)}")
                
                # Show sample requests
                if pending:
                    print(f"\nSample pending request:")
                    print(json.dumps(pending[0], indent=2, default=str))
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"Exception: {e}")

if __name__ == "__main__":
    check_status()
