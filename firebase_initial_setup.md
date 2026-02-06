# Firebase Initial Data Setup

## Instructions for Firebase Console Setup

### 1. Enable Firebase Services
Go to Firebase Console → Project Settings → General

Enable:
- ✅ Firebase Authentication (Email/Password)
- ✅ Cloud Firestore 
- ✅ Firebase Storage

### 2. Deploy Security Rules
```bash
# Deploy Firestore rules
firebase deploy --only firestore:rules

# Deploy Storage rules  
firebase deploy --only storage:rules
```

### 3. Create Initial Admin User
In Firebase Console → Authentication → Users:
- Create user: `official@barangay.gov`
- Password: `official123`
- UID will be auto-generated

### 4. Add Admin User to Firestore
In Firestore Database, create document in `users` collection:

```javascript
// users/{official-uid}
{
  "uid": "official-001", // Use this fixed UID for consistency
  "email": "official@barangay.gov", 
  "role": "official",
  "fullName": "Barangay Official",
  "contactNumber": "09876543210",
  "address": "Barangay Office",
  "verified": true,
  "discountRate": 0,
  "createdAt": timestamp,
  "updatedAt": timestamp
}
```

### 5. Add Sample Facilities
Create these documents in `facilities` collection:

```javascript
// facilities/community-garden
{
  "name": "Community Garden ni Eden",
  "price": 69,
  "downpayment": 34.5,
  "description": "Garden benches, shaded areas, water access",
  "amenities": "Garden nga ni, benches, shades, water",
  "capacity": 69,
  "icon": "park",
  "createdBy": "official-001",
  "createdAt": timestamp,
  "updatedAt": timestamp,
  "active": true
}

// facilities/multi-purpose-hall  
{
  "name": "Multi-Purpose Hall",
  "price": 100,
  "downpayment": 50,
  "description": "Spacious hall for events and meetings",
  "amenities": "Tables, chairs, sound system, air conditioning",
  "capacity": 100,
  "icon": "event_seat",
  "createdBy": "official-001", 
  "createdAt": timestamp,
  "updatedAt": timestamp,
  "active": true
}

// facilities/meeting-room
{
  "name": "Meeting Room",
  "price": 30,
  "downpayment": 15,
  "description": "Air-conditioned meeting room with projector",
  "amenities": "Projector, whiteboard, air conditioning, tables",
  "capacity": 15,
  "icon": "meeting_room",
  "createdBy": "official-001",
  "createdAt": timestamp,
  "updatedAt": timestamp,
  "active": true
}

// facilities/covered-court
{
  "name": "Covered Court",
  "price": 75,
  "downpayment": 35,
  "description": "Covered court for various sports activities",
  "amenities": "Volleyball net, badminton setup, lighting",
  "capacity": 50,
  "icon": "sports_volleyball",
  "createdBy": "official-001",
  "createdAt": timestamp,
  "updatedAt": timestamp,
  "active": true
}

// facilities/basketball-court
{
  "name": "Basketball Court",
  "price": 50,
  "downpayment": 25,
  "description": "Full-size basketball court with proper lighting",
  "amenities": "Basketball hoops, lighting, benches",
  "capacity": 20,
  "icon": "sports_basketball", 
  "createdBy": "official-001",
  "createdAt": timestamp,
  "updatedAt": timestamp,
  "active": true
}
```

### 6. Create Sample Resident User
```javascript
// users/{resident-uid}
{
  "uid": "resident-001",
  "email": "leo052904@gmail.com",
  "role": "resident", 
  "fullName": "John Leo Lopez",
  "contactNumber": "09656692463",
  "address": "Mountain Ville",
  "verified": false,
  "discountRate": 0,
  "createdAt": timestamp,
  "updatedAt": timestamp
}
```

### 7. Create Indexes for Performance
In Firestore Database → Indexes → Composite Indexes:

```javascript
// Bookings collection indexes
{
  "collectionId": "bookings",
  "queryScope": "COLLECTION",
  "fields": [
    {"fieldPath": "facilityId", "order": "ASCENDING"},
    {"fieldPath": "date", "order": "ASCENDING"},
    {"fieldPath": "status", "order": "ASCENDING"}
  ]
}

{
  "collectionId": "bookings", 
  "queryScope": "COLLECTION",
  "fields": [
    {"fieldPath": "residentId", "order": "ASCENDING"},
    {"fieldPath": "status", "order": "ASCENDING"},
    {"fieldPath": "createdAt", "order": "DESCENDING"}
  ]
}

// Verification requests indexes
{
  "collectionId": "verificationRequests",
  "queryScope": "COLLECTION", 
  "fields": [
    {"fieldPath": "status", "order": "ASCENDING"},
    {"fieldPath": "submittedAt", "order": "DESCENDING"}
  ]
}
```

### 8. Test Authentication Flow
1. Open app and select "Resident"
2. Try to login with: `leo052904@gmail.com`
3. If user doesn't exist, sign up first
4. Verify dashboard loads correctly

### 9. Test Official Flow  
1. Open app and select "Barangay Official"
2. Login with: `official@barangay.gov` / `official123`
3. Verify official dashboard loads
4. Test facility management and booking approval

### 10. Verify Storage Rules
Test uploading files to:
- `receipts/` - Payment receipts
- `verification/` - User photos and ID
- `facilities/` - Facility images

## Backend API Endpoints Needed

Your Express.js backend should handle:

### Authentication
- `POST /api/auth/login` - User login
- `POST /api/auth/register` - User registration
- `GET /api/auth/profile` - Get user profile

### Users  
- `GET /api/users/officials` - Get all officials
- `PUT /api/users/:id` - Update user profile
- `GET /api/users/:id` - Get user details

### Facilities
- `GET /api/facilities` - Get all facilities
- `POST /api/facilities` - Create facility (official only)
- `PUT /api/facilities/:id` - Update facility (official only)
- `DELETE /api/facilities/:id` - Delete facility (official only)

### Bookings
- `GET /api/bookings/facility/:id/:startDate/:endDate` - Get facility bookings
- `POST /api/bookings` - Create booking
- `PUT /api/bookings/:id` - Update booking status
- `GET /api/bookings/user/:email` - Get user bookings

### Verification Requests
- `POST /api/verification` - Submit verification request
- `GET /api/verification` - Get all requests (official)
- `PUT /api/verification/:id` - Approve/reject request

### Events (Official Quick Booking)
- `POST /api/events` - Create official event
- `GET /api/events/facility/:id/:startDate/:endDate` - Get facility events

### File Uploads
- `POST /api/upload/receipt` - Upload payment receipt
- `POST /api/upload/verification` - Upload verification photos
- `POST /api/upload/facility` - Upload facility image

## Next Steps After Setup

1. Test all authentication flows
2. Verify Firestore rules work correctly
3. Test file uploads to Storage
4. Implement real-time updates
5. Add push notifications (optional)
6. Set up monitoring and analytics
