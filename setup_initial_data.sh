#!/bin/bash

# Firebase Initial Data Setup Script
# Run this script to set up initial data for Barangay Reserve

echo "🔥 Setting up Firebase initial data..."

# Create Admin User
echo "📝 Creating admin user..."
firebase auth:import users.json --project barangay-reserve-cloud

# Create Facilities
echo "🏢 Creating facilities..."

# Community Garden
firebase firestore:doc barangay-reserve-cloud/facilities/community-garden --create-json '{
  "name": "Community Garden ni Eden",
  "price": 69,
  "downpayment": 34.5,
  "description": "Garden benches, shaded areas, water access",
  "amenities": "Garden nga ni, benches, shades, water",
  "capacity": 69,
  "icon": "park",
  "createdBy": "official-001",
  "createdAt": "'$(date -u +%Y-%m-%dT%H:%M:%S.%3NZ)'",
  "updatedAt": "'$(date -u +%Y-%m-%dT%H:%M:%S.%3NZ)'",
  "active": true
}'

# Multi-Purpose Hall
firebase firestore:doc barangay-reserve-cloud/facilities/multi-purpose-hall --create-json '{
  "name": "Multi-Purpose Hall",
  "price": 100,
  "downpayment": 50,
  "description": "Spacious hall for events and meetings",
  "amenities": "Tables, chairs, sound system, air conditioning",
  "capacity": 100,
  "icon": "event_seat",
  "createdBy": "official-001",
  "createdAt": "'$(date -u +%Y-%m-%dT%H:%M:%S.%3NZ)'",
  "updatedAt": "'$(date -u +%Y-%m-%dT%H:%M:%S.%3NZ)'",
  "active": true
}'

# Meeting Room
firebase firestore:doc barangay-reserve-cloud/facilities/meeting-room --create-json '{
  "name": "Meeting Room",
  "price": 30,
  "downpayment": 15,
  "description": "Air-conditioned meeting room with projector",
  "amenities": "Projector, whiteboard, air conditioning, tables",
  "capacity": 15,
  "icon": "meeting_room",
  "createdBy": "official-001",
  "createdAt": "'$(date -u +%Y-%m-%dT%H:%M:%S.%3NZ)'",
  "updatedAt": "'$(date -u +%Y-%m-%dT%H:%M:%S.%3NZ)'",
  "active": true
}'

# Covered Court
firebase firestore:doc barangay-reserve-cloud/facilities/covered-court --create-json '{
  "name": "Covered Court",
  "price": 75,
  "downpayment": 35,
  "description": "Covered court for various sports activities",
  "amenities": "Volleyball net, badminton setup, lighting",
  "capacity": 50,
  "icon": "sports_volleyball",
  "createdBy": "official-001",
  "createdAt": "'$(date -u +%Y-%m-%dT%H:%M:%S.%3NZ)'",
  "updatedAt": "'$(date -u +%Y-%m-%dT%H:%M:%S.%3NZ)'",
  "active": true
}'

# Basketball Court
firebase firestore:doc barangay-reserve-cloud/facilities/basketball-court --create-json '{
  "name": "Basketball Court",
  "price": 50,
  "downpayment": 25,
  "description": "Full-size basketball court with proper lighting",
  "amenities": "Basketball hoops, lighting, benches",
  "capacity": 20,
  "icon": "sports_basketball",
  "createdBy": "official-001",
  "createdAt": "'$(date -u +%Y-%m-%dT%H:%M:%S.%3NZ)'",
  "updatedAt": "'$(date -u +%Y-%m-%dT%H:%M:%S.%3NZ)'",
  "active": true
}'

# Create Admin User Document
echo "👤 Creating admin user document..."
firebase firestore:doc barangay-reserve-cloud/users/official-001 --create-json '{
  "uid": "official-001",
  "email": "official@barangay.gov",
  "role": "official",
  "fullName": "Barangay Official",
  "contactNumber": "09876543210",
  "address": "Barangay Office",
  "verified": true,
  "discountRate": 0,
  "createdAt": "'$(date -u +%Y-%m-%dT%H:%M:%S.%3NZ)'",
  "updatedAt": "'$(date -u +%Y-%m-%dT%H:%M:%S.%3NZ)'"
}'

# Create Sample Resident User Document
echo "👤 Creating sample resident user..."
firebase firestore:doc barangay-reserve-cloud/users/resident-001 --create-json '{
  "uid": "resident-001",
  "email": "leo052904@gmail.com",
  "role": "resident",
  "fullName": "John Leo Lopez",
  "contactNumber": "09656692463",
  "address": "Mountain Ville",
  "verified": false,
  "discountRate": 0,
  "createdAt": "'$(date -u +%Y-%m-%dT%H:%M:%S.%3NZ)'",
  "updatedAt": "'$(date -u +%Y-%m-%dT%H:%M:%S.%3NZ)'"
}'

# Create Indexes
echo "📊 Creating database indexes..."

# Bookings collection index
firebase firestore:indexes create barangay-reserve-cloud --collection-group bookings \
  --query-field "facilityId"=ASC \
  --query-field "date"=ASC \
  --query-field "status"=ASC

# User bookings index
firebase firestore:indexes create barangay-reserve-cloud --collection-group bookings \
  --query-field "residentId"=ASC \
  --query-field "status"=ASC \
  --query-field "createdAt"=DESC

# Verification requests index
firebase firestore:indexes create barangay-reserve-cloud --collection-group verificationRequests \
  --query-field "status"=ASC \
  --query-field "submittedAt"=DESC

echo "✅ Initial data setup complete!"
echo ""
echo "📱 Test Accounts:"
echo "   Official: official@barangay.gov / official123"
echo "   Resident: leo052904@gmail.com / [create new password]"
echo ""
echo "🔍 Next Steps:"
echo "   1. Test the app with these accounts"
echo "   2. Verify all features work correctly"
echo "   3. Check calendar colors and booking flows"
