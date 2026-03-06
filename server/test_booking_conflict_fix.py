#!/usr/bin/env python3
"""
Test script to verify booking conflict detection and data isolation fix
Tests the /api/bookings/check-conflict endpoint with proper user isolation
"""

import requests
import json
import sqlite3
from datetime import datetime, timedelta
import sys
import os

# Configuration
BASE_URL = "http://localhost:8000"
DB_PATH = "barangay.db"

class BookingConflictTest:
    def __init__(self):
        self.base_url = BASE_URL
        self.db_path = DB_PATH
        self.test_users = []
        self.test_facilities = []
        
    def setup_test_data(self):
        """Create test users and facilities for testing"""
        print("🔧 Setting up test data...")
        
        # Connect to database
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create test users if they don't exist
        test_user_emails = [
            "test_user1@example.com",
            "test_user2@example.com", 
            "test_user3@example.com"
        ]
        
        for email in test_user_emails:
            # Check if user exists
            cursor.execute('SELECT id FROM users WHERE email = ?', (email,))
            user = cursor.fetchone()
            
            if not user:
                # Create test user
                cursor.execute('''
                    INSERT INTO users (email, full_name, role, verified, password, created_at)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (email, f"Test User {email.split('@')[0]}", 'resident', 1, 'test_password', datetime.now()))
                user_id = cursor.lastrowid
                print(f"✅ Created test user: {email} (ID: {user_id})")
                self.test_users.append({'id': user_id, 'email': email})
            else:
                self.test_users.append({'id': user[0], 'email': email})
                print(f"📋 Using existing test user: {email} (ID: {user[0]})")
        
        # Create test facility if it doesn't exist
        cursor.execute('SELECT id FROM facilities WHERE name = ?', ('Test Facility',))
        facility = cursor.fetchone()
        
        if not facility:
            cursor.execute('''
                INSERT INTO facilities (name, description, hourly_rate, downpayment_rate, created_at)
                VALUES (?, ?, ?, ?, ?)
            ''', ('Test Facility', 'Test facility for conflict detection', 100.0, 20.0, datetime.now()))
            facility_id = cursor.lastrowid
            print(f"✅ Created test facility: Test Facility (ID: {facility_id})")
        else:
            facility_id = facility[0]
            print(f"📋 Using existing test facility: Test Facility (ID: {facility_id})")
        
        self.test_facilities.append({'id': facility_id, 'name': 'Test Facility'})
        
        conn.commit()
        conn.close()
        
        print(f"🎯 Setup complete: {len(self.test_users)} users, {len(self.test_facilities)} facilities")
        
    def cleanup_test_data(self):
        """Clean up test bookings"""
        print("🧹 Cleaning up test bookings...")
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Delete test bookings
        for user in self.test_users:
            cursor.execute('DELETE FROM bookings WHERE user_id = ?', (user['id'],))
        
        conn.commit()
        conn.close()
        print("✅ Test bookings cleaned up")
        
    def test_conflict_detection_same_user(self):
        """Test that same user doesn't get conflict with their own booking"""
        print("\n🧪 TEST 1: Same user conflict detection")
        
        user = self.test_users[0]
        facility = self.test_facilities[0]
        test_date = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
        test_timeslot = "10:00 AM - 11:00 AM"
        
        # First, create a booking for user1
        booking_data = {
            'facility_id': facility['id'],
            'date': test_date,
            'timeslot': test_timeslot,
            'user_email': user['email'],
            'status': 'pending',
            'purpose': 'Test booking',
            'total_amount': 100,
            'contact_number': '1234567890',
            'address': 'Test Address'
        }
        
        try:
            # Create booking
            response = requests.post(f"{self.base_url}/api/bookings", json=booking_data)
            if response.status_code == 200:
                booking_result = response.json()
                print(f"✅ Created booking for {user['email']}: {booking_result.get('message', 'Success')}")
                
                # Now check for conflict - should return NO conflict for same user
                conflict_data = {
                    'facility_id': facility['id'],
                    'date': test_date,
                    'timeslot': test_timeslot,
                    'user_email': user['email']
                }
                
                conflict_response = requests.post(f"{self.base_url}/api/bookings/check-conflict", json=conflict_data)
                conflict_result = conflict_response.json()
                
                print(f"🔍 Conflict check result: {conflict_result}")
                
                if conflict_result.get('success') and not conflict_result.get('has_conflict'):
                    print("✅ PASS: Same user correctly sees no conflict with their own booking")
                    return True
                else:
                    print("❌ FAIL: Same user incorrectly sees conflict with their own booking")
                    return False
            else:
                print(f"❌ Failed to create booking: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Exception in test 1: {e}")
            return False
            
    def test_conflict_detection_different_users(self):
        """Test that different users DO get conflict with each other's bookings"""
        print("\n🧪 TEST 2: Different users conflict detection")
        
        user1 = self.test_users[0]
        user2 = self.test_users[1]
        facility = self.test_facilities[0]
        test_date = (datetime.now() + timedelta(days=2)).strftime('%Y-%m-%d')
        test_timeslot = "02:00 PM - 03:00 PM"
        
        # First, create a booking for user1
        booking_data = {
            'facility_id': facility['id'],
            'date': test_date,
            'timeslot': test_timeslot,
            'user_email': user1['email'],
            'status': 'approved',
            'purpose': 'Test booking user1',
            'total_amount': 100,
            'contact_number': '1234567890',
            'address': 'Test Address'
        }
        
        try:
            # Create booking for user1
            response = requests.post(f"{self.base_url}/api/bookings", json=booking_data)
            if response.status_code == 200:
                print(f"✅ Created booking for {user1['email']}")
                
                # Now check for conflict from user2 - should return CONFLICT
                conflict_data = {
                    'facility_id': facility['id'],
                    'date': test_date,
                    'timeslot': test_timeslot,
                    'user_email': user2['email']
                }
                
                conflict_response = requests.post(f"{self.base_url}/api/bookings/check-conflict", json=conflict_data)
                conflict_result = conflict_response.json()
                
                print(f"🔍 Conflict check result for {user2['email']}: {conflict_result}")
                
                if conflict_result.get('success') and conflict_result.get('has_conflict'):
                    print("✅ PASS: Different user correctly sees conflict with existing booking")
                    
                    # Verify the conflict info shows the correct booking user
                    conflict_info = conflict_result.get('conflict_info', {})
                    if conflict_info.get('user_email') == user1['email']:
                        print(f"✅ PASS: Conflict info correctly shows booking by {user1['email']}")
                        return True
                    else:
                        print(f"❌ FAIL: Conflict info shows wrong user: {conflict_info.get('user_email')}")
                        return False
                else:
                    print("❌ FAIL: Different user doesn't see conflict with existing booking")
                    return False
            else:
                print(f"❌ Failed to create booking: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Exception in test 2: {e}")
            return False
            
    def test_no_conflict_available_timeslot(self):
        """Test that available timeslot returns no conflict"""
        print("\n🧪 TEST 3: Available timeslot conflict detection")
        
        user = self.test_users[2]
        facility = self.test_facilities[0]
        test_date = (datetime.now() + timedelta(days=3)).strftime('%Y-%m-%d')
        test_timeslot = "04:00 PM - 05:00 PM"
        
        # Check for conflict on a timeslot that should be available
        conflict_data = {
            'facility_id': facility['id'],
            'date': test_date,
            'timeslot': test_timeslot,
            'user_email': user['email']
        }
        
        try:
            conflict_response = requests.post(f"{self.base_url}/api/bookings/check-conflict", json=conflict_data)
            conflict_result = conflict_response.json()
            
            print(f"🔍 Conflict check result: {conflict_result}")
            
            if conflict_result.get('success') and not conflict_result.get('has_conflict'):
                print("✅ PASS: Available timeslot correctly shows no conflict")
                return True
            else:
                print("❌ FAIL: Available timeslot incorrectly shows conflict")
                return False
                
        except Exception as e:
            print(f"❌ Exception in test 3: {e}")
            return False
            
    def test_invalid_user_handling(self):
        """Test that invalid user email is handled properly"""
        print("\n🧪 TEST 4: Invalid user handling")
        
        facility = self.test_facilities[0]
        test_date = (datetime.now() + timedelta(days=4)).strftime('%Y-%m-%d')
        test_timeslot = "06:00 PM - 07:00 PM"
        
        # Check for conflict with invalid user email
        conflict_data = {
            'facility_id': facility['id'],
            'date': test_date,
            'timeslot': test_timeslot,
            'user_email': 'invalid_user@example.com'
        }
        
        try:
            conflict_response = requests.post(f"{self.base_url}/api/bookings/check-conflict", json=conflict_data)
            conflict_result = conflict_response.json()
            
            print(f"🔍 Conflict check result: {conflict_result}")
            
            if not conflict_result.get('success') and 'User not found' in conflict_result.get('message', ''):
                print("✅ PASS: Invalid user correctly returns error")
                return True
            else:
                print("❌ FAIL: Invalid user handling incorrect")
                return False
                
        except Exception as e:
            print(f"❌ Exception in test 4: {e}")
            return False
            
    def run_all_tests(self):
        """Run all tests and report results"""
        print("🚀 Starting Booking Conflict Detection Tests")
        print("=" * 60)
        
        # Check if server is running
        try:
            response = requests.get(f"{self.base_url}/", timeout=5)
            print(f"✅ Server is running at {self.base_url}")
        except:
            print(f"❌ Server is not running at {self.base_url}")
            print("Please start the server first: python server.py")
            return False
        
        # Setup test data
        self.setup_test_data()
        
        # Run tests
        tests = [
            ("Same User Conflict Detection", self.test_conflict_detection_same_user),
            ("Different Users Conflict Detection", self.test_conflict_detection_different_users),
            ("Available Timeslot Detection", self.test_no_conflict_available_timeslot),
            ("Invalid User Handling", self.test_invalid_user_handling)
        ]
        
        results = []
        for test_name, test_func in tests:
            try:
                result = test_func()
                results.append((test_name, result))
            except Exception as e:
                print(f"❌ Test '{test_name}' failed with exception: {e}")
                results.append((test_name, False))
        
        # Cleanup
        self.cleanup_test_data()
        
        # Report results
        print("\n" + "=" * 60)
        print("📊 TEST RESULTS SUMMARY")
        print("=" * 60)
        
        passed = 0
        failed = 0
        
        for test_name, result in results:
            status = "✅ PASS" if result else "❌ FAIL"
            print(f"{status}: {test_name}")
            if result:
                passed += 1
            else:
                failed += 1
        
        print(f"\n🎯 Total: {len(results)} tests")
        print(f"✅ Passed: {passed}")
        print(f"❌ Failed: {failed}")
        
        if failed == 0:
            print("\n🎉 ALL TESTS PASSED! Booking conflict detection is working correctly.")
            return True
        else:
            print(f"\n⚠️  {failed} test(s) failed. Please check the implementation.")
            return False

if __name__ == "__main__":
    # Change to server directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    server_dir = os.path.join(script_dir)
    
    if os.path.exists(server_dir):
        os.chdir(server_dir)
        print(f"📁 Working directory: {os.getcwd()}")
    
    # Run tests
    tester = BookingConflictTest()
    success = tester.run_all_tests()
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)
