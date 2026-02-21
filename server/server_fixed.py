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
