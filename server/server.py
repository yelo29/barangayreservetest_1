#!/usr/bin/env python3
"""
Barangay Reserve Server
Free, self-hosted solution for students
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import sqlite3
import json
from datetime import datetime
import os
from config import Config

app = Flask(__name__)
# Dynamic CORS configuration for DuckDNS
CORS(app, origins=Config.get_cors_origins())

# Database setup
def init_db():
    import sqlite3
    conn = sqlite3.connect(Config.DATABASE_PATH)
    cursor = conn.cursor()
    
    # Create tables
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE,
            password TEXT,
            full_name TEXT,
            role TEXT,
            verified BOOLEAN DEFAULT FALSE,
            discount_rate REAL DEFAULT 0.0,
            contact_number TEXT,
            address TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS facilities (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            description TEXT,
            price REAL,
            image_url TEXT,
            active BOOLEAN DEFAULT 1,
            amenities TEXT,
            downpayment REAL,
            capacity INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            facility_id INTEGER,
            user_email TEXT,
            date TEXT,
            timeslot TEXT,
            purpose TEXT,
            status TEXT DEFAULT 'pending',
            payment_details TEXT,
            receipt_base64 TEXT,
            contact_number TEXT,
            address TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (facility_id) REFERENCES facilities (id)
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS verification_requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            request_reference VARCHAR(20) NOT NULL,
            user_id INTEGER NOT NULL,
            verification_type VARCHAR(20) NOT NULL,
            requested_discount_rate DECIMAL(3,2) NOT NULL,
            user_photo_base64 TEXT,
            user_photo_filename VARCHAR(255),
            valid_id_base64 TEXT,
            valid_id_filename VARCHAR(255),
            proof_of_residency_base64 TEXT,
            proof_of_residency_filename VARCHAR(255),
            additional_documents TEXT,
            residential_address TEXT,
            years_of_residence INTEGER,
            status VARCHAR(30) DEFAULT 'pending',
            reviewed_by INTEGER,
            reviewed_at DATETIME,
            approval_notes TEXT,
            rejection_reason TEXT,
            additional_info_requested TEXT,
            additional_info_provided TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    conn.commit()
    conn.close()

# Initialize database on startup
init_db()

# Helper function to get database connection
def get_db_connection():
    print(f"🔍 DEBUG: Connecting to database at: {Config.DATABASE_PATH}")
    conn = sqlite3.connect(Config.DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# Alias for backward compatibility
def get_db():
    return get_db_connection()

# Add missing columns to existing database
def migrate_database():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Add missing columns to facilities table if they don't exist
    try:
        cursor.execute('ALTER TABLE facilities ADD COLUMN active BOOLEAN DEFAULT 1')
    except:
        pass  # Column might already exist
    
    try:
        cursor.execute('ALTER TABLE facilities ADD COLUMN amenities TEXT')
    except:
        pass  # Column might already exist
    
    try:
        cursor.execute('ALTER TABLE facilities ADD COLUMN downpayment REAL')
    except:
        pass  # Column might already exist
    
    try:
        cursor.execute('ALTER TABLE facilities ADD COLUMN updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP')
    except:
        pass  # Column might already exist
    
    conn.commit()
    conn.close()
    print("Database migration completed")

# Run migration
migrate_database()

# API Routes

@app.route('/')
def home():
    return jsonify({
        'message': 'Barangay Reserve Server Running!',
        'status': 'online',
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/me', methods=['GET'])
def get_current_user():
    # This is a simplified version - in production, you'd validate the JWT token
    # For now, we'll return a mock user or require email parameter
    email = request.args.get('email')
    if not email:
        return jsonify({'success': False, 'error': 'Email parameter required'})
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT id, email, full_name, role, verified, verification_type, discount_rate, contact_number, address, profile_photo_url, is_active, email_verified, last_login, created_at, updated_at FROM users WHERE email = ?', (email,))
    user = cursor.fetchone()
    
    conn.close()
    
    if user:
        return jsonify({
            'success': True,
            'user': {
                'id': user[0],
                'email': user[1],
                'full_name': user[2],
                'role': user[3],
                'verified': user[4],
                'verification_type': user[5],
                'discount_rate': user[6],
                'contact_number': user[7],
                'address': user[8],
                'profile_photo_url': user[9],
                'is_active': user[10],
                'email_verified': user[11],
                'last_login': user[12],
                'created_at': user[13],
                'updated_at': user[14]
            }
        })
    else:
        return jsonify({'success': False, 'error': 'User not found'})

@app.route('/api/facilities', methods=['GET'])
def get_facilities():
    try:
        conn = get_db()
        facilities = conn.execute('SELECT * FROM facilities').fetchall()
        conn.close()
        
        facilities_list = [dict(facility) for facility in facilities]
        
        return jsonify({
            'success': True,
            'data': facilities_list
        })
    except Exception as e:
        print(f"❌ Facilities endpoint error: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/bookings', methods=['GET'])
def get_bookings():
    print("🔍 BOOKINGS ENDPOINT CALLED!")  # Simple debug test
    user_email = request.args.get('user_email')
    user_role = request.args.get('user_role', 'resident')  # Default to resident for privacy
    exclude_user_role = request.args.get('excludeUserRole', '').lower() == 'true'  # New parameter to exclude user role filtering
    
    conn = get_db()
    cursor = conn.cursor()
    
    try:
        if exclude_user_role:
            # Return ALL bookings without any user role filtering (for official use)
            print("🔍 Returning ALL bookings (excludeUserRole=true)")
            bookings = cursor.execute('''
                SELECT b.id, b.booking_reference, b.user_id, b.facility_id, b.time_slot_id, 
                       b.booking_date, b.start_time, b.end_time, b.duration_hours,
                       b.purpose, b.expected_attendees, b.special_requirements,
                       b.contact_number, b.contact_address, b.base_rate, b.discount_rate,
                       b.discount_amount, b.downpayment_amount, b.total_amount,
                       b.receipt_base64, b.receipt_filename, b.receipt_uploaded_at,
                       b.status, b.priority_level, b.approved_by, b.approved_at,
                       b.rejection_reason, b.is_competitive, b.competing_booking_ids,
                       b.competition_resolved, b.created_at, b.updated_at,
                       f.name as facility_name, u.full_name, u.email as user_email, u.verified, u.discount_rate, u.role as user_role
                FROM bookings b
                LEFT JOIN facilities f ON b.facility_id = f.id
                LEFT JOIN users u ON b.user_id = u.id
                ORDER BY b.booking_date DESC, b.start_time ASC
            ''').fetchall()
            
            # Create dictionary manually with proper column names
            result = []
            column_names = [
                'id', 'booking_reference', 'user_id', 'facility_id', 'time_slot_id',
                'booking_date', 'start_time', 'end_time', 'duration_hours',
                'purpose', 'expected_attendees', 'special_requirements',
                'contact_number', 'contact_address', 'base_rate', 'discount_rate',
                'discount_amount', 'downpayment_amount', 'total_amount',
                'receipt_base64', 'receipt_filename', 'receipt_uploaded_at',
                'status', 'priority_level', 'approved_by', 'approved_at',
                'rejection_reason', 'is_competitive', 'competing_booking_ids',
                'competition_resolved', 'created_at', 'updated_at',
                'facility_name', 'full_name', 'user_email', 'verified', 'discount_rate', 'user_role'
            ]
            
            for booking in bookings:
                booking_dict = {}
                for i, col_name in enumerate(column_names):
                    if i < len(booking):
                        booking_dict[col_name] = booking[i]
                result.append(booking_dict)
        elif user_role == 'resident' and user_email:
            # Residents can see all bookings for calendar (but without sensitive details)
            bookings = cursor.execute('''
                SELECT b.*, f.name as facility_name, u.full_name, u.email as user_email, u.verified, u.discount_rate, u.role as user_role
                FROM bookings b
                LEFT JOIN facilities f ON b.facility_id = f.id
                LEFT JOIN users u ON b.user_id = u.id
                ORDER BY b.booking_date DESC, b.start_time ASC
            ''').fetchall()
            
            # For residents, return only essential booking info (privacy protection)
            result = []
            for booking in bookings:
                booking_dict = dict(booking)
                
                # Debug logging for privacy check
                print(f"🔍 PRIVACY CHECK: booking_email='{booking_dict['user_email']}' vs user_email='{user_email}'")
                
                # Remove sensitive information for residents (but keep email for official detection)
                if booking_dict['user_email'] and user_email and booking_dict['user_email'].lower().strip() != user_email.lower().strip():
                    # Store original email for official detection
                    original_email = booking_dict['user_email']
                    
                    # Remove sensitive details for other users' bookings
                    booking_dict['full_name'] = 'Reserved'
                    booking_dict['user_email'] = 'private'
                    booking_dict['contact_number'] = 'private'
                    booking_dict['contact_address'] = 'private'
                    booking_dict['receipt_base64'] = None
                    booking_dict['purpose'] = 'Private Booking'
                    
                    # Add a flag for official detection (preserves original email logic)
                    booking_dict['is_official_booking'] = (
                        original_email and (
                            'official' in original_email or 
                            'barangay' in original_email or 
                            'admin' in original_email
                        )
                    )
                    
                    print(f"🔍 PRIVACY APPLIED: Masked booking for user {original_email}")
                else:
                    print(f"🔍 PRIVACY NOT APPLIED: User can see full booking details")
                
                result.append(booking_dict)
                
        elif user_role == 'official':
            # Officials can see all bookings
            bookings = cursor.execute('''
                SELECT b.*, f.name as facility_name, u.full_name, u.email as user_email, u.verified, u.discount_rate, u.role as user_role
                FROM bookings b
                LEFT JOIN facilities f ON b.facility_id = f.id
                LEFT JOIN users u ON b.user_id = u.id
                ORDER BY b.booking_date DESC, b.start_time ASC
            ''').fetchall()
            result = [dict(booking) for booking in bookings]
        else:
            result = []
            
        return jsonify({
            'success': True,
            'data': result
        })
            
    except Exception as e:
        print(f"❌ Error in bookings endpoint: {e}")
        return jsonify({'success': False, 'message': 'Error fetching bookings'}), 500
    finally:
        conn.close()

@app.route('/api/bookings/<int:booking_id>/status', methods=['PUT'])
def update_booking_status(booking_id):
    try:
        data = request.get_json()
        new_status = data.get('status')
        rejection_reason = data.get('rejection_reason')
        
        if new_status not in ['pending', 'approved', 'rejected']:
            return jsonify({'success': False, 'message': 'Invalid status'}), 400
        
        conn = get_db()
        cursor = conn.cursor()
        
        # Get the booking details before updating
        cursor.execute('''
            SELECT facility_id, booking_date, start_time, user_id, status 
            FROM bookings WHERE id = ?
        ''', (booking_id,))
        
        booking = cursor.fetchone()
        if not booking:
            conn.close()
            return jsonify({'success': False, 'message': 'Booking not found'}), 404
        
        facility_id, date, timeslot, user_id, current_status = booking
        
        print(f"🔍 DEBUG: Updating booking {booking_id} from {current_status} to {new_status}")
        if rejection_reason:
            print(f"🔍 DEBUG: Rejection reason: {rejection_reason}")
        
        # Update the booking status and rejection reason
        if rejection_reason and new_status == 'rejected':
            cursor.execute('''
                UPDATE bookings 
                SET status = ?, rejection_reason = ?
                WHERE id = ?
            ''', (new_status, rejection_reason, booking_id))
            print(f"🔍 DEBUG: Updated booking {booking_id} with rejection reason")
        else:
            cursor.execute('''
                UPDATE bookings 
                SET status = ?
                WHERE id = ?
            ''', (new_status, booking_id))
            print(f"🔍 DEBUG: Updated booking {booking_id} status only")
        
        # If approving, automatically reject other pending bookings for the same time slot
        if new_status == 'approved' and current_status == 'pending':
            print(f"🏆 Approving booking {booking_id} and rejecting competitors for {facility_id} {date} {timeslot}")
            
            cursor.execute('''
                UPDATE bookings 
                SET status = 'rejected'
                WHERE facility_id = ? AND booking_date = ? AND start_time = ? 
                AND user_id != ? AND status = 'pending'
            ''', (facility_id, date, timeslot, user_id))
            
            rejected_count = cursor.rowcount
            print(f"🚫 Auto-rejected {rejected_count} competing bookings")
        
        conn.commit()
        conn.close()
        
        return jsonify({'success': True, 'message': f'Booking {new_status} successfully'})
        
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/bookings', methods=['POST'])
def create_booking():
    data = request.json
    print(f"🔍 DEBUG: create_booking called with data: {data}")
    print(f"🔍 DEBUG: receipt_base64 in data: {'receipt_base64' in data}")
    if 'receipt_base64' in data:
        print(f"🔍 DEBUG: receipt_base64 length: {len(str(data['receipt_base64']))}")
        print(f"🔍 DEBUG: receipt_base64 starts with data:image: {str(data['receipt_base64']).startswith('data:image')}")
    
    # Validate required fields
    required_fields = ['facility_id', 'user_email', 'date', 'timeslot']
    for field in required_fields:
        if field not in data:
            return jsonify({'success': False, 'message': f'Missing required field: {field}'}), 400
    
    conn = get_db()
    cursor = conn.cursor()
    
    try:
        print(f"🔍 DEBUG: Database path: {Config.DATABASE_PATH}")
        
        # Get user_id from email
        cursor.execute('SELECT id, role FROM users WHERE email = ?', (data['user_email'],))
        user_result = cursor.fetchone()
        
        if not user_result:
            return jsonify({'success': False, 'message': 'User not found'}), 404
        
        user_id = user_result[0]
        user_role = user_result[1]
        print(f"🔍 DEBUG: Found user_id: {user_id}, role: {user_role} for email: {data['user_email']}")
        
        # Check if this is an official booking
        is_official_booking = user_role == 'official'
        print(f"🔍 DEBUG: Is official booking: {is_official_booking}")
        
        # Check if USER already has this exact time slot (prevent duplicate user bookings)
        cursor.execute('''
            SELECT id, user_id, status FROM bookings 
            WHERE facility_id = ? AND booking_date = ? AND start_time = ? AND user_id = ?
        ''', (data['facility_id'], data['date'], data['timeslot'], user_id))
        
        user_existing_booking = cursor.fetchone()
        
        # If user already has this exact time slot, block it
        if user_existing_booking:
            return jsonify({
                'success': False, 
                'message': 'You already have a booking for this time slot. Please choose a different time.',
                'error_type': 'duplicate_user_booking'
            }), 409
        
        # AUTO-REJECTION LOGIC FOR OFFICIAL BOOKINGS
        rejected_resident_bookings = []
        if is_official_booking:
            print(f"🏆 OFFICIAL BOOKING DETECTED - Checking for ALL resident bookings on this date...")
            
            # Find ALL resident pending bookings for this date and facility (not just overlapping time slots)
            cursor.execute('''
                SELECT b.id, b.user_id, b.start_time, b.end_time, b.status, u.email as user_email, u.full_name
                FROM bookings b
                LEFT JOIN users u ON b.user_id = u.id
                WHERE b.facility_id = ? 
                AND b.booking_date = ? 
                AND b.status = 'pending'
                AND (u.role = 'resident' OR u.role = '0' OR u.role IS NULL OR u.role LIKE '0.%')
            ''', (data['facility_id'], data['date']))
            
            overlapping_bookings = cursor.fetchall()
            print(f"🔍 DEBUG: Found {len(overlapping_bookings)} overlapping resident bookings")
            
            # Auto-reject overlapping resident bookings with apology message
            apology_message = """Dear Resident,

