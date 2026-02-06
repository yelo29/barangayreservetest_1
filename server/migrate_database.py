#!/usr/bin/env python3
"""
Database Migration Script
Migrate from old schema to new comprehensive schema and populate with sample data
"""

import sqlite3
import json
from datetime import datetime, timedelta
import hashlib
from config import Config

def migrate_and_populate():
    conn = sqlite3.connect(Config.DATABASE_PATH)
    cursor = conn.cursor()
    
    print("🔄 Starting database migration and population...")
    
    # Insert sample users
    print("📝 Creating sample users...")
    users = [
        {
            'email': 'official@barangay.com',
            'password': 'password123',
            'full_name': 'Maria Santos',
            'role': 'official',
            'verified': True,
            'discount_rate': 0.00,
            'contact_number': '09123456789',
            'address': 'Barangay Hall, Main Street'
        },
        {
            'email': 'secretary@barangay.gov',
            'password': 'barangay123',
            'full_name': 'Barangay Secretary',
            'role': 'official',
            'verified': True,
            'discount_rate': 0.00,
            'contact_number': '09123456790',
            'address': 'Barangay Hall, Main Street'
        },
        {
            'email': 'leo052904@gmail.com',
            'password': 'zepol052904',
            'full_name': 'John Leo L. Lopez',
            'role': 'resident',
            'verified': True,
            'verification_type': 'resident',
            'discount_rate': 0.10,
            'contact_number': '09123456791',
            'address': '123 Residential Street'
        },
        {
            'email': 'saloestillopez@gmail.com',
            'password': 'salo3029',
            'full_name': 'Salo E. Lopez',
            'role': 'resident',
            'verified': True,
            'verification_type': 'non-resident',
            'discount_rate': 0.05,
            'contact_number': '09123456792',
            'address': '456 Subdivision Road'
        },
        {
            'email': 'resident@barangay.com',
            'password': 'password123',
            'full_name': 'Juan Dela Cruz',
            'role': 'resident',
            'verified': False,
            'discount_rate': 0.00,
            'contact_number': '09123456793',
            'address': '789 Community Avenue'
        }
    ]
    
    for user in users:
        password_hash = hashlib.sha256(user['password'].encode()).hexdigest()
        cursor.execute('''
            INSERT OR REPLACE INTO users (
                email, password_hash, full_name, role, verified, verification_type,
                discount_rate, contact_number, address, created_at, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            user['email'], password_hash, user['full_name'], user['role'],
            user['verified'], user.get('verification_type'), user['discount_rate'],
            user['contact_number'], user['address'], datetime.now(), datetime.now()
        ))
    
    # Insert sample facilities
    print("🏢 Creating sample facilities...")
    facilities = [
        {
            'name': 'Covered Court',
            'description': 'Covered court for various sports activities',
            'hourly_rate': 75.00,
            'downpayment_rate': 0.50,
            'max_capacity': 50,
            'amenities': ['Volleyball net', 'Badminton setup', 'Lighting', 'Sound system'],
            'operating_hours': {
                'monday': {'open': '08:00', 'close': '21:00'},
                'tuesday': {'open': '08:00', 'close': '21:00'},
                'wednesday': {'open': '08:00', 'close': '21:00'},
                'thursday': {'open': '08:00', 'close': '21:00'},
                'friday': {'open': '08:00', 'close': '21:00'},
                'saturday': {'open': '08:00', 'close': '21:00'},
                'sunday': {'open': '08:00', 'close': '21:00'}
            }
        },
        {
            'name': 'Meeting Room',
            'description': 'Air-conditioned meeting room with projector',
            'hourly_rate': 30.00,
            'downpayment_rate': 0.50,
            'max_capacity': 15,
            'amenities': ['Projector', 'Whiteboard', 'Air conditioning', 'Tables', 'Chairs'],
            'operating_hours': {
                'monday': {'open': '08:00', 'close': '17:00'},
                'tuesday': {'open': '08:00', 'close': '17:00'},
                'wednesday': {'open': '08:00', 'close': '17:00'},
                'thursday': {'open': '08:00', 'close': '17:00'},
                'friday': {'open': '08:00', 'close': '17:00'},
                'saturday': {'open': '09:00', 'close': '12:00'},
                'sunday': {'open': 'closed', 'close': 'closed'}
            }
        },
        {
            'name': 'Multi-Purpose Hall',
            'description': 'Spacious hall for events and meetings',
            'hourly_rate': 100.00,
            'downpayment_rate': 0.50,
            'max_capacity': 100,
            'amenities': ['Tables', 'Chairs', 'Sound system', 'Air conditioning', 'Stage'],
            'operating_hours': {
                'monday': {'open': '08:00', 'close': '22:00'},
                'tuesday': {'open': '08:00', 'close': '22:00'},
                'wednesday': {'open': '08:00', 'close': '22:00'},
                'thursday': {'open': '08:00', 'close': '22:00'},
                'friday': {'open': '08:00', 'close': '22:00'},
                'saturday': {'open': '08:00', 'close': '22:00'},
                'sunday': {'open': '08:00', 'close': '22:00'}
            }
        },
        {
            'name': 'Community Garden',
            'description': 'Outdoor space for community activities',
            'hourly_rate': 25.00,
            'downpayment_rate': 0.35,
            'max_capacity': 30,
            'amenities': ['Garden tools', 'Shed', 'Water source', 'Benches'],
            'operating_hours': {
                'monday': {'open': '06:00', 'close': '18:00'},
                'tuesday': {'open': '06:00', 'close': '18:00'},
                'wednesday': {'open': '06:00', 'close': '18:00'},
                'thursday': {'open': '06:00', 'close': '18:00'},
                'friday': {'open': '06:00', 'close': '18:00'},
                'saturday': {'open': '06:00', 'close': '18:00'},
                'sunday': {'open': '06:00', 'close': '18:00'}
            }
        },
        {
            'name': 'Basketball Court',
            'description': 'Outdoor basketball court with lighting',
            'hourly_rate': 50.00,
            'downpayment_rate': 0.40,
            'max_capacity': 20,
            'amenities': ['Basketball hoops', 'Scoreboard', 'Lighting', 'Benches'],
            'operating_hours': {
                'monday': {'open': '06:00', 'close': '21:00'},
                'tuesday': {'open': '06:00', 'close': '21:00'},
                'wednesday': {'open': '06:00', 'close': '21:00'},
                'thursday': {'open': '06:00', 'close': '21:00'},
                'friday': {'open': '06:00', 'close': '21:00'},
                'saturday': {'open': '06:00', 'close': '21:00'},
                'sunday': {'open': '06:00', 'close': '21:00'}
            }
        }
    ]
    
    for facility in facilities:
        cursor.execute('''
            INSERT INTO facilities (
                name, description, hourly_rate, downpayment_rate, max_capacity,
                amenities, operating_hours, created_at, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            facility['name'], facility['description'], facility['hourly_rate'],
            facility['downpayment_rate'], facility['max_capacity'],
            json.dumps(facility['amenities']), json.dumps(facility['operating_hours']),
            datetime.now(), datetime.now()
        ))
    
    # Create time slots for each facility
    print("⏰ Creating time slots...")
    time_slots_config = {
        'Covered Court': [
            ('08:00', '09:00', 60),
            ('09:00', '10:00', 60),
            ('10:00', '11:00', 60),
            ('11:00', '12:00', 60),
            ('13:00', '14:00', 60),
            ('14:00', '15:00', 60),
            ('15:00', '16:00', 60),
            ('16:00', '17:00', 60),
            ('17:00', '18:00', 60),
            ('18:00', '19:00', 60),
            ('19:00', '20:00', 60),
            ('20:00', '21:00', 60)
        ],
        'Meeting Room': [
            ('08:00', '09:00', 60),
            ('09:00', '10:00', 60),
            ('10:00', '11:00', 60),
            ('11:00', '12:00', 60),
            ('13:00', '14:00', 60),
            ('14:00', '15:00', 60),
            ('15:00', '16:00', 60),
            ('16:00', '17:00', 60)
        ],
        'Multi-Purpose Hall': [
            ('08:00', '10:00', 120),
            ('10:00', '12:00', 120),
            ('13:00', '15:00', 120),
            ('15:00', '17:00', 120),
            ('17:00', '19:00', 120),
            ('19:00', '21:00', 120)
        ],
        'Community Garden': [
            ('06:00', '08:00', 120),
            ('08:00', '10:00', 120),
            ('10:00', '12:00', 120),
            ('14:00', '16:00', 120),
            ('16:00', '18:00', 120)
        ],
        'Basketball Court': [
            ('06:00', '07:00', 60),
            ('07:00', '08:00', 60),
            ('08:00', '09:00', 60),
            ('09:00', '10:00', 60),
            ('10:00', '11:00', 60),
            ('11:00', '12:00', 60),
            ('14:00', '15:00', 60),
            ('15:00', '16:00', 60),
            ('16:00', '17:00', 60),
            ('17:00', '18:00', 60),
            ('18:00', '19:00', 60),
            ('19:00', '20:00', 60),
            ('20:00', '21:00', 60)
        ]
    }
    
    for facility_name, slots in time_slots_config.items():
        facility = cursor.execute('SELECT id FROM facilities WHERE name = ?', (facility_name,)).fetchone()
        if facility:
            facility_id = facility[0]  # Access by index since it's a tuple
            for start_time, end_time, duration in slots:
                cursor.execute('''
                    INSERT INTO time_slots (
                        facility_id, start_time, end_time, duration_minutes, created_at, updated_at
                    ) VALUES (?, ?, ?, ?, ?, ?)
                ''', (facility_id, start_time, end_time, duration, datetime.now(), datetime.now()))
    
    # Create sample verification requests
    print("📋 Creating sample verification requests...")
    verification_requests = [
        {
            'user_email': 'resident@barangay.com',
            'verification_type': 'resident',
            'requested_discount_rate': 0.10,
            'residential_address': '789 Community Avenue',
            'years_of_residence': 5,
            'status': 'pending'
        }
    ]
    
    for req in verification_requests:
        user = cursor.execute('SELECT id FROM users WHERE email = ?', (req['user_email'],)).fetchone()
        if user:
            user_id = user[0]  # Access by index
            # Get next verification request number
            next_id = cursor.execute('SELECT COUNT(*) + 1 FROM verification_requests').fetchone()[0]
            request_reference = f"VRQ-{datetime.now().year}-{next_id:05d}"
            cursor.execute('''
                INSERT INTO verification_requests (
                    request_reference, user_id, verification_type, requested_discount_rate,
                    residential_address, years_of_residence, status, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                request_reference, user_id, req['verification_type'], req['requested_discount_rate'],
                req['residential_address'], req['years_of_residence'], req['status'],
                datetime.now(), datetime.now()
            ))
    
    # Create sample bookings
    print("📅 Creating sample bookings...")
    sample_bookings = [
        {
            'user_email': 'leo052904@gmail.com',
            'facility_name': 'Covered Court',
            'booking_date': (datetime.now() + timedelta(days=2)).strftime('%Y-%m-%d'),
            'time_slot_start': '14:00',
            'purpose': 'Basketball practice',
            'status': 'approved'
        },
        {
            'user_email': 'saloestillopez@gmail.com',
            'facility_name': 'Meeting Room',
            'booking_date': (datetime.now() + timedelta(days=3)).strftime('%Y-%m-%d'),
            'time_slot_start': '10:00',
            'purpose': 'Community meeting',
            'status': 'pending'
        }
    ]
    
    for booking in sample_bookings:
        user = cursor.execute('SELECT id, verified, discount_rate FROM users WHERE email = ?', (booking['user_email'],)).fetchone()
        facility = cursor.execute('SELECT id, hourly_rate, downpayment_rate FROM facilities WHERE name = ?', (booking['facility_name'],)).fetchone()
        time_slot = cursor.execute('''
            SELECT id, end_time, duration_minutes FROM time_slots 
            WHERE facility_id = ? AND start_time = ?
        ''', (facility[0], booking['time_slot_start'])).fetchone()
        
        if user and facility and time_slot:
            # Calculate pricing
            duration_hours = time_slot[2] / 60
            base_rate = facility[1] * duration_hours
            discount_rate = user[1] if user[1] else 0.0
            discount_amount = base_rate * discount_rate
            total_amount = base_rate - discount_amount
            downpayment_amount = total_amount * facility[2]
            
            # Get next booking number
            next_id = cursor.execute('SELECT COUNT(*) + 1 FROM bookings').fetchone()[0]
            booking_reference = f"BRG-{datetime.now().year}-{next_id:05d}"
            
            cursor.execute('''
                INSERT INTO bookings (
                    booking_reference, user_id, facility_id, time_slot_id,
                    booking_date, start_time, end_time, duration_hours,
                    purpose, base_rate, discount_rate, discount_amount,
                    downpayment_amount, total_amount, status, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                booking_reference, user[0], facility[0], time_slot[0],
                booking['booking_date'], booking['time_slot_start'], time_slot[1], duration_hours,
                booking['purpose'], base_rate, discount_rate, discount_amount,
                downpayment_amount, total_amount, booking['status'], datetime.now(), datetime.now()
            ))
    
    conn.commit()
    conn.close()
    
    print("✅ Database migration and population completed successfully!")
    print(f"📊 Database location: {Config.DATABASE_PATH}")
    print("\n📋 Sample accounts created:")
    print("👤 Officials:")
    print("  - official@barangay.com / password123")
    print("  - secretary@barangay.gov / barangay123")
    print("👥 Residents:")
    print("  - leo052904@gmail.com / zepol052904 (verified, 10% discount)")
    print("  - saloestillopez@gmail.com / salo3029 (verified, 5% discount)")
    print("  - resident@barangay.com / password123 (unverified, 0% discount)")

if __name__ == "__main__":
    migrate_and_populate()
