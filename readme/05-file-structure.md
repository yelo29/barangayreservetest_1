# Project File Structure Documentation

## 📁 Complete Directory Structure

```
barangayreservetest_1/
├── 📁 lib/                          # Main application code
│   ├── 📁 config/                   # Configuration files
│   │   └── 📄 app_config.dart        # Server URL and app settings
│   ├── 📁 dashboard/                 # Dashboard screens and tabs
│   │   ├── 📄 barangay_official_dashboard.dart
│   │   ├── 📄 resident_dashboard.dart
│   │   ├── 📁 tabs/                   # Dashboard tabs
│   │   │   ├── 📁 official/          # Official-specific tabs
│   │   │   ├── 📄 authentication_requests_tab.dart
│   │   │   ├── 📄 official_booking_requests_tab.dart
│   │   │   ├── 📄 official_home_tab.dart
│   │   │   └── 📄 [other official tabs...]
│   │   ├── 📁 resident/           # Resident-specific tabs
│   │   │   ├── 📄 form_screen.dart
│   │   │   └── 📄 [other resident tabs...]
│   │   ├── 📄 official_home_tab.dart
│   │   ├── 📄 resident_bookings_tab.dart
│   │   ├── 📄 resident_home_tab.dart
│   │   └── 📄 resident_profile_tab.dart
│   │   └── 📁 widgets/              # Dashboard widgets
│   │       └── [dashboard widgets...]
│   ├── 📁 models/                    # Data models
│   │   ├── 📄 booking_model.dart      # Booking data structure
│   │   ├── 📄 facility_model.dart    # Facility data structure
│   │   └── 📄 user_model.dart        # User data structure
│   ├── 📁 screens/                   # Main application screens
│   │   ├── 📄 booking_detail_screen.dart
│   │   ├── 📄 booking_form_screen.dart
│   │   ├── 📄 facility_calendar_screen.dart
│   │   ├── 📄 official_account_settings_screen.dart
│   │   ├── 📄 official_booking_form_screen.dart
│   │   ├── 📄 official_login_screen.dart
│   │   ├── 📄 resident_account_settings_new.dart
│   │   ├── 📄 resident_login_screen.dart
│   │   ├── 📄 resident_verification_new.dart
│   │   ├── 📄 selection_screen.dart    # Role selection entry point
│   │   ├── 📄 server_config_screen.dart
│   │   └── 📄 server_test_screen.dart
│   ├── 📁 services/                  # Business logic and API
│   │   ├── 📄 api_service.dart        # Main HTTP API service
│   │   ├── 📄 auth_api_service.dart   # Authentication service
│   │   ├── 📄 ban_detection_service.dart  # Ban detection (stub)
│   │   ├── 📄 ban_validation_service.dart # Ban validation
│   │   ├── 📄 base64_image_service.dart # Image handling
│   │   ├── 📄 data_service.dart       # Data management
│   │   └── 📄 permission_service.dart # App permissions
│   ├── 📁 utils/                     # Utility functions
│   │   └── 📄 debug_logger.dart     # Logging utility
│   ├── 📁 widgets/                   # Reusable UI components
│   │   ├── 📄 base64_image_widget.dart
│   │   ├── 📄 enhanced_calendar.dart
│   │   ├── 📄 loading_widget.dart
│   │   └── 📄 [other widgets...]
│   └── 📄 main.dart                 # App entry point
├── 📁 assets/                         # Static assets
│   ├── 📁 images/                   # App images and icons
│   │   ├── 📁 qr_codes/              # QR code images
│   │   └── [other images...]
│   └── 📁 icon/                     # App icons
├── 📁 server/                         # Backend server code
│   ├── 📄 server.py                 # Flask API server
│   └── 📄 barangay.db              # SQLite database
├── 📁 backend/                        # Additional backend files
│   ├── 📁 node_modules/             # Node dependencies
│   └── [backend files...]
├── 📄 pubspec.yaml                   # Flutter dependencies
├── 📄 README.md                      # Project overview
└── 📁 readme/                        # Documentation (this folder)
    ├── 📄 01-resident-workflow.md
    ├── 📄 02-official-workflow.md
    ├── 📄 03-database-schema.md
    ├── 📄 04-selection-screen-flow.md
    └── 📄 05-file-structure.md
```

---

## 📱 Core Application Files

### **🎯 Entry Points**:
- **`main.dart`**: Application initialization and setup
- **`selection_screen.dart`**: Role selection and navigation hub

