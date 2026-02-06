#!/bin/bash

# Firebase Setup Script for Barangay Reserve
# Run this script to initialize your Firebase database

echo "🔥 Setting up Firebase data for Barangay Reserve..."

# Check if Firebase CLI is installed
if ! command -v firebase &> /dev/null; then
    echo "❌ Firebase CLI not found. Please install it first:"
    echo "npm install -g firebase-tools"
    exit 1
fi

# Deploy Firestore rules
echo "📋 Deploying Firestore security rules..."
firebase deploy --only firestore:rules

# Create initial data using Firebase CLI
echo "🏢 Creating facilities..."

# Facility 1: Covered Court
firebase firestore:create facilities/facility_1 --data '{
  "name": "Covered Court",
  "price": 2000,
  "downpayment": 500,
  "description": "Multi-purpose covered court for sports and events",
  "capacity": 100,
  "active": true,
  "createdBy": "quhdIp1XlAS2NHzSVoaPgW191N52",
  "createdAt": "'$(date -u +%Y-%m-%dT%H:%M:%S.%3NZ)'"
}'

# Facility 2: Multi-Purpose Hall
firebase firestore:create facilities/facility_2 --data '{
  "name": "Multi-Purpose Hall",
  "price": 1500,
  "downpayment": 300,
  "description": "Indoor hall for meetings and small events",
  "capacity": 50,
  "active": true,
  "createdBy": "quhdIp1XlAS2NHzSVoaPgW191N52",
  "createdAt": "'$(date -u +%Y-%m-%dT%H:%M:%S.%3NZ)'"
}'

# Facility 3: Basketball Court
firebase firestore:create facilities/facility_3 --data '{
  "name": "Basketball Court",
  "price": 1000,
  "downpayment": 200,
  "description": "Outdoor basketball court with lighting",
  "capacity": 20,
  "active": true,
  "createdBy": "quhdIp1XlAS2NHzSVoaPgW191N52",
  "createdAt": "'$(date -u +%Y-%m-%dT%H:%M:%S.%3NZ)'"
}'

echo "👤 Creating official user..."

# Create official user document
firebase firestore:create users/quhdIp1XlAS2NHzSVoaPgW191N52 --data '{
  "uid": "quhdIp1XlAS2NHzSVoaPgW191N52",
  "email": "official@barangay.gov",
  "role": "official",
  "fullName": "Barangay Official",
  "contactNumber": "09876543210",
  "address": "Barangay Office, City Hall",
  "verified": true,
  "discountRate": 0,
  "createdAt": "'$(date -u +%Y-%m-%dT%H:%M:%S.%3NZ)'",
  "updatedAt": "'$(date -u +%Y-%m-%dT%H:%M:%S.%3NZ)'",
  "emailVerified": true,
  "active": true
}'

echo "✅ Firebase setup complete!"
echo ""
echo "🎯 Next Steps:"
echo "1. Test official login: official@barangay.gov / official123"
echo "2. Test resident signup with any email"
echo "3. Verify Cloudinary upload preset 'barangay_reserve'"
echo ""
echo "🚀 Your Barangay Reserve app is ready!"
