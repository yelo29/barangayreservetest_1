# Official User Workflow Documentation

## 🏛️ Official User Journey

### **1. Official Authentication**
- **File**: `lib/screens/official_login_screen.dart`
- **Function**: Official login and session management
- **API Endpoints**: `/api/auth/login` (with official role)
- **Features**:
  - Email/password authentication for officials
  - Role-based access control
  - Session persistence

### **2. Official Dashboard Navigation**
- **File**: `lib/dashboard/barangay_official_dashboard.dart`
- **Function**: Main navigation hub for officials
- **Features**:
  - Access to all official modules
  - User statistics and overview
  - Quick action buttons

### **3. Booking Request Management**
- **File**: `lib/dashboard/tabs/official/official_booking_requests_tab.dart`
- **Function**: Review and manage resident booking requests
- **API Endpoints**:
  - `/api/bookings` (get pending bookings)
  - `/api/bookings/{id}/status` (update booking status)
- **Features**:
  - View all pending booking requests
  - Approve/reject bookings with reasons
  - Filter by date, facility, status
  - Bulk operations support

### **4. Booking Details Review**
- **File**: `lib/screens/booking_detail_screen.dart`
- **Function**: Detailed view of individual bookings
- **Features**:
  - Complete booking information display
  - Receipt and document viewing
  - Status history tracking
  - User information display

### **5. User Account Management**
- **File**: `lib/dashboard/tabs/official/authentication_requests_tab.dart`
- **Function**: Manage resident verification requests
- **API Endpoints**:
  - `/api/verification-requests` (get all requests)
  - `/api/verification-requests/{id}/status` (update status)
- **Features**:
  - Review verification documents
  - Approve/reject verification requests
  - Add discount rates for verified users
  - Bulk verification processing

### **6. Official Records Management**
- **File**: `lib/dashboard/official_records_tab.dart`
- **Function**: View and manage barangay records
- **Features**:
  - Booking history
  - User management
  - Facility usage statistics
  - Report generation

### **7. Official Account Settings**
- **File**: `lib/screens/official_account_settings_screen.dart`
- **Function**: Manage official account settings
- **API Endpoints**: `/api/users/profile` (official profile)
- **Features**:
  - Personal information management
  - Password change
  - Notification preferences
  - Account security settings

### **8. Official Home Dashboard**
- **File**: `lib/dashboard/tabs/official_home_tab.dart`
- **Function**: Official home dashboard
- **Features**:
  - Statistics overview
  - Recent activities
  - Quick actions
  - System notifications

### **9. Facility Management**
- **File**: `lib/screens/official_booking_form_screen.dart`
- **Function**: Manage barangay facilities
- **API Endpoints**:
  - `/api/facilities` (CRUD operations)
  - `/api/facilities/{id}/timeslots` (time slot management)
- **Features**:
  - Add/edit/delete facilities
  - Manage time slots
  - Set availability
  - Facility configuration

## 🔄 Official Flow Summary

```
Login → Dashboard → Review Requests → Approve/Reject → Manage Records
          ↓
      Facility Management → User Verification → Reports
```

## 🛡️ Administrative Features

### **User Management**
- **Ban System**: Integrated with user management
- **Role Control**: Resident vs Official access
- **Verification**: Approve resident verification requests
- **Discount Rates**: Set user-specific discounts

### **Booking Oversight**
- **Real-time Updates**: Live booking status tracking
- **Approval Workflow**: Multi-step approval process
- **Rejection Reasons**: Detailed rejection tracking
- **Bulk Operations**: Mass approval/rejection capabilities

### **System Administration**
- **Facility Management**: Complete CRUD operations
- **Time Slot Configuration**: Dynamic availability
- **User Analytics**: Usage statistics and reports
- **System Health**: Monitoring and maintenance

## 📊 Official Dashboard Features

### **Main Tabs**:
1. **Home**: Overview and statistics
2. **Booking Requests**: Pending approvals
3. **Authentication**: User verification
4. **Records**: Historical data
5. **Facilities**: Resource management

### **Quick Actions**:
- **Approve All**: Bulk approval
- **Export Reports**: Data export
- **System Settings**: Configuration
- **User Search**: Find specific users

## 🔗 Official API Integration

All official features use HTTP API calls with:
- **Enhanced Permissions**: Official-level access
- **Administrative Functions**: User management capabilities
- **Bulk Operations**: Efficient processing
- **Audit Trail**: Complete action logging

## 🎯 Official Responsibilities

### **Primary Duties**:
1. **Review Booking Requests**: Ensure proper facility usage
2. **Verify Residents**: Process verification applications
3. **Manage Facilities**: Maintain resource availability
4. **Monitor System**: Ensure smooth operations
5. **Generate Reports**: Track barangay activities

### **Decision Making**:
- **Booking Approvals**: Based on availability and rules
- **User Verification**: Document validation
- **Resource Allocation**: Fair distribution
- **Policy Enforcement**: Ensure compliance
