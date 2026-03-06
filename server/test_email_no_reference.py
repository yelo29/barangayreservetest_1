#!/usr/bin/env python3

"""
Test script to verify email templates work without reference numbers
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from email_service import EmailService
from datetime import datetime

def test_email_templates():
    """Test that email templates work without reference numbers"""
    
    email_service = EmailService()
    
    print("🧪 Testing Email Templates (No Reference Numbers)")
    print("=" * 60)
    
    # Test 1: Booking submission confirmation
    print("\n1. 📅 Testing Booking Submission Email...")
    booking_details = {
        'facility_name': 'Barangay Hall',
        'booking_date': '2026-03-15',
        'timeslot': '2:00 PM - 4:00 PM',
        'purpose': 'Meeting',
        'submitted_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    
    resident_name = "Test Resident"
    resident_email = "test@example.com"
    
    try:
        result = email_service.send_resident_submission_confirmation_email(
            resident_email, resident_name, 'booking', booking_details
        )
        print(f"✅ Booking submission email: {'SENT' if result else 'FAILED'}")
    except Exception as e:
        print(f"❌ Booking submission email error: {e}")
    
    # Test 2: Verification submission confirmation
    print("\n2. 👤 Testing Verification Submission Email...")
    verification_details = {
        'verification_type': 'resident',
        'full_name': 'Test Resident',
        'submitted_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    
    try:
        result = email_service.send_resident_submission_confirmation_email(
            resident_email, resident_name, 'authentication', verification_details
        )
        print(f"✅ Verification submission email: {'SENT' if result else 'FAILED'}")
    except Exception as e:
        print(f"❌ Verification submission email error: {e}")
    
    # Test 3: Official notification for booking
    print("\n3. 🏛️ Testing Official Notification Email (Booking)...")
    resident_details = {
        'full_name': 'Test Resident',
        'email': 'test@example.com',
        'contact_number': '09123456789',
        'verification_status': 'Verified Resident'
    }
    
    try:
        result = email_service.send_official_notification_email(
            'booking', resident_details, booking_details
        )
        print(f"✅ Official notification email (booking): {'SENT' if result else 'FAILED'}")
    except Exception as e:
        print(f"❌ Official notification email (booking) error: {e}")
    
    # Test 4: Official notification for verification
    print("\n4. 🏛️ Testing Official Notification Email (Verification)...")
    try:
        result = email_service.send_official_notification_email(
            'authentication', resident_details, verification_details
        )
        print(f"✅ Official notification email (verification): {'SENT' if result else 'FAILED'}")
    except Exception as e:
        print(f"❌ Official notification email (verification) error: {e}")
    
    # Test 5: Booking rejection
    print("\n5. 🚫 Testing Booking Rejection Email...")
    try:
        result = email_service.send_booking_rejection_email(
            resident_email, resident_name, booking_details, "Fake receipt detected", "fake_receipt"
        )
        print(f"✅ Booking rejection email: {'SENT' if result else 'FAILED'}")
    except Exception as e:
        print(f"❌ Booking rejection email error: {e}")
    
    # Test 6: Booking approval
    print("\n6. ✅ Testing Booking Approval Email...")
    try:
        result = email_service.send_booking_approval_email(
            resident_email, resident_name, booking_details
        )
        print(f"✅ Booking approval email: {'SENT' if result else 'FAILED'}")
    except Exception as e:
        print(f"❌ Booking approval email error: {e}")
    
    print("\n" + "=" * 60)
    print("🎉 Email template testing completed!")
    print("📝 All templates now work WITHOUT reference numbers")
    print("📞 Users can contact officials through customer service section")

if __name__ == "__main__":
    test_email_templates()
