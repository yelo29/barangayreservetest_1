# Resident User Workflow Documentation

## 📱 Resident User Journey

### **1. User Registration & Authentication**
- **File**: `lib/screens/resident_login_screen.dart`
- **Function**: User login and registration
- **API Endpoint**: `/api/auth/login`, `/api/auth/register`
- **Features**: 
  - Email/password authentication
  - Remember me functionality
  - Session management

### **2. Main Dashboard Navigation**
- **File**: `lib/dashboard/resident_dashboard.dart`
- **Function**: Main navigation hub for residents
- **Features**:
  - Quick access to booking, profile, verification
  - User status display
  - Navigation to all resident features

### **3. Facility Booking Process**
- **File**: `lib/screens/booking_form_screen.dart`
- **Function**: Book barangay facilities
- **API Endpoints**: 
  - `/api/facilities` (get facilities)
  - `/api/available-timeslots` (get time slots)
  - `/api/bookings` (create booking)
- **Features**:
  - Facility selection
  - Calendar date picker
  - Time slot selection
  - Payment integration
  - Receipt upload

### **4. Booking Management**
- **File**: `lib/dashboard/tabs/resident_bookings_tab.dart`
- **Function**: View and manage resident bookings
- **API Endpoint**: `/api/bookings` (get user bookings)
- **Features**:
  - View all bookings (pending, approved, rejected)
  - Filter by status and date
  - Cancel pending bookings

### **5. Account Verification**
- **File**: `lib/screens/resident_verification_new.dart`
- **Function**: Submit verification documents
- **API Endpoint**: `/api/verification-requests`
- **Features**:
  - Document upload
  - Personal information form
  - Verification status tracking

### **6. Profile Management**
- **File**: `lib/screens/resident_account_settings_new.dart`
- **Function**: Manage personal account settings
- **API Endpoints**:
  - `/api/users/profile` (get/update profile)
  - `/api/users/{id}` (update user data)
- **Features**:
  - Personal information editing
  - Contact details update
  - Password change
  - Profile photo upload

### **7. Home Screen Features**
- **File**: `lib/dashboard/tabs/resident_home_tab.dart`
- **Function**: Resident home dashboard
- **Features**:
  - Quick booking access
  - Recent bookings display
  - Announcements
  - Quick actions

## 🔄 Resident Flow Summary

```
Login → Dashboard → Book Facility → Upload Receipt → Track Status
          ↓
      Profile Management → Verification → Account Settings
```

## 🛡️ Security Features

### **Ban Validation**
- **File**: `lib/services/ban_validation_service.dart`
- **Function**: Prevent banned users from accessing features
- **Features**:
  - Real-time ban status checking
  - User-friendly ban dialogs
  - Automatic logout on ban detection

### **Session Management**
- **File**: `lib/services/auth_api_service.dart`
- **Function**: Handle user authentication and sessions
- **Features**:
  - JWT-like token management
  - Automatic session refresh
  - Secure logout

## 📊 Data Models

### **User Model**
- **File**: `lib/models/user_model.dart`
- **Fields**: id, email, fullName, role, verified, discountRate, etc.

### **Booking Model**
- **File**: `lib/models/booking_model.dart`
- **Fields**: id, facilityId, userEmail, date, timeslot, status, etc.

## 🔗 API Integration

All resident features use HTTP API calls to:
- **Base URL**: Configured in `lib/config/app_config.dart`
- **Authentication**: Bearer token-based
- **Error Handling**: Centralized in API service
- **Ban Protection**: Server-side validation
