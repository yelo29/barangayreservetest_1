import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:shared_preferences/shared_preferences.dart';
import '../config/app_config.dart';

class DataService {
  // Get current user data from SharedPreferences
  static Future<Map<String, dynamic>?> getCurrentUserData() async {
    final prefs = await SharedPreferences.getInstance();
    final userEmail = prefs.getString('user_email');
    final userRole = prefs.getString('user_role');
    final userId = prefs.getString('user_id');
    final userName = prefs.getString('user_name');
    
    if (userEmail == null) return null;
    
    return {
      'email': userEmail,
      'role': userRole ?? 'resident',
      'id': userId,
      'name': userName,
    };
  }
  
  // Get authentication headers
  static Future<Map<String, String>> getHeaders() async {
    Map<String, String> headers = {
      'Content-Type': 'application/json',
      'Accept': 'application/json',
    };

    final token = await _getToken();
    if (token != null) {
      headers['Authorization'] = 'Bearer $token';
    }

    return headers;
  }
  
  static Future<String?> _getToken() async {
    final prefs = await SharedPreferences.getInstance();
    return prefs.getString('auth_token');
  }
  
  // Fetch user profile data
  static Future<Map<String, dynamic>> fetchUserProfile() async {
    try {
      final userData = await getCurrentUserData();
      if (userData == null) {
        return {'success': false, 'error': 'User not logged in'};
      }
      
      final response = await http.get(
        Uri.parse('${AppConfig.baseUrl}/api/users/profile/${userData['email']}'),
        headers: await getHeaders(),
      );
      
      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        return {'success': true, 'data': data};
      } else {
        return {'success': false, 'error': 'Failed to fetch profile'};
      }
    } catch (e) {
      return {'success': false, 'error': e.toString()};
    }
  }
  
  // Fetch facilities data
  static Future<Map<String, dynamic>> fetchFacilities() async {
    try {
      final response = await http.get(
        Uri.parse('${AppConfig.baseUrl}/api/facilities'),
        headers: await getHeaders(),
      );
      
      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        
        // Handle different response formats with proper type casting
        if (data is List) {
          // Direct array response from server - cast to List<Map<String, dynamic>>
          List<Map<String, dynamic>> facilitiesData = [];
          if (data.isNotEmpty) {
            facilitiesData = List<Map<String, dynamic>>.from(data);
          }
          return {'success': true, 'data': facilitiesData};
        } else if (data is Map && data['success'] == true) {
          // Wrapped response object - cast to Map<String, dynamic>
          Map<String, dynamic> responseMap = Map<String, dynamic>.from(data);
          
          // Ensure facilities data is properly typed
          if (responseMap['data'] is List) {
            List<Map<String, dynamic>> facilitiesData = [];
            if (responseMap['data'].isNotEmpty) {
              facilitiesData = List<Map<String, dynamic>>.from(responseMap['data']);
            }
            responseMap['data'] = facilitiesData;
          }
          
          return responseMap;
        } else {
          return {'success': false, 'error': 'Invalid response format'};
        }
      } else {
        return {'success': false, 'error': 'HTTP ${response.statusCode}'};
      }
    } catch (e) {
      return {'success': false, 'error': e.toString()};
    }
  }
  
  // Fetch bookings data with proper authentication
  static Future<Map<String, dynamic>> fetchBookings({
    String? facilityId,
    String? date,
    String? status,
    String? userRole, // Optional override for user_role
    bool? excludeUserRole, // New flag to completely exclude user_role parameter
  }) async {
    try {
      final userData = await getCurrentUserData();
      if (userData == null) {
        return {'success': false, 'error': 'User not logged in'};
      }
      
      // Build query parameters
      Map<String, String> queryParams = {};
      if (facilityId != null) queryParams['facility_id'] = facilityId;
      if (date != null) queryParams['date'] = date;
      if (status != null) queryParams['status'] = status;
      
      // Use provided userRole or default to current user's role
      if (excludeUserRole == true) {
        // Completely exclude user_role parameter
      } else if (userRole != null) {
        if (userRole.isNotEmpty) {
          queryParams['user_role'] = userRole;
        }
        // If userRole is empty string, don't add user_role parameter at all
      } else {
        queryParams['user_role'] = userData['role'];
      }
      
      // For residents, include their email (only if not excluding user_role)
      if (userData['role'] == 'resident' && excludeUserRole != true) {
        queryParams['user_email'] = userData['email'];
      }
      
      String queryString = queryParams.entries
          .map((e) => '${e.key}=${Uri.encodeComponent(e.value)}')
          .join('&');
      
      String url = '${AppConfig.baseUrl}/api/bookings';
      if (queryString.isNotEmpty) {
        url += '?$queryString';
      }
      
      print('🔍 DataService.fetchBookings URL: $url');
      print('🔍 DataService.fetchBookings userRole: ${userData['role']}');
      print('🔍 DataService.fetchBookings userEmail: ${userData['email']}');

      final response = await http.get(
        Uri.parse(url),
        headers: await getHeaders(),
      );

      print('🔍 DataService.fetchBookings response status: ${response.statusCode}');

      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        
        // Handle different response formats with proper type casting
        if (data is List) {
          // Direct array response from server - cast to List<Map<String, dynamic>>
          List<Map<String, dynamic>> bookingsData = [];
          if (data.isNotEmpty) {
            bookingsData = List<Map<String, dynamic>>.from(data);
          }
          return {'success': true, 'data': bookingsData};
        } else if (data is Map && data['success'] == true) {
          // Wrapped response object - cast to Map<String, dynamic>
          Map<String, dynamic> responseMap = Map<String, dynamic>.from(data);
          
          // Ensure bookings data is properly typed
          if (responseMap['data'] is List) {
            List<Map<String, dynamic>> bookingsData = [];
            if (responseMap['data'].isNotEmpty) {
              bookingsData = List<Map<String, dynamic>>.from(responseMap['data']);
            }
            responseMap['data'] = bookingsData;
          }
          
          return responseMap;
        } else {
          // Fallback for any other format
          List<Map<String, dynamic>> bookingsData = [];
          if (data is List && data.isNotEmpty) {
            bookingsData = List<Map<String, dynamic>>.from(data);
          }
          return {'success': true, 'data': bookingsData};
        }
      } else {
        return {'success': false, 'error': 'HTTP ${response.statusCode}'};
      }
    } catch (e) {
      print('❌ DataService.fetchBookings exception: $e');
      return {'success': false, 'error': e.toString()};
    }
  }
  
  // Fetch time slots for a facility
  static Future<Map<String, dynamic>> fetchTimeSlots({
    required String facilityId,
    required String date,
  }) async {
    try {
      final response = await http.get(
        Uri.parse('${AppConfig.baseUrl}/api/available-timeslots?facility_id=$facilityId&date=$date'),
        headers: await getHeaders(),
      );
      
      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        return {'success': true, 'data': data};
      } else {
        return {'success': false, 'error': 'HTTP ${response.statusCode}'};
      }
    } catch (e) {
      return {'success': false, 'error': e.toString()};
    }
  }
  
  // Fetch verification requests (for officials)
  static Future<Map<String, dynamic>> fetchVerificationRequests() async {
    try {
      final response = await http.get(
        Uri.parse('${AppConfig.baseUrl}/api/verification-requests'),
        headers: await getHeaders(),
      );
      
      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        return {'success': true, 'data': data};
      } else {
        return {'success': false, 'error': 'HTTP ${response.statusCode}'};
      }
    } catch (e) {
      return {'success': false, 'error': e.toString()};
    }
  }
  
  // Fetch officials list
  static Future<Map<String, dynamic>> fetchOfficials() async {
    try {
      final response = await http.get(
        Uri.parse('${AppConfig.baseUrl}/api/officials'),
        headers: await getHeaders(),
      );
      
      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        
        // Handle different response formats with proper type casting
        if (data is Map && data['success'] == true) {
          // Wrapped response object - cast to Map<String, dynamic>
          Map<String, dynamic> responseMap = Map<String, dynamic>.from(data);
          
          // Ensure officials data is properly typed
          if (responseMap['data'] is List) {
            List<Map<String, dynamic>> officialsData = [];
            if (responseMap['data'].isNotEmpty) {
              officialsData = List<Map<String, dynamic>>.from(responseMap['data']);
            }
            responseMap['data'] = officialsData;
          }
          
          return responseMap;
        } else {
          return {'success': false, 'error': 'Invalid response format'};
        }
      } else {
        return {'success': false, 'error': 'HTTP ${response.statusCode}'};
      }
    } catch (e) {
      return {'success': false, 'error': e.toString()};
    }
  }
}
