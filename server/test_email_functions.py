#!/usr/bin/env python3
"""
Email Service Test Script
Tests all email notification functions to ensure they work properly
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from email_service import EmailService
from email_config import EMAIL_ENABLED, DEBUG_EMAIL, SENDER_EMAIL

def test_email_service():
    """Test all email service functions"""
    
    print("🔧 EMAIL SERVICE TEST")
    print("=" * 50)
    
    # Check email configuration
    print(f"📧 Email Enabled: {EMAIL_ENABLED}")
    print(f"🔍 Debug Mode: {DEBUG_EMAIL}")
    print(f"📤 Sender Email: {SENDER_EMAIL}")
    print()
    
    # Initialize email service
    email_service = EmailService()
    
    # Test data
    resident_email = "jl052904@gmail.com"
    resident_name = "Test Resident"
    
    # Test 1: Booking Overlap Email
    print("🧪 TEST 1: Booking Overlap Email")
    print("-" * 30)
    
    original_booking = {
        'facility_name': 'Basketball Court',
        'booking_date': '2026-04-06',
        'start_time': '12:00 PM',
        'end_time': '2:00 PM'
    }
    
    official_booking = {
        'facility_name': 'Basketball Court',
        'booking_date': '2026-04-06',
        'start_time': '1:00 PM',
        'end_time': '3:00 PM',
        'official_name': 'Captain Barangay'
    }
    
    overlap_result = email_service.send_booking_overlap_email(
        resident_email, resident_name, original_booking, official_booking
    )
    print(f"✅ Overlap Email Result: {overlap_result}")
    print()
    
    # Test 2: Official Notification Email (Booking Request)
    print("🧪 TEST 2: Official Notification Email (Booking Request)")
    print("-" * 30)
    
    resident_details = {
        'name': 'Test Resident',
        'email': 'test@example.com',
        'phone': '09123456789'
    }
    
    booking_details = {
        'facility_name': 'Basketball Court',
        'booking_date': '2026-04-06',
        'start_time': '12:00 PM',
        'end_time': '2:00 PM',
        'purpose': 'Practice'
    }
    
    official_notification_result = email_service.send_official_notification_email(
        'booking', resident_details, booking_details
    )
    print(f"✅ Official Notification Result: {official_notification_result}")
    print()
    
    # Test 3: Official Notification Email (Authentication Request)
    print("🧪 TEST 3: Official Notification Email (Authentication Request)")
    print("-" * 30)
    
    auth_details = {
        'verification_type': 'resident',
        'full_name': 'Test Resident',
        'address': '123 Test Street',
        'contact_number': '09123456789',
        'id_type': 'National ID',
        'submission_date': '2026-04-04'
    }
    
    auth_notification_result = email_service.send_official_notification_email(
        'authentication', resident_details, auth_details
    )
    print(f"✅ Auth Notification Result: {auth_notification_result}")
    print()
    
    # Test 4: Resident Confirmation Email (Booking)
    print("🧪 TEST 4: Resident Confirmation Email (Booking)")
    print("-" * 30)
    
    resident_confirmation_result = email_service.send_resident_submission_confirmation_email(
        resident_email, resident_name, 'booking', booking_details
    )
    print(f"✅ Resident Confirmation Result: {resident_confirmation_result}")
    print()
    
    # Test 5: Resident Confirmation Email (Authentication)
    print("🧪 TEST 5: Resident Confirmation Email (Authentication)")
    print("-" * 30)
    
    resident_auth_confirmation_result = email_service.send_resident_submission_confirmation_email(
        resident_email, resident_name, 'authentication', auth_details
    )
    print(f"✅ Resident Auth Confirmation Result: {resident_auth_confirmation_result}")
    print()
    
    # Test 6: Standard Booking Approval
    print("🧪 TEST 6: Standard Booking Approval")
    print("-" * 30)
    
    approval_booking_details = {
        'facility_name': 'Basketball Court',
        'booking_date': '2026-04-06',
        'start_time': '12:00 PM',
        'end_time': '2:00 PM',
        'discount_rate': 10.0
    }
    
    approval_result = email_service.send_booking_approval_email(
        resident_email, resident_name, approval_booking_details
    )
    print(f"✅ Approval Email Result: {approval_result}")
    print()
    
    # Test 7: Standard Booking Rejection
    print("🧪 TEST 7: Standard Booking Rejection")
    print("-" * 30)
    
    rejection_booking_details = {
        'facility_name': 'Basketball Court',
        'booking_date': '2026-04-06',
        'start_time': '12:00 PM',
        'end_time': '2:00 PM',
        'rejection_reason': 'fake_payment'
    }
    
    rejection_result = email_service.send_booking_rejection_email(
        resident_email, resident_name, rejection_booking_details, 'fake_payment'
    )
    print(f"✅ Rejection Email Result: {rejection_result}")
    print()
    
    print("=" * 50)
    print("🎯 EMAIL TEST COMPLETE!")
    print()
    
    if DEBUG_EMAIL:
        print("📝 DEBUG MODE: Check console output above for email content")
    else:
        print("📧 LIVE MODE: Check your email inbox for sent emails")
    
    print(f"📧 Test emails should be sent to: {resident_email}")
    print(f"📧 Official notifications sent to: {SENDER_EMAIL}")
    
    return True

if __name__ == "__main__":
    try:
        test_email_service()
        print("✅ Email test completed successfully!")
    except Exception as e:
        print(f"❌ Email test failed: {str(e)}")
        import traceback
        traceback.print_exc()
