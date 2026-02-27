import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os
from datetime import datetime
from typing import Optional, Dict, Any
from email_config import *

class EmailService:
    def __init__(self):
        # Email configuration from config file
        self.smtp_server = SMTP_SERVER
        self.smtp_port = SMTP_PORT
        self.sender_email = SENDER_EMAIL
        self.app_password = APP_PASSWORD
        self.email_enabled = EMAIL_ENABLED
        self.debug_email = DEBUG_EMAIL
        
    def _create_smtp_connection(self):
        """Create SMTP connection with app password authentication"""
        try:
            context = ssl.create_default_context()
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls(context=context)
            server.login(self.sender_email, self.app_password)
            return server
        except Exception as e:
            print(f"❌ Error creating SMTP connection: {e}")
            raise
    
    def _send_email(self, recipient_email: str, subject: str, body: str, is_html: bool = False) -> bool:
        """Send email using SMTP"""
        
        # Check if email is enabled
        if not self.email_enabled:
            print(f"📧 Email disabled - Would have sent to {recipient_email}: {subject}")
            return True
        
        # Debug mode - print email content instead of sending
        if self.debug_email:
            print(f"📧 DEBUG EMAIL - To: {recipient_email}")
            print(f"📧 DEBUG EMAIL - Subject: {subject}")
            print(f"📧 DEBUG EMAIL - Body: {body[:200]}...")
            return True
        
        try:
            server = self._create_smtp_connection()
            
            # Create message
            msg = MIMEMultipart("alternative")
            msg["Subject"] = subject
            msg["From"] = self.sender_email
            msg["To"] = recipient_email
            
            # Add body
            if is_html:
                msg.attach(MIMEText(body, "html"))
            else:
                msg.attach(MIMEText(body, "plain"))
            
            # Send email
            server.send_message(msg)
            server.quit()
            
            print(f"✅ Email sent successfully to {recipient_email}")
            return True
            
        except Exception as e:
            print(f"❌ Error sending email to {recipient_email}: {e}")
            return False
    
    def send_booking_rejection_email(self, recipient_email: str, recipient_name: str, 
                                   booking_details: Dict[str, Any], rejection_reason: str, 
                                   rejection_type: Optional[str] = None) -> bool:
        """Send email for booking rejection"""
        
        subject = "🚫 Booking Rejected - Barangay Facility Reservation"
        
        # Create HTML email template
        html_body = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Booking Rejection</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    line-height: 1.6;
                    color: #333;
                    max-width: 600px;
                    margin: 0 auto;
                    padding: 20px;
                }}
                .header {{
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    padding: 30px;
                    text-align: center;
                    border-radius: 10px 10px 0 0;
                }}
                .content {{
                    background: #f9f9f9;
                    padding: 30px;
                    border-radius: 0 0 10px 10px;
                    box-shadow: 0 0 20px rgba(0,0,0,0.1);
                }}
                .booking-details {{
                    background: white;
                    padding: 20px;
                    border-radius: 8px;
                    margin: 20px 0;
                    border-left: 4px solid #dc3545;
                }}
                .rejection-reason {{
                    background: #fff3cd;
                    border: 1px solid #ffeaa7;
                    padding: 15px;
                    border-radius: 5px;
                    margin: 20px 0;
                }}
                .footer {{
                    text-align: center;
                    margin-top: 30px;
                    color: #666;
                    font-size: 12px;
                }}
                .btn {{
                    display: inline-block;
                    padding: 12px 24px;
                    background: #007bff;
                    color: white;
                    text-decoration: none;
                    border-radius: 5px;
                    margin: 10px 5px;
                }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>🏛️ Barangay Facility Reservation</h1>
                <h2>Booking Status Update</h2>
            </div>
            
            <div class="content">
                <p>Dear <strong>{recipient_name}</strong>,</p>
                
                <p>We regret to inform you that your facility booking request has been <strong>rejected</strong>.</p>
                
                <div class="booking-details">
                    <h3>📋 Booking Details</h3>
                    <p><strong>Facility:</strong> {booking_details.get('facility_name', 'N/A')}</p>
                    <p><strong>Date:</strong> {booking_details.get('booking_date', 'N/A')}</p>
                    <p><strong>Time:</strong> {booking_details.get('timeslot', 'N/A')}</p>
                    <p><strong>Booking Reference:</strong> {booking_details.get('booking_reference', 'N/A')}</p>
                </div>
                
                <div class="rejection-reason">
                    <h3>🚫 Reason for Rejection</h3>
                    <p>{rejection_reason}</p>
                    {f'<p><strong>Rejection Type:</strong> {rejection_type}</p>' if rejection_type else ''}
                </div>
                
                {self._get_violation_warning(rejection_type) if rejection_type == 'fake_receipt' else ''}
                
                <p>If you believe this is an error or have questions about this decision, please contact the barangay office.</p>
                
                <div style="text-align: center; margin: 30px 0;">
                    <a href="#" class="btn">📅 Book Another Time</a>
                    <a href="#" class="btn">📞 Contact Office</a>
                </div>
                
                <p>Thank you for your understanding.</p>
            </div>
            
            <div class="footer">
                <p>© 2024 Barangay Management System | This is an automated message, please do not reply to this email.</p>
            </div>
        </body>
        </html>
        """
        
        return self._send_email(recipient_email, subject, html_body, is_html=True)
    
    def send_booking_approval_email(self, recipient_email: str, recipient_name: str, 
                                  booking_details: Dict[str, Any]) -> bool:
        """Send email for booking approval"""
        
        subject = "✅ Booking Approved - Barangay Facility Reservation"
        
        html_body = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Booking Approval</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    line-height: 1.6;
                    color: #333;
                    max-width: 600px;
                    margin: 0 auto;
                    padding: 20px;
                }}
                .header {{
                    background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
                    color: white;
                    padding: 30px;
                    text-align: center;
                    border-radius: 10px 10px 0 0;
                }}
                .content {{
                    background: #f9f9f9;
                    padding: 30px;
                    border-radius: 0 0 10px 10px;
                    box-shadow: 0 0 20px rgba(0,0,0,0.1);
                }}
                .booking-details {{
                    background: white;
                    padding: 20px;
                    border-radius: 8px;
                    margin: 20px 0;
                    border-left: 4px solid #28a745;
                }}
                .approval-notice {{
                    background: #d4edda;
                    border: 1px solid #c3e6cb;
                    padding: 15px;
                    border-radius: 5px;
                    margin: 20px 0;
                }}
                .footer {{
                    text-align: center;
                    margin-top: 30px;
                    color: #666;
                    font-size: 12px;
                }}
                .btn {{
                    display: inline-block;
                    padding: 12px 24px;
                    background: #007bff;
                    color: white;
                    text-decoration: none;
                    border-radius: 5px;
                    margin: 10px 5px;
                }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>🏛️ Barangay Facility Reservation</h1>
                <h2>Booking Confirmed!</h2>
            </div>
            
            <div class="content">
                <p>Dear <strong>{recipient_name}</strong>,</p>
                
                <div class="approval-notice">
                    <h3>🎉 Good News!</h3>
                    <p>Your facility booking request has been <strong>approved</strong> and confirmed.</p>
                </div>
                
                <div class="booking-details">
                    <h3>📋 Booking Details</h3>
                    <p><strong>Facility:</strong> {booking_details.get('facility_name', 'N/A')}</p>
                    <p><strong>Date:</strong> {booking_details.get('booking_date', 'N/A')}</p>
                    <p><strong>Time:</strong> {booking_details.get('timeslot', 'N/A')}</p>
                    <p><strong>Booking Reference:</strong> {booking_details.get('booking_reference', 'N/A')}</p>
                    <p><strong>Status:</strong> <span style="color: #28a745;">✅ CONFIRMED</span></p>
                </div>
                
                <p>Please arrive on time and bring any necessary documents or equipment for your activity.</p>
                
                <div style="text-align: center; margin: 30px 0;">
                    <a href="#" class="btn">📅 View My Bookings</a>
                    <a href="#" class="btn">📞 Contact Office</a>
                </div>
                
                <p>We look forward to serving you!</p>
            </div>
            
            <div class="footer">
                <p>© 2024 Barangay Management System | This is an automated message, please do not reply to this email.</p>
            </div>
        </body>
        </html>
        """
        
        return self._send_email(recipient_email, subject, html_body, is_html=True)
    
    def send_verification_approval_email(self, recipient_email: str, recipient_name: str, 
                                       verification_type: str, discount_rate: float) -> bool:
        """Send email for verification request approval"""
        
        subject = "✅ Verification Approved - Barangay Resident Status"
        
        verification_display = "Resident" if verification_type == "resident" else "Non-Resident"
        
        html_body = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Verification Approval</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    line-height: 1.6;
                    color: #333;
                    max-width: 600px;
                    margin: 0 auto;
                    padding: 20px;
                }}
                .header {{
                    background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
                    color: white;
                    padding: 30px;
                    text-align: center;
                    border-radius: 10px 10px 0 0;
                }}
                .content {{
                    background: #f9f9f9;
                    padding: 30px;
                    border-radius: 0 0 10px 10px;
                    box-shadow: 0 0 20px rgba(0,0,0,0.1);
                }}
                .verification-details {{
                    background: white;
                    padding: 20px;
                    border-radius: 8px;
                    margin: 20px 0;
                    border-left: 4px solid #28a745;
                }}
                .discount-badge {{
                    background: #ffc107;
                    color: #333;
                    padding: 10px 20px;
                    border-radius: 20px;
                    display: inline-block;
                    font-weight: bold;
                    margin: 10px 0;
                }}
                .footer {{
                    text-align: center;
                    margin-top: 30px;
                    color: #666;
                    font-size: 12px;
                }}
                .btn {{
                    display: inline-block;
                    padding: 12px 24px;
                    background: #007bff;
                    color: white;
                    text-decoration: none;
                    border-radius: 5px;
                    margin: 10px 5px;
                }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>🏛️ Barangay Management System</h1>
                <h2>Verification Approved!</h2>
            </div>
            
            <div class="content">
                <p>Dear <strong>{recipient_name}</strong>,</p>
                
                <p>Congratulations! Your verification request has been <strong>approved</strong>.</p>
                
                <div class="verification-details">
                    <h3>🎉 Verification Details</h3>
                    <p><strong>Status:</strong> <span style="color: #28a745;">✅ VERIFIED</span></p>
                    <p><strong>Verification Type:</strong> {verification_display}</p>
                    <p><strong>Effective Date:</strong> {datetime.now().strftime('%B %d, %Y')}</p>
                    
                    <div class="discount-badge">
                        💰 Discount Rate: {int(discount_rate * 100)}%
                    </div>
                </div>
                
                <p>As a verified {verification_display.lower()}, you now enjoy special benefits including:</p>
                <ul>
                    <li>✅ Priority booking access</li>
                    <li>💰 {int(discount_rate * 100)}% discount on facility rentals</li>
                    <li>📋 Enhanced booking privileges</li>
                </ul>
                
                <div style="text-align: center; margin: 30px 0;">
                    <a href="#" class="btn">📅 Book a Facility</a>
                    <a href="#" class="btn">👤 View Profile</a>
                </div>
                
                <p>Thank you for completing the verification process!</p>
            </div>
            
            <div class="footer">
                <p>© 2024 Barangay Management System | This is an automated message, please do not reply to this email.</p>
            </div>
        </body>
        </html>
        """
        
        return self._send_email(recipient_email, subject, html_body, is_html=True)
    
    def send_verification_rejection_email(self, recipient_email: str, recipient_name: str, 
                                       verification_type: str, rejection_reason: str) -> bool:
        """Send email for verification request rejection"""
        
        subject = "🚫 Verification Rejected - Barangay Resident Status"
        
        verification_display = "Resident" if verification_type == "resident" else "Non-Resident"
        
        html_body = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Verification Rejection</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    line-height: 1.6;
                    color: #333;
                    max-width: 600px;
                    margin: 0 auto;
                    padding: 20px;
                }}
                .header {{
                    background: linear-gradient(135deg, #dc3545 0%, #c82333 100%);
                    color: white;
                    padding: 30px;
                    text-align: center;
                    border-radius: 10px 10px 0 0;
                }}
                .content {{
                    background: #f9f9f9;
                    padding: 30px;
                    border-radius: 0 0 10px 10px;
                    box-shadow: 0 0 20px rgba(0,0,0,0.1);
                }}
                .verification-details {{
                    background: white;
                    padding: 20px;
                    border-radius: 8px;
                    margin: 20px 0;
                    border-left: 4px solid #dc3545;
                }}
                .rejection-reason {{
                    background: #fff3cd;
                    border: 1px solid #ffeaa7;
                    padding: 15px;
                    border-radius: 5px;
                    margin: 20px 0;
                }}
                .footer {{
                    text-align: center;
                    margin-top: 30px;
                    color: #666;
                    font-size: 12px;
                }}
                .btn {{
                    display: inline-block;
                    padding: 12px 24px;
                    background: #007bff;
                    color: white;
                    text-decoration: none;
                    border-radius: 5px;
                    margin: 10px 5px;
                }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>🏛️ Barangay Management System</h1>
                <h2>Verification Update</h2>
            </div>
            
            <div class="content">
                <p>Dear <strong>{recipient_name}</strong>,</p>
                
                <p>We regret to inform you that your {verification_display.lower()} verification request has been <strong>rejected</strong>.</p>
                
                <div class="verification-details">
                    <h3>📋 Verification Details</h3>
                    <p><strong>Status:</strong> <span style="color: #dc3545;">❌ REJECTED</span></p>
                    <p><strong>Verification Type:</strong> {verification_display}</p>
                    <p><strong>Review Date:</strong> {datetime.now().strftime('%B %d, %Y')}</p>
                </div>
                
                <div class="rejection-reason">
                    <h3>🚫 Reason for Rejection</h3>
                    <p>{rejection_reason}</p>
                </div>
                
                <p>If you believe this is an error or would like to submit additional documentation, please:</p>
                <ol>
                    <li>Review the rejection reason above</li>
                    <li>Prepare any additional required documents</li>
                    <li>Submit a new verification request with complete requirements</li>
                </ol>
                
                <div style="text-align: center; margin: 30px 0;">
                    <a href="#" class="btn">📄 Submit New Request</a>
                    <a href="#" class="btn">📞 Contact Office</a>
                </div>
                
                <p>Thank you for your understanding.</p>
            </div>
            
            <div class="footer">
                <p>© 2024 Barangay Management System | This is an automated message, please do not reply to this email.</p>
            </div>
        </body>
        </html>
        """
        
        return self._send_email(recipient_email, subject, html_body, is_html=True)
    
    def _get_violation_warning(self, rejection_type: str) -> str:
        """Get violation warning for fake receipt rejections"""
        if rejection_type == 'fake_receipt':
            return """
            <div style="background: #f8d7da; border: 1px solid #f5c6cb; padding: 15px; border-radius: 5px; margin: 20px 0;">
                <h3 style="color: #721c24;">⚠️ Important Notice</h3>
                <p style="color: #721c24;">This violation has been recorded in our system. Repeated violations may result in account suspension or permanent ban.</p>
                <p style="color: #721c24;">Please ensure all payment receipts are genuine and verifiable.</p>
            </div>
            """
        return ""

# Global email service instance
email_service = EmailService()
