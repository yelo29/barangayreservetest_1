#!/usr/bin/env python3
"""
Simplified Barangay Reserve Server for testing verification status
"""

from flask import Flask, request, jsonify, g
from flask_cors import CORS
import sqlite3
import json
from datetime import datetime
import os

app = Flask(__name__)
CORS(app, origins=['*'])

# Database configuration
DATABASE_PATH = 'server/barangay.db'

def get_db_connection():
    """Get database connection"""
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        conn.row_factory = sqlite3.Row
        return conn
    except Exception as e:
        print(f"Database connection failed: {e}")
        raise

# Simple token validation (for testing)
def token_required(f):
    def decorated_function(*args, **kwargs):
        # For testing, we'll just set a dummy user
        g.current_user = {'id': 1, 'email': 'test@example.com'}
        return f(*args, **kwargs)
    return decorated_function

@app.route('/api/verification/status', methods=['GET'])
@token_required
def get_verification_status():
    """Check if current user has pending verification request"""
    conn = None
    try:
        # Get current user from token
        current_user = g.current_user
        user_id = current_user['id']
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Check for existing pending verification request
        cursor.execute('''
            SELECT id, verification_type, status, created_at
            FROM verification_requests 
            WHERE user_id = ? AND status = 'pending'
            ORDER BY created_at DESC
            LIMIT 1
        ''', (user_id,))
        
        pending_request = cursor.fetchone()
        conn.close()
        
        if pending_request:
            return jsonify({
                'success': True,
                'hasPendingRequest': True,
                'pendingRequest': {
                    'id': pending_request[0],
                    'verificationType': pending_request[1],
                    'status': pending_request[2],
                    'createdAt': pending_request[3]
                }
            })
        else:
            return jsonify({
                'success': True,
                'hasPendingRequest': False,
                'pendingRequest': None
            })
            
    except Exception as e:
        print(f"Error checking verification status: {e}")
        if conn:
            try:
                conn.close()
            except:
                pass
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/verification-requests', methods=['POST'])
def create_verification_request():
    """Create verification request with duplicate check"""
    conn = None
    try:
        data = request.get_json()
        print(f"Received verification request data: {data}")
        
        if not data.get('residentId') or not data.get('verificationType'):
            return jsonify({'success': False, 'message': 'User ID and verification type are required'})
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Check for existing pending verification request
        cursor.execute('''
            SELECT id, verification_type, created_at
            FROM verification_requests 
            WHERE user_id = ? AND status = 'pending'
            ORDER BY created_at DESC
            LIMIT 1
        ''', (data.get('residentId'),))
        
        existing_pending = cursor.fetchone()
        if existing_pending:
            existing_type = existing_pending[1]
            created_at = existing_pending[2]
            print(f"DUPLICATE VERIFICATION REQUEST: User already has pending request from {created_at}")
            return jsonify({
                'success': False, 
                'message': 'You already have a verification request pending. Please wait for your request to be either Approved or Rejected before you can submit again.',
                'error_type': 'duplicate_request',
                'existingRequest': {
                    'id': existing_pending[0],
                    'verificationType': existing_type,
                    'createdAt': created_at
                }
            }), 409
        
        # Insert new verification request
        cursor.execute('''
            INSERT INTO verification_requests 
            (request_reference, user_id, verification_type, requested_discount_rate, user_photo_base64, valid_id_base64, 
             residential_address, status, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            f"VR-{data.get('residentId')}-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            data.get('residentId'),
            data.get('verificationType', ''),
            0.1 if data.get('verificationType') == 'resident' else 0.05,
            data.get('userPhotoUrl', ''),
            data.get('validIdUrl', ''),
            data.get('address', ''),
            data.get('status', 'pending'),
            data.get('submittedAt')
        ))
        
        conn.commit()
        conn.close()
        
        print("Verification request created successfully")
        return jsonify({'success': True, 'message': 'Verification request submitted successfully'})
        
    except Exception as e:
        print(f"Error creating verification request: {e}")
        if conn:
            try:
                conn.close()
            except:
                pass
        return jsonify({'success': False, 'message': str(e)})

@app.route('/')
def home():
    return jsonify({
        'message': 'Simple Verification Server Running!',
        'status': 'online',
        'timestamp': datetime.now().isoformat()
    })

if __name__ == '__main__':
    print("Starting Simple Verification Server...")
    print("Server will be available at: http://localhost:8000")
    print("API endpoints:")
    print("   GET    /api/verification/status")
    print("   POST   /api/verification-requests")
    
    app.run(host='0.0.0.0', port=8000, debug=True)
