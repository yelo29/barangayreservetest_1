# 🚀 QUICK FIREBASE SETUP GUIDE

## ✅ Already Done:
- Firebase Authentication (Email/Password & Google) ✅
- Cloud Firestore Database ✅

## 🔧 Next Steps:

### 1. Download Configuration Files
Go to Firebase Console → Project Settings → General

**For Android:**
- Download `google-services.json`
- Place in: `android/app/google-services.json`

**For iOS:**
- Download `GoogleService-Info.plist` 
- Place in: `ios/Runner/GoogleService-Info.plist`

### 2. Deploy Firestore Security Rules
```bash
firebase deploy --only firestore:rules
```

### 3. Create Initial Data

#### Option A: Manual Setup (Recommended)
Create these documents in Firestore Console:

**Users Collection:**
```
Document ID: quhdIp1XlAS2NHzSVoaPgW191N52
Fields:
- uid: "quhdIp1XlAS2NHzSVoaPgW191N52"
- email: "official@barangay.gov"
- role: "official"
- fullName: "Barangay Official"
- contactNumber: "09876543210"
- address: "Barangay Office"
- verified: true
- discountRate: 0
- createdAt: (timestamp)
- updatedAt: (timestamp)
- emailVerified: true
- active: true
```

**Facilities Collection:**
```
Document ID: facility_1
Fields:
- name: "Covered Court"
- price: 2000
- downpayment: 500
- description: "Multi-purpose covered court for sports and events"
- capacity: 100
- active: true
- createdBy: "quhdIp1XlAS2NHzSVoaPgW191N52"
- createdAt: (timestamp)

Document ID: facility_2  
Fields:
- name: "Multi-Purpose Hall"
- price: 1500
- downpayment: 300
- description: "Indoor hall for meetings and small events"
- capacity: 50
- active: true
- createdBy: "quhdIp1XlAS2NHzSVoaPgW191N52"
- createdAt: (timestamp)
```

#### Option B: Use Setup Script
Run this script to auto-create data:
```bash
chmod +x setup_data.sh
./setup_data.sh
```

### 4. Cloudinary Setup
1. Go to https://cloudinary.com/console
2. Create upload preset named: `barangay_reserve`
3. Set as: **Unsigned**
4. Your API key is already configured: `381763147845335`

### 5. Test the App
```bash
flutter run
```

**Login Credentials:**
- **Official**: `official@barangay.gov` / `official123`
- **Resident**: Sign up with any email

## 🎯 Ready to Test!
Once you complete steps 1-3, your app will be fully functional with real Firebase backend!
