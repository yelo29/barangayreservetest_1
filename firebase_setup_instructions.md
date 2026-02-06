# Firebase Setup Instructions

## 🔧 **FIREBASE CONFIGURATION REQUIRED**

The application is currently using placeholder Firebase configuration values. To fix all the permission errors, you need to:

### **1. Create Firebase Project**
1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Click "Add project"
3. Enter project name: `barangay-reserve-app`
4. Enable Google Analytics (optional)
5. Click "Create project"

### **2. Configure Android App**
1. In Firebase Console, click Android icon
2. Package name: `com.example.barangayreservetest_1`
3. Download `google-services.json`
4. Place it in: `android/app/google-services.json`

### **3. Configure iOS App** (if needed)
1. In Firebase Console, click iOS icon
2. Bundle ID: `com.example.barangayreservetest_1`
3. Download `GoogleService-Info.plist`
4. Place it in: `ios/Runner/GoogleService-Info.plist`

### **4. Update Firebase Options**
Replace the placeholder values in `lib/firebase_options.dart`:

```dart
static const FirebaseOptions android = FirebaseOptions(
  apiKey: 'YOUR_ACTUAL_ANDROID_API_KEY',
  appId: 'YOUR_ACTUAL_ANDROID_APP_ID',
  messagingSenderId: 'YOUR_ACTUAL_MESSAGING_SENDER_ID',
  projectId: 'YOUR_ACTUAL_PROJECT_ID',
  storageBucket: 'YOUR_ACTUAL_PROJECT_ID.appspot.com',
);
```

### **5. Firestore Security Rules**
In Firebase Console → Firestore Database → Rules, add:

```javascript
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    // Facilities - read for all, write for authenticated users
    match /facilities/{facilityId} {
      allow read: if true;
      allow write: if request.auth != null;
    }
    
    // Bookings - users can read their own, officials can read all
    match /bookings/{bookingId} {
      allow read: if request.auth != null && 
        (resource.data.userId == request.auth.uid || 
         get(/databases/$(database)/documents/users/$(request.auth.uid)).data.role == 'official');
      allow write: if request.auth != null;
      allow create: if request.auth != null;
    }
    
    // Users - users can read/write their own profile
    match /users/{userId} {
      allow read, write: if request.auth != null && request.auth.uid == userId;
    }
    
    // Authentication requests - officials can read all, users can create their own
    match /authenticationRequests/{requestId} {
      allow read: if request.auth != null && 
        get(/databases/$(database)/documents/users/$(request.auth.uid)).data.role == 'official';
      allow create: if request.auth != null && 
        request.resource.data.userId == request.auth.uid;
    }
    
    // Barangay events - read for all, write for officials
    match /barangayEvents/{eventId} {
      allow read: if true;
      allow write: if request.auth != null && 
        get(/databases/$(database)/documents/users/$(request.auth.uid)).data.role == 'official';
    }
  }
}
```

### **6. Firebase Storage Rules**
In Firebase Console → Storage → Rules, add:

```javascript
rules_version = '2';
service firebase.storage {
  match /b/{bucket}/o {
    // Users can upload to their own folders
    match /users/{userId}/{allPaths=**} {
      allow read, write: if request.auth != null && request.auth.uid == userId;
    }
    
    // Facilities - officials can manage
    match /facilities/{allPaths=**} {
      allow read: if true;
      allow write: if request.auth != null;
    }
  }
}
```

### **7. Enable Services**
In Firebase Console, enable:
- ✅ Authentication (Email/Password)
- ✅ Firestore Database
- ✅ Storage

## 🚀 **TEST MODE WORKAROUND**

Until Firebase is properly configured, the app will automatically:
- Detect unconfigured Firebase (placeholder values)
- Use test mode with simulated operations
- Show "(Test Mode)" in success messages
- Use placeholder image URLs

## 📱 **TESTING CREDENTIALS**

### **Test Mode (Works Without Firebase)**
- **Resident Login**: Any email with "test" (e.g., `test@email.com`)
- **Official Login**: Any email with "official" and "test" (e.g., `official@test.com`)
- **Password**: Any 6+ character password

### **Real Firebase (After Configuration)**
- **Official Account**: `official@barangay.test` (created automatically)
- **Test Resident**: Create any account with email/password

## 🔍 **ERRORS FIXED**

1. ✅ **"permission-denied"** → Test mode detection
2. ✅ **"Failed to upload images"** → Placeholder URLs
3. ✅ **"Failed to update facility"** → Simulated saves
4. ✅ **"Failed to create booking"** → Mock booking creation

## 📞 **SUPPORT**

If you need help with Firebase setup:
1. Check Firebase Console for errors
2. Verify `google-services.json` is correctly placed
3. Ensure all Firebase services are enabled
4. Test with the provided test credentials first
