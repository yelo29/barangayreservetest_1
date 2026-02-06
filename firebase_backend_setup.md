# Firebase Backend Configuration for Barangay Reserve

## Project Details
- **Project ID**: barangay-reserve-cloud
- **Storage Bucket**: barangay-reserve-cloud.firebasestorage.app
- **Package Name**: ph.barangay.reserve

## Firebase Services Setup

### 1. Firebase Authentication
Enable the following in Firebase Console:
- Email/Password Authentication
- Google Sign-In (optional)

### 2. Firestore Database
Create the following collections:

#### users Collection
```
users/{userId}
{
  "uid": "firebaseAuthUID",
  "email": "user@gmail.com", 
  "role": "resident | official",
  "fullName": "Juan Dela Cruz",
  "contactNumber": "09XXXXXXXXX",
  "address": "Barangay Sample, City",
  "verified": false,
  "discountRate": 0,
  "createdAt": timestamp,
  "updatedAt": timestamp
}
```

#### facilities Collection
```
facilities/{facilityId}
{
  "name": "Covered Court",
  "price": 2000,
  "downpayment": 500,
  "description": "Multi-purpose court",
  "amenities": "Volleyball net, lighting, benches",
  "capacity": 50,
  "icon": "sports_volleyball",
  "createdBy": "officialUID",
  "createdAt": timestamp,
  "updatedAt": timestamp,
  "active": true
}
```

#### bookings Collection
```
bookings/{bookingId}
{
  "facilityId": "facilityId",
  "facilityName": "Covered Court", 
  "date": "2026-02-05",
  "timeSlot": "08:00 AM - 10:00 AM",
  "residentId": "residentUID",
  "residentName": "Juan Dela Cruz",
  "contactNumber": "09XXXXXXXXX",
  "address": "Barangay Sample",
  "purpose": "Birthday Celebration",
  "payment": {
    "gcashNumber": "09XXXXXXXXX",
    "gcashName": "Barangay Treasurer", 
    "email": "payment@example.com",
    "receiptDetails": "Ref#123456",
    "receiptImageUrl": "storageURL"
  },
  "status": "pending | approved | rejected",
  "verifiedResident": false,
  "discountApplied": 0,
  "createdAt": timestamp,
  "updatedAt": timestamp,
  "approvedBy": "officialUID",
  "approvedDate": timestamp
}
```

#### verificationRequests Collection
```
verificationRequests/{requestId}
{
  "residentId": "residentUID",
  "fullName": "Juan Dela Cruz",
  "contactNumber": "09XXXXXXXXX", 
  "address": "Barangay Sample",
  "userPhotoUrl": "storageURL",
  "validIdUrl": "storageURL",
  "status": "pending | approved | rejected",
  "submittedAt": timestamp,
  "reviewedBy": "officialUID",
  "reviewedAt": timestamp,
  "discountRate": 0.05 | 0.10
}
```

#### events Collection (Official Quick Booking)
```
events/{eventId}
{
  "facilityId": "facilityId",
  "facilityName": "Covered Court",
  "date": "2026-02-10",
  "type": "barangay_event | official_booking",
  "purpose": "Official meeting",
  "createdBy": "officialUID",
  "createdAt": timestamp
}
```

### 3. Firebase Storage Structure
```
storage/
├── receipts/
│   └── {bookingId}.jpg
├── verification/
│   ├── userPhoto_{userId}.jpg
│   └── validId_{userId}.jpg
└── facilities/
    └── {facilityId}.jpg
```

### 4. Firestore Security Rules

#### firestore.rules
```
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    
    // Users collection rules
    match /users/{userId} {
      allow read, write: if request.auth != null && 
        (request.auth.uid == userId || 
         get(/databases/$(database)/documents/users/$(request.auth.uid)).data.role == 'official');
    }
    
    // Facilities collection rules
    match /facilities/{facilityId} {
      allow read: if request.auth != null;
      allow write, create, update: if request.auth != null && 
        get(/databases/$(database)/documents/users/$(request.auth.uid)).data.role == 'official';
    }
    
    // Bookings collection rules
    match /bookings/{bookingId} {
      allow read: if request.auth != null && 
        (resource.data.residentId == request.auth.uid || 
         get(/databases/$(database)/documents/users/$(request.auth.uid)).data.role == 'official');
      allow create: if request.auth != null && 
        request.auth.uid == resource.data.residentId;
      allow update: if request.auth != null && 
        get(/databases/$(database)/documents/users/$(request.auth.uid)).data.role == 'official';
    }
    
    // Verification requests collection rules
    match /verificationRequests/{requestId} {
      allow read: if request.auth != null && 
        (resource.data.residentId == request.auth.uid || 
         get(/databases/$(database)/documents/users/$(request.auth.uid)).data.role == 'official');
      allow create: if request.auth != null && 
        request.auth.uid == resource.data.residentId;
      allow update: if request.auth != null && 
        get(/databases/$(database)/documents/users/$(request.auth.uid)).data.role == 'official';
    }
    
    // Events collection rules (official bookings)
    match /events/{eventId} {
      allow read, write: if request.auth != null && 
        get(/databases/$(database)/documents/users/$(request.auth.uid)).data.role == 'official';
    }
  }
}
```

#### storage.rules
```
rules_version = '2';
service firebase.storage {
  match /b/{bucket}/o {
    // Receipt images
    match /receipts/{receiptId} {
      allow read, write: if request.auth != null;
    }
    
    // Verification photos
    match /verification/{userId}/{allPaths=**} {
      allow read, write: if request.auth != null && 
        (request.auth.uid == userId || 
         get(/databases/$(database)/documents/users/$(request.auth.uid)).data.role == 'official');
    }
    
    // Facility images
    match /facilities/{facilityId} {
      allow read: if request.auth != null;
      allow write: if request.auth != null && 
        get(/databases/$(database)/documents/users/$(request.auth.uid)).data.role == 'official';
    }
  }
}
```

## Implementation Steps

1. **Firebase Console Setup**
   - Enable Authentication (Email/Password)
   - Create Firestore Database
   - Enable Storage
   - Set up security rules

2. **Backend API Endpoints**
   - User authentication
   - CRUD operations for all collections
   - File upload handlers
   - Role-based access control

3. **Frontend Integration**
   - Firebase Auth integration
   - Real-time Firestore listeners
   - Image upload functionality
   - Role-based UI rendering

## Next Steps

1. Set up Firebase Console with above configuration
2. Deploy security rules
3. Create initial admin user in users collection
4. Add sample facilities data
5. Test authentication flow
