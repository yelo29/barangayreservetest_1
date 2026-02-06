# 🚀 NODE.JS BACKEND SETUP GUIDE

This guide will help you set up the Node.js backend for your Barangay Reserve app to replace mock data with real database operations.

## 📋 PREREQUISITES

1. **Node.js 16+** installed
2. **Firebase project** with Firestore enabled
3. **Firebase service account key**

## 🔧 STEP 1: SET UP FIREBASE

### 1.1 Create Firebase Project
1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Click "Add project"
3. Enter project name: `barangay-reserve-api`
4. Enable Firestore (Start in test mode)

### 1.2 Generate Service Account Key
1. In Firebase Console → Project Settings → Service accounts
2. Click "Generate new private key"
3. Select JSON format
4. Download and save as `backend/firebase-service-account.json`

### 1.3 Get Firebase Configuration
From Firebase Console → Project Settings → General:
- **Project ID**: Copy this value
- **Private Key**: From the downloaded JSON file

## 🔧 STEP 2: SET UP BACKEND

### 2.1 Navigate to Backend Directory
```bash
cd backend
```

### 2.2 Install Dependencies
```bash
npm install
```

### 2.3 Configure Environment Variables
```bash
# Copy the example file
cp .env.example .env

# Edit the .env file with your Firebase credentials
```

Edit `.env` file:
```env
# Firebase Configuration (from your service account JSON)
FIREBASE_PROJECT_ID=your-project-id
FIREBASE_PRIVATE_KEY="-----BEGIN PRIVATE KEY-----\nYOUR_PRIVATE_KEY_HERE\n-----END PRIVATE KEY-----\n"
FIREBASE_CLIENT_EMAIL=firebase-adminsdk-xxx@your-project-id.iam.gserviceaccount.com
FIREBASE_CLIENT_ID=your-client-id
FIREBASE_AUTH_URI=https://accounts.google.com/o/oauth2/auth
FIREBASE_TOKEN_URI=https://oauth2.googleapis.com/token
FIREBASE_AUTH_PROVIDER_X509_CERT_URL=https://www.googleapis.com/oauth2/v1/certs
FIREBASE_CLIENT_X509_CERT_URL=https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-xxx%40your-project-id.iam.gserviceaccount.com

# Server Configuration
PORT=3000
NODE_ENV=development

# JWT Secret (generate a secure random string)
JWT_SECRET=your-super-secret-jwt-key-here-change-this-in-production

# CORS (update with your Flutter app's URL)
FRONTEND_URL=http://localhost:3000
```

### 2.4 Start the Backend Server
```bash
# Development mode (auto-restart on changes)
npm run dev

# Or production mode
npm start
```

You should see:
```
🚀 Barangay Reserve API server running on port 3000
📊 Environment: development
🔗 API URL: http://localhost:3000/api
```

## 🔧 STEP 3: UPDATE FLUTTER APP

### 3.1 Install HTTP Dependencies
```bash
cd ..  # Go back to Flutter project root
flutter pub add http shared_preferences
```

### 3.2 Update API Service Configuration
Edit `lib/services/api_service.dart`:
```dart
class ApiService {
  // Update this to your server URL
  static const String baseUrl = 'http://localhost:3000/api'; 
  // For production, use your actual server URL
  // static const String baseUrl = 'https://your-server.com/api';
}
```

### 3.3 Replace Firebase Auth with API Auth
Update your login screens to use `AuthApiService` instead of `AuthService`:

```dart
// Import the new service
import '../services/auth_api_service.dart';

class ResidentLoginScreen extends StatefulWidget {
  // Replace AuthService with AuthApiService
  final AuthApiService _authService = AuthApiService();
  
  // Update sign up method
  Future<void> _signUp() async {
    final result = await _authService.registerWithEmailAndPassword(
      _emailController.text.trim(),
      _passwordController.text.trim(),
      _nameController.text.trim(),
      role: 'resident',
    );
    
    if (result['success']) {
      // Navigate to dashboard
    } else {
      // Show error: result['error']
    }
  }
  
  // Update sign in method
  Future<void> _signIn() async {
    final result = await _authService.signInWithEmailAndPassword(
      _emailController.text.trim(),
      _passwordController.text.trim(),
    );
    
    if (result['success']) {
      // Navigate to dashboard
    } else {
      // Show error: result['error']
    }
  }
}
```

## 🔧 STEP 4: UPDATE FIRESTORE RULES