### **🏠 Resident Features**:
- **`resident_login_screen.dart`**: Resident authentication
- **`booking_form_screen.dart`**: Facility booking interface
- **`resident_bookings_tab.dart`**: Booking management
- **`resident_verification_new.dart`**: Document verification
- **`resident_account_settings_new.dart`**: Profile management

### **🏛️ Official Features**:
- **`official_login_screen.dart`**: Official authentication
- **`official_booking_requests_tab.dart`**: Booking approval
- **`authentication_requests_tab.dart`**: User verification
- **`official_booking_form_screen.dart`**: Facility management
- **`official_account_settings_screen.dart`**: Admin settings

---

## 🔧 Service Layer Architecture

### **🌐 API Services**:
- **`api_service.dart`**: Main HTTP client and endpoints
- **`auth_api_service.dart`**: Authentication and session management
- **`data_service.dart`**: Data operations and caching

### **🛡️ Security Services**:
- **`ban_validation_service.dart`**: Ban status checking
- **`ban_detection_service.dart`**: Ban detection (stub implementation)
- **`permission_service.dart`**: App permission handling

### **🖼️ Utility Services**:
- **`base64_image_service.dart`**: Image encoding/decoding
- **`debug_logger.dart`**: Application logging
- **`permission_service.dart`**: Device permissions

---

## 📊 Data Models

### **📋 Core Models**:
- **`user_model.dart`**: User data structure (SQLite-based)
- **`booking_model.dart`**: Booking data structure (SQLite-based)
- **`facility_model.dart`**: Facility data structure

### **🔄 Model Features**:
- **JSON Serialization**: For API communication
- **SQLite Mapping**: Database operations
- **Validation**: Data integrity checks
- **Helper Methods**: Common operations

---

## 🎨 UI Components

### **📱 Screens**:
- **Main Screens**: 13 primary application screens
- **Dashboard Tabs**: 5 main navigation tabs
- **Settings Screens**: Account and configuration

### **🧩 Widgets**:
- **Reusable Components**: Calendar, image widgets, loading indicators
- **Custom Components**: Base64 image handling, enhanced UI elements
- **Form Components**: Input validation and submission

---

## 🗄️ Database Structure

### **📁 Database Files**:
- **`server/barangay.db`**: Main SQLite database
- **Tables**: users, facilities, bookings, verification_requests, available_timeslots

### **🔗 Backend Integration**:
- **`server/server.py`**: Flask API server
- **API Endpoints**: RESTful services for all operations
- **Authentication**: JWT-like token management

---

## 📦 Dependencies and Configuration

### **📋 pubspec.yaml**:
- **Flutter SDK**: ^3.9.0
- **HTTP**: http, url_launcher
- **Storage**: shared_preferences
- **UI**: table_calendar, image_picker
- **Images**: cloudinary_public
- **Firebase**: Removed (commented out)

### **⚙️ Configuration**:
- **`app_config.dart`**: Dynamic server URL configuration
- **Environment**: Development and production settings
- **API Base URL**: Configurable endpoint management

---

## 🔄 Build and Deployment

### **📱 Flutter Build**:
- **APK Output**: `build/app/outputs/flutter-apk/`
- **Release Build**: Production-ready APK
- **Debug Build**: Development testing

### **🌐 Server Deployment**:
- **Flask Server**: Python-based backend
- **SQLite Database**: Self-contained data storage
- **API Documentation**: RESTful endpoint documentation

---

## 🎯 Architecture Summary

### **📱 Frontend (Flutter)**:
- **Role-Based UI**: Resident vs Official interfaces
- **Service Layer**: API communication and business logic
- **State Management**: StatefulWidget pattern
- **Navigation**: Material Design navigation

### **🗄️ Backend (Flask + SQLite)**:
- **RESTful API**: HTTP endpoints for all operations
- **Database**: SQLite for data persistence
- **Authentication**: Token-based session management
- **Security**: Ban validation and user management

### **🔗 Integration**:
- **HTTP Communication**: JSON-based API calls
- **Authentication**: Bearer token security
- **Error Handling**: Centralized error management
- **Data Validation**: Client and server-side validation

---

## 📈 Scalability Considerations

### **📊 Current Scale**:
- **Users**: Supports unlimited residents and officials
- **Bookings**: Efficient time slot management
- **Facilities**: Dynamic facility addition
- **Verification**: Document processing workflow

### **🚀 Future Enhancements**:
- **Multi-tenancy**: Support multiple barangays
- **Real-time Updates**: WebSocket integration
- **Mobile Admin**: Official mobile app
- **Analytics**: Usage statistics and reporting

This file structure provides a solid foundation for the barangay reservation system with clear separation of concerns and maintainable code organization.
