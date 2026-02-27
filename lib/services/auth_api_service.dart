import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:shared_preferences/shared_preferences.dart';
import 'api_service.dart';
import 'data_service.dart';

class AuthApiService {
  static AuthApiService? _instance;
  static AuthApiService get instance => _instance ??= AuthApiService._();
  
  AuthApiService._();

  Map<String, dynamic>? _currentUser;
  bool _isInitialized = false;

  // Get auth token from SharedPreferences
  static Future<String?> _getToken() async {
    final prefs = await SharedPreferences.getInstance();
    return prefs.getString('auth_token');
  }

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
          // Set current user
          _currentUser = data['user'];
          
          // CRITICAL: Clear verification status cache to prevent data isolation leaks
          await clearVerificationStatus();
          
          // Save authentication token and persist session like in login
          try {
            final prefs = await SharedPreferences.getInstance();
            
            // Save auth token
            if (data['token'] != null) {
              await prefs.setString('auth_token', data['token']);
              print('🔍 Saved auth token during registration');
            }
            
            // Save user data
            await prefs.setString('user_email', _currentUser!['email'] ?? '');
            await prefs.setString('user_full_name', _currentUser!['full_name'] ?? '');
            await prefs.setString('user_role', _currentUser!['role'] ?? '');
            await prefs.setBool('user_verified', _currentUser!['verified'] ?? false);
            await prefs.setString('user_verification_type', _currentUser!['verification_type']?.toString() ?? '');
            await prefs.setDouble('user_discount_rate', (_currentUser!['discount_rate'] ?? 0).toDouble());
            await prefs.setString('user_contact_number', _currentUser!['contact_number'] ?? '');
            await prefs.setString('user_address', _currentUser!['address'] ?? '');
            await prefs.setString('user_created_at', _currentUser!['created_at'] ?? '');
            await prefs.setInt('user_id', _currentUser!['id'] ?? 0);
            
            print('🔍 Saved user session during registration');
          } catch (e) {
            print('❌ AuthApiService SharedPreferences error during registration: $e');
          }
          
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
        
        // CRITICAL: Clear verification status cache to prevent data isolation leaks
        await clearVerificationStatus();
        
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
          // Save profile photo to SharedPreferences
          if (user['profile_photo_url'] != null && user['profile_photo_url'].toString().isNotEmpty) {
            await prefs.setString('user_profile_photo_url', user['profile_photo_url'].toString());
            print('🔍 Saved profile photo to SharedPreferences during login: ${user['profile_photo_url']}');
          }
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
        
        // CRITICAL: Clear verification status cache to prevent data isolation leaks
        await clearVerificationStatus();
        
        print('✅ User restored successfully');
        