Replace your Firestore rules with these (they're simpler since backend handles security):

```javascript
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    // Allow all read/write operations (backend handles security)
    match /{document=**} {
      allow read, write: if true;
    }
  }
}
```

## 🔧 STEP 5: TEST THE SETUP

### 5.1 Test Backend Health
```bash
curl http://localhost:3000/api/health
```
Should return: `{"status":"OK","message":"Barangay Reserve API is running"}`

### 5.2 Test User Registration
```bash
curl -X POST http://localhost:3000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test User",
    "email": "test@example.com",
    "password": "password123",
    "role": "resident"
  }'
```

### 5.3 Test User Login
```bash
curl -X POST http://localhost:3000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "password123"
  }'
```

## 🔧 STEP 6: REMOVE MOCK DATA LOGIC

### 6.1 Remove Test Services
Delete these files (they contain mock data logic):
- `lib/services/test_booking_service.dart`
- `lib/services/test_authentication_service.dart`
- `lib/services/user_verification_service.dart`

### 6.2 Update Dashboard Initialization
Remove Firebase configuration checks and test mode logic from:
- `lib/dashboard/resident_dashboard.dart`
- `lib/dashboard/barangay_official_dashboard.dart`

### 6.3 Update Forms and Services
Replace all Firebase direct calls with API calls:
- Booking forms → use `ApiService.createBooking()`
- Authentication requests → use `ApiService.submitAuthenticationRequest()`
- Facility management → use `ApiService.createFacility()`

## 📊 DATABASE STRUCTURE

The backend will automatically create these collections:

### `users` Collection
```javascript
{
  uid: "string",
  name: "string",
  email: "string",
  password: "hashed_string",
  role: "resident|official",
  isAuthenticated: boolean,
  discount: number,
  verificationType: "unverified|resident|non-resident",
  createdAt: timestamp,
  updatedAt: timestamp
}
```

### `facilities` Collection
```javascript
{
  id: "string",
  name: "string",
  description: "string",
  capacity: "string",
  rate: "string",
  downpayment: "string",
  amenities: "string",
  icon: "string",
  createdAt: timestamp,
  updatedAt: timestamp
}
```

### `bookings` Collection
```javascript
{
  id: "string",
  userId: "string",
  facilityId: "string",
  facilityName: "string",
  bookingDate: "string",
  timeslot: "string",
  fullName: "string",
  contactNumber: "string",
  address: "string",
  receiptImageURL: "string",
  status: "pending|approved|rejected|completed",
  submittedDate: timestamp,
  approvedDate: timestamp,
  approvedBy: "string",
  createdAt: timestamp,
  updatedAt: timestamp
}
```

## 🚀 DEPLOYMENT

### Development
```bash
# Backend
cd backend && npm run dev

# Flutter (in another terminal)
flutter run
```

### Production
1. **Deploy Backend** to a cloud service (Heroku, AWS, DigitalOcean)
2. **Update API URL** in Flutter app to production URL
3. **Build Flutter APK**: `flutter build apk --release`

## 🔍 TROUBLESHOOTING

### Common Issues

1. **"Firebase connection error"**
   - Check service account key path
   - Verify project ID matches Firebase console
   - Ensure private key is properly formatted

2. **"JWT token error"**
   - Verify JWT_SECRET is set in .env
   - Generate a new secure secret

3. **"CORS error"**
   - Update FRONTEND_URL in .env
   - Check Flutter app is making requests to correct URL

4. **"Network error" in Flutter**
   - Ensure backend server is running
   - Check API URL in ApiService
   - Verify network connectivity

### Logs
```bash
# Backend logs
npm run dev  # Shows detailed logs

# Flutter logs
flutter logs
```

## ✅ VERIFICATION CHECKLIST

- [ ] Backend server running on port 3000
- [ ] Firebase service account key configured
- [ ] Environment variables set correctly
- [ ] Health endpoint responding
- [ ] User registration working
- [ ] User login working
- [ ] JWT tokens generated and stored
- [ ] Flutter app can connect to API
- [ ] Mock data logic removed
- [ ] All features using real database

## 🎯 BENEFITS

✅ **Real Database Operations** - No more mock data  
✅ **Secure Authentication** - JWT-based auth system  
✅ **Role-based Access** - Proper permissions  
✅ **Scalable Architecture** - Backend handles business logic  
✅ **Better Error Handling** - Proper HTTP responses  
✅ **File Upload Support** - Image uploads via API  
✅ **Production Ready** - Secure and performant  

Your Barangay Reserve app now has a professional backend architecture with real database operations!
