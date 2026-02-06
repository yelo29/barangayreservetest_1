@echo off
echo 🔥 Setting up Firebase data for Barangay Reserve...

REM Create facilities
echo 🏢 Creating facilities...

firebase firestore:delete facilities/facility_1
firebase firestore:delete facilities/facility_2  
firebase firestore:delete facilities/facility_3
firebase firestore:delete users/quhdIp1XlAS2NHzSVoaPgW191N52

echo Creating Covered Court...
curl -X POST "https://firestore.googleapis.com/v1/projects/barangay-reserve-cloud/databases/(default)/documents/facilities" ^
-H "Content-Type: application/json" ^
-d "{
  \"fields\": {
    \"name\": {\"stringValue\": \"Covered Court\"},
    \"price\": {\"integerValue\": 2000},
    \"downpayment\": {\"integerValue\": 500},
    \"description\": {\"stringValue\": \"Multi-purpose covered court for sports and events\"},
    \"capacity\": {\"integerValue\": 100},
    \"active\": {\"booleanValue\": true},
    \"createdBy\": {\"stringValue\": \"quhdIp1XlAS2NHzSVoaPgW191N52\"},
    \"createdAt\": {\"timestampValue\": \"2026-01-31T09:00:00.000Z\"}
  }
}"

echo Creating Multi-Purpose Hall...
curl -X POST "https://firestore.googleapis.com/v1/projects/barangay-reserve-cloud/databases/(default)/documents/facilities" ^
-H "Content-Type: application/json" ^
-d "{
  \"fields\": {
    \"name\": {\"stringValue\": \"Multi-Purpose Hall\"},
    \"price\": {\"integerValue\": 1500},
    \"downpayment\": {\"integerValue\": 300},
    \"description\": {\"stringValue\": \"Indoor hall for meetings and small events\"},
    \"capacity\": {\"integerValue\": 50},
    \"active\": {\"booleanValue\": true},
    \"createdBy\": {\"stringValue\": \"quhdIp1XlAS2NHzSVoaPgW191N52\"},
    \"createdAt\": {\"timestampValue\": \"2026-01-31T09:00:00.000Z\"}
  }
}"

echo Creating Basketball Court...
curl -X POST "https://firestore.googleapis.com/v1/projects/barangay-reserve-cloud/databases/(default)/documents/facilities" ^
-H "Content-Type: application/json" ^
-d "{
  \"fields\": {
    \"name\": {\"stringValue\": \"Basketball Court\"},
    \"price\": {\"integerValue\": 1000},
    \"downpayment\": {\"integerValue\": 200},
    \"description\": {\"stringValue\": \"Outdoor basketball court with lighting\"},
    \"capacity\": {\"integerValue\": 20},
    \"active\": {\"booleanValue\": true},
    \"createdBy\": {\"stringValue\": \"quhdIp1XlAS2NHzSVoaPgW191N52\"},
    \"createdAt\": {\"timestampValue\": \"2026-01-31T09:00:00.000Z\"}
  }
}"

REM Create official user
echo 👤 Creating official user...

curl -X POST "https://firestore.googleapis.com/v1/projects/barangay-reserve-cloud/databases/(default)/documents/users" ^
-H "Content-Type: application/json" ^
-d "{
  \"fields\": {
    \"uid\": {\"stringValue\": \"quhdIp1XlAS2NHzSVoaPgW191N52\"},
    \"email\": {\"stringValue\": \"official@barangay.gov\"},
    \"role\": {\"stringValue\": \"official\"},
    \"fullName\": {\"stringValue\": \"Barangay Official\"},
    \"contactNumber\": {\"stringValue\": \"09876543210\"},
    \"address\": {\"stringValue\": \"Barangay Office, City Hall\"},
    \"verified\": {\"booleanValue\": true},
    \"discountRate\": {\"doubleValue\": 0},
    \"createdAt\": {\"timestampValue\": \"2026-01-31T09:00:00.000Z\"},
    \"updatedAt\": {\"timestampValue\": \"2026-01-31T09:00:00.000Z\"},
    \"emailVerified\": {\"booleanValue\": true},
    \"active\": {\"booleanValue\": true}
  }
}"

echo ✅ Firebase setup complete!
echo 🎯 Test with: official@barangay.gov / official123
echo 📱 Now run: flutter run
pause
