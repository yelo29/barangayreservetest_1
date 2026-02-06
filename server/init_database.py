#!/usr/bin/env python3
"""
Database Initialization Script
Creates the comprehensive database schema
"""

import sqlite3
import json
from datetime import datetime
import hashlib
from config import Config

def init_database():
    conn = sqlite3.connect(Config.DATABASE_PATH)
    cursor = conn.cursor()
    
    print("🔄 Initializing comprehensive database schema...")
    
    # Drop existing tables to start fresh
    tables_to_drop = [
        'user_sessions', 'facility_availability_rules', 'notifications',
        'booking_audit_log', 'barangay_events', 'verification_requests',
        'bookings', 'time_slots', 'facilities', 'users'
    ]
    
    for table in tables_to_drop:
        cursor.execute(f"DROP TABLE IF EXISTS {table}")
        print(f"🗑️  Dropped table: {table}")
    
    # Create USERS table
    print("📝 Creating users table...")
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
    print("🏢 Creating facilities table...")
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
    print("⏰ Creating time_slots table...")
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
    print("📅 Creating bookings table...")
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
    print("👤 Creating verification_requests table...")
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
    print("🎉 Creating barangay_events table...")
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
    
    # Create USER_SESSIONS table
    print("🔐 Creating user_sessions table...")
    cursor.execute('''
        CREATE TABLE user_sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            
            -- Session Information
            session_token VARCHAR(255) UNIQUE NOT NULL,
            device_id VARCHAR(255),
            device_type VARCHAR(20) DEFAULT 'mobile',
            
            -- Session Status
            is_active BOOLEAN DEFAULT TRUE,
            expires_at DATETIME NOT NULL,
            
            -- Location and Security
            ip_address VARCHAR(45),
            user_agent TEXT,
            last_activity DATETIME DEFAULT CURRENT_TIMESTAMP,
            
            -- System Fields
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')
    
    # Create indexes for performance
    print("📊 Creating indexes...")
    indexes = [
        ('idx_users_email', 'users(email)'),
        ('idx_users_role', 'users(role)'),
        ('idx_users_verified', 'users(verified)'),
        ('idx_facilities_active', 'facilities(is_active)'),
        ('idx_facilities_name', 'facilities(name)'),
        ('idx_time_slots_facility', 'time_slots(facility_id, start_time)'),
        ('idx_time_slots_active', 'time_slots(is_active)'),
        ('idx_bookings_user_status', 'bookings(user_id, status)'),
        ('idx_bookings_facility_date', 'bookings(facility_id, booking_date)'),
        ('idx_bookings_date_status', 'bookings(booking_date, status)'),
        ('idx_bookings_reference', 'bookings(booking_reference)'),
        ('idx_bookings_competitive', 'bookings(is_competitive, competition_resolved)'),
        ('idx_verification_user_status', 'verification_requests(user_id, status)'),
        ('idx_verification_status', 'verification_requests(status)'),
        ('idx_events_facility_dates', 'barangay_events(facility_id, start_date, end_date)'),
        ('idx_events_status', 'barangay_events(status)'),
        ('idx_sessions_token', 'user_sessions(session_token)'),
        ('idx_sessions_user_active', 'user_sessions(user_id, is_active)')
    ]
    
    for index_name, index_def in indexes:
        cursor.execute(f'CREATE INDEX {index_name} ON {index_def}')
        print(f"  ✅ Created index: {index_name}")
    
    conn.commit()
    conn.close()
    
    print("✅ Database schema initialized successfully!")
    print(f"📊 Database location: {Config.DATABASE_PATH}")

if __name__ == "__main__":
    init_database()
