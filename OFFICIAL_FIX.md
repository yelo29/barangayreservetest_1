# OFFICIAL ACCOUNT SETUP - URGENT FIX

## 🚨 Problem: Official Account Exists in Auth but Not in Firestore

The official account `official@barangay.gov` was created in Firebase Authentication but lacks a Firestore document, causing the "Full name must be at least 2 characters" error.

## 🔧 Immediate Fix: Create Official Firestore Document

### Step 1: Go to Firebase Console
1. Open: https://console.firebase.google.com/
2. Select project: `barangay-reserve-cloud`
3. Go to **Firestore Database**

### Step 2: Create Official Document
1. Click **"Start collection"** if needed, or go to **users** collection
2. Click **"Add document"**
3. **Document ID:** `quhdIp1XlAS2NHzSVoaPgW191N52` (use the actual UID from logs)
4. **Add these fields:**

```json
{
  "uid": "quhdIp1XlAS2NHzSVoaPgW191N52",
  "email": "official@barangay.gov",
  "role": "official",
  "fullName": "Barangay Official",
  "contactNumber": "09876543210",
  "address": "Barangay Office, Main Building",
  "verified": true,
  "discountRate": 0,
  "createdAt": "2026-01-31T00:00:00.000Z",
  "updatedAt": "2026-01-31T00:00:00.000Z",
  "lastLoginAt": "2026-01-31T00:00:00.000Z",
  "emailVerified": true,
  "active": true
}
```

### Step 3: Verify Fields
- ✅ **uid**: Must match Firebase Auth UID
- ✅ **role**: Must be "official"
- ✅ **fullName**: "Barangay Official"
- ✅ **verified**: true
- ✅ **active**: true

## 🎯 After Fix

The official login should work and you'll see:
```
🔥 Firebase Auth - Sign in successful: quhdIp1XlAS2NHzSVoaPgW191N52
🔥 Firebase Auth - User data loaded: official
```

## 📱 Test Both Accounts

1. **Official**: `official@barangay.gov` / `official123` ✅
2. **Resident**: `leo052904@gmail.com` / `resident123` ✅

**Create the Firestore document NOW to fix the official login!** 🚀
