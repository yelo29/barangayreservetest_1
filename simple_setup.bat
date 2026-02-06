@echo off
echo 🔥 Simple Firebase Setup for Barangay Reserve
echo.
echo 📋 Manual Setup Instructions:
echo.
echo 1. Go to Firebase Console: https://console.firebase.google.com/
echo 2. Select your project: barangay-reserve-cloud
echo 3. Go to Firestore Database
echo 4. Create these collections manually:
echo.
echo === FACILITIES COLLECTION ===
echo Document ID: facility_1
echo Fields:
echo   name: "Covered Court"
echo   price: 2000
echo   downpayment: 500
echo   description: "Multi-purpose covered court for sports and events"
echo   capacity: 100
echo   active: true
echo   createdBy: "quhdIp1XlAS2NHzSVoaPgW191N52"
echo   createdAt: "2026-01-31T09:00:00.000Z"
echo.
echo Document ID: facility_2
echo Fields:
echo   name: "Multi-Purpose Hall"
echo   price: 1500
echo   downpayment: 300
echo   description: "Indoor hall for meetings and small events"
echo   capacity: 50
echo   active: true
echo   createdBy: "quhdIp1XlAS2NHzSVoaPgW191N52"
echo   createdAt: "2026-01-31T09:00:00.000Z"
echo.
echo === USERS COLLECTION ===
echo Document ID: quhdIp1XlAS2NHzSVoaPgW191N52
echo Fields:
echo   uid: "quhdIp1XlAS2NHzSVoaPgW191N52"
echo   email: "official@barangay.gov"
echo   role: "official"
echo   fullName: "Barangay Official"
echo   contactNumber: "09876543210"
echo   address: "Barangay Office, City Hall"
echo   verified: true
echo   discountRate: 0
echo   createdAt: "2026-01-31T09:00:00.000Z"
echo   updatedAt: "2026-01-31T09:00:00.000Z"
echo   emailVerified: true
echo   active: true
echo.
echo 🎯 Test Credentials:
echo   Official: official@barangay.gov / official123
echo   Resident: Sign up with any email
echo.
echo 📱 After setup, run: flutter run
echo.
pause
