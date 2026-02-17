import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:shared_preferences/shared_preferences.dart';
import 'api_service.dart';
import '../config/app_config.dart';
import 'dart:async';

class AuthApiService {
  static final AuthApiService _instance = AuthApiService._internal();
  factory AuthApiService() => _instance;
  AuthApiService._internal();

  Map<String, dynamic>? _currentUser;
  bool _isInitialized = false;

  // Initialize user session
  Future<void> initializeUser() async {
    if (_isInitialized) return;
    
    try {
      print('🔍 Initializing user session...');
      await restoreUserFromToken();
      _isInitialized = true;
      print('🔍 User session initialized');
    } catch (e) {
      print('❌ Error initializing user session: $e');
      _isInitialized = true; // Prevent infinite retry
    }
  }

  // Get current user
  Map<String, dynamic>? get currentUser => _currentUser;

  // Check if user is authenticated
  bool get isAuthenticated => _currentUser != null;

  // Ensure user is loaded
  Future<Map<String, dynamic>?> ensureUserLoaded() async {
    if (!_isInitialized) {
      await initializeUser();
    }
    
    if (_currentUser == null) {
      await restoreUserFromToken();
    }
    
    return _currentUser;
  }

  // Note: Ban detection logic removed - user will implement new approach

  // Register user
  Future<Map<String, dynamic>> registerWithEmailAndPassword(
    String name, 
    String email, 
    String password, 
    {String role = 'resident'}
  ) async {
    try {
      print('🔍 Registering user: $email');
      
      final response = await http.post(
        Uri.parse('${ApiService.baseUrl}/api/auth/register'),
        headers: await ApiService.getHeaders(includeAuth: false),
        body: json.encode({
          'name': name,
          'email': email,
          'password': password,
          'role': role,
        }),
      );

      print('🔍 Registration response status: ${response.statusCode}');
      print('🔍 Registration response body: ${response.body}');

      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        if (data['success'] == true) {
          _currentUser = data['user'];
          return data;
        } else {
          return {'success': false, 'message': data['message'] ?? 'Registration failed'};
        }
      } else {
        // For non-200 status codes, try to parse error message from response body
        try {
          final errorData = json.decode(response.body);
          return {'success': false, 'message': errorData['message'] ?? 'Server error: ${response.statusCode}'};
        } catch (e) {
          return {'success': false, 'message': 'Server error: ${response.statusCode}'};
        }
      }
    } catch (e) {
      print('❌ Registration exception: $e');
      return {'success': false, 'message': 'Network error: $e'};
    }
  }

  // Login user
  Future<Map<String, dynamic>> signInWithEmailAndPassword(
    String email, 
    String password, 
    {String role = 'resident'}
  ) async {
    try {
      print('🔍 Login attempt for email: $email');
      
      final result = await ApiService.login(email, password);
      
      if (result['success'] == true) {
        print('🔍 AuthApiService: Processing successful login...');
        
        // Convert integer booleans to actual booleans and handle verification types
        Map<String, dynamic> user = Map<String, dynamic>.from(result['user']);
        
        print('🔍 AuthApiService: Converting boolean fields...');
        print('🔍 AuthApiService: verified = ${user['verified']} (${user['verified'].runtimeType})');
        print('🔍 AuthApiService: email_verified = ${user['email_verified']} (${user['email_verified'].runtimeType})');
        print('🔍 AuthApiService: is_active = ${user['is_active']} (${user['is_active'].runtimeType})');
        
        // Handle verification status properly - support both int and bool types
        dynamic verifiedStatus = user['verified'];
        if (verifiedStatus is bool) {
          // Server returned boolean (true/false)
          if (verifiedStatus == true) {
            // Check verification_type to determine resident vs non-resident
            String? verificationType = user['verification_type'];
            if (verificationType == 'resident') {
              user['verified'] = true;
              user['verification_type'] = 'resident';
            } else if (verificationType == 'non-resident') {
              user['verified'] = true;
              user['verification_type'] = 'non-resident';
            } else {
              // Default to resident if type is missing
              user['verified'] = true;
              user['verification_type'] = 'resident';
            }
          } else {
            user['verified'] = false;
            user['verification_type'] = null;
          }
        } else if (verifiedStatus is int) {
          // Server returned integer (0, 1, 2)
          int status = verifiedStatus;
          if (status == 1) {
            user['verified'] = true;
            user['verification_type'] = 'resident';
          } else if (status == 2) {
            user['verified'] = true;
            user['verification_type'] = 'non-resident';
          } else {
            user['verified'] = false;
            user['verification_type'] = null;
          }
        } else {
          // Fallback
          user['verified'] = false;
          user['verification_type'] = null;
        }
        
        user['email_verified'] = user['email_verified'] == 1 || user['email_verified'] == true;
        user['is_active'] = user['is_active'] == 1 || user['is_active'] == true;
        
        print('🔍 AuthApiService: Boolean conversion completed');
        
        _currentUser = user;
        
        // Note: Ban checking removed - user will implement new approach
        
        // Save user data to SharedPreferences
        final prefs = await SharedPreferences.getInstance();
        try {
          await prefs.setString('auth_token', result['token'] ?? '');
          await prefs.setString('user_email', user['email']?.toString() ?? '');
          await prefs.setString('user_id', user['id']?.toString() ?? '0');
          await prefs.setString('user_name', user['full_name']?.toString() ?? '');
          await prefs.setString('user_role', user['role']?.toString() ?? '');
          await prefs.setBool('user_verified', user['verified'] ?? false);
          await prefs.setDouble('user_discount_rate', (user['discount_rate'] ?? 0.0).toDouble());
        } catch (e) {
          print('❌ AuthApiService SharedPreferences error: $e');
          print('❌ User data: $user');
          throw e;
        }
        
        print('✅ Login successful');
        return {'success': true, 'user': user, 'token': result['token']};
      } else {
        print('❌ Login failed: ${result['message']}');
        return result;
      }
    } catch (e) {
      print('❌ Login exception: $e');
      return {'success': false, 'message': 'Network error: $e'};
    }
  }

  // Restore user from token
  Future<Map<String, dynamic>?> restoreUserFromToken() async {
    try {
      print('🔍 Restoring user from token...');
      
      final prefs = await SharedPreferences.getInstance();
      final userEmail = prefs.getString('user_email');
      
      if (userEmail == null) {
        print('❌ No user email found in storage');
        _currentUser = null;
        return null;
      }
      
      final result = await ApiService.getCurrentUser(email: userEmail);
      
      if (result['success'] == true && result['user'] != null) {
        // Convert integer booleans to actual booleans and handle verification types
        Map<String, dynamic> user = Map<String, dynamic>.from(result['user']);
        
        // Handle verification status properly - support both int and bool types
        dynamic verifiedStatus = user['verified'];
        if (verifiedStatus is bool) {
          // Server returned boolean (true/false)
          if (verifiedStatus == true) {
            // Check verification_type to determine resident vs non-resident
            String? verificationType = user['verification_type'];
            if (verificationType == 'resident') {
              user['verified'] = true;
              user['verification_type'] = 'resident';
            } else if (verificationType == 'non-resident') {
              user['verified'] = true;
              user['verification_type'] = 'non-resident';
            } else {
              // Default to resident if type is missing
              user['verified'] = true;
              user['verification_type'] = 'resident';
            }
          } else {
            user['verified'] = false;
            user['verification_type'] = null;
          }
        } else if (verifiedStatus is int) {
          // Server returned integer (0, 1, 2)
          int status = verifiedStatus;
          if (status == 1) {
            user['verified'] = true;
            user['verification_type'] = 'resident';
          } else if (status == 2) {
            user['verified'] = true;
            user['verification_type'] = 'non-resident';
          } else {
            user['verified'] = false;
            user['verification_type'] = null;
          }
        } else {
          // Fallback
          user['verified'] = false;
          user['verification_type'] = null;
        }
        
        user['email_verified'] = user['email_verified'] == 1 || user['email_verified'] == true;
        user['is_active'] = user['is_active'] == 1 || user['is_active'] == true;
        
        _currentUser = user;
        print('✅ User restored successfully');
        
        // Note: Ban checking removed - user will implement new approach
        
        return _currentUser;
      } else {
        print('❌ Failed to restore user: ${result['error']}');
        _currentUser = null;
        return null;
      }
    } catch (e) {
      print('❌ Restore user exception: $e');
      _currentUser = null;
      return null;
    }
  }

  // Get current user data
  Future<Map<String, dynamic>?> getCurrentUser() async {
    if (_currentUser != null) {
      return _currentUser;
    }
    
    return await restoreUserFromToken();
  }

  // Check if user is verified
  bool isUserVerified() {
    if (_currentUser == null) return false;
    
    // Check different possible field names for verification status
    return _currentUser!['verified'] == true ||
           _currentUser!['is_verified'] == true ||
           _currentUser!['emailVerified'] == true;
  }

  // Get user discount rate
  double getUserDiscountRate() {
    if (_currentUser == null) return 0.0;
    
    // Check different possible field names for discount rate
    final discountRate = _currentUser!['discount_rate'] ?? 
                        _currentUser!['discountRate'] ?? 
                        _currentUser!['user_discount_rate'] ?? 
                        0.0;
    
    // Convert to double if needed
    if (discountRate is String) {
      return double.tryParse(discountRate) ?? 0.0;
    } else if (discountRate is int) {
      return discountRate.toDouble();
    } else if (discountRate is double) {
      return discountRate;
    }
    
    return 0.0;
  }

  // Get user ID
  String? getUserId() {
    if (_currentUser == null) return null;
    return _currentUser!['id']?.toString();
  }

  // Get user role
  String? getUserRole() {
    if (_currentUser == null) return null;
    return _currentUser!['role']?.toString();
  }

  // Get user email
  String? getUserEmail() {
    if (_currentUser == null) return null;
    return _currentUser!['email']?.toString();
  }

  // Get user name
  String? getUserName() {
    if (_currentUser == null) return null;
    return _currentUser!['full_name']?.toString() ?? 
           _currentUser!['name']?.toString() ?? 
           'User';
  }

  // Check if user is official
  bool isOfficial() {
    final role = getUserRole();
    return role == 'official';
  }

  // Check if user is resident
  bool isResident() {
    final role = getUserRole();
    return role == 'resident';
  }

  // Get user profile
  Future<Map<String, dynamic>?> getUserProfile() async {
    try {
      final userId = getUserId();
      if (userId == null) return null;
      
      final response = await http.get(
        Uri.parse('${ApiService.baseUrl}/api/users/$userId'),
        headers: await ApiService.getHeaders(),
      );

      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        if (data['success'] == true) {
          return data['user'];
        }
      }
      
      return null;
    } catch (e) {
      print('❌ Get user profile exception: $e');
      return null;
    }
  }

  // Update user profile
  Future<Map<String, dynamic>> updateUserProfile(Map<String, dynamic> userData) async {
    try {
      final userId = getUserId();
      if (userId == null) {
        return {'success': false, 'message': 'User not logged in'};
      }
      
      final response = await http.put(
        Uri.parse('${ApiService.baseUrl}/api/users/$userId'),
        headers: await ApiService.getHeaders(),
        body: json.encode(userData),
      );

      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        if (data['success'] == true) {
          // Update current user data
          _currentUser = {...?_currentUser, ...data['user']};
          return data;
        } else {
          return {'success': false, 'message': data['message'] ?? 'Update failed'};
        }
      } else {
        // For non-200 status codes, try to parse error message from response body
        try {
          final errorData = json.decode(response.body);
          return {'success': false, 'message': errorData['message'] ?? 'Server error: ${response.statusCode}'};
        } catch (e) {
          return {'success': false, 'message': 'Server error: ${response.statusCode}'};
        }
      }
    } catch (e) {
      print('❌ Update user profile exception: $e');
      return {'success': false, 'message': 'Network error: $e'};
    }
  }

  // Logout user
  Future<Map<String, dynamic>> signOut() async {
    try {
      print('🔍 Signing out user...');
      
      final result = await ApiService.logout();
      
      // Clear local data
      _currentUser = null;
      _isInitialized = false;
      
      print('✅ User signed out successfully');
      return result;
    } catch (e) {
      print('❌ Sign out exception: $e');
      // Still clear local data even if network fails
      _currentUser = null;
      _isInitialized = false;
      return {'success': true, 'message': 'Signed out successfully'};
    }
  }

  // Clear all user data (for testing/debugging)
  Future<void> clearUserData() async {
    try {
      await ApiService.clearUserData();
      _currentUser = null;
      _isInitialized = false;
      print('🔍 Cleared all user data');
    } catch (e) {
      print('❌ Clear user data exception: $e');
    }
  }

  // Save user email to preferences (for compatibility)
  Future<void> _saveUserEmail(String email) async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString('user_email', email);
  }

  // Get user email from preferences (for compatibility)
  Future<String?> _getUserEmail() async {
    final prefs = await SharedPreferences.getInstance();
    return prefs.getString('user_email');
  }

  // Remove user email from preferences (for compatibility)
  Future<void> _removeUserEmail() async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.remove('user_email');
  }

  // Debug method to print current user info
  void debugPrintCurrentUser() {
    if (_currentUser != null) {
      print('🔍 Current User Debug Info:');
      print('  ID: ${getUserId()}');
      print('  Email: ${getUserEmail()}');
      print('  Name: ${getUserName()}');
      print('  Role: ${getUserRole()}');
      print('  Verified: ${isUserVerified()}');
      print('  Discount Rate: ${getUserDiscountRate()}');
      print('  Is Official: ${isOfficial()}');
      print('  Is Resident: ${isResident()}');
    } else {
      print('🔍 No current user logged in');
    }
  }

  // Update current user data
  Future<void> updateCurrentUser(Map<String, dynamic> userData) async {
    try {
      final prefs = await SharedPreferences.getInstance();
      
      // Update local storage
      if (userData['id'] != null) {
        await prefs.setString('user_id', userData['id'].toString());
      }
      if (userData['full_name'] != null) {
        await prefs.setString('user_name', userData['full_name']);
      }
      if (userData['verified'] != null) {
        await prefs.setBool('user_verified', userData['verified']);
      }
      if (userData['discount_rate'] != null) {
        await prefs.setDouble('user_discount_rate', userData['discount_rate'].toDouble());
      }
      
      // Update current user object
      if (_currentUser != null) {
        _currentUser = {...?_currentUser, ...userData};
      }
      
      print('✅ User data updated successfully');
    } catch (e) {
      print('❌ Error updating user data: $e');
    }
  }

  // Additional helper methods for compatibility
  String getUserFullName() {
    return getUserName() ?? 'User';
  }

  String getUserContactNumber() {
    if (_currentUser != null) {
      return _currentUser!['contact_number'] ?? '';
    }
    return '';
  }

  String getUserProfilePhoto() {
    if (_currentUser != null) {
      return _currentUser!['profile_photo_url'] ?? '';
    }
    return '';
  }

  bool isVerifiedResident() {
    if (_currentUser != null) {
      return _currentUser!['verified'] == true && 
             (_currentUser!['verification_type'] == 'resident' || 
              _currentUser!['discount_rate'] == 0.1);
    }
    return false;
  }

  bool isVerifiedNonResident() {
    if (_currentUser != null) {
      return _currentUser!['verified'] == true && 
             (_currentUser!['verification_type'] == 'non-resident' || 
              _currentUser!['discount_rate'] == 0.05);
    }
    return false;
  }
}
