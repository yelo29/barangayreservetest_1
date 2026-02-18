# 📁 Lib Folder Structure Documentation

This document provides a comprehensive overview of the file structure within the `lib/` folder of the Barangay Reserve Flutter application.

## 📂 Directory Overview

```
lib/
├── config/                 # App configuration files
├── dashboard/              # Main dashboard screens
│   ├── tabs/              # Tab components for dashboards
│   │   ├── official/      # Official dashboard tabs
│   │   └── resident/      # Resident dashboard tabs
│   └── widgets/           # Dashboard-specific widgets
├── main.dart              # App entry point
├── models/                # Data models and entities
├── screens/               # Main app screens
├── services/              # API and business logic services
├── utils/                 # Utility functions and helpers
└── widgets/               # Reusable UI components
```

---

## 🎯 MAIN SCREENS (`lib/screens/`)

| Screen | File | Description |
|--------|------|-------------|
| **Selection Screen** | `selection_screen.dart` | ✅ Initial screen to choose user role (Resident/Official) |
| **Resident Login** | `resident_login_screen.dart` | Login screen for resident users |
| **Official Login** | `official_login_screen.dart` | Login screen for barangay officials |
| **Booking Form** | `booking_form_screen.dart` | Main booking form for facility reservations |
| **Official Booking Form** | `official_booking_form_screen.dart` | Booking form specifically for officials |
| **Booking Details** | `booking_detail_screen.dart` | Screen to view detailed booking information |
| **Facility Calendar** | `facility_calendar_screen.dart` | Calendar view for facility availability |
| **Resident Verification** | `resident_verification_new.dart` | Resident identity verification screen |
| **Resident Account Settings** | `resident_account_settings_new.dart` | Account management for residents |
| **Official Account Settings** | `official_account_settings_screen.dart` | Account management for officials |
| **Server Config** | `server_config_screen.dart` | Server configuration settings |
| **Server Test** | `server_test_screen.dart` | Server connectivity testing |

---

## 🏠 DASHBOARD SCREENS (`lib/dashboard/`)

| Dashboard | File | Description |
|-----------|------|-------------|
| **Resident Dashboard** | `resident_dashboard.dart` | ✅ Main dashboard for resident users |
| **Official Dashboard** | `barangay_official_dashboard.dart` | Main dashboard for barangay officials |

---

## 📱 RESIDENT TABS (`lib/dashboard/tabs/resident/`)

| Tab | File | Description |
|-----|------|-------------|
| **Resident Home Tab** | `resident_home_tab.dart` | ✅ Home screen showing facilities and quick actions |
| **Resident Bookings Tab** | `resident_bookings_tab.dart` | ✅ User's booking history and management |
| **Resident Profile Tab** | `resident_profile_tab.dart` | ✅ User profile and account settings |
| **Form Screen** | `form_screen.dart` | Additional form interface for residents |
| **My Bookings Page** | `my_bookings_page.dart` | Detailed view of user's bookings |
| **Resident Home Page** | `resident_home_page.dart` | Alternative home page layout |

---

## 👮 OFFICIAL TABS (`lib/dashboard/tabs/official/`)

| Tab | File | Description |
|-----|------|-------------|
| **Official Home Tab** | `official_home_tab.dart` | ✅ Overview of facilities and statistics |
| **Authentication Requests Tab** | `authentication_requests_tab.dart` | ✅ Process resident verification requests |
| **Official Booking Requests Tab** | `official_booking_requests_tab.dart` | ✅ Manage and approve/reject booking requests |
| **Official Profile Tab** | `official_profile_tab.dart` | ✅ Official profile and settings |
| **Facility Edit Screen** | `facility_edit_screen.dart` | Add/Edit facility information |
| **Official Calendar Screen** | `official_calendar_screen.dart` | Calendar view for official bookings |
| **Barangay Event Screen** | `barangay_event_screen.dart` | Manage barangay events |
| **Official Event Form** | `official_event_form.dart` | Create/edit event forms |
| **Official Bookings Page** | `official_bookings_page.dart` | View all official bookings |

---

## ⚙️ SUPPORTING FOLDERS

### **Config** (`lib/config/`)
- **Purpose**: Application configuration and settings
- **Key Files**:
  - `app_config.dart` - Base URL, server settings, environment configs

### **Models** (`lib/models/`)
- **Purpose**: Data models and entity classes
- **Usage**: Define data structures for API responses and local data

### **Services** (`lib/services/`)
- **Purpose**: API services and business logic
- **Key Files**:
  - `data_service.dart` - Main data fetching service
  - `auth_api_service.dart` - Authentication and user management
  - `ban_detection_service.dart` - User ban monitoring

### **Utils** (`lib/utils/`)
- **Purpose**: Utility functions and helpers
- **Key Files**:
  - `debug_logger.dart` - Logging and debugging utilities

### **Widgets** (`lib/widgets/`)
- **Purpose**: Reusable UI components
- **Key Files**:
  - `enhanced_calendar.dart` - Custom calendar widget
  - `loading_widget.dart` - Loading indicators
  - Various other reusable components

---

## 🔍 QUICK REFERENCE GUIDE

### **Most Frequently Accessed Files:**
- **Selection Screen**: `lib/screens/selection_screen.dart`
- **Resident Home Tab**: `lib/dashboard/tabs/resident/resident_home_tab.dart`
- **Official Home Tab**: `lib/dashboard/tabs/official/official_home_tab.dart`
- **Authentication Requests**: `lib/dashboard/tabs/official/authentication_requests_tab.dart`
- **Booking Requests**: `lib/dashboard/tabs/official/official_booking_requests_tab.dart`

### **Navigation Flow:**
```
Selection Screen
├── Resident Login → Resident Dashboard
│   ├── Home Tab (facilities)
│   ├── Bookings Tab (my bookings)
│   └── Profile Tab (account settings)
└── Official Login → Official Dashboard
    ├── Home Tab (overview)
    ├── Requests Tab (booking requests)
    ├── Auth Tab (verification requests)
    └── Profile Tab (official settings)
```

---

## 📝 File Naming Conventions

### **Screens**: `snake_case.dart`
- `selection_screen.dart`
- `resident_login_screen.dart`
- `official_booking_form_screen.dart`

### **Tabs**: `snake_case.dart`
- `resident_home_tab.dart`
- `official_authentication_tab.dart`
- `facility_edit_screen.dart`

### **Services**: `snake_case.dart`
- `data_service.dart`
- `auth_api_service.dart`
- `ban_detection_service.dart`

### **Models**: `snake_case.dart` (if present)
- `user_model.dart`
- `booking_model.dart`

---

## 🚀 Development Tips

### **Adding New Screens:**
1. Create screen file in `lib/screens/`
2. Update navigation in relevant dashboard
3. Add to main.dart if needed

### **Adding New Tabs:**
1. Create tab file in appropriate `lib/dashboard/tabs/` subfolder
2. Import and add to dashboard's tab list
3. Update bottom navigation

### **Modifying Services:**
1. Edit service files in `lib/services/`
2. Update models in `lib/models/` if needed
3. Test across all affected screens

---

## 📊 File Size Overview (Approximate)

| Category | Total Files | Total Size |
|----------|-------------|------------|
| Screens | 12 files | ~300KB |
| Dashboard | 23 files | ~400KB |
| Services | 7 files | ~50KB |
| Widgets | 8 files | ~100KB |
| **Total** | **50+ files** | **~850KB** |

---

*Last Updated: February 18, 2026*
*Generated for Barangay Reserve Flutter Application*
