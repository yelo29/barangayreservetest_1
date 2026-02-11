#!/usr/bin/env python3
"""
Comprehensive Test Suite for Barangay Reserve Application
Tests all authentication fixes and core functionality
"""

import requests
import json
import time
from datetime import datetime, timedelta

class BarangayReserveTester:
    def __init__(self):
        self.base_url = "http://192.168.18.12:8000"
        self.session = requests.Session()
        self.test_results = []
        
    def log_test(self, test_name, success, message=""):
        """Log test results"""
        status = "✅ PASS" if success else "❌ FAIL"
        result = f"{status} - {test_name}"
        if message:
            result += f": {message}"
        print(result)
        self.test_results.append({
            'test': test_name,
            'success': success,
            'message': message,
            'timestamp': datetime.now().isoformat()
        })
        
    def test_server_connection(self):
        """Test basic server connectivity"""
        try:
            response = requests.get(f"{self.base_url}/health", timeout=5)
            self.log_test(
                "Server Connection", 
                response.status_code == 200,
                f"Status: {response.status_code}"
            )
            return response.status_code == 200
        except Exception as e:
            self.log_test("Server Connection", False, str(e))
            return False
    
    def test_resident_registration(self):
        """Test resident user registration"""
        try:
            test_user = {
                "name": "Test Resident",
                "email": "testresident@example.com",
                "password": "test123456",
                "role": "resident"
            }
            
            response = requests.post(
                f"{self.base_url}/api/auth/register",
                json=test_user,
                timeout=10
            )
            
            success = response.status_code == 200
            data = response.json() if success else {}
            
            self.log_test(
                "Resident Registration",
                success and data.get('success', False),
                f"Status: {response.status_code}, Message: {data.get('message', 'No message')}"
            )
            
            return success and data.get('success', False)
        except Exception as e:
            self.log_test("Resident Registration", False, str(e))
            return False
    
    def test_resident_login(self):
        """Test resident user login"""
        try:
            login_data = {
                "email": "testresident@example.com",
                "password": "test123456"
            }
            
            response = requests.post(
                f"{self.base_url}/api/auth/login",
                json=login_data,
                timeout=10
            )
            
            success = response.status_code == 200
            data = response.json() if success else {}
            
            if success and data.get('success'):
                # Store token for authenticated requests
                token = data.get('token')
                if token:
                    self.session.headers.update({'Authorization': f'Bearer {token}'})
            
            self.log_test(
                "Resident Login",
                success and data.get('success', False),
                f"Status: {response.status_code}, Token received: {bool(data.get('token'))}"
            )
            
            return success and data.get('success', False)
        except Exception as e:
            self.log_test("Resident Login", False, str(e))
            return False
    
    def test_official_registration(self):
        """Test official user registration"""
        try:
            test_official = {
                "name": "Test Official",
                "email": "testofficial@example.com", 
                "password": "official123456",
                "role": "official"
            }
            
            response = requests.post(
                f"{self.base_url}/api/auth/register",
                json=test_official,
                timeout=10
            )
            
            success = response.status_code == 200
            data = response.json() if success else {}
            
            self.log_test(
                "Official Registration",
                success and data.get('success', False),
                f"Status: {response.status_code}, Message: {data.get('message', 'No message')}"
            )
            
            return success and data.get('success', False)
        except Exception as e:
            self.log_test("Official Registration", False, str(e))
            return False
    
    def test_official_login(self):
        """Test official user login"""
        try:
            login_data = {
                "email": "testofficial@example.com",
                "password": "official123456"
            }
            
            response = requests.post(
                f"{self.base_url}/api/auth/login",
                json=login_data,
                timeout=10
            )
            
            success = response.status_code == 200
            data = response.json() if success else {}
            
            if success and data.get('success'):
                # Store token for authenticated requests
                token = data.get('token')
                if token:
                    self.session.headers.update({'Authorization': f'Bearer {token}'})
            
            self.log_test(
                "Official Login",
                success and data.get('success', False),
                f"Status: {response.status_code}, Token received: {bool(data.get('token'))}"
            )
            
            return success and data.get('success', False)
        except Exception as e:
            self.log_test("Official Login", False, str(e))
            return False
    
    def test_fetch_facilities(self):
        """Test fetching facilities (both resident and official)"""
        try:
            response = self.session.get(
                f"{self.base_url}/api/facilities",
                timeout=10
            )
            
            success = response.status_code == 200
            data = response.json() if success else {}
            
            facilities = data.get('data', []) if data.get('success') else []
            
            self.log_test(
                "Fetch Facilities",
                success and data.get('success', False),
                f"Status: {response.status_code}, Facilities count: {len(facilities)}"
            )
            
            return success and data.get('success', False)
        except Exception as e:
            self.log_test("Fetch Facilities", False, str(e))
            return False
    
    def test_create_facility(self):
        """Test facility creation (official only)"""
        try:
            facility_data = {
                "name": "Test Facility",
                "description": "A test facility for automated testing",
                "amenities": '["Test amenity 1", "Test amenity 2"]',
                "max_capacity": 25,
                "hourly_rate": 150,
                "downpayment_rate": 75,
                "active": True,
                "main_photo_url": "🏢"
            }
            
            response = self.session.post(
                f"{self.base_url}/api/facilities",
                json=facility_data,
                timeout=10
            )
            
            success = response.status_code == 200
            data = response.json() if success else {}
            
            self.log_test(
                "Create Facility (Official)",
                success and data.get('success', False),
                f"Status: {response.status_code}, Message: {data.get('message', 'No message')}"
            )
            
            return success and data.get('success', False)
        except Exception as e:
            self.log_test("Create Facility (Official)", False, str(e))
            return False
    
    def test_create_booking(self):
        """Test booking creation (resident)"""
        try:
            # First login as resident
            self.test_resident_login()
            
            booking_data = {
                "facility_id": 1,
                "date": (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d'),
                "start_time": "09:00",
                "end_time": "11:00",
                "purpose": "Test booking for automated testing",
                "receipt_base64": "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg==",
                "payment_method": "cash",
                "total_amount": 300,
                "downpayment_amount": 150
            }
            
            response = self.session.post(
                f"{self.base_url}/api/bookings",
                json=booking_data,
                timeout=10
            )
            
            success = response.status_code == 200
            data = response.json() if success else {}
            
            self.log_test(
                "Create Booking (Resident)",
                success and data.get('success', False),
                f"Status: {response.status_code}, Message: {data.get('message', 'No message')}"
            )
            
            return success and data.get('success', False)
        except Exception as e:
            self.log_test("Create Booking (Resident)", False, str(e))
            return False
    
    def test_fetch_bookings(self):
        """Test fetching bookings (official sees all, resident sees own)"""
        try:
            response = self.session.get(
                f"{self.base_url}/api/bookings",
                timeout=10
            )
            
            success = response.status_code == 200
            data = response.json() if success else {}
            
            bookings = data.get('data', []) if data.get('success') else []
            
            self.log_test(
                "Fetch Bookings",
                success and data.get('success', False),
                f"Status: {response.status_code}, Bookings count: {len(bookings)}"
            )
            
            return success and data.get('success', False)
        except Exception as e:
            self.log_test("Fetch Bookings", False, str(e))
            return False
    
    def test_update_booking_status(self):
        """Test booking status update (official only)"""
        try:
            # First login as official
            self.test_official_login()
            
            update_data = {
                "status": "approved",
                "rejection_reason": ""
            }
            
            response = self.session.put(
                f"{self.base_url}/api/bookings/1/status",
                json=update_data,
                timeout=10
            )
            
            success = response.status_code == 200
            data = response.json() if success else {}
            
            self.log_test(
                "Update Booking Status (Official)",
                success and data.get('success', False),
                f"Status: {response.status_code}, Message: {data.get('message', 'No message')}"
            )
            
            return success and data.get('success', False)
        except Exception as e:
            self.log_test("Update Booking Status (Official)", False, str(e))
            return False
    
    def test_verification_request(self):
        """Test verification request creation (resident)"""
        try:
            # Login as resident
            self.test_resident_login()
            
            verification_data = {
                "verification_type": "resident",
                "residential_address": "123 Test Street, Test City",
                "user_photo_base64": "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg==",
                "valid_id_base64": "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg=="
            }
            
            response = self.session.post(
                f"{self.base_url}/api/verification-requests",
                json=verification_data,
                timeout=10
            )
            
            success = response.status_code == 200
            data = response.json() if success else {}
            
            self.log_test(
                "Create Verification Request (Resident)",
                success and data.get('success', False),
                f"Status: {response.status_code}, Message: {data.get('message', 'No message')}"
            )
            
            return success and data.get('success', False)
        except Exception as e:
            self.log_test("Create Verification Request (Resident)", False, str(e))
            return False
    
    def test_fetch_verification_requests(self):
        """Test fetching verification requests (official only)"""
        try:
            # Login as official
            self.test_official_login()
            
            response = self.session.get(
                f"{self.base_url}/api/verification-requests",
                timeout=10
            )
            
            success = response.status_code == 200
            data = response.json() if success else {}
            
            requests = data.get('data', []) if data.get('success') else []
            
            self.log_test(
                "Fetch Verification Requests (Official)",
                success and data.get('success', False),
                f"Status: {response.status_code}, Requests count: {len(requests)}"
            )
            
            return success and data.get('success', False)
        except Exception as e:
            self.log_test("Fetch Verification Requests (Official)", False, str(e))
            return False
    
    def test_update_verification_status(self):
        """Test verification status update (official only)"""
        try:
            # Login as official
            self.test_official_login()
            
            update_data = {
                "status": "approved",
                "discount_rate": "0.10"
            }
            
            response = self.session.put(
                f"{self.base_url}/api/verification-requests/1",
                json=update_data,
                timeout=10
            )
            
            success = response.status_code == 200
            data = response.json() if success else {}
            
            self.log_test(
                "Update Verification Status (Official)",
                success and data.get('success', False),
                f"Status: {response.status_code}, Message: {data.get('message', 'No message')}"
            )
            
            return success and data.get('success', False)
        except Exception as e:
            self.log_test("Update Verification Status (Official)", False, str(e))
            return False
    
    def test_user_profile(self):
        """Test user profile fetching"""
        try:
            response = self.session.get(
                f"{self.base_url}/api/users/profile/testresident@example.com",
                timeout=10
            )
            
            success = response.status_code == 200
            data = response.json() if success else {}
            
            self.log_test(
                "Fetch User Profile",
                success and data.get('success', False),
                f"Status: {response.status_code}, User found: {bool(data.get('user'))}"
            )
            
            return success and data.get('success', False)
        except Exception as e:
            self.log_test("Fetch User Profile", False, str(e))
            return False
    
    def test_delete_facility(self):
        """Test facility deletion (official only)"""
        try:
            # Login as official
            self.test_official_login()
            
            response = self.session.delete(
                f"{self.base_url}/api/facilities/999",  # Use non-existent ID to test endpoint
                timeout=10
            )
            
            # 404 is expected for non-existent facility, but 200 means endpoint works
            success = response.status_code in [200, 404]
            data = response.json() if response.status_code == 200 else {}
            
            self.log_test(
                "Delete Facility (Official)",
                success,
                f"Status: {response.status_code}, Endpoint accessible: {success}"
            )
            
            return success
        except Exception as e:
            self.log_test("Delete Facility (Official)", False, str(e))
            return False
    
    def run_all_tests(self):
        """Run comprehensive test suite"""
        print("🚀 Starting Barangay Reserve Comprehensive Test Suite")
        print("=" * 60)
        print(f"📡 Testing server: {self.base_url}")
        print("=" * 60)
        
        # Basic connectivity
        if not self.test_server_connection():
            print("❌ Server not accessible. Stopping tests.")
            return False
        
        # Authentication tests
        print("\n🔐 Authentication Tests:")
        self.test_resident_registration()
        self.test_resident_login()
        self.test_official_registration()
        self.test_official_login()
        
        # Facility tests
        print("\n🏢 Facility Tests:")
        self.test_fetch_facilities()
        self.test_create_facility()
        self.test_delete_facility()
        
        # Booking tests
        print("\n📅 Booking Tests:")
        self.test_create_booking()
        self.test_fetch_bookings()
        self.test_update_booking_status()
        
        # Verification tests
        print("\n✅ Verification Tests:")
        self.test_verification_request()
        self.test_fetch_verification_requests()
        self.test_update_verification_status()
        
        # User profile tests
        print("\n👤 User Profile Tests:")
        self.test_user_profile()
        
        # Summary
        self.print_summary()
        return True
    
    def print_summary(self):
        """Print test summary"""
        print("\n" + "=" * 60)
        print("📊 TEST SUMMARY")
        print("=" * 60)
        
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results if result['success'])
        failed_tests = total_tests - passed_tests
        
        print(f"Total Tests: {total_tests}")
        print(f"✅ Passed: {passed_tests}")
        print(f"❌ Failed: {failed_tests}")
        print(f"📈 Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        
        if failed_tests > 0:
            print("\n❌ FAILED TESTS:")
            for result in self.test_results:
                if not result['success']:
                    print(f"  • {result['test']}: {result['message']}")
        
        print("\n🎯 RECOMMENDATIONS:")
        if failed_tests == 0:
            print("  ✅ All tests passed! Your authentication fixes are working perfectly.")
            print("  🚀 You can confidently focus on your next ideas.")
        else:
            print("  ⚠️  Some tests failed. Review the failed tests above.")
            print("  🔧 Fix the issues before proceeding with new features.")
        
        print("=" * 60)

if __name__ == "__main__":
    # Create tester instance
    tester = BarangayReserveTester()
    
    # Run all tests
    tester.run_all_tests()
    
    # Save results to file for reference
    with open('test_results.json', 'w') as f:
        json.dump(tester.test_results, f, indent=2, default=str)
    
    print(f"\n📁 Test results saved to: test_results.json")
