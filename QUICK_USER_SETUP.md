# Quick Firebase User Setup

## 🚨 IMPORTANT: Only Official Needs Manual Creation!

Residents can sign up directly through the app. Only the official user needs manual creation.

## 🔧 Step 1: Create Official User (Manual)

### Firebase Console Setup:
1. Go to Firebase Console: https://console.firebase.google.com/
2. Select project: `barangay-reserve-cloud`
3. Go to **Authentication** → **Users**
4. Click **"Add user"**

### Create Official User:
- **Email:** `official@barangay.gov`
- **Password:** `official123`
- **Display Name:** `Barangay Official`

## 🔧 Step 2: Create Official Firestore Document

1. Go to Firebase Console → Firestore Database
2. Create document in **users** collection:
3. **Document ID:** `official-001`

```json
{
  "uid": "official-001",
  "email": "official@barangay.gov", 
  "role": "official",
  "fullName": "Barangay Official",
  "contactNumber": "09876543210",
  "address": "Barangay Office",
  "verified": true,
  "discountRate": 0,
  "createdAt": "2026-01-31T00:00:00.000Z",
  "updatedAt": "2026-01-31T00:00:00.000Z"
}
```

## 🔧 Step 3: Residents Sign Up Through App

Residents can register directly:
1. Open the app
2. Go to **Resident Login**
3. Click **"Don't have an account? Sign up"**
4. Fill in the registration form:
   - Email: `leo052904@gmail.com`
   - Password: `resident123`
   - Full Name: `John Leo Lopez`
   - Contact: `09656692463`
   - Address: `Mountain Ville`

The app will automatically:
- Create Firebase Auth user
- Create Firestore document
- Set role as 'resident'

## 📱 Test Accounts:

### Official (Manual Setup Required):
- **Email:** `official@barangay.gov`
- **Password:** `official123`

### Resident (Sign Up Through App):
- **Email:** `leo052904@gmail.com`
- **Password:** `resident123` (create during signup)

## 🎯 Success Indicators:

After setup, you should see logs like:
```
🔥 Firebase initialized successfully
🔥 Firebase Auth - Sign up successful: [user-uid]
🔥 Firebase Auth - User document created: resident
```

## 🚀 Flow:

1. **Official:** Manual setup → Test login
2. **Resident:** App signup → Automatic account creation → Test login

**This is much better - residents self-register, only official needs manual setup!** 🎉