        // Load profile photo from SharedPreferences as fallback
        final profilePhotoUrl = prefs.getString('user_profile_photo_url');
        if (profilePhotoUrl != null && profilePhotoUrl.isNotEmpty) {
          _currentUser!['profile_photo_url'] = profilePhotoUrl;
          print('🔍 Loaded profile photo from SharedPreferences during restore: $profilePhotoUrl');
        }
        
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
      return {'success': false, 'message': 'Network error: $e'};
    }
  }

  // Refresh current user data from server
  Future<Map<String, dynamic>?> refreshCurrentUser() async {
    try {
      final token = await _getToken();
      if (token == null) return null;
      
      final userEmail = getUserEmail();
      if (userEmail == null) return null;
      
      final response = await http.get(
        Uri.parse('${ApiService.baseUrl}/api/users/profile/$userEmail'),
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer $token',
        },
      );

      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        if (data['success'] == true) {
          final user = data['user'];
          
          // Convert integer booleans to actual booleans and handle verification types
          Map<String, dynamic> processedUser = Map<String, dynamic>.from(user);
          
          // Handle verification status properly - support both int and bool types
          dynamic verifiedStatus = processedUser['verified'];
          if (verifiedStatus is bool) {
            // Server returned boolean (true/false)
            if (verifiedStatus == true) {
              // Check verification_type to determine resident vs non-resident
              String? verificationType = processedUser['verification_type'];
              if (verificationType == 'resident') {
                processedUser['verified'] = true;
                processedUser['verification_type'] = 'resident';
              } else if (verificationType == 'non-resident') {
                processedUser['verified'] = true;
                processedUser['verification_type'] = 'non-resident';
              } else {
                // Default to resident if type is missing
                processedUser['verified'] = true;
                processedUser['verification_type'] = 'resident';
              }
            } else {
              processedUser['verified'] = false;
              processedUser['verification_type'] = null;
            }
          } else if (verifiedStatus is int) {
            // Server returned integer (0, 1, 2)
            int status = verifiedStatus;
            if (status == 1) {
              processedUser['verified'] = true;
              processedUser['verification_type'] = 'resident';
            } else if (status == 2) {
              processedUser['verified'] = true;
              processedUser['verification_type'] = 'non-resident';
            } else {
              processedUser['verified'] = false;
              processedUser['verification_type'] = null;
            }
          } else {
            // Fallback
            processedUser['verified'] = false;
            processedUser['verification_type'] = null;
          }
          
          processedUser['email_verified'] = processedUser['email_verified'] == 1 || processedUser['email_verified'] == true;
          processedUser['is_active'] = processedUser['is_active'] == 1 || processedUser['is_active'] == true;
          
          // Merge with existing user data to preserve fields like profile_photo_url
          if (_currentUser != null) {
            _currentUser = {..._currentUser!, ...processedUser};
          } else {
            _currentUser = processedUser;
          }
          
          print('🔍 Verification status after merge:');
          print('  - verified: ${_currentUser!['verified']} (${_currentUser!['verified'].runtimeType})');
          print('  - verification_type: ${_currentUser!['verification_type']}');
          print('  - isVerifiedResident(): ${isVerifiedResident()}');
          print('  - isVerifiedNonResident(): ${isVerifiedNonResident()}');
          print('  - isUserVerified(): ${isUserVerified()}');
          
          // Update SharedPreferences with fresh data
          final prefs = await SharedPreferences.getInstance();
          await prefs.setString('user_name', processedUser['full_name']?.toString() ?? '');
          await prefs.setDouble('user_discount_rate', (processedUser['discount_rate'] ?? 0.0).toDouble());
          await prefs.setBool('user_verified', processedUser['verified'] ?? false);
          
          // Preserve existing profile photo if server has empty one
          final existingProfilePhoto = prefs.getString('user_profile_photo_url');
          final serverProfilePhoto = processedUser['profile_photo_url']?.toString() ?? '';
          
          if (serverProfilePhoto.isNotEmpty) {
            // Server has profile photo, use it
            await prefs.setString('user_profile_photo_url', serverProfilePhoto);
            print('🔍 Updated profile photo from server: $serverProfilePhoto');
          } else if (existingProfilePhoto != null && existingProfilePhoto.isNotEmpty) {
            // Server has empty profile photo, preserve existing one
            await prefs.setString('user_profile_photo_url', existingProfilePhoto);
            print('🔍 Preserved existing profile photo: $existingProfilePhoto');
            // Update current user with preserved photo
            _currentUser!['profile_photo_url'] = existingProfilePhoto;
          }
          
          print('🔍 User data refreshed from server');
          return processedUser;
        }
      }
      return null;
    } catch (e) {
      print('❌ Error refreshing user data: $e');
      return null;
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
      if (userData['profile_photo_url'] != null) {
        await prefs.setString('user_profile_photo_url', userData['profile_photo_url']);
        print('🔍 Saved profile photo to SharedPreferences: ${userData['profile_photo_url']}');
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
      // Prioritize SharedPreferences (most recent manual update)
      final profilePhotoUrl = _currentUser!['profile_photo_url']?.toString() ?? '';
      if (profilePhotoUrl.isNotEmpty) {
        print('🔍 getUserProfilePhoto: Using current user photo: $profilePhotoUrl');
        return profilePhotoUrl;
      }
    }
    return '';
  }

  bool isVerifiedResident() {
    if (_currentUser != null) {
      final verified = _currentUser!['verified'] == true;
      final verificationType = _currentUser!['verification_type'] == 'resident';
      final discountRate = _currentUser!['discount_rate'] == 0.1;
      final result = verified && (verificationType || discountRate);
      
      print('🔍 isVerifiedResident() debug:');
      print('  - verified: $verified');
      print('  - verification_type: ${_currentUser!['verification_type']} (resident: $verificationType)');
      print('  - discount_rate: ${_currentUser!['discount_rate']} (0.1: $discountRate)');
      print('  - final result: $result');
      
      return result;
    }
    return false;
  }

  bool isVerifiedNonResident() {
    if (_currentUser != null) {
      final verified = _currentUser!['verified'] == true;
      final verificationType = _currentUser!['verification_type'] == 'non-resident';
      final discountRate = _currentUser!['discount_rate'] == 0.05;
      final result = verified && (verificationType || discountRate);
      
      print('🔍 isVerifiedNonResident() debug:');
      print('  - verified: $verified');
      print('  - verification_type: ${_currentUser!['verification_type']} (non-resident: $verificationType)');
      print('  - discount_rate: ${_currentUser!['discount_rate']} (0.05: $discountRate)');
      print('  - final result: $result');
      
      return result;
    }
    return false;
  }

  // Verification Status Management - Data Isolation
  static Map<String, dynamic>? _verificationStatus;

  static Future<Map<String, dynamic>?> getVerificationStatus() async {
    // Always fetch fresh verification status to prevent data isolation leaks
    // Remove caching to ensure real-time data consistency
    
    final instance = AuthApiService.instance;
    final currentUser = await instance.getCurrentUser();
    if (currentUser != null) {
      final status = await DataService.checkVerificationStatus(currentUser['id']);
      if (status['success']) {
        _verificationStatus = status;
        return status;
      }
    }
    return null;
  }

  static Future<void> clearVerificationStatus() async {
    _verificationStatus = null;
  }

  static Future<void> updateVerificationStatus(Map<String, dynamic> status) async {
    _verificationStatus = status;
  }

  static bool canSubmitVerification() {
    return _verificationStatus?['can_submit'] ?? true;
  }

  static String verificationLockMessage() {
    return _verificationStatus?['lock_message'] ?? '';
  }

  static String currentVerificationStatus() {
    return _verificationStatus?['current_status'] ?? 'none';
  }
}
