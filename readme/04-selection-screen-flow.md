# Selection Screen Flow Documentation

## 🎯 Role Selection Process

### **File**: `lib/screens/selection_screen.dart`

---

## 📱 Screen Overview

The selection screen serves as the **central entry point** for all users, directing them to appropriate workflows based on their role selection.

---

## 🔄 User Flow Process

### **1. Initial Screen Load**
```dart
// Selection Screen Initialization
class SelectionScreen extends StatefulWidget {
  final GlobalKey<NavigatorState> navigatorKey;
  
  // Screen displays role selection options
  // Checks for existing user session
  // Shows branding and welcome message
}
```

### **2. Role Selection Options**

#### **🏠 Resident Role**
- **Button**: "I'm a Resident"
- **Navigation**: `resident_login_screen.dart`
- **Purpose**: Access resident booking and verification features

#### **🏛️ Official Role**
- **Button**: "I'm a Barangay Official"
- **Navigation**: `official_login_screen.dart`
- **Purpose**: Access administrative and management features

---

## 📋 Code Flow Analysis

### **Before Role Selection**

```dart
// Selection Screen State Management
class _SelectionScreenState extends State<SelectionScreen> {
  
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Column(
        children: [
          // App branding and logo
          _buildHeader(),
          
          // Role selection buttons
          _buildRoleButtons(),
          
          // Additional options
          _buildAdditionalOptions(),
        ],
      ),
    );
  }
}
```

### **Role Button Implementation**

```dart
// Resident Role Selection
ElevatedButton(
  onPressed: () {
    Navigator.push(
      context,
      MaterialPageRoute(
        builder: (context) => ResidentLoginScreen(),
      ),
    );
  },
  child: Text('I\'m a Resident'),
),

// Official Role Selection  
ElevatedButton(
  onPressed: () {
    Navigator.push(
      context,
      MaterialPageRoute(
        builder: (context) => OfficialLoginScreen(),
      ),
    );
  },
  child: Text('I\'m a Barangay Official'),
),
```

---

## 🔄 Navigation Flow

### **Resident Path**:
```
Selection Screen → Resident Login → Resident Dashboard → Booking Features
     ↓
Account Settings → Verification → Profile Management
```

### **Official Path**:
```
Selection Screen → Official Login → Official Dashboard → Administrative Features
     ↓
Booking Management → User Verification → Facility Management
```

---

## 🎨 UI Components

### **Main Structure**:
- **Header**: App logo and welcome message
- **Role Selection**: Two prominent buttons for role choice
- **Footer**: Additional options and support information

### **Design Elements**:
- **Color Scheme**: Barangay-themed colors
- **Typography**: Clear, readable fonts
- **Button Styling**: Distinct visual hierarchy
- **Responsive**: Works on all screen sizes

---

## 🔐 Authentication Integration

### **Session Check**:
```dart
// Check for existing session
@override
void initState() {
  super.initState();
  _checkExistingSession();
}

Future<void> _checkExistingSession() async {
  // Check if user is already logged in
  // Navigate directly to appropriate dashboard
  // Skip login if valid session exists
}
```

### **Role-Based Routing**:
```dart
// Navigate based on role
void _navigateToRole(String role) {
  switch (role) {
    case 'resident':
      Navigator.pushReplacementNamed(context, '/resident-dashboard');
      break;
    case 'official':
      Navigator.pushReplacementNamed(context, '/official-dashboard');
      break;
  }
}
```

---

## 📱 User Experience Flow

### **First-Time User**:
1. **Launch App** → Selection Screen appears
2. **Choose Role** → Tap appropriate role button
3. **Login Screen** → Enter credentials
4. **Dashboard** → Access role-specific features

### **Returning User**:
1. **Launch App** → Check for existing session
2. **Auto-Login** → Navigate directly to dashboard
3. **Skip Selection** → Already authenticated

---

## 🛠️ Technical Implementation

### **Key Methods**:

#### **Role Navigation**:
```dart
void _navigateToResidentLogin() {
  Navigator.push(
    context,
    MaterialPageRoute(builder: (context) => ResidentLoginScreen()),
  );
}

void _navigateToOfficialLogin() {
  Navigator.push(
    context,
    MaterialPageRoute(builder: (context) => OfficialLoginScreen()),
  );
}
```

#### **Session Management**:
```dart
Future<void> _checkExistingSession() async {
  final userData = await AuthApiService().getCurrentUserData();
  if (userData != null) {
    _navigateToDashboard(userData['role']);
  }
}
```

---

## 🎯 Business Logic

### **Role Determination**:
- **Resident**: Access booking, verification, profile features
- **Official**: Access administrative, management, approval features
- **Separation**: Clear distinction between user types

### **Security Considerations**:
- **Role Validation**: Server confirms user role
- **Session Security**: Secure token management
- **Access Control**: Role-based feature access

---

## 📊 Error Handling

### **Navigation Errors**:
```dart
try {
  Navigator.push(context, MaterialPageRoute(...));
} catch (e) {
  // Handle navigation errors
  ScaffoldMessenger.of(context).showSnackBar(
    SnackBar(content: Text('Navigation error: $e')),
  );
}
```

### **Session Validation**:
```dart
// Validate session before navigation
if (await _isSessionValid()) {
  _navigateToDashboard();
} else {
  _clearSessionAndShowLogin();
}
```

---

## 🔄 Future Enhancements

### **Potential Improvements**:
1. **Role Preview**: Show feature preview for each role
2. **Quick Demo**: Demo mode for unauthenticated users
3. **Role Switching**: Allow users with multiple roles
4. **Biometric Login**: Fingerprint/face recognition
5. **Offline Mode**: Basic functionality without internet

### **Scalability Considerations**:
- **Multiple Roles**: Support for additional user types
- **Dynamic Routing**: Configuration-based navigation
- **Theme Support**: Role-based UI themes
- **Accessibility**: Screen reader and keyboard navigation

---

## 🎯 Summary

The selection screen serves as the **critical gateway** to the barangay reservation system, ensuring users are properly routed to their appropriate workflows based on their role. It provides:

- ✅ **Clear Role Distinction**: Resident vs Official paths
- ✅ **Intuitive Navigation**: Simple button-based selection
- ✅ **Session Management**: Automatic login for returning users
- ✅ **Error Handling**: Graceful failure management
- ✅ **User Experience**: Smooth transition to features

This design ensures users can quickly and easily access the appropriate features for their role in the barangay system.
