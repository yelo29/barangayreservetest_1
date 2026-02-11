#!/usr/bin/env python3
"""
Image Upload Test for Booking Form
Tests the red screen issue when picking images
"""

import requests
import json
import base64

class ImageUploadTester:
    def __init__(self):
        self.base_url = "http://192.168.18.12:8000"
        
    def test_image_processing(self):
        """Test image processing that might cause red screen"""
        
        print("Testing Image Upload Processing")
        print("=" * 40)
        
        # Test 1: Valid base64 image
        try:
            # Small 1x1 pixel PNG in base64
            valid_base64 = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg=="
            
            # Test if it can be decoded
            decoded = base64.b64decode(valid_base64)
            print(f"[PASS] Valid base64 image: {len(decoded)} bytes decoded")
        except Exception as e:
            print(f"[FAIL] Valid base64 image: {str(e)}")
        
        # Test 2: Invalid base64 (might cause red screen)
        try:
            invalid_base64 = "invalid_base64_string"
            decoded = base64.b64decode(invalid_base64)
            print(f"[WARN] Invalid base64: Should have failed but didn't")
        except Exception as e:
            print(f"[PASS] Invalid base64: Correctly failed with {str(e)}")
        
        # Test 3: Data URL parsing (common issue)
        try:
            data_url = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg=="
            
            if data_url.startswith('data:'):
                # Extract base64 part
                base64_part = data_url.split(',')[1]
                decoded = base64.b64decode(base64_part)
                print(f"[PASS] Data URL parsing: {len(decoded)} bytes decoded")
            else:
                print("[FAIL] Data URL parsing: Not a data URL")
        except Exception as e:
            print(f"[FAIL] Data URL parsing: {str(e)}")
        
        # Test 4: Large image base64 (might cause memory issues)
        try:
            # Create a larger base64 string (simulating a real image)
            large_base64 = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg==" * 100  # Repeat to make it larger
            
            decoded = base64.b64decode(large_base64)
            print(f"[PASS] Large base64: {len(decoded)} bytes decoded")
        except Exception as e:
            print(f"[FAIL] Large base64: {str(e)}")
        
        # Test 5: Booking submission with image
        try:
            booking_data = {
                "facility_id": 1,
                "date": "2026-02-12",
                "start_time": "09:00",
                "end_time": "11:00",
                "purpose": "Test booking with image",
                "receipt_base64": "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg==",
                "payment_method": "cash",
                "total_amount": 300,
                "downpayment_amount": 150
            }
            
            response = requests.post(
                f"{self.base_url}/api/bookings",
                json=booking_data,
                timeout=10
            )
            
            print(f"[PASS] Booking with image: Endpoint responded ({response.status_code})")
        except Exception as e:
            print(f"[FAIL] Booking with image: {str(e)}")
        
        print("\nImage Upload Testing Complete!")
        print("If all tests pass, the issue might be in Flutter image handling")

if __name__ == "__main__":
    tester = ImageUploadTester()
    tester.test_image_processing()
