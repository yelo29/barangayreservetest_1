#!/usr/bin/env python3
"""
Barangay Reserve Server - Updated Version
Comprehensive backend for barangay reservation system
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import sqlite3
import json
import os
from datetime import datetime, timedelta
import hashlib
import secrets
from config import Config
from functools import wraps
import re

app = Flask(__name__)
# Dynamic CORS configuration for DuckDNS
CORS(app, origins=Config.get_cors_origins())

# Database setup with comprehensive schema
def init_db():
    conn = sqlite3.connect(Config.DATABASE_PATH)
    cursor = conn.cursor()
    
    # Drop existing tables to start fresh
    cursor.execute("DROP TABLE IF EXISTS user_sessions")
    cursor.execute("DROP TABLE IF EXISTS facility_availability_rules")
    cursor.execute("DROP TABLE IF EXISTS notifications")
    cursor.execute("DROP TABLE IF EXISTS booking_audit_log")
    cursor.execute("DROP TABLE IF EXISTS barangay_events")
    cursor.execute("DROP TABLE IF EXISTS verification_requests")
    cursor.execute("DROP TABLE IF EXISTS bookings")
    cursor.execute("DROP TABLE IF EXISTS time_slots")
    cursor.execute("DROP TABLE IF EXISTS facilities")
    cursor.execute("DROP TABLE IF EXISTS users")
    
    # Create USERS table
    cursor.execute('''
        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email VARCHAR(255) UNIQUE NOT NULL,
            password_hash VARCHAR(255) NOT NULL,
            full_name VARCHAR(255) NOT NULL,
            role VARCHAR(20) DEFAULT 'resident' CHECK (role IN ('resident', 'official')),
            
            -- Verification System
            verified BOOLEAN DEFAULT FALSE,
            verification_type VARCHAR(20) DEFAULT NULL,
            discount_rate DECIMAL(3,2) DEFAULT 0.00,
            
            -- Contact Information
            contact_number VARCHAR(20),
            address TEXT,
            
            -- Profile Management
            profile_photo_url TEXT,
            profile_photo_base64 TEXT,
            
            -- Account Status
            is_active BOOLEAN DEFAULT TRUE,
            email_verified BOOLEAN DEFAULT FALSE,
            last_login DATETIME,
            
            -- System Fields
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            created_by INTEGER
        )
    ''')
    
    # Create FACILITIES table
    cursor.execute('''
        CREATE TABLE facilities (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(255) NOT NULL,
            description TEXT,
            
            -- Pricing Information
            hourly_rate DECIMAL(10,2) NOT NULL,
            downpayment_rate DECIMAL(3,2) DEFAULT 0.50,
            
            -- Capacity and Physical Details
            max_capacity INTEGER,
            floor_area DECIMAL(8,2),
            
            -- Amenities (JSON array)
            amenities TEXT,
            
            -- Media
            main_photo_url TEXT,
            photos TEXT,
            
            -- Status and Availability
            is_active BOOLEAN DEFAULT TRUE,
            requires_approval BOOLEAN DEFAULT TRUE,
            
            -- Time Slot Configuration
            booking_window_days INTEGER DEFAULT 30,
            min_booking_hours INTEGER DEFAULT 1,
            max_booking_hours INTEGER DEFAULT 4,
            
            -- Operating Hours (JSON)
            operating_hours TEXT,
            
            -- System Fields
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            created_by INTEGER
        )
    ''')
    
    # Create TIME_SLOTS table
    cursor.execute('''
        CREATE TABLE time_slots (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            facility_id INTEGER NOT NULL,
            
            -- Time Information
            start_time TIME NOT NULL,
            end_time TIME NOT NULL,
            duration_minutes INTEGER NOT NULL,
            
            -- Slot Configuration
            is_active BOOLEAN DEFAULT TRUE,
            max_concurrent_bookings INTEGER DEFAULT 1,
            
            -- Pricing Variations
            rate_multiplier DECIMAL(3,2) DEFAULT 1.00,
            
            -- System Fields
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            
            FOREIGN KEY (facility_id) REFERENCES facilities(id) ON DELETE CASCADE
        )
    ''')
    
    # Create BOOKINGS table
    cursor.execute('''
        CREATE TABLE bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            booking_reference VARCHAR(20) UNIQUE NOT NULL,
            
            -- User and Facility
            user_id INTEGER NOT NULL,
            facility_id INTEGER NOT NULL,
            time_slot_id INTEGER NOT NULL,
            
            -- Date and Time
            booking_date DATE NOT NULL,
            start_time TIME NOT NULL,
            end_time TIME NOT NULL,
            duration_hours DECIMAL(3,1) NOT NULL,
            
            -- Booking Details
            purpose TEXT NOT NULL,
            expected_attendees INTEGER DEFAULT 1,
            special_requirements TEXT,
            
            -- Contact Information
            contact_number VARCHAR(20),
            contact_address TEXT,
            
            -- Financial Information
            base_rate DECIMAL(10,2) NOT NULL,
            discount_rate DECIMAL(3,2) DEFAULT 0.00,
            discount_amount DECIMAL(10,2) DEFAULT 0.00,
            downpayment_amount DECIMAL(10,2) NOT NULL,
            total_amount DECIMAL(10,2) NOT NULL,
            
            -- Receipt Information
            receipt_base64 TEXT,
            receipt_filename VARCHAR(255),
            receipt_uploaded_at DATETIME,
            
            -- Status Tracking
            status VARCHAR(20) DEFAULT 'pending' CHECK (status IN ('pending', 'approved', 'rejected', 'cancelled', 'completed', 'no_show')),
            priority_level INTEGER DEFAULT 0,
            
            -- Approval Information
            approved_by INTEGER,
            approved_at DATETIME,
            rejection_reason TEXT,
            
            -- Competition Tracking
            is_competitive BOOLEAN DEFAULT FALSE,
            competing_booking_ids TEXT,
            competition_resolved BOOLEAN DEFAULT FALSE,
            
            -- System Fields
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (facility_id) REFERENCES facilities(id),
            FOREIGN KEY (time_slot_id) REFERENCES time_slots(id),
            FOREIGN KEY (approved_by) REFERENCES users(id)
        )
    ''')
    
    # Create VERIFICATION_REQUESTS table
    cursor.execute('''
        CREATE TABLE verification_requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            request_reference VARCHAR(20) UNIQUE NOT NULL,
            
            -- User Information
            user_id INTEGER NOT NULL,
            
            -- Verification Type
            verification_type VARCHAR(20) NOT NULL,
            requested_discount_rate DECIMAL(3,2) NOT NULL,
            
            -- Document Storage (Base64)
            user_photo_base64 TEXT,
            user_photo_filename VARCHAR(255),
            valid_id_base64 TEXT,
            valid_id_filename VARCHAR(255),
            proof_of_residency_base64 TEXT,
            proof_of_residency_filename VARCHAR(255),
            
            -- Additional Documents (JSON)
            additional_documents TEXT,
            
            -- Address Information
            residential_address TEXT,
            years_of_residence INTEGER,
            
            -- Status Tracking
            status VARCHAR(30) DEFAULT 'pending' CHECK (status IN ('pending', 'approved', 'rejected', 'requires_additional_info')),
            
            -- Review Information
            reviewed_by INTEGER,
            reviewed_at DATETIME,
            approval_notes TEXT,
            rejection_reason TEXT,
            
            -- Follow-up Information
            additional_info_requested TEXT,
            additional_info_provided TEXT,
            
            -- System Fields
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (reviewed_by) REFERENCES users(id)
        )
    ''')
    
    # Create BARANGAY_EVENTS table
    cursor.execute('''
        CREATE TABLE barangay_events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            event_reference VARCHAR(20) UNIQUE NOT NULL,
            
            -- Event Details
            title VARCHAR(255) NOT NULL,
            description TEXT,
            event_type VARCHAR(20) DEFAULT 'other',
            
            -- Scheduling
            facility_id INTEGER NOT NULL,
            start_date DATE NOT NULL,
            end_date DATE NOT NULL,
            start_time TIME NOT NULL,
            end_time TIME NOT NULL,
            
            -- Event Configuration
            is_recurring BOOLEAN DEFAULT FALSE,
            recurring_pattern TEXT,
            
            -- Capacity and Access
            max_attendees INTEGER,
            is_public BOOLEAN DEFAULT TRUE,
            requires_registration BOOLEAN DEFAULT FALSE,
            
            -- Event Management
            organizer_id INTEGER NOT NULL,
            status VARCHAR(20) DEFAULT 'scheduled',
            
            -- Media and Resources
            event_photo_url TEXT,
            event_documents TEXT,
            
            -- System Fields
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            
            FOREIGN KEY (facility_id) REFERENCES facilities(id),
            FOREIGN KEY (organizer_id) REFERENCES users(id)
        )
    ''')
    
    # Create indexes for performance
    cursor.execute('CREATE INDEX idx_users_email ON users(email)')
    cursor.execute('CREATE INDEX idx_users_role ON users(role)')
    cursor.execute('CREATE INDEX idx_users_verified ON users(verified)')
    
    cursor.execute('CREATE INDEX idx_facilities_active ON facilities(is_active)')
    cursor.execute('CREATE INDEX idx_facilities_name ON facilities(name)')
    
    cursor.execute('CREATE INDEX idx_time_slots_facility ON time_slots(facility_id, start_time)')
    cursor.execute('CREATE INDEX idx_time_slots_active ON time_slots(is_active)')
    
    cursor.execute('CREATE INDEX idx_bookings_user_status ON bookings(user_id, status)')
    cursor.execute('CREATE INDEX idx_bookings_facility_date ON bookings(facility_id, booking_date)')
    cursor.execute('CREATE INDEX idx_bookings_date_status ON bookings(booking_date, status)')
    cursor.execute('CREATE INDEX idx_bookings_reference ON bookings(booking_reference)')
    cursor.execute('CREATE INDEX idx_bookings_competitive ON bookings(is_competitive, competition_resolved)')
    
    cursor.execute('CREATE INDEX idx_verification_user_status ON verification_requests(user_id, status)')
    cursor.execute('CREATE INDEX idx_verification_status ON verification_requests(status)')
    
    cursor.execute('CREATE INDEX idx_events_facility_dates ON barangay_events(facility_id, start_date, end_date)')
    cursor.execute('CREATE INDEX idx_events_status ON barangay_events(status)')
    
    conn.commit()
    conn.close()
    print("✅ Database initialized with comprehensive schema")

# Initialize database on startup
init_db()

# Helper function to get database connection
def get_db():
    conn = sqlite3.connect(Config.DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# Helper function to generate booking reference
def generate_booking_reference():
    year = datetime.now().year
    count = get_db().execute("SELECT COUNT(*) FROM bookings WHERE created_at >= ?", 
                           (f"{year}-01-01",)).fetchone()[0] + 1
    return f"BRG-{year}-{count:05d}"

# Helper function to generate verification reference
def generate_verification_reference():
    year = datetime.now().year
    count = get_db().execute("SELECT COUNT(*) FROM verification_requests WHERE created_at >= ?", 
                           (f"{year}-01-01",)).fetchone()[0] + 1
    return f"VRQ-{year}-{count:05d}"

# Helper function to generate event reference
def generate_event_reference():
    year = datetime.now().year
    count = get_db().execute("SELECT COUNT(*) FROM barangay_events WHERE created_at >= ?", 
                           (f"{year}-01-01",)).fetchone()[0] + 1
    return f"EVT-{year}-{count:05d}"

# JWT-like token generation (simplified)
def generate_token(user_id, email, role):
    payload = {
        'uid': str(user_id),
        'email': email,
        'role': role,
        'iat': int(datetime.now().timestamp()),
        'exp': int((datetime.now() + timedelta(days=7)).timestamp())
    }
    # Simple token encoding (in production, use proper JWT)
    token = secrets.token_urlsafe(32)
    
    # Store session
    conn = get_db()
    conn.execute('''
        INSERT INTO user_sessions (user_id, session_token, expires_at)
        VALUES (?, ?, ?)
    ''', (user_id, token, datetime.now() + timedelta(days=7)))
    conn.commit()
    conn.close()
    
    return token

# Authentication decorator
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'error': 'Token is missing'}), 401
        
        if token.startswith('Bearer '):
            token = token[7:]
        
        conn = get_db()
        session = conn.execute('''
            SELECT s.user_id, u.email, u.role 
            FROM user_sessions s
            JOIN users u ON s.user_id = u.id
            WHERE s.session_token = ? AND s.is_active = TRUE AND s.expires_at > ?
        ''', (token, datetime.now())).fetchone()
        conn.close()
        
        if not session:
            return jsonify({'error': 'Invalid token'}), 401
        
        request.current_user = dict(session)
        return f(*args, **kwargs)
    return decorated

# Password hashing
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# API Routes

@app.route('/api/auth/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        
        if not email or not password:
            return jsonify({'error': 'Email and password required'}), 400
        
        conn = get_db()
        user = conn.execute('''
            SELECT id, email, password_hash, full_name, role, verified, discount_rate,
                   contact_number, address, profile_photo_url
            FROM users WHERE email = ? AND is_active = TRUE
        ''', (email,)).fetchone()
        
        if not user or user['password_hash'] != hash_password(password):
            conn.close()
            return jsonify({'error': 'Invalid credentials'}), 401
        
        # Update last login
        conn.execute('UPDATE users SET last_login = ? WHERE id = ?', 
                    (datetime.now(), user['id']))
        conn.commit()
        
        # Generate token
        token = generate_token(user['id'], user['email'], user['role'])
        
        user_data = {
            'id': user['id'],
            'email': user['email'],
            'full_name': user['full_name'],
            'role': user['role'],
            'verified': bool(user['verified']),
            'discount_rate': user['discount_rate'],
            'contact_number': user['contact_number'] or '',
            'address': user['address'] or '',
            'profile_photo_url': user['profile_photo_url'] or '',
            'is_authenticated': True
        }
        
        conn.close()
        
        return jsonify({
            'success': True,
            'message': 'Login successful',
            'user': user_data,
            'token': token
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/me', methods=['GET'])
@token_required
def get_current_user():
    try:
        user_id = request.current_user['user_id']
        conn = get_db()
        user = conn.execute('''
            SELECT id, email, full_name, role, verified, discount_rate,
                   contact_number, address, profile_photo_url, created_at
            FROM users WHERE id = ?
        ''', (user_id,)).fetchone()
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        user_data = dict(user)
        user_data['verified'] = bool(user_data['verified'])
        
        conn.close()
        return jsonify({
            'success': True,
            'user': user_data
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/facilities', methods=['GET'])
def get_facilities():
    try:
        conn = get_db()
        facilities = conn.execute('''
            SELECT id, name, description, hourly_rate, downpayment_rate, max_capacity,
                   amenities, main_photo_url, photos, is_active, requires_approval,
                   booking_window_days, min_booking_hours, max_booking_hours,
                   operating_hours, created_at, updated_at
            FROM facilities 
            WHERE is_active = TRUE
            ORDER BY name
        ''').fetchall()
        
        result = []
        for facility in facilities:
            fac_data = dict(facility)
            # Parse JSON fields
            if fac_data['amenities']:
                try:
                    fac_data['amenities'] = json.loads(fac_data['amenities'])
                except:
                    fac_data['amenities'] = []
            else:
                fac_data['amenities'] = []
            
            if fac_data['photos']:
                try:
                    fac_data['photos'] = json.loads(fac_data['photos'])
                except:
                    fac_data['photos'] = []
            else:
                fac_data['photos'] = []
            
            if fac_data['operating_hours']:
                try:
                    fac_data['operating_hours'] = json.loads(fac_data['operating_hours'])
                except:
                    fac_data['operating_hours'] = {}
            else:
                fac_data['operating_hours'] = {}
            
            # Convert boolean fields
            fac_data['is_active'] = bool(fac_data['is_active'])
            fac_data['requires_approval'] = bool(fac_data['requires_approval'])
            
            result.append(fac_data)
        
        conn.close()
        return jsonify({
            'success': True,
            'data': result
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/bookings', methods=['GET'])
@token_required
def get_bookings():
    try:
        user_id = request.current_user['user_id']
        user_role = request.current_user['role']
        user_email = request.current_user['email']
        
        # Get query parameters
        facility_id = request.args.get('facility_id')
        date = request.args.get('date')
        status = request.args.get('status')
        
        conn = get_db()
        
        if user_role == 'official':
            # Officials can see all bookings
            query = '''
                SELECT b.*, u.email as user_email, u.full_name as user_name,
                       f.name as facility_name
                FROM bookings b
                JOIN users u ON b.user_id = u.id
                JOIN facilities f ON b.facility_id = f.id
                WHERE 1=1
            '''
            params = []
        else:
            # Residents can only see their own bookings
            query = '''
                SELECT b.*, u.email as user_email, u.full_name as user_name,
                       f.name as facility_name
                FROM bookings b
                JOIN users u ON b.user_id = u.id
                JOIN facilities f ON b.facility_id = f.id
                WHERE b.user_id = ?
            '''
            params = [user_id]
        
        # Add filters
        if facility_id:
            query += ' AND b.facility_id = ?'
            params.append(facility_id)
        
        if date:
            query += ' AND b.booking_date = ?'
            params.append(date)
        
        if status:
            query += ' AND b.status = ?'
            params.append(status)
        
        query += ' ORDER BY b.created_at DESC'
        
        bookings = conn.execute(query, params).fetchall()
        
        result = []
        for booking in bookings:
            booking_data = dict(booking)
            # Parse JSON fields
            if booking_data['competing_booking_ids']:
                try:
                    booking_data['competing_booking_ids'] = json.loads(booking_data['competing_booking_ids'])
                except:
                    booking_data['competing_booking_ids'] = []
            else:
                booking_data['competing_booking_ids'] = []
            
            # Convert boolean fields
            booking_data['is_competitive'] = bool(booking_data['is_competitive'])
            booking_data['competition_resolved'] = bool(booking_data['competition_resolved'])
            
            result.append(booking_data)
        
        conn.close()
        return jsonify({
            'success': True,
            'data': result
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/bookings', methods=['POST'])
@token_required
def create_booking():
    try:
        user_id = request.current_user['user_id']
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['facility_id', 'booking_date', 'time_slot_id', 'purpose']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'{field} is required'}), 400
        
        conn = get_db()
        
        # Get facility and time slot info
        facility = conn.execute('''
            SELECT hourly_rate, downpayment_rate, requires_approval
            FROM facilities WHERE id = ? AND is_active = TRUE
        ''', (data['facility_id'],)).fetchone()
        
        if not facility:
            return jsonify({'error': 'Facility not found'}), 404
        
        time_slot = conn.execute('''
            SELECT start_time, end_time, duration_minutes
            FROM time_slots WHERE id = ? AND facility_id = ? AND is_active = TRUE
        ''', (data['time_slot_id'], data['facility_id'])).fetchone()
        
        if not time_slot:
            return jsonify({'error': 'Time slot not found'}), 404
        
        # Get user info for discount
        user = conn.execute('''
            SELECT verified, discount_rate FROM users WHERE id = ?
        ''', (user_id,)).fetchone()
        
        # Calculate pricing
        base_rate = facility['hourly_rate']
        duration_hours = time_slot['duration_minutes'] / 60
        total_base = base_rate * duration_hours
        
        discount_rate = user['discount_rate'] if user['verified'] else 0.0
        discount_amount = total_base * discount_rate
        total_amount = total_base - discount_amount
        downpayment_amount = total_amount * facility['downpayment_rate']
        
        # Check for competitive bookings
        existing_bookings = conn.execute('''
            SELECT id, user_id, status
            FROM bookings 
            WHERE facility_id = ? AND booking_date = ? AND time_slot_id = ?
            AND status IN ('pending', 'approved')
        ''', (data['facility_id'], data['booking_date'], data['time_slot_id'])).fetchall()
        
        is_competitive = len(existing_bookings) > 0
        competing_ids = [str(b['id']) for b in existing_bookings if b['id'] != user_id]
        
        # Create booking
        booking_reference = generate_booking_reference()
        
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO bookings (
                booking_reference, user_id, facility_id, time_slot_id,
                booking_date, start_time, end_time, duration_hours,
                purpose, expected_attendees, special_requirements,
                contact_number, contact_address,
                base_rate, discount_rate, discount_amount,
                downpayment_amount, total_amount,
                receipt_base64, receipt_filename, receipt_uploaded_at,
                status, is_competitive, competing_booking_ids
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            booking_reference, user_id, data['facility_id'], data['time_slot_id'],
            data['booking_date'], time_slot['start_time'], time_slot['end_time'], duration_hours,
            data['purpose'], data.get('expected_attendees', 1), data.get('special_requirements'),
            data.get('contact_number'), data.get('contact_address'),
            base_rate, discount_rate, discount_amount,
            downpayment_amount, total_amount,
            data.get('receipt_base64'), data.get('receipt_filename'), 
            datetime.now() if data.get('receipt_base64') else None,
            'pending', is_competitive, json.dumps(competing_ids) if competing_ids else None
        ))
        
        booking_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return jsonify({
            'success': True,
            'message': 'Booking created successfully',
            'booking_id': booking_id,
            'booking_reference': booking_reference,
            'is_competitive': is_competitive
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/verification-requests', methods=['GET'])
@token_required
def get_verification_requests():
    try:
        user_role = request.current_user['role']
        
        if user_role != 'official':
            return jsonify({'error': 'Access denied'}), 403
        
        conn = get_db()
        requests = conn.execute('''
            SELECT vr.*, u.email as user_email, u.full_name as user_name
            FROM verification_requests vr
            JOIN users u ON vr.user_id = u.id
            ORDER BY vr.created_at DESC
        ''').fetchall()
        
        result = []
        for req in requests:
            req_data = dict(req)
            # Parse JSON fields
            if req_data['additional_documents']:
                try:
                    req_data['additional_documents'] = json.loads(req_data['additional_documents'])
                except:
                    req_data['additional_documents'] = {}
            else:
                req_data['additional_documents'] = {}
            
            result.append(req_data)
        
        conn.close()
        return jsonify({
            'success': True,
            'data': result
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Health check endpoint
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '2.0.0'
    })

if __name__ == '__main__':
    print("🚀 Starting Barangay Reserve Server v2.0.0")
    print(f"📊 Database: {Config.DATABASE_PATH}")
    print(f"🌐 Server: http://{Config.HOST}:{Config.PORT}")
    app.run(host=Config.HOST, port=Config.PORT, debug=Config.DEBUG)
