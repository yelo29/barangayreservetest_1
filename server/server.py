#!/usr/bin/env python3
"""
Barangay Reserve Server - Fixed version
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
            downpayment REAL DEFAULT 0.0,
            capacity INTEGER DEFAULT 0
        )
    ''')
    
    conn.commit()
    conn.close()

def get_db_connection():
    conn = sqlite3.connect(Config.DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# Essential missing endpoints from original server

@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.json
    
    try:
        conn = get_db_connection()
        user = conn.execute(
            'SELECT id, email, password, full_name, role, verified, verification_type, discount_rate, contact_number, address, profile_photo_url, is_active, email_verified, last_login, created_at, updated_at, fake_booking_violations, is_banned, banned_at, ban_reason FROM users WHERE email = ?',
            (data['email'],)
        ).fetchone()
        
        if user:
            # Check if user is banned before proceeding
            user_dict = {
                'id': user[0],
                'email': user[1],
                'password': user[2],
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
                'fake_booking_violations': user[16] if len(user) > 16 else 0,
                'is_banned': user[17] if len(user) > 17 else False,
                'banned_at': user[18] if len(user) > 18 else None,
                'ban_reason': user[19] if len(user) > 19 else None
            }
            
            if user_dict['is_banned']:
                conn.close()
                return jsonify({
                    'success': False,
                    'message': 'This email has been banned permanently'
                }), 403
            
            # Hash the provided password and compare with stored hash
            import hashlib
            password_hash = hashlib.sha256(data['password'].encode()).hexdigest()
            
            if user_dict['password'] == password_hash:
                # Generate a simple session token (in production, use JWT)
                import uuid
                session_token = str(uuid.uuid4())
                
                # Update last login
                conn.execute(
                    'UPDATE users SET last_login = CURRENT_TIMESTAMP WHERE id = ?',
                    (user_dict['id'],)
                )
                conn.commit()
                conn.close()
                
                return jsonify({
                    'success': True,
                    'user': {
                        'id': user_dict['id'],
                        'email': user_dict['email'],
                        'full_name': user_dict['full_name'],
                        'role': user_dict['role'],
                        'verified': user_dict['verified'],
                        'verification_type': user_dict['verification_type'],
                        'discount_rate': user_dict['discount_rate'],
                        'contact_number': user_dict['contact_number'],
                        'address': user_dict['address'],
                        'profile_photo_url': user_dict['profile_photo_url'],
                        'is_active': user_dict['is_active'],
                        'email_verified': user_dict['email_verified'],
                        'last_login': user_dict['last_login'],
                        'created_at': user_dict['created_at'],
                        'updated_at': user_dict['updated_at'],
                        'fake_booking_violations': user_dict['fake_booking_violations'],
                        'is_banned': user_dict['is_banned'],
                        'is_authenticated': True
                    },
                    'token': session_token
                })
            else:
                conn.close()
                return jsonify({
                    'success': False,
                    'message': 'Invalid credentials'
                }), 401
        else:
            conn.close()
            return jsonify({
                'success': False,
                'message': 'User not found'
            }), 404
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Login failed: {str(e)}'
        }), 500

@app.route('/api/me', methods=['GET'])
def get_current_user():
    # This is a simplified version - in production, you'd validate the JWT token
    # For now, we'll return a mock user or require email parameter
    email = request.args.get('email')
    if not email:
        return jsonify({'success': False, 'error': 'Email parameter required'})
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT id, email, full_name, role, verified, verification_type, discount_rate, contact_number, address, profile_photo_url, is_active, email_verified, last_login, created_at, updated_at, fake_booking_violations, is_banned, banned_at, ban_reason FROM users WHERE email = ?', (email,))
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
                'updated_at': user[14],
                'fake_booking_violations': user[15],
                'is_banned': user[16],
                'banned_at': user[17],
                'ban_reason': user[18],
                'is_authenticated': True
            }
        })
    else:
        return jsonify({'success': False, 'message': 'User not found'}), 404

@app.route('/api/facilities', methods=['GET'])
def get_facilities():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM facilities WHERE active = 1')
        facilities = cursor.fetchall()
        conn.close()
        
        return jsonify({
            'success': True,
            'data': [dict(facility) for facility in facilities]
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/bookings', methods=['GET'])
def get_bookings():
    print("🔍 BOOKINGS ENDPOINT CALLED!")  # Simple debug test
    user_email = request.args.get('user_email')
    facility_id = request.args.get('facility_id')
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        if user_email:
            # Get bookings for specific user
            cursor.execute('''
                SELECT b.*, f.name as facility_name 
                FROM bookings b 
                JOIN facilities f ON b.facility_id = f.id 
                WHERE b.user_email = ?
                ORDER BY b.booking_date DESC, b.time_slot_id ASC
            ''', (user_email,))
        elif facility_id:
            # Get bookings for specific facility
            cursor.execute('''
                SELECT b.*, f.name as facility_name 
                FROM bookings b 
                JOIN facilities f ON b.facility_id = f.id 
                WHERE b.facility_id = ?
                ORDER BY b.booking_date DESC, b.time_slot_id ASC
            ''', (facility_id,))
        else:
            # Get all bookings
            cursor.execute('''
                SELECT b.*, f.name as facility_name 
                FROM bookings b 
                JOIN facilities f ON b.facility_id = f.id 
                ORDER BY b.booking_date DESC, b.time_slot_id ASC
            ''')
        
        bookings = cursor.fetchall()
        conn.close()
        
        return jsonify({
            'success': True,
            'data': [dict(booking) for booking in bookings]
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# Profile endpoint - FIXED VERSION
@app.route('/api/users/profile', methods=['PUT', 'GET'])
def update_user_profile():
    try:
        if request.method == 'GET':
            # Handle GET request for profile retrieval
            email = request.args.get('email')
            if not email:
                return jsonify({'success': False, 'message': 'Email parameter required'}), 400
            
            conn = get_db_connection()
            cursor = conn.cursor()
            
            cursor.execute('SELECT id, email, full_name, role, verified, discount_rate, contact_number, address, created_at, updated_at FROM users WHERE email = ?', (email,))
            user = cursor.fetchone()
            conn.close()
            
            if not user:
                return jsonify({'success': False, 'message': 'User not found'}), 404
            
            # Convert to dictionary with proper keys
            user_data = {
                'id': user[0],
                'fullName': user[2],
                'email': user[1],
                'contactNumber': user[6],
                'address': user[7],
                'isVerified': user[3],
                'verificationStatus': 'verified' if user[3] else 'unverified',
                'createdAt': user[4]
            }
            
            return jsonify({'success': True, 'data': user_data})
        
        elif request.method == 'PUT':
            # Handle PUT request for profile update
            data = request.get_json()
            
            if not data:
                return jsonify({'success': False, 'message': 'No data provided'}), 400
            
            # Get current user data to preserve email
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT email FROM users WHERE id = ?", (data.get('id'),))
            result = cursor.fetchone()
            conn.close()
            
            if not result:
                return jsonify({'success': False, 'message': 'User not found'}), 404
            
            # Update user profile
            cursor.execute("""
                UPDATE users 
                SET full_name = ?, contact_number = ?, address = ?, updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
                """, (
                    data.get('full_name', ''),
                    data.get('contact_number', ''),
                    data.get('address', ''),
                    data.get('id')
                ))
            conn.commit()
            conn.close()
            
            return jsonify({'success': True, 'message': 'Profile updated successfully'})
        
        else:
            return jsonify({'success': False, 'message': 'Method not allowed'}), 405

    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

# Keep all existing endpoints - just add our fixed one
# Copy all other existing routes from the original server.py file
# This ensures we don't break any existing functionality

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=8000)