We apologize but your booking has been automatically rescheduled due to an official barangay business requirement.

Your payment will be refunded within 3-5 business days.

Thank you for your understanding and cooperation.

Barangay Management"""
            
            for booking in overlapping_bookings:
                # Extract resident booking info
                booking_id = booking[0]
                resident_email = booking[5] if booking[5] else 'Unknown'
                resident_name = booking[6] if booking[6] else 'Resident'
                resident_timeslot = booking[2]  # Use just the start_time (already contains full timeslot)
                
                print(f"🚫 AUTO-REJECTING booking {booking_id} for {resident_name} ({resident_email}) - Time: {resident_timeslot}")
                
                # Update resident booking to rejected with apology
                cursor.execute('''
                    UPDATE bookings 
                    SET status = 'rejected', 
                        rejection_reason = ?,
                        updated_at = CURRENT_TIMESTAMP
                    WHERE id = ?
                ''', (apology_message, booking_id))
                
                rejected_resident_bookings.append({
                    'booking_id': booking_id,
                    'resident_name': resident_name,
                    'resident_email': resident_email,
                    'timeslot': resident_timeslot  # Use resident's actual time slot
                })
            
            if rejected_resident_bookings:
                print(f"✅ Auto-rejected {len(rejected_resident_bookings)} resident bookings")
        
        # Check if user has too many pending bookings (optional limit)
        cursor.execute('''
            SELECT COUNT(*) FROM bookings 
            WHERE user_id = ? AND status = 'pending'
        ''', (user_id,))
        
        pending_count = cursor.fetchone()[0]
        if pending_count >= 5:  # Limit to 5 pending bookings per user
            return jsonify({
                'success': False, 
                'message': 'You have too many pending bookings. Please wait for approval or cancel some bookings.',
                'error_type': 'too_many_pending'
            }), 429
        
        # ALLOW multiple users to book same time slot (competitive booking)
        # No need to check if other users have this slot - that's the point!
        
        # Create booking
        booking_status = 'approved' if is_official_booking else data.get('status', 'pending')
        print(f"🔍 DEBUG: Setting booking status to: {booking_status}")
        
        cursor.execute('''
            INSERT INTO bookings (facility_id, user_id, booking_date, start_time, end_time, status, purpose, total_amount, contact_number, contact_address, booking_reference, time_slot_id, duration_hours, base_rate, downpayment_amount, receipt_base64)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            data['facility_id'],
            user_id,
            data['date'],
            data['timeslot'],  # start_time
            data['timeslot'],  # end_time (same as start for all-day)
            booking_status,
            data.get('purpose', ''),
            data.get('total_amount', 0),
            data.get('contact_number', ''),
            data.get('address', ''),
            f'BR{datetime.now().strftime("%Y%m%d%H%M%S")}{user_id}',  # Generate booking reference
            0,  # Default time_slot_id for all-day bookings
            24.0,  # Duration hours for all-day booking
            0.0,  # Base rate (free for officials)
            0.0,   # Downpayment amount (free for officials)
            data.get('receipt_base64', None)  # Add receipt_base64 field
        ))
        
        booking_id = cursor.lastrowid
        conn.commit()
        
        # Debug: Check if receipt was saved
        if data.get('receipt_base64'):
            print(f"✅ RECEIPT SAVED: receipt_base64 length = {len(str(data['receipt_base64']))} for booking {booking_id}")
        else:
            print(f"⚠️ NO RECEIPT: receipt_base64 is null for booking {booking_id}")
        
        # Prepare response message
        response_message = 'Booking submitted successfully!' if not is_official_booking else 'Official booking created successfully!'
        
        if is_official_booking and rejected_resident_bookings:
            response_message += f' Auto-rejected {len(rejected_resident_bookings)} resident booking(s).'
        
        return jsonify({
            'success': True, 
            'message': response_message,
            'booking_id': booking_id,
            'status': booking_status,
            'rejected_resident_bookings': rejected_resident_bookings,
            'note': 'Multiple users may book the same time slot. First approved booking wins!' if not is_official_booking else 'Official bookings take priority over resident bookings.'
        })
        
    except Exception as e:
        conn.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500
    finally:
        conn.close()

@app.route('/api/available-timeslots', methods=['GET'])
def get_available_timeslots():
    """Get available time slots for a specific facility and date (competitive booking)"""
    facility_id = request.args.get('facility_id')
    date = request.args.get('date')
    user_email = request.args.get('user_email')  # Optional: for user-specific availability
    
    print(f"🔍 DEBUG: Available timeslots request - facility_id: {facility_id}, date: {date}, user_email: {user_email}")
    
    if not facility_id or not date:
        return jsonify({'success': False, 'message': 'facility_id and date are required'}), 400
    
    conn = get_db()
    
    try:
        # Get all time slots from database for this facility
        cursor = conn.cursor()
        cursor.execute('''
            SELECT start_time, end_time FROM time_slots 
            WHERE facility_id = ? 
            ORDER BY sort_order
        ''', (facility_id,))
        
        time_slots_db = cursor.fetchall()
        
        # Convert to format expected by frontend
        all_timeslots = []
        for start_time, end_time in time_slots_db:
            # Just use the format "6:00 AM - 8:00 AM" as is
            timeslot_str = f"{start_time} - {end_time}"
            all_timeslots.append(timeslot_str)
        
        print(f"🔍 DEBUG: Found {len(all_timeslots)} time slots for facility {facility_id}")
        
        # Get all bookings for this facility and date (excluding rejected)
        cursor.execute('''
            SELECT start_time, user_id, status FROM bookings 
            WHERE facility_id = ? AND booking_date = ? AND status != 'rejected'
        ''', (facility_id, date))
        
        all_bookings = cursor.fetchall()
        print(f"🔍 DEBUG: Found {len(all_bookings)} bookings for this facility/date")
        for booking in all_bookings:
            print(f"🔍 DEBUG: Booking - timeslot: {booking[0]}, user: {booking[1]}, status: {booking[2]}")
        
        # Categorize time slots for competitive booking
        available_slots = []
        user_booked_slots = []
        competitive_slots = []  # Slots with multiple bookings
        approved_slots = []      # Slots that are already taken (approved)
        
        for timeslot in all_timeslots:
            bookings_for_slot = [b for b in all_bookings if b[0] == timeslot]
            
            if not bookings_for_slot:
                # No bookings for this slot
                available_slots.append(timeslot)
                print(f"🔍 DEBUG: {timeslot} -> available (no bookings)")
            else:
                # Check if any booking is approved (slot is taken)
                has_approved = any(b[2] == 'approved' for b in bookings_for_slot)
                
                if has_approved:
                    approved_slots.append(timeslot)
                    print(f"🔍 DEBUG: {timeslot} -> approved (has approved booking)")
                elif len(bookings_for_slot) > 1:
                    # Multiple pending bookings - competitive!
                    competitive_slots.append(timeslot)
                    print(f"🔍 DEBUG: {timeslot} -> competitive (multiple pending)")
                else:
                    # Single booking - check if it's the current user
                    if user_email and bookings_for_slot[0][1] == user_email:
                        user_booked_slots.append(timeslot)
                        print(f"🔍 DEBUG: {timeslot} -> user booked (current user)")
                    else:
                        # Another user has this slot (but it's competitive)
                        competitive_slots.append(timeslot)
                        print(f"🔍 DEBUG: {timeslot} -> competitive (other user)")
        
        print(f"🔍 DEBUG: Final counts - available: {len(available_slots)}, user_booked: {len(user_booked_slots)}, competitive: {len(competitive_slots)}, approved: {len(approved_slots)}")
        
        return jsonify({
            'success': True,
            'default_timeslots': all_timeslots,  # Changed from available_timeslots to default_timeslots
            'available_timeslots': available_slots,
            'user_booked_timeslots': user_booked_slots,
            'competitive_timeslots': competitive_slots,  # New: competitive slots
            'approved_timeslots': approved_slots,        # New: already taken slots
            'total_available': len(available_slots),
            'competitive_count': len(competitive_slots),
            'date': date,
            'facility_id': facility_id,
            'note': 'Competitive booking: Multiple users can book same slot. First approved wins!'
        })
        
    except Exception as e:
        print(f"❌ Error in get_available_timeslots: {e}")
        return jsonify({'success': False, 'message': str(e)}), 500
    finally:
        conn.close()

@app.route('/api/auth/logout', methods=['POST'])
def logout():
    try:
        # In a real app, you would invalidate the session/token here
        # For now, just return success
        return jsonify({
            'success': True,
            'message': 'Logged out successfully'
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.json
    
    try:
        conn = get_db()
        user = conn.execute(
            'SELECT * FROM users WHERE email = ?',
            (data['email'],)
        ).fetchone()
        conn.close()
        
        if user:
            # Hash the provided password and compare with stored hash
            import hashlib
            password_hash = hashlib.sha256(data['password'].encode()).hexdigest()
            
            if user[2] == password_hash:  # user[2] is password_hash
                # Generate a simple session token (in production, use JWT)
                import uuid
                session_token = str(uuid.uuid4())
                
                return jsonify({
                    'success': True,
                    'user': {
                        'id': user[0],
                        'email': user[1],
                        'full_name': user[3],
                        'role': user[4],
                        'verified': bool(user[5]),
                        'verification_type': user[6],
                        'discount_rate': user[7],
                        'contact_number': user[8],
                        'address': user[9],
                        'profile_photo_url': user[10],
                        'is_active': user[11],
                        'email_verified': user[12],
                        'last_login': user[13],
                        'created_at': user[14],
                        'updated_at': user[15],
                        'is_authenticated': True
                    },
                    'token': session_token
                })
            else:
                return jsonify({
                    'success': False,
                    'message': 'Invalid credentials'
                }), 401
        else:
            return jsonify({
                'success': False,
                'message': 'Invalid credentials'
            }), 401
    except Exception as e:
        print(f"❌ Login error: {e}")
        return jsonify({
            'success': False,
            'message': f'Login failed: {str(e)}'
        }), 500

@app.route('/api/auth/register', methods=['POST'])
def register():
    data = request.json
    
    conn = get_db()
    cursor = conn.cursor()
    
    try:
        # Check if user already exists
        cursor.execute('SELECT id FROM users WHERE email = ?', (data['email'],))
        existing_user = cursor.fetchone()
        
        if existing_user:
            conn.close()
            return jsonify({
                'success': False,
                'message': 'User with this email already exists'
            }), 400
        
        # Hash the password
        import hashlib
        password_hash = hashlib.sha256(data['password'].encode()).hexdigest()
        
        cursor.execute('''
            INSERT INTO users (email, password_hash, full_name, role)
            VALUES (?, ?, ?, ?)
        ''', (data['email'], password_hash, data['name'], data['role']))
        
        # Get the newly created user
        cursor.execute('SELECT * FROM users WHERE email = ?', (data['email'],))
        user = cursor.fetchone()
        
        conn.commit()
        conn.close()
        
        return jsonify({
            'success': True, 
            'message': 'User registered successfully',
            'user': {
                'id': user[0],
                'email': user[1],
                'full_name': user[3],
                'role': user[4],
                'verified': bool(user[5]),
                'created_at': user[16]
            }
        })
    except Exception as e:
        print(f"❌ Registration error: {e}")
        conn.close()
        return jsonify({
            'success': False,
            'message': f'Registration failed: {str(e)}'
        }), 500
    except sqlite3.IntegrityError:
        conn.close()
        return jsonify({
            'success': False,
            'message': 'Email already exists'
        }), 400

# Add sample data
@app.route('/api/setup-sample-data', methods=['POST'])
def setup_sample_data():
    conn = get_db()
    cursor = conn.cursor()
    
    # Add sample facilities
    facilities = [
        ('Community Hall', 'Spacious hall for events and meetings', 1000.0, '', 0.5, 100, 'Tables, chairs, sound system', '8:00 AM - 10:00 PM'),
        ('Basketball Court', 'Full-size basketball court with lighting', 500.0, '', 0.3, 50, 'Basketball hoops, lighting, scoreboard', '6:00 AM - 10:00 PM'),
        ('Swimming Pool', 'Olympic-size swimming pool with facilities', 1500.0, '', 0.4, 200, 'Showers, lockers, lifeguard on duty', '6:00 AM - 9:00 PM'),
        ('Shooting Range', 'Indoor shooting range with safety equipment', 2000.0, '', 0.5, 30, 'Safety gear, targets, instructor available', '8:00 AM - 6:00 PM')
    ]
    
    cursor.executemany('''
        INSERT OR IGNORE INTO facilities (name, description, hourly_rate, main_photo_url, downpayment_rate, max_capacity, amenities, operating_hours)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', facilities)
    
    # Add sample users
    users = [
        ('resident@barangay.com', 'password123', 'Juan Dela Cruz', 'resident'),
        ('official@barangay.com', 'password123', 'Maria Santos', 'official')
    ]
    
    cursor.executemany('''
        INSERT OR IGNORE INTO users (email, password_hash, full_name, role)
        VALUES (?, ?, ?, ?)
    ''', users)
    
    # Add time slots for each facility
    time_slots = []
    
    # Community Hall (Facility ID 1)
    for hour in range(8, 22):  # 8 AM to 9 PM
        start_time = f"{hour % 12 or 12}:00 {'AM' if hour < 12 else 'PM'}"
        end_time = f"{(hour + 1) % 12 or 12}:00 {'AM' if hour + 1 < 12 else 'PM'}"
        time_slots.append((1, start_time, end_time))
    
    # Basketball Court (Facility ID 2)
    for hour in range(6, 22):  # 6 AM to 9 PM
        start_time = f"{hour % 12 or 12}:00 {'AM' if hour < 12 else 'PM'}"
        end_time = f"{(hour + 1) % 12 or 12}:00 {'AM' if hour + 1 < 12 else 'PM'}"
        time_slots.append((2, start_time, end_time))
    
    # Swimming Pool (Facility ID 3)
    for hour in range(6, 21):  # 6 AM to 8 PM
        start_time = f"{hour % 12 or 12}:00 {'AM' if hour < 12 else 'PM'}"
        end_time = f"{(hour + 1) % 12 or 12}:00 {'AM' if hour + 1 < 12 else 'PM'}"
        time_slots.append((3, start_time, end_time))
    
    # Shooting Range (Facility ID 4)
    for hour in range(8, 18):  # 8 AM to 5 PM
        start_time = f"{hour % 12 or 12}:00 {'AM' if hour < 12 else 'PM'}"
        end_time = f"{(hour + 1) % 12 or 12}:00 {'AM' if hour + 1 < 12 else 'PM'}"
        time_slots.append((4, start_time, end_time))
    
    cursor.executemany('''
        INSERT OR IGNORE INTO time_slots (facility_id, start_time, end_time)
        VALUES (?, ?, ?)
    ''', time_slots)
    
    conn.commit()
    conn.close()
    
    return jsonify({'success': True, 'message': 'Sample data added'})

# Facility Management endpoints
@app.route('/api/facilities', methods=['POST'])
def create_facility():
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data.get('name') or not data.get('price'):
            return jsonify({'success': False, 'message': 'Name and hourly rate are required'})
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Insert new facility
        cursor.execute('''
            INSERT INTO facilities (name, description, hourly_rate, main_photo_url, active, amenities, downpayment_rate, max_capacity)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            data['name'],
            data.get('description', ''),
            float(data['price']),  # Map price to hourly_rate
            data.get('image_url', ''),  # Map image_url to main_photo_url
            data.get('active', True),
            data.get('amenities', ''),
            float(data.get('downpayment', 0)),  # Map downpayment to downpayment_rate
            int(data.get('capacity', 0))  # Map capacity to max_capacity
        ))
        
        facility_id = cursor.lastrowid
        print(f"🔍 Created facility {facility_id}: {data['name']}")
        
        # Generate default time slots for the new facility
        # Default operating hours: 8:00 AM to 9:00 PM (can be customized per facility type)
        operating_hours = data.get('operating_hours', '8:00 AM - 9:00 PM')
        
        # Parse operating hours or use defaults
        start_hour = 8  # Default 8 AM
        end_hour = 21   # Default 9 PM (last slot starts at 8 PM)
        
        # Adjust hours based on facility type if specified
        facility_name = data['name'].lower()
        if 'basketball' in facility_name or 'court' in facility_name:
            start_hour, end_hour = 6, 22  # 6 AM to 9 PM
        elif 'swimming' in facility_name or 'pool' in facility_name:
            start_hour, end_hour = 6, 21  # 6 AM to 8 PM
        elif 'shooting' in facility_name or 'range' in facility_name:
            start_hour, end_hour = 8, 18  # 8 AM to 5 PM
        
        print(f"🔍 Generating time slots for facility {facility_id}: {start_hour}:00 to {end_hour}:00")
        
        # Generate time slots (2-hour slots for better management)
        time_slots = []
        for i, hour in enumerate(range(start_hour, end_hour, 2)):  # Increment by 2 hours
            start_time = f"{hour % 12 or 12}:00 {'AM' if hour < 12 else 'PM'}"
            end_time = f"{(hour + 2) % 12 or 12}:00 {'AM' if hour + 2 < 12 else 'PM'}"
            duration_minutes = 120  # 2 hour slots
            sort_order = i + 1  # Chronological order
            time_slots.append((facility_id, start_time, end_time, duration_minutes, sort_order))
        
        # Insert time slots
        cursor.executemany('''
            INSERT INTO time_slots (facility_id, start_time, end_time, duration_minutes, sort_order)
            VALUES (?, ?, ?, ?, ?)
        ''', time_slots)
        
        print(f"🔍 Created {len(time_slots)} time slots for facility {facility_id}")
        
        conn.commit()
        conn.close()
        
        return jsonify({
            'success': True, 
            'message': 'Facility created successfully with time slots',
            'facility_id': facility_id,
            'time_slots_created': len(time_slots)
        })
        
    except Exception as e:
        print(f"❌ create_facility error: {e}")
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/facilities/<int:facility_id>/regenerate-timeslots', methods=['POST'])
def regenerate_facility_timeslots(facility_id):
    """Regenerate time slots for an existing facility"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Get facility info
        cursor.execute('SELECT name FROM facilities WHERE id = ?', (facility_id,))
        facility = cursor.fetchone()
        
        if not facility:
            return jsonify({'success': False, 'message': 'Facility not found'}), 404
        
        facility_name = facility[0]
        print(f"🔍 Regenerating time slots for facility {facility_id}: {facility_name}")
        
        # Delete existing time slots for this facility
        cursor.execute('DELETE FROM time_slots WHERE facility_id = ?', (facility_id,))
        deleted_count = cursor.rowcount
        print(f"🔍 Deleted {deleted_count} existing time slots")
        
        # Determine operating hours based on facility type
        facility_name_lower = facility_name.lower()
        if 'basketball' in facility_name_lower or 'court' in facility_name_lower:
            start_hour, end_hour = 6, 22  # 6 AM to 9 PM
        elif 'swimming' in facility_name_lower or 'pool' in facility_name_lower:
            start_hour, end_hour = 6, 21  # 6 AM to 8 PM
        elif 'shooting' in facility_name_lower or 'range' in facility_name_lower:
            start_hour, end_hour = 8, 18  # 8 AM to 5 PM
        else:
            start_hour, end_hour = 6, 21  # Default 6 AM to 8 PM
        
        # Generate new time slots (2-hour slots for better management)
        time_slots = []
        for i, hour in enumerate(range(start_hour, end_hour, 2)):  # Increment by 2 hours
            start_time = f"{hour % 12 or 12}:00 {'AM' if hour < 12 else 'PM'}"
            end_time = f"{(hour + 2) % 12 or 12}:00 {'AM' if hour + 2 < 12 else 'PM'}"
            duration_minutes = 120  # 2 hour slots
            sort_order = i + 1  # Chronological order
            time_slots.append((facility_id, start_time, end_time, duration_minutes, sort_order))
        
        # Insert new time slots
        cursor.executemany('''
            INSERT INTO time_slots (facility_id, start_time, end_time, duration_minutes, sort_order)
            VALUES (?, ?, ?, ?, ?)
        ''', time_slots)
        
        print(f"🔍 Created {len(time_slots)} new time slots for facility {facility_id}")
        
        conn.commit()
        conn.close()
        
        return jsonify({
            'success': True,
            'message': f'Time slots regenerated for {facility_name}',
            'time_slots_created': len(time_slots),
            'deleted_slots': deleted_count
        })
        
    except Exception as e:
        print(f"❌ regenerate_timeslots error: {e}")
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/facilities/<int:facility_id>', methods=['PUT'])
def update_facility(facility_id):
    try:
        data = request.get_json()
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Update facility
        cursor.execute('''
            UPDATE facilities 
            SET name = ?, description = ?, hourly_rate = ?, main_photo_url = ?, active = ?, amenities = ?, downpayment_rate = ?, max_capacity = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        ''', (
            data.get('name'),
            data.get('description', ''),
            float(data.get('price', 0)),  # Map price to hourly_rate
            data.get('image_url', ''),  # Map image_url to main_photo_url
            data.get('active', True),
            data.get('amenities', ''),
            float(data.get('downpayment', 0)),  # Map downpayment to downpayment_rate
            int(data.get('capacity', 0)),  # Map capacity to max_capacity
            facility_id
        ))
        
        conn.commit()
        conn.close()
        
        return jsonify({'success': True, 'message': 'Facility updated successfully'})
        
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/facilities/<int:facility_id>', methods=['DELETE'])
def delete_facility(facility_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Delete facility
        cursor.execute('DELETE FROM facilities WHERE id = ?', (facility_id,))
        
        conn.commit()
        conn.close()
        
        return jsonify({'success': True, 'message': 'Facility deleted successfully'})
        
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

# User Profile Management
@app.route('/api/users/<int:user_id>', methods=['GET'])
def get_user_by_id(user_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
        user = cursor.fetchone()
        
        if user:
            return jsonify({
                'success': True,
                'user': {
                    'id': user[0],
                    'email': user[1],
                    'password': user[2],
                    'full_name': user[3],
                    'role': user[4],
                    'created_at': user[5],
                    'contact_number': user[6],
                    'verified': user[7],
                    'discount_rate': user[8],
                    'address': user[9],
                    'profile_photo_url': user[10],
                    'is_authenticated': True
                }
            })
        else:
            return jsonify({'success': False, 'message': 'User not found'}), 404
            
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500
    finally:
        conn.close()

@app.route('/api/users/profile', methods=['PUT'])
def update_user_profile():
    try:
        data = request.get_json()
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE users 
            SET full_name = ?, contact_number = ?, address = ?
            WHERE email = ?
        ''', (
            data.get('full_name', ''),
            data.get('contact_number', ''),
            data.get('address', ''),
            data['email']
        ))
        
        conn.commit()
        conn.close()
        
        return jsonify({'success': True, 'message': 'Profile updated successfully'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/users/profile/<email>', methods=['GET'])
def get_user_profile(email):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, email, full_name, contact_number, address, role, verified, discount_rate, created_at
            FROM users 
            WHERE email = ?
        ''', (email,))
        
        user = cursor.fetchone()
        conn.close()
        
        if user:
            return jsonify({
                'success': True,
                'user': {
                    'id': user[0],
                    'email': user[1],
                    'full_name': user[2],
                    'contact_number': user[3],
                    'address': user[4],
                    'role': user[5],
                    'verified': user[6],
                    'discount_rate': user[7],
                    'created_at': user[8]
                }
            })
        else:
            return jsonify({'success': False, 'message': 'User not found'}), 404
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

# Get officials for customer service
@app.route('/api/officials', methods=['GET'])
def get_officials():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, full_name, contact_number, role, email
            FROM users 
            WHERE role = 'official' AND full_name IS NOT NULL AND full_name != ''
            ORDER BY role, full_name
        ''')
        
        officials = cursor.fetchall()
        conn.close()
        
        officials_list = []
        for official in officials:
            # Convert personal names to positions
            display_name = official[1]  # full_name
            name_lower = official[1].lower()
            email_lower = official[4].lower()
            
            # Check name first
            if 'captain' in name_lower:
                display_name = 'Barangay Captain'
            elif 'secretary' in name_lower:
                display_name = 'Barangay Secretary'
            elif 'treasurer' in name_lower:
                display_name = 'Barangay Treasurer'
            elif 'councilor' in name_lower:
                display_name = 'Barangay Councilor'
            # Then check email as fallback
            elif 'captain' in email_lower:
                display_name = 'Barangay Captain'
            elif 'secretary' in email_lower:
                display_name = 'Barangay Secretary'
            elif 'treasurer' in email_lower:
                display_name = 'Barangay Treasurer'
            elif 'councilor' in email_lower:
                display_name = 'Barangay Councilor'
            
            officials_list.append({
                'id': official[0],
                'full_name': display_name,
                'contact_number': official[2],
                'role': official[3],
                'email': official[4]
            })
        
        # Remove duplicates based on position, preferring .gov emails and then contact numbers
        seen_positions = {}
        unique_officials = []
        for official in officials_list:
            position = official['full_name']
            current_contact = official['contact_number']
            current_email = official['email']
            
            # If we haven't seen this position yet
            if position not in seen_positions:
                seen_positions[position] = official
            else:
                existing = seen_positions[position]
                existing_email = existing['email']
                existing_contact = existing['contact_number']
                
                # Prefer .gov emails over .com emails
                if '.gov' in current_email and '.com' in existing_email:
                    seen_positions[position] = official
                # If both have same email domain, prefer one with contact number
                elif (current_contact is not None and current_contact != '' and 
                      (existing_contact is None or existing_contact == '')):
                    seen_positions[position] = official
        
        # Convert back to list
        unique_officials = list(seen_positions.values())
        
        return jsonify({
            'success': True,
            'data': unique_officials
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

# Verification Requests
@app.route('/api/verification-requests', methods=['GET', 'POST'])
def verification_requests():
    if request.method == 'GET':
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # Get all verification requests (not just pending) for filtering
            cursor.execute('''
                SELECT vr.id, vr.user_id, vr.verification_type, vr.requested_discount_rate, 
                       vr.user_photo_base64, vr.valid_id_base64, vr.status, 
                       vr.residential_address, vr.created_at, vr.updated_at, u.email, u.full_name, u.contact_number
                FROM verification_requests vr
                LEFT JOIN users u ON vr.user_id = u.id
                ORDER BY vr.created_at DESC
            ''')
            
            requests = cursor.fetchall()
            conn.close()
            
            requests_list = []
            for req in requests:
                requests_list.append({
                    'id': req[0],
                    'residentId': req[1],  # user_id from database - frontend expects this
                    'verificationType': req[2],
                    'discountRate': req[3],
                    'userPhotoUrl': req[4],  # user_photo_base64 - frontend expects this
                    'validIdUrl': req[5],    # valid_id_base64 - frontend expects this
                    'status': req[6],
                    'address': req[7],      # residential_address - frontend expects this
                    'submittedAt': req[8],  # created_at - frontend expects this
                    'updatedAt': req[9],     # updated_at
                    'email': req[10],
                    'fullName': req[11],    # from users table
                    'contactNumber': req[12] # from users table
                })
            
            return jsonify({
                'success': True,
                'data': requests_list
            })
            
        except Exception as e:
            print(f"❌ Error fetching verification requests: {e}")
            # Ensure database connection is closed on error
            if 'conn' in locals():
                try:
                    conn.close()
                except:
                    pass
            return jsonify({'success': False, 'message': str(e)}), 500
    
    elif request.method == 'POST':
        conn = None
        try:
            data = request.get_json()
            print(f"🔍 Received verification request data: {data}")
            
            # Validate required fields
            if not data.get('residentId') or not data.get('verificationType'):
                print("❌ Validation failed: Missing residentId or verificationType")
                return jsonify({'success': False, 'message': 'User ID and verification type are required'})
            
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # Insert new verification request
            cursor.execute('''
                INSERT INTO verification_requests 
                (request_reference, user_id, verification_type, requested_discount_rate, user_photo_base64, valid_id_base64, 
                 residential_address, status, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                f"VR-{data.get('residentId')}-{datetime.now().strftime('%Y%m%d%H%M%S')}",  # Generate unique request reference
                data.get('residentId'),  # frontend sends residentId, map to user_id
                data.get('verificationType', ''),
                0.1 if data.get('verificationType') == 'resident' else 0.05,  # Set discount rate based on type
                data.get('userPhotoUrl', ''),  # frontend sends userPhotoUrl, map to user_photo_base64
                data.get('validIdUrl', ''),    # frontend sends validIdUrl, map to valid_id_base64
                data.get('address', ''),       # frontend sends address, map to residential_address
                data.get('status', 'pending'),
                data.get('submittedAt')        # frontend sends submittedAt, map to created_at
            ))
            
            # Also update user's contact number if provided
            if data.get('contactNumber'):
                cursor.execute('''
                    UPDATE users 
                    SET contact_number = ?
                    WHERE id = ?
                ''', (data.get('contactNumber'), data.get('residentId')))
            
            conn.commit()
            conn.close()
            
            print("✅ Verification request created successfully")
            return jsonify({'success': True, 'message': 'Verification request submitted successfully'})
            
        except Exception as e:
            print(f"❌ Error creating verification request: {e}")
            # Ensure database connection is closed on error
            if conn:
                try:
                    conn.close()
                except:
                    pass
            return jsonify({'success': False, 'message': str(e)})

