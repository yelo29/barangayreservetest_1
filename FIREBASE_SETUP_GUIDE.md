# Firebase Initial Data Setup Guide (Updated - No Storage)

## 🔧 Step 1: Enable Firebase Services

1. Go to Firebase Console: https://console.firebase.google.com/
2. Select project: `barangay-reserve-cloud`
3. Enable these services:
   - ✅ Firebase Authentication (Email/Password)
   - ✅ Cloud Firestore 
   - ❌ Firebase Storage (DISABLED - Billing Required)
   - ✅ Cloudinary (Free tier for images)

## 🔧 Step 2: Deploy Security Rules

Run these commands in your terminal:
```bash
# Deploy Firestore rules only
firebase deploy --only firestore:rules

# Note: Storage rules are disabled - we use Cloudinary instead
```

## 🔧 Step 3: Set Up Cloudinary

1. Go to Cloudinary Dashboard: https://cloudinary.com/
2. Sign up for free account
3. Get your Cloud Name from dashboard
4. Update `cloudinary_service.dart` with your cloud name:
   ```dart
   _cloudinary = CloudinaryPublic(
     'your-cloud-name', // Replace with your actual cloud name
     url: 'https://api.cloudinary.com/v1_1/your-cloud-name/image/auto/upload',
   );
   ```

## 🔧 Step 4: Create Admin User

### Firebase Console
1. Go to Firebase Console → Authentication → Users
2. Click "Add user"
3. Enter:
   - Email: `official@barangay.gov`
   - Password: `official123`
4. Click "Add user"

## 🔧 Step 5: Create Initial Data in Firestore

### Method 1: Firebase Console (Recommended)
1. Go to Firebase Console → Firestore Database
2. Create these documents:

#### Users Collection
**Document ID:** `official-001`
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
  "createdAt": "2026-01-30T23:52:00.000Z",
  "updatedAt": "2026-01-30T23:52:00.000Z"
}
```

**Document ID:** `resident-001`
```json
{
  "uid": "resident-001", 
  "email": "leo052904@gmail.com",
  "role": "resident",
  "fullName": "John Leo Lopez",
  "contactNumber": "09656692463",
  "address": "Mountain Ville",
  "verified": false,
  "discountRate": 0,
  "createdAt": "2026-01-30T23:52:00.000Z",
  "updatedAt": "2026-01-30T23:52:00.000Z"
}
```

#### Facilities Collection
**Document ID:** `community-garden`
```json
{
  "name": "Community Garden ni Eden",
  "price": 69,
  "downpayment": 34.5,
  "description": "Garden benches, shaded areas, water access",
  "amenities": "Garden nga ni, benches, shades, water",
  "capacity": 69,
  "icon": "park",
  "createdBy": "official-001",
  "createdAt": "2026-01-30T23:52:00.000Z",
  "updatedAt": "2026-01-30T23:52:00.000Z",
  "active": true
}
```

**Document ID:** `multi-purpose-hall`
```json
{
  "name": "Multi-Purpose Hall",
  "price": 100,
  "downpayment": 50,
  "description": "Spacious hall for events and meetings",
  "amenities": "Tables, chairs, sound system, air conditioning",
  "capacity": 100,
  "icon": "event_seat",
  "createdBy": "official-001",
  "createdAt": "2026-01-30T23:52:00.000Z",
  "updatedAt": "2026-01-30T23:52:00.000Z",
  "active": true
}
```

**Document ID:** `meeting-room`
```json
{
  "name": "Meeting Room",
  "price": 30,
  "downpayment": 15,
  "description": "Air-conditioned meeting room with projector",
  "amenities": "Projector, whiteboard, air conditioning, tables",
  "capacity": 15,
  "icon": "meeting_room",
  "createdBy": "official-001",
  "createdAt": "2026-01-30T23:52:00.000Z",
  "updatedAt": "2026-01-30T23:52:00.000Z",
  "active": true
}
```

**Document ID:** `covered-court`
```json
{
  "name": "Covered Court",
  "price": 75,
  "downpayment": 35,
  "description": "Covered court for various sports activities",
  "amenities": "Volleyball net, badminton setup, lighting",
  "capacity": 50,
  "icon": "sports_volleyball",
  "createdBy": "official-001",
  "createdAt": "2026-01-30T23:52:00.000Z",
  "updatedAt": "2026-01-30T23:52:00.000Z",
  "active": true
}
```

**Document ID:** `basketball-court`
```json
{
  "name": "Basketball Court",
  "price": 50,
  "downpayment": 25,
  "description": "Full-size basketball court with proper lighting",
  "amenities": "Basketball hoops, lighting, benches",
  "capacity": 20,
  "icon": "sports_basketball",
  "createdBy": "official-001",
  "createdAt": "2026-01-30T23:52:00.000Z",
  "updatedAt": "2026-01-30T23:52:00.000Z",
  "active": true
}
```

## 🔧 Step 5: Create Database Indexes

1. Go to Firebase Console → Firestore Database → Indexes
2. Create these composite indexes:

### Index 1: Bookings by Facility and Date
- **Collection:** `bookings`
- **Fields:**
  - `facilityId` (Ascending)
  - `date` (Ascending)
  - `status` (Ascending)

### Index 2: User Bookings
- **Collection:** `bookings`
- **Fields:**
  - `residentId` (Ascending)
  - `status` (Ascending)
  - `createdAt` (Descending)

### Index 3: Verification Requests
- **Collection:** `verificationRequests`
- **Fields:**
  - `status` (Ascending)
  - `submittedAt` (Descending)

## 🔧 Step 6: Test the App

### Test Accounts:
- **Official:** `official@barangay.gov` / `official123`
- **Resident:** `leo052904@gmail.com` / [create new password in app]

### Test Steps:
1. **Login as Official**
   - Verify dashboard loads
   - Check facilities are visible
   - Test quick booking functionality

2. **Login as Resident**
   - Verify dashboard loads
   - Check facilities are visible
   - Test booking creation
   - Test calendar colors

3. **Test Calendar Colors**
   - Create some bookings
   - Verify calendar shows:
     - White: Available dates
     - Yellow: Pending bookings
     - Green: Approved bookings

## 🔧 Step 7: Verify All Features

### Authentication:
- ✅ Login/Logout works
- ✅ Role-based access works
- ✅ User profiles load correctly

### Booking System:
- ✅ Facility selection works
- ✅ Calendar displays correctly
- ✅ Booking creation works
- ✅ Status updates work

### Data Storage:
- ✅ Firestore data is saved
- ✅ Firebase Storage uploads work
- ✅ Real-time updates work

## 🎯 Success Criteria

When all of these work, your Firebase backend is properly set up:
- ✅ Users can authenticate with Firebase Auth
- ✅ Data is stored in Firestore collections
- ✅ Files upload to Firebase Storage
- ✅ Security rules protect data properly
- ✅ Real-time updates work in the app

## 🚀 Ready to Go!

Once you complete these steps, your Barangay Reserve app will have a fully functional Firebase backend with proper authentication, data storage, and real-time capabilities.
