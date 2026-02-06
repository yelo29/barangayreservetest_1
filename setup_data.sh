#!/bin/bash

# Firebase Initial Data Setup Script
echo "🔥 Setting up Firebase initial data..."

# Set the project
echo "📋 Setting project to barangay-reserve-cloud..."
firebase use barangay-reserve-cloud

# Create Admin User Document
echo "👤 Creating admin user document..."
firebase firestore:doc users/official-001 --create-data '{
  "uid": "official-001",
  "email": "official@barangay.gov",
  "role": "official",
  "fullName": "Barangay Official",
  "contactNumber": "09876543210",
  "address": "Barangay Office",
  "verified": true,
  "discountRate": 0,
  "createdAt": "2026-01-30T23:52:00.000Z",
  "updatedAt": "2026-01-30T23:52:00.000Z"
}'

# Create Facilities
echo "🏢 Creating facilities..."

# Community Garden
firebase firestore:doc facilities/community-garden --create-data '{
  "name": "Community Garden ni Eden",
  "price": 69,
  "downpayment": 34.5,
  "description": "Garden benches, shaded areas, water access",
  "amenities": "Garden nga ni, benches, shades, water",
  "capacity": 69,
  "icon": "park",
  "createdBy": "official-001",
  "createdAt": "2026-01-30T23:52:00.000Z",
  "updatedAt": "2026-01-30T23:52:00.000Z",
  "active": true
}'

# Multi-Purpose Hall
firebase firestore:doc facilities/multi-purpose-hall --create-data '{
  "name": "Multi-Purpose Hall",
  "price": 100,
  "downpayment": 50,
  "description": "Spacious hall for events and meetings",
  "amenities": "Tables, chairs, sound system, air conditioning",
  "capacity": 100,
  "icon": "event_seat",
  "createdBy": "official-001",
  "createdAt": "2026-01-30T23:52:00.000Z",
  "updatedAt": "2026-01-30T23:52:00.000Z",
  "active": true
}'

# Meeting Room
firebase firestore:doc facilities/meeting-room --create-data '{
  "name": "Meeting Room",
  "price": 30,
  "downpayment": 15,
  "description": "Air-conditioned meeting room with projector",
  "amenities": "Projector, whiteboard, air conditioning, tables",
  "capacity": 15,
  "icon": "meeting_room",
  "createdBy": "official-001",
  "createdAt": "2026-01-30T23:52:00.000Z",
  "updatedAt": "2026-01-30T23:52:00.000Z",
  "active": true
}'

# Covered Court
firebase firestore:doc facilities/covered-court --create-data '{
  "name": "Covered Court",
  "price": 75,
  "downpayment": 35,
  "description": "Covered court for various sports activities",
  "amenities": "Volleyball net, badminton setup, lighting",
  "capacity": 50,
  "icon": "sports_volleyball",
  "createdBy": "official-001",
  "createdAt": "2026-01-30T23:52:00.000Z",
  "updatedAt": "2026-01-30T23:52:00.000Z",
  "active": true
}'

# Basketball Court
firebase firestore:doc facilities/basketball-court --create-data '{
  "name": "Basketball Court",
  "price": 50,
  "downpayment": 25,
  "description": "Full-size basketball court with proper lighting",
  "amenities": "Basketball hoops, lighting, benches",
  "capacity": 20,
  "icon": "sports_basketball",
  "createdBy": "official-001",
  "createdAt": "2026-01-30T23:52:00.000Z",
  "updatedAt": "2026-01-30T23:52:00.000Z",
  "active": true
}'

# Create Sample Resident User Document
echo "👤 Creating sample resident user document..."
firebase firestore:doc users/resident-001 --create-data '{
  "uid": "resident-001",
  "email": "leo052904@gmail.com",
  "role": "resident",
  "fullName": "John Leo Lopez",
  "contactNumber": "09656692463",
  "address": "Mountain Ville",
  "verified": false,
  "discountRate": 0,
  "createdAt": "2026-01-30T23:52:00.000Z",
  "updatedAt": "2026-01-30T23:52:00.000Z"
}'

echo "✅ Initial data setup complete!"
echo ""
echo "📱 Test Accounts:"
echo "   Official: official@barangay.gov / official123"
echo "   Resident: leo052904@gmail.com / [create new password in app]"
echo ""
echo "🔍 Next Steps:"
echo "   1. Enable Firebase Authentication in Firebase Console"
echo "   2. Create the official user manually in Firebase Console"
echo "   3. Test the app with these accounts"
echo "   4. Verify all features work correctly"
