import 'dart:convert';
import 'dart:typed_data';
import 'package:http/http.dart' as http;
import 'package:shared_preferences/shared_preferences.dart';
import 'package:url_launcher/url_launcher.dart';
import 'package:image_picker/image_picker.dart';
import 'base64_image_service.dart';
import '../config/app_config.dart';
import 'ban_detection_service.dart';

class ApiService {
  // Dynamic server URL - works with Python Flask server
  static String get baseUrl => AppConfig.baseUrl;
  
  // Token management (JWT-like tokens from new backend)
  static Future<void> _saveToken(String token) async {
    try {
      print('🔍 _saveToken called with token: $token');
      print('🔍 Token type: ${token.runtimeType}');
      
      final prefs = await SharedPreferences.getInstance();
      print('🔍 SharedPreferences instance created');
      
      await prefs.setString('auth_token', token);
      print('🔍 Token saved to SharedPreferences');
      
      print('🔍 Saved auth token: $token');
    } catch (e) {
      print('❌ _saveToken error: $e');
      print('❌ Token type: ${token.runtimeType}');
      print('❌ Stack trace: ${StackTrace.current}');
    }
  }

  static Future<Map<String, dynamic>> updateUserProfile(Map<String, dynamic> userData) async {
    try {
      final token = await _getToken();
      if (token == null) {
        return {'success': false, 'message': 'No authentication token found'};
      }

      final url = '$baseUrl/api/users/profile';
      print('📝 Updating user profile at: $url');
      print('📝 Profile data: $userData');

      final response = await http.post(
        Uri.parse(url),
        headers: await getHeaders(),
        body: json.encode(userData),
      );

      print('📥 Profile update response status: ${response.statusCode}');

      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        print('📥 Profile update response: $data');
        if (data['success'] == true) {
          // Update local user data
          final prefs = await SharedPreferences.getInstance();
          await prefs.setString('user_email', userData['email'] ?? '');
          
          return {'success': true, 'message': 'Profile updated successfully'};
        } else {
          return {'success': false, 'message': data['message'] ?? 'Failed to update profile'};
        }
      } else {
        print('❌ Profile update error response: ${response.body}');
        return {'success': false, 'message': 'Server error: ${response.statusCode}'};
      }
    } catch (e) {
      print('❌ updateUserProfile error: $e');
      print('❌ Error type: ${e.runtimeType}');
      return {'success': false, 'message': 'Network error: $e'};
    }
  }

  static Future<Map<String, dynamic>> getVerificationStatus(String userId) async {
    try {
      final token = await _getToken();
      if (token == null) {
        return {'success': false, 'message': 'No authentication token found'};
      }

      final response = await http.get(
        Uri.parse('$baseUrl/api/users/verification-status/$userId'),
        headers: await getHeaders(),
      );

      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        return {'success': true, 'data': data['data']};
      } else {
        return {'success': false, 'message': 'Failed to check verification status'};
      }
    } catch (e) {
      print('❌ getVerificationStatus error: $e');
      return {'success': false, 'message': 'Network error: $e'};
    }
  }

  static Future<Map<String, dynamic>> createVerificationRequest(Map<String, dynamic> verificationData) async {
    try {
      final token = await _getToken();
      if (token == null) {
        return {'success': false, 'message': 'No authentication token found'};
      }

      final response = await http.post(
        Uri.parse('$baseUrl/api/users/verification-request'),
        headers: await getHeaders(),
        body: json.encode(verificationData),
      );

      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        return {'success': true, 'message': data['message'] ?? 'Verification request submitted'};
      } else {
        return {'success': false, 'message': 'Failed to submit verification request'};
      }
    } catch (e) {
      print('❌ createVerificationRequest error: $e');
      return {'success': false, 'message': 'Network error: $e'};
    }
  }

  static Future<String?> _getToken() async {
    final prefs = await SharedPreferences.getInstance();
    final token = prefs.getString('auth_token');
    print('🔍 Retrieved auth token: $token');
    return token;
  }
  
  static Future<void> _removeToken() async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.remove('auth_token');
    print('🔍 Removed auth token');
  }

  // Headers (JWT Bearer token authentication)
  static Future<Map<String, String>> getHeaders({bool includeAuth = true}) async {
    Map<String, String> headers = {
      'Content-Type': 'application/json',
      'Accept': 'application/json',
    };

    if (includeAuth) {
      final token = await _getToken();
      
      if (token != null) {
        headers['Authorization'] = 'Bearer $token';
        print('🔍 Adding JWT Bearer token for authentication');
      } else {
        print('🔍 No auth token available for authentication');
      }
    }

    return headers;
  }

  // Authentication
  static Future<Map<String, dynamic>> login(String email, String password) async {
    try {
      print('🔍 ApiService.login called');
      print('🔍 Using baseUrl: $baseUrl');
      print('🔍 Full login URL: $baseUrl/api/auth/login');
      print('🔍 Login data: email=$email');
      
      final response = await http.post(
        Uri.parse('$baseUrl/api/auth/login'),
        headers: await getHeaders(includeAuth: false),
        body: json.encode({
          'email': email,
          'password': password,
        }),
      );

      print('🔍 Login response status: ${response.statusCode}');
      print('🔍 Login response body: ${response.body}');

      if (response.statusCode == 200) {
        print('🔍 Parsing JSON response...');
        final data = json.decode(response.body);
        print('🔍 Parsed response data: $data');
        
        if (data['success'] == true) {
          print('🔍 Login successful, processing data...');
          
          // Save token and user data
          if (data['token'] != null) {
            print('🔍 About to save token...');
            await _saveToken(data['token']);
            print('🔍 Token saved successfully');
          } else {
            print('🔍 No token in response');
          }
          
          print('🔍 About to save user data...');
          // Save user data to preferences for easy access
          if (data['user'] != null) {
            print('🔍 User data found: ${data['user']}');
            final prefs = await SharedPreferences.getInstance();
            try {
              print('🔍 Saving basic user fields...');
              await prefs.setString('user_email', data['user']['email']?.toString() ?? '');
              await prefs.setString('user_id', data['user']['id']?.toString() ?? '0');
              await prefs.setString('user_name', data['user']['full_name']?.toString() ?? '');
              await prefs.setString('user_role', data['user']['role']?.toString() ?? 'resident');
              
              print('🔍 Converting boolean fields...');
              // Convert integer booleans to actual booleans with null safety
              final verified = data['user']['verified'];
              final emailVerified = data['user']['email_verified'];
              final isActive = data['user']['is_active'];
              
              print('🔍 Converting booleans: verified=$verified (${verified.runtimeType}), email_verified=$emailVerified (${emailVerified.runtimeType}), is_active=$isActive (${isActive.runtimeType})');
              
              print('🔍 Saving verified field...');
              await prefs.setBool('user_verified', (verified == 1 || verified == true) ?? false);
              print('🔍 Saving discount rate...');
              await prefs.setDouble('user_discount_rate', (data['user']['discount_rate'] ?? 0.0).toDouble());
              print('🔍 Saving contact number...');
              await prefs.setString('user_contact_number', data['user']['contact_number']?.toString() ?? '');
              print('🔍 Saving profile photo...');
              await prefs.setString('user_profile_photo_url', data['user']['profile_photo_url']?.toString() ?? '');
              print('🔍 User data saved successfully');
            } catch (e) {
              print('❌ SharedPreferences error: $e');
              print('❌ User data: ${data['user']}');
              throw e;
            }
          } else {
            print('🔍 No user data in response');
          }
          
          print('🔍 Returning success data...');
          return data;
        } else {
          print('🔍 Login failed: ${data['message']}');
          return {'success': false, 'message': data['message'] ?? 'Login failed'};
        }
      } else {
        print('🔍 HTTP error: ${response.statusCode}');
        // For non-200 status codes, try to parse error message from response body
        try {
          final errorData = json.decode(response.body);
          return {'success': false, 'message': errorData['message'] ?? 'Server error: ${response.statusCode}'};
        } catch (e) {
          return {'success': false, 'message': 'Server error: ${response.statusCode}'};
        }
      }
    } catch (e) {
      print('❌ ApiService.login exception: $e');
      return {'success': false, 'message': 'Network error: $e'};
    }
  }

  // Get current user
  static Future<Map<String, dynamic>> getCurrentUser({String? email}) async {
    try {
      String url = '$baseUrl/api/me';
      if (email != null) {
        url += '?email=$email';
      }
      
      final response = await http.get(
        Uri.parse(url),
        headers: await getHeaders(),
      );

      print('🔍 getCurrentUser response status: ${response.statusCode}');
      print('🔍 getCurrentUser response body: ${response.body}');

      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        return data;
      } else {
        return {'success': false, 'error': 'HTTP ${response.statusCode}'};
      }
    } catch (e) {
      print('❌ getCurrentUser exception: $e');
      return {'success': false, 'error': e.toString()};
    }
  }

  // Get facilities
  static Future<Map<String, dynamic>> getFacilities() async {
    try {
      final response = await http.get(
        Uri.parse('$baseUrl/api/facilities'),
        headers: await getHeaders(),
      );

      print('🔍 getFacilities response status: ${response.statusCode}');
      print('🔍 getFacilities response body: ${response.body}');

      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        return await _handleApiResponse(data, 'getFacilities');
      } else {
        return {'success': false, 'error': 'HTTP ${response.statusCode}'};
      }
    } catch (e) {
      print('❌ getFacilities exception: $e');
      return {'success': false, 'error': e.toString()};
    }
  }

  // Get bookings
  static Future<Map<String, dynamic>> getBookings({
    String? facilityId,
    String? date,
    String? status,
    String? userRole,
  }) async {
    try {
      // Build query parameters
      Map<String, String> queryParams = {};
      if (facilityId != null) queryParams['facility_id'] = facilityId;
      if (date != null) queryParams['date'] = date;
      if (status != null) queryParams['status'] = status;
      
      String queryString = queryParams.entries
          .map((e) => '${e.key}=${Uri.encodeComponent(e.value)}')
          .join('&');
      
      String url = '$baseUrl/api/bookings';
      if (queryString.isNotEmpty) {
        url += '?$queryString';
      }
      
      print('🔍 getBookings URL: $url');
      print('🔍 getBookings userRole: $userRole');

      final response = await http.get(
        Uri.parse(url),
        headers: await getHeaders(),
      );

      print('🔍 getBookings response status: ${response.statusCode}');

      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        if (data['success'] == true) {
          return data;
        } else {
          return {'success': false, 'error': data['error'] ?? 'Failed to get bookings'};
        }
      } else {
        print('🔍 getBookings - failed with status: ${response.statusCode}');
        return {'success': false, 'error': 'HTTP ${response.statusCode}'};
      }
    } catch (e) {
      print('❌ getBookings exception: $e');
      return {'success': false, 'error': e.toString()};
    }
  }

  // Create booking
  static Future<Map<String, dynamic>> createBooking(Map<String, dynamic> bookingData) async {
    try {
      print('🔍 createBooking called with data: $bookingData');
      
      final response = await http.post(
        Uri.parse('$baseUrl/api/bookings'),
        headers: await getHeaders(),
        body: json.encode(bookingData),
      );

      print('🔍 createBooking response status: ${response.statusCode}');
      print('🔍 createBooking response body: ${response.body}');

      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        
        // Handle response and check for ban status
        return await _handleApiResponse(data, 'createBooking');
      } else {
        // Try to parse error response for detailed error information
        try {
          final errorData = json.decode(response.body);
          return {
            'success': false, 
            'error': errorData['message'] ?? 'HTTP ${response.statusCode}',
            'error_type': errorData['error_type'],
            'ban_reason': errorData['ban_reason']
          };
        } catch (e) {
          return {'success': false, 'error': 'HTTP ${response.statusCode}'};
        }
      }
    } catch (e) {
      print('❌ createBooking exception: $e');
      return {'success': false, 'error': e.toString()};
    }
  }

  // Update booking status
  static Future<Map<String, dynamic>> updateBookingStatus(int bookingId, String status, {String? rejectionReason, String? rejectionType}) async {
    try {
      Map<String, dynamic> updateData = {
        'status': status,
      };
      
      if (rejectionReason != null) {
        updateData['rejection_reason'] = rejectionReason;
      }
      
      if (rejectionType != null) {
        updateData['rejection_type'] = rejectionType;
      }
      
      final response = await http.put(
        Uri.parse('$baseUrl/api/bookings/$bookingId/status'),
        headers: await getHeaders(),
        body: json.encode(updateData),
      );

      print('🔍 updateBookingStatus response status: ${response.statusCode}');
      print('🔍 updateBookingStatus response body: ${response.body}');

      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        if (data['success'] == true) {
          return data;
        } else {
          return {'success': false, 'error': data['error'] ?? 'Failed to update booking'};
        }
      } else {
        return {'success': false, 'error': 'HTTP ${response.statusCode}'};
      }
    } catch (e) {
      print('❌ updateBookingStatus exception: $e');
      return {'success': false, 'error': e.toString()};
    }
  }

  // Get verification requests
  static Future<Map<String, dynamic>> getVerificationRequests() async {
    try {
      final response = await http.get(
        Uri.parse('$baseUrl/api/verification-requests'),
        headers: await getHeaders(),
      );

      print('🔍 getVerificationRequests response status: ${response.statusCode}');

      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        if (data['success'] == true) {
          return data;
        } else {
          return {'success': false, 'error': data['error'] ?? 'Failed to get verification requests'};
        }
      } else {
        return {'success': false, 'error': 'HTTP ${response.statusCode}'};
      }
    } catch (e) {
      print('❌ getVerificationRequests exception: $e');
      return {'success': false, 'error': e.toString()};
    }
  }

  // Update verification status
  static Future<Map<String, dynamic>> updateVerificationStatus(int requestId, String status, {String? notes, String? rejectionReason, String? profilePhotoUrl, double? discountRate}) async {
    try {
      Map<String, dynamic> updateData = {
        'status': status,
      };
      
      if (notes != null) {
        updateData['approval_notes'] = notes;
      }
      
      if (rejectionReason != null) {
        updateData['rejection_reason'] = rejectionReason;
      }
      
      // Add profile photo URL if provided (for approved requests)
      if (profilePhotoUrl != null && status == 'approved') {
        updateData['profilePhotoUrl'] = profilePhotoUrl;
      }
      
      // Add discount rate for approved requests
      if (discountRate != null && status == 'approved') {
        updateData['discountRate'] = discountRate;
      }
      
      // Add current timestamp
      updateData['updatedAt'] = DateTime.now().toIso8601String();
      
      final response = await http.put(
        Uri.parse('$baseUrl/api/verification-requests/$requestId'), // Fixed endpoint
        headers: await getHeaders(),
        body: json.encode(updateData),
      );

      print('🔍 updateVerificationStatus response status: ${response.statusCode}');
      print('🔍 updateVerificationStatus request data: $updateData');

      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        if (data['success'] == true) {
          return data;
        } else {
          return {'success': false, 'error': data['error'] ?? 'Failed to update verification status'};
        }
      } else {
        return {'success': false, 'error': 'HTTP ${response.statusCode}'};
      }
    } catch (e) {
      print('❌ updateVerificationStatus exception: $e');
      return {'success': false, 'error': e.toString()};
    }
  }

  // Get time slots for a facility and date
  static Future<Map<String, dynamic>> getTimeSlots(int facilityId, String date) async {
    try {
      final response = await http.get(
        Uri.parse('$baseUrl/api/facilities/$facilityId/timeslots?date=$date'),
        headers: await getHeaders(),
      );

      print('🔍 getTimeSlots response status: ${response.statusCode}');

      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        if (data['success'] == true) {
          return data;
        } else {
          return {'success': false, 'error': data['error'] ?? 'Failed to get time slots'};
        }
      } else {
        return {'success': false, 'error': 'HTTP ${response.statusCode}'};
      }
    } catch (e) {
      print('❌ getTimeSlots exception: $e');
      return {'success': false, 'error': e.toString()};
    }
  }

  // Logout
  static Future<Map<String, dynamic>> logout() async {
    try {
      final response = await http.post(
        Uri.parse('$baseUrl/api/auth/logout'),
        headers: await getHeaders(),
      );

      // Clear local token regardless of server response
      await _removeToken();
      
      // Clear user preferences
      final prefs = await SharedPreferences.getInstance();
      await prefs.remove('user_email');
      await prefs.remove('user_id');
      await prefs.remove('user_name');
      await prefs.remove('user_role');
      await prefs.remove('user_verified');
      await prefs.remove('user_discount_rate');
      await prefs.remove('user_contact_number');
      await prefs.remove('user_profile_photo_url');

      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        return data;
      } else {
        return {'success': true, 'message': 'Logged out successfully'};
      }
    } catch (e) {
      print('❌ logout exception: $e');
      // Still clear local data even if network fails
      await _removeToken();
      return {'success': true, 'message': 'Logged out successfully'};
    }
  }

  // Health check
  static Future<Map<String, dynamic>> healthCheck() async {
    try {
      final response = await http.get(
        Uri.parse('$baseUrl/health'),
        headers: await getHeaders(includeAuth: false),
      );

      if (response.statusCode == 200) {
        return json.decode(response.body);
      } else {
        return {'status': 'unhealthy', 'error': 'HTTP ${response.statusCode}'};
      }
    } catch (e) {
      print('❌ healthCheck exception: $e');
      return {'status': 'unhealthy', 'error': e.toString()};
    }
  }

  // Utility methods
  static Future<void> clearUserData() async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.clear();
    print('🔍 Cleared all user data');
  }

  // Additional methods for compatibility
  static Future<Map<String, dynamic>> register(String name, String email, String password, {String role = 'resident'}) async {
    try {
      print('🔍 ApiService.register called');
      print('🔍 Using baseUrl: $baseUrl');
      print('🔍 Full register URL: $baseUrl/api/auth/register');
      print('🔍 Registration data: name=$name, email=$email, role=$role');
      
      final response = await http.post(
        Uri.parse('$baseUrl/api/auth/register'),
        headers: await getHeaders(includeAuth: false),
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
        print('🔍 Parsed response data: $data');
        return data;
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

  static Future<List<Map<String, dynamic>>> getOfficials() async {
    try {
      final response = await http.get(
        Uri.parse('$baseUrl/api/users?role=official'),
        headers: await getHeaders(),
      );

      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        if (data['success'] == true) {
          return List<Map<String, dynamic>>.from(data['data'] ?? []);
        }
      }
      return [];
    } catch (e) {
      print('❌ getOfficials error: $e');
      return [];
    }
  }

  static Future<Map<String, dynamic>> updateProfile(Map<String, dynamic> profileData) async {
    try {
      final response = await http.put(
        Uri.parse('$baseUrl/api/users/profile'),
        headers: await getHeaders(),
        body: json.encode(profileData),
      );

      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        return data;
      } else {
        print('❌ updateProfile failed with status: ${response.statusCode}');
        print('❌ Response body: ${response.body}');
        return {'success': false, 'message': 'Update failed'};
      }
    } catch (e) {
      print('❌ updateProfile error: $e');
      return {'success': false, 'message': e.toString()};
    }
  }

  static Future<Map<String, dynamic>> getUserProfile(String email) async {
    try {
      final response = await http.get(
        Uri.parse('$baseUrl/api/users/profile?email=$email'),
        headers: await getHeaders(),
      );

      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        return data;
      } else {
        return {'success': false, 'error': 'Profile not found'};
      }
    } catch (e) {
      print('❌ getUserProfile error: $e');
      return {'success': false, 'error': e.toString()};
    }
  }

  static Future<Map<String, dynamic>> uploadProfilePhoto(XFile image) async {
    try {
      final token = await _getToken();
      if (token == null) {
        return {'success': false, 'message': 'No authentication token found'};
      }

      final url = '$baseUrl/api/users/profile-photo';
      print('📤 Uploading profile photo to: $url');

      // First test basic connectivity to the server
      print('🔍 Testing server connectivity...');
      final connectivityTest = await http.get(
        Uri.parse('$baseUrl/api/health'),
        headers: await getHeaders(),
      );
      print('🔍 Connectivity test status: ${connectivityTest.statusCode}');

      // Create multipart request for file upload
      final request = http.MultipartRequest(
        'POST',
        Uri.parse(url),
      );

      // Add image file
      final imageBytes = await image.readAsBytes();
      print('📸 Image size: ${imageBytes.length} bytes');
      
      final imageFile = http.MultipartFile.fromBytes(
        'profile_photo',
        imageBytes,
        filename: image.name,
      );
      request.files.add(imageFile);

      // Add authentication
      final headers = await getHeaders();
      // For multipart requests, we need to remove Content-Type from headers
      // and let http package set it automatically with boundary
      final multipartHeaders = Map<String, String>.from(headers);
      multipartHeaders.remove('Content-Type');
      print('🔐 Request headers: $multipartHeaders');
      request.headers.addAll(multipartHeaders);

      print('📤 Sending request...');
      final response = await request.send();
      print('📥 Response status code: ${response.statusCode}');
      print('📥 Response headers: ${response.headers}');

      if (response.statusCode == 200) {
        final responseBody = await response.stream.bytesToString();
        print('📥 Response body: $responseBody');
        final data = json.decode(responseBody);
        if (data['success'] == true) {
          return {'success': true, 'photo_url': data['photo_url']};
        } else {
          return {'success': false, 'message': data['message'] ?? 'Failed to upload photo'};
        }
      } else {
        final responseBody = await response.stream.bytesToString();
        print('❌ Error response body: $responseBody');
        return {'success': false, 'message': 'Server error: ${response.statusCode}'};
      }
    } catch (e) {
      print('❌ uploadProfilePhoto error: $e');
      print('❌ Error type: ${e.runtimeType}');
      
      // Check if it's a network connectivity issue
      if (e.toString().contains('Failed to fetch')) {
        return {'success': false, 'message': 'Network error: Unable to connect to server. Please check if the server is running and accessible.'};
      }
      
      return {'success': false, 'message': 'Network error: $e'};
    }
  }

  static Future<Map<String, dynamic>> createFacility(Map<String, dynamic> facilityData) async {
    try {
      final response = await http.post(
        Uri.parse('$baseUrl/api/facilities'),
        headers: await getHeaders(),
        body: json.encode(facilityData),
      );

      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        return data;
      } else {
        return {'success': false, 'message': 'Failed to create facility'};
      }
    } catch (e) {
      print('❌ createFacility error: $e');
      return {'success': false, 'message': e.toString()};
    }
  }

  static Future<Map<String, dynamic>> updateFacility(String facilityId, Map<String, dynamic> facilityData) async {
    try {
      final response = await http.put(
        Uri.parse('$baseUrl/api/facilities/$facilityId'),
        headers: await getHeaders(),
        body: json.encode(facilityData),
      );

      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        return data;
      } else {
        return {'success': false, 'message': 'Failed to update facility'};
      }
    } catch (e) {
      print('❌ updateFacility error: $e');
      return {'success': false, 'message': e.toString()};
    }
  }

  static Future<Map<String, dynamic>> deleteFacility(String facilityId) async {
    try {
      final response = await http.delete(
        Uri.parse('$baseUrl/api/facilities/$facilityId'),
        headers: await getHeaders(),
      );

      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        return data;
      } else {
        return {'success': false, 'message': 'Failed to delete facility'};
      }
    } catch (e) {
      print('❌ deleteFacility error: $e');
      return {'success': false, 'message': e.toString()};
    }
  }

  static Future<Map<String, dynamic>> regenerateFacilityTimeSlots(String facilityId) async {
    try {
      final response = await http.post(
        Uri.parse('$baseUrl/api/facilities/$facilityId/regenerate-timeslots'),
        headers: await getHeaders(),
      );

      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        return data;
      } else {
        return {'success': false, 'message': 'Failed to regenerate time slots'};
      }
    } catch (e) {
      print('❌ regenerateFacilityTimeSlots error: $e');
      return {'success': false, 'message': e.toString()};
    }
  }

  /// Handle API response and check for ban status
  static Future<Map<String, dynamic>> _handleApiResponse(
    Map<String, dynamic> response, 
    String operation
  ) async {
    // Check if response indicates user is banned
    if (response['success'] == false) {
      final message = response['message']?.toString().toLowerCase() ?? '';
      
      if (message.contains('banned') || message.contains('permanently banned')) {
        print('🚨 ApiService: User banned detected in $operation response');
        print('🚨 Ban message: ${response['message']}');
        
        // Trigger automatic logout for banned user
        await BanDetectionService.checkAndHandleBanStatus();
        
        return {
          ...response,
          'user_banned': true,
          'auto_logout_triggered': true
        };
      }
    }
    
    return response;
  }
}