@app.route('/api/verification-requests/<int:request_id>', methods=['PUT'])
def update_verification_request(request_id):
    try:
        data = request.get_json()
        print(f"🔍 Received verification update data: {data}")
        
        if not data.get('status'):
            return jsonify({'success': False, 'message': 'Status is required'})
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Update verification request
        cursor.execute('''
            UPDATE verification_requests 
            SET status = ?, updated_at = ?
            WHERE id = ?
        ''', (
            data.get('status'),
            data.get('updatedAt', datetime.now().isoformat()),
            request_id
        ))
        
        # Also update the user's verification status and discount rate
        if data.get('status') in ['approved', 'rejected']:
            # Get verification request details to determine verification type and photos
            cursor.execute('''
                SELECT verification_type, user_photo_base64 FROM verification_requests WHERE id = ?
            ''', (request_id,))
            verification_request = cursor.fetchone()
            verification_type = verification_request[0] if verification_request else 'resident'
            user_photo_base64 = verification_request[1] if len(verification_request) > 1 else None
            
            # Use provided discount rate or determine from verification type
            if data.get('discountRate') is not None:
                discount_rate = float(data.get('discountRate'))
            else:
                discount_rate = 0.1 if verification_type == 'resident' else 0.05
            
            # Set verified status based on approval and verification type
            if data.get('status') == 'approved':
                # For residents: verified = 1, For non-residents: verified = 2
                is_verified = 1 if verification_type == 'resident' else 2
            else:
                is_verified = 0  # rejected
                discount_rate = 0.0
            
            # Update user verification and discount
            cursor.execute('''
                UPDATE users 
                SET verified = ?, discount_rate = ?, verification_type = ?, updated_at = ?
                WHERE id = (SELECT user_id FROM verification_requests WHERE id = ?)
            ''', (is_verified, discount_rate, verification_type, datetime.now(), request_id))
            
            # Update user profile photo if approved and photo provided
            if data.get('status') == 'approved' and (data.get('profilePhotoUrl') or user_photo_base64):
                profile_photo = data.get('profilePhotoUrl') or user_photo_base64
                cursor.execute('''
                    UPDATE users 
                    SET profile_photo_url = ?
                    WHERE id = (SELECT user_id FROM verification_requests WHERE id = ?)
                ''', (profile_photo, request_id))
                print(f"✅ Updated profile photo for user with verification request ID: {request_id}")
        
        conn.commit()
        conn.close()
        
        print(f"✅ Verification request {request_id} updated successfully")
        return jsonify({'success': True, 'message': 'Verification request updated successfully'})
        
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

if __name__ == '__main__':
    print("🚀 Starting Barangay Reserve Server...")
    print(f"📱 Server will be available at: http://localhost:{Config.PORT}")
    print("🌐 API endpoints:")
    print("   GET    /api/facilities")
    print("   POST   /api/facilities")
    print("   PUT    /api/facilities/<id>")
    print("   DELETE /api/facilities/<id>")
    print("   GET    /api/bookings")
    print("   POST   /api/bookings")
    print("   GET    /api/verification-requests")
    print("   POST   /api/verification-requests")
    print("   PUT    /api/verification-requests/<id>")
    print("   POST   /api/login")
    print("   POST   /api/register")
    print("   PUT    /api/users/profile")
    print("   GET    /api/users/profile/<email>")
    print("   POST   /api/setup-sample-data")
    
    app.run(host=Config.HOST, port=Config.PORT, debug=Config.DEBUG)
