#!/usr/bin/env python3
"""
Barangay Reserve Server
Free, self-hosted solution for students
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import sqlite3
import json
import os
from config import Config
from datetime import datetime
import os

app = Flask(__name__)
# Dynamic CORS configuration for DuckDNS
CORS(app, origins=Config.get_cors_origins())

# Database setup
def init_db():
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
            resident_id INTEGER,
            full_name TEXT,
            contact_number TEXT,
            address TEXT,
            verification_type TEXT,
            user_photo_url TEXT,
            valid_id_url TEXT,
            status TEXT DEFAULT 'pending',
            discount_rate REAL DEFAULT 0.0,
            submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (resident_id) REFERENCES users (id)
        )
    ''')
    
    conn.commit()
    conn.close()

# Initialize database on startup
init_db()

# Helper function to get database connection
def get_db():
    conn = sqlite3.connect('barangay.db')
    conn.row_factory = sqlite3.Row
    return conn

# Helper function to get database connection (alias for get_db)
def get_db_connection():
    return get_db()

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
    
    # Add profile_photo_url column to users table if it doesn't exist
    try:
        cursor.execute('ALTER TABLE users ADD COLUMN profile_photo_url TEXT')
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
    
    cursor.execute('SELECT id, email, password, full_name, role, verified, discount_rate, contact_number, address, profile_photo_url, created_at FROM users WHERE email = ?', (email,))
    user = cursor.fetchone()
    
    conn.close()
    
    if user:
        return jsonify({
            'success': True,
            'user': {
                'id': user[0],
                'email': user[1],
                'full_name': user[3],
                'role': user[4],
                'verified': user[5],
                'discount_rate': user[6],
                'contact_number': user[7],
                'address': user[8],
                'profile_photo_url': user[9],
                'created_at': user[10]
            }
        })
    else:
        return jsonify({'success': False, 'error': 'User not found'})

@app.route('/api/facilities', methods=['GET'])
def get_facilities():
    conn = get_db()
    facilities = conn.execute('SELECT * FROM facilities').fetchall()
    conn.close()
    
    return jsonify([dict(facility) for facility in facilities])

@app.route('/api/bookings', methods=['GET'])
def get_bookings():
    print("🔍 BOOKINGS ENDPOINT CALLED!")  # Simple debug test
    user_email = request.args.get('user_email')
    user_role = request.args.get('user_role', 'resident')  # Default to resident for privacy
    
    conn = get_db()
    cursor = conn.cursor()
    
    try:
        if user_email and user_role == 'resident':
            # Residents can only see their own bookings (privacy protection)
            bookings = cursor.execute('''
                SELECT b.*, f.name as facility_name, u.full_name, u.email as user_email, u.verified, u.discount_rate
                FROM bookings b
                LEFT JOIN facilities f ON b.facility_id = f.id
                LEFT JOIN users u ON b.user_email = u.email
                WHERE b.user_email = ?
                ORDER BY b.date DESC, b.timeslot ASC
            ''', (user_email,)).fetchall()
            
            # For residents, return only essential booking info (privacy protection)
            result = []
            for booking in bookings:
                booking_dict = dict(booking)
                # Remove sensitive information for residents
                if booking_dict['user_email'] != user_email:
                    continue  # Skip if not the user's own booking (extra protection)
                result.append(booking_dict)
            
            return jsonify(result)
            
        elif user_email and user_role == 'official':
            # Officials can see all bookings for management
            bookings = cursor.execute('''
                SELECT b.*, f.name as facility_name, u.full_name, u.email as user_email, u.verified, u.discount_rate
                FROM bookings b
                LEFT JOIN facilities f ON b.facility_id = f.id
                LEFT JOIN users u ON b.user_email = u.email
                ORDER BY b.date DESC, b.timeslot ASC
            ''').fetchall()
            
            return jsonify([dict(booking) for booking in bookings])
            
        else:
            # No user email provided - return limited info for security
            return jsonify({'success': False, 'message': 'User email required for privacy protection'}), 401
            
    except Exception as e:
        print(f"❌ Error in bookings endpoint: {e}")
        return jsonify({'success': False, 'message': 'Error fetching bookings'}), 500
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
    
    conn = get_db()
    user = conn.execute(
        'SELECT * FROM users WHERE email = ? AND password = ?',
        (data['email'], data['password'])
    ).fetchone()
    conn.close()
    
    if user:
        # Generate a simple session token (in production, use JWT)
        import uuid
        session_token = str(uuid.uuid4())
        
        return jsonify({
            'success': True,
            'user': {
                'id': user[0],  # SQLite numeric ID
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
                'is_authenticated': True,
                # Add verification fields for compatibility
                'verificationType': 'resident' if user[7] and user[8] == 0.1 else 'non-resident' if user[7] and user[8] == 0.05 else 'unverified',
                'discount': user[8] if user[8] else 0,
            },
            'token': session_token
        })
    else:
        return jsonify({
            'success': False,
            'message': 'Invalid credentials'
        }), 401

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)