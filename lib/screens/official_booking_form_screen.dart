import 'dart:convert';
import 'dart:async';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:intl/intl.dart';
import 'package:http/http.dart' as http;
import '../services/api_service.dart' as api_service;
import '../services/data_service.dart';
import '../utils/debug_logger.dart';
import '../services/auth_api_service.dart';
import '../widgets/loading_widget.dart';
import '../config/app_config.dart';

class OfficialBookingFormScreen extends StatefulWidget {
  final Map<String, dynamic> facility;
  final DateTime selectedDate;
  final Map<String, dynamic>? userData;

  const OfficialBookingFormScreen({
    super.key,
    required this.facility,
    required this.selectedDate,
    this.userData,
  });

  @override
  State<OfficialBookingFormScreen> createState() => _OfficialBookingFormScreenState();
}

class _OfficialBookingFormScreenState extends State<OfficialBookingFormScreen> {
  final _formKey = GlobalKey<FormState>();
  
  bool _isLoadingTimeSlots = true;
  bool _isSubmitting = false;
  
  // Enhanced data for official booking
  List<Map<String, dynamic>> _allTimeSlots = [];
  List<Map<String, dynamic>> _residentBookings = [];
  Map<String, dynamic> _officialUserData = {};

  @override
  void initState() {
    super.initState();
    _initializeData();
  }

  @override
  void dispose() {
    super.dispose();
  }

  Future<void> _initializeData() async {
    setState(() => _isLoadingTimeSlots = true);
    
    try {
      // Get official user data
      final userData = await DataService.getCurrentUserData();
      if (userData != null) {
        _officialUserData = userData;
      }

      // Load existing resident bookings for this date FIRST
      await _loadResidentBookings();
      
      // Then load all time slots for the facility (so resident bookings can be matched)
      await _loadTimeSlots();
      
    } catch (e) {
      DebugLogger.error('Error initializing official booking form: $e');
    } finally {
      setState(() => _isLoadingTimeSlots = false);
    }
  }

  Future<void> _loadTimeSlots() async {
    try {
      DebugLogger.ui('🔍 Loading time slots with ${_residentBookings.length} resident bookings available for matching');
      
      // Use same time slot format as resident form for consistency
      final defaultTimeSlots = [
        '6:00 AM - 8:00 AM',
        '8:00 AM - 10:00 AM',
        '10:00 AM - 12:00 PM',
        '12:00 PM - 2:00 PM',
        '2:00 PM - 4:00 PM',
        '4:00 PM - 6:00 PM',
        '6:00 PM - 8:00 PM',
        '8:00 PM - 10:00 PM',
      ];
      
      // Fetch availability using same endpoint as resident form
      final response = await http.get(
        Uri.parse('${AppConfig.baseUrl}/api/available-timeslots?facility_id=${widget.facility['id']}&date=${DateFormat('yyyy-MM-dd').format(widget.selectedDate)}&user_email=${_officialUserData['user_email'] ?? 'official@barangay.gov'}'),
        headers: {'Content-Type': 'application/json'},
      );
      
      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        if (data['success']) {
          final defaultTimeSlots = List<String>.from(data['default_timeslots'] ?? []);
          final competitiveSlots = List<String>.from(data['competitive_timeslots'] ?? []);
          final approvedSlots = List<String>.from(data['approved_timeslots'] ?? []);
          
          // Convert to enhanced time slot format with resident booking info
          _allTimeSlots = defaultTimeSlots.map((timeSlot) {
            DebugLogger.ui('🔍 Time slot matching - Processing time slot: "$timeSlot"');
            DebugLogger.ui('🔍 Time slot matching - Resident bookings to check: ${_residentBookings.length}');
            
            // Collect ALL matching resident bookings for this time slot
            final matchingResidentBookings = _residentBookings.where((booking) {
              String bookingTime = booking['time_slot'] ?? booking['timeslot'] ?? '';
              
              // If time_slot is not available, try to construct from start_time and end_time
              if (bookingTime.isEmpty) {
                final startTime = booking['start_time'] ?? '';
                final endTime = booking['end_time'] ?? '';
                if (startTime.isNotEmpty && endTime.isNotEmpty) {
                  bookingTime = '$startTime - $endTime';
                }
              }
              
              // Convert both to comparable format (remove spaces, normalize)
              final normalizedSlot = timeSlot.replaceAll(':', '').replaceAll(' ', '').toUpperCase();
              final normalizedBooking = bookingTime.replaceAll(':', '').replaceAll(' ', '').toUpperCase();
              
              // Check for exact match or partial match
              final matches = normalizedBooking.contains(normalizedSlot) || 
                     normalizedSlot.contains(normalizedBooking) ||
                     bookingTime.contains(timeSlot) ||
                     _formatTimeForDisplay(bookingTime) == timeSlot;
              
              if (matches) {
                DebugLogger.ui('🔍 Time slot MATCH: "$timeSlot" matches booking "$bookingTime"');
              } else {
                DebugLogger.ui('🔍 Time slot NO MATCH: "$timeSlot" vs booking "$bookingTime"');
              }
              
              return matches;
            }).toList();
            
            final hasResidentBooking = matchingResidentBookings.isNotEmpty;
            
            DebugLogger.ui('🔍 Time slot matching - Found ${matchingResidentBookings.length} matching bookings for "$timeSlot"');
            if (matchingResidentBookings.isNotEmpty) {
              for (int i = 0; i < matchingResidentBookings.length; i++) {
                DebugLogger.ui('🔍 Time slot matching - Match $i: ${matchingResidentBookings[i]['start_time']} (${matchingResidentBookings[i]['status']})');
              }
            }
            
            // For display, we'll show the first booking, but store all for the dialog
            final residentBooking = hasResidentBooking ? matchingResidentBookings.first : <String, dynamic>{};
            
            DebugLogger.ui('🔍 Time slot "$timeSlot" - has_resident_booking: $hasResidentBooking, status: ${hasResidentBooking ? (residentBooking['status'] == 'approved' ? 'approved' : 'pending') : 'available'}, background: ${hasResidentBooking ? (residentBooking['status'] == 'approved' ? 'Colors.green.shade100' : 'Colors.yellow.shade100') : 'Colors.grey.shade100'}');
            
            return {
              'id': defaultTimeSlots.indexOf(timeSlot),
              'time_slot': timeSlot,
              'is_available': !hasResidentBooking,
              'has_resident_booking': hasResidentBooking,
              'resident_booking': residentBooking,
              'all_resident_bookings': matchingResidentBookings, // Store all matching bookings
              'resident_count': matchingResidentBookings.length, // Add count for display
              'status': hasResidentBooking ? (residentBooking['status'] == 'approved' ? 'approved' : 'pending') : 'available',
              'background_color': hasResidentBooking 
                ? (residentBooking['status'] == 'approved' ? Colors.green.shade100 : Colors.yellow.shade100)
                : Colors.grey.shade100,
              'border_color': hasResidentBooking 
                ? (residentBooking['status'] == 'approved' ? Colors.green : Colors.orange)
                : Colors.grey.shade300,
              'text_color': hasResidentBooking 
                ? (residentBooking['status'] == 'approved' ? Colors.green.shade800 : Colors.orange.shade800)
                : Colors.black87,
            };
          }).toList();
        }
      }
      
      DebugLogger.ui('Loaded ${_allTimeSlots.length} time slots for official booking');
      
      // Debug: Print final time slot states
      for (int i = 0; i < _allTimeSlots.length && i < 3; i++) {
        final slot = _allTimeSlots[i];
        DebugLogger.ui('🔍 Final time slot $i: "${slot['time_slot']}" - available: ${slot['is_available']}, has_resident_booking: ${slot['has_resident_booking']}, status: ${slot['status']}');
      }
    } catch (e) {
      DebugLogger.error('Error loading time slots: $e');
      // Create default time slots even on error
      _allTimeSlots = [
        {'id': 0, 'time_slot': '6:00 AM - 8:00 AM', 'is_available': true, 'has_resident_booking': false, 'resident_booking': {}, 'status': 'available', 'background_color': Colors.grey.shade100, 'border_color': Colors.grey.shade300, 'text_color': Colors.black87},
        {'id': 1, 'time_slot': '8:00 AM - 10:00 AM', 'is_available': true, 'has_resident_booking': false, 'resident_booking': {}, 'status': 'available', 'background_color': Colors.grey.shade100, 'border_color': Colors.grey.shade300, 'text_color': Colors.black87},
        {'id': 2, 'time_slot': '10:00 AM - 12:00 PM', 'is_available': true, 'has_resident_booking': false, 'resident_booking': {}, 'status': 'available', 'background_color': Colors.grey.shade100, 'border_color': Colors.grey.shade300, 'text_color': Colors.black87},
        {'id': 3, 'time_slot': '12:00 PM - 2:00 PM', 'is_available': true, 'has_resident_booking': false, 'resident_booking': {}, 'status': 'available', 'background_color': Colors.grey.shade100, 'border_color': Colors.grey.shade300, 'text_color': Colors.black87},
        {'id': 4, 'time_slot': '2:00 PM - 4:00 PM', 'is_available': true, 'has_resident_booking': false, 'resident_booking': {}, 'status': 'available', 'background_color': Colors.grey.shade100, 'border_color': Colors.grey.shade300, 'text_color': Colors.black87},
        {'id': 5, 'time_slot': '4:00 PM - 6:00 PM', 'is_available': true, 'has_resident_booking': false, 'resident_booking': {}, 'status': 'available', 'background_color': Colors.grey.shade100, 'border_color': Colors.grey.shade300, 'text_color': Colors.black87},
        {'id': 6, 'time_slot': '6:00 PM - 8:00 PM', 'is_available': true, 'has_resident_booking': false, 'resident_booking': {}, 'status': 'available', 'background_color': Colors.grey.shade100, 'border_color': Colors.grey.shade300, 'text_color': Colors.black87},
        {'id': 7, 'time_slot': '8:00 PM - 10:00 PM', 'is_available': true, 'has_resident_booking': false, 'resident_booking': {}, 'status': 'available', 'background_color': Colors.grey.shade100, 'border_color': Colors.grey.shade300, 'text_color': Colors.black87},
      ];
    }
  }

  Future<void> _loadResidentBookings() async {
    try {
      DebugLogger.ui('🔍 _loadResidentBookings() called');
      
      // Get ALL bookings first (like official home tab does), then filter client-side
      final bookingsData = await DataService.fetchBookings(
        excludeUserRole: true, // Completely exclude user_role parameter
      );
      
      DebugLogger.ui('🔍 Official booking form - Fetching ALL bookings (no filters)');
      DebugLogger.ui('🔍 API Response: $bookingsData');
      
      if (bookingsData['success'] == true) {
        // Check both possible response keys: 'bookings' or 'data'
        List<dynamic> bookingsList = [];
        if (bookingsData['bookings'] != null) {
          bookingsList = bookingsData['bookings'];
          DebugLogger.ui('🔍 Using bookings key: ${bookingsList.length} total bookings found');
        } else if (bookingsData['data'] != null) {
          bookingsList = bookingsData['data'];
          DebugLogger.ui('🔍 Using data key: ${bookingsList.length} total bookings found');
        } else {
          DebugLogger.ui('🔍 No bookings found in response');
        }
        
        // Filter client-side for specific facility, date, and resident bookings
        final targetDate = DateFormat('yyyy-MM-dd').format(widget.selectedDate);
        final targetFacilityId = widget.facility['id'].toString();
        
        DebugLogger.ui('🔍 Filtering for facility: $targetFacilityId, date: $targetDate');
        DebugLogger.ui('🔍 Total bookings received: ${bookingsList.length}');
        
        // First, let's see ALL bookings for target date (any facility)
        final allBookingsForDate = List<Map<String, dynamic>>.from(bookingsList)
            .where((booking) => booking['booking_date']?.toString() == targetDate)
            .toList();
        
        DebugLogger.ui('🔍 All bookings for $targetDate: ${allBookingsForDate.length}');
        for (int i = 0; i < allBookingsForDate.length && i < 5; i++) {
          final booking = allBookingsForDate[i];
          DebugLogger.ui('🔍 Date booking $i: ${booking['start_time']} - ${booking['status']} - ${booking['user_email']} - Facility: ${booking['facility_id']} - Role: ${booking['user_role']}');
        }
        
        // Now filter for our specific facility and handle the user_role issue properly
        DebugLogger.ui('🔍 DEBUG: Before filtering - bookingsList length: ${bookingsList.length}');
        
        // Debug each booking individually to see what's happening
        for (int i = 0; i < bookingsList.length && i < 5; i++) {
          final booking = bookingsList[i];
          final dateMatch = booking['booking_date']?.toString() == targetDate;
          final facilityMatch = booking['facility_id'].toString() == targetFacilityId;
          final statusMatch = (booking['status'] == 'pending' || booking['status'] == 'approved');
          final role = booking['user_role'];
          
          // Debug role matching in detail
          final isResidentString = booking['user_role'] == 'resident';
          final isNull = booking['user_role'] == null;
          final isZeroString = booking['user_role'] == '0';
          final isZeroNum = booking['user_role'] == 0;
          final startsWithZero = booking['user_role'].toString().startsWith('0.');
          final is005 = booking['user_role'] == '0.05';
          final is01 = booking['user_role'] == '0.1';
          
          final roleMatch = isResidentString || isNull || isZeroString || isZeroNum || startsWithZero || is005 || is01 || 
                       booking['user_role'] == 0.05 || booking['user_role'] == 0.1;  // Handle double values
          final shouldInclude = dateMatch && facilityMatch && statusMatch && roleMatch;
          
          DebugLogger.ui('🔍 DEBUG: Individual booking $i - Date: $dateMatch, Facility: $facilityMatch, Status: $statusMatch, Role: $role (type: ${role.runtimeType}) -> $roleMatch, Should Include: $shouldInclude');
        }
        
        // Debug: Print first booking to see available fields
            if (bookingsList.isNotEmpty) {
              DebugLogger.ui('🔍 DEBUG: First booking fields: ${bookingsList[0].keys.toList()}');
              DebugLogger.ui('🔍 DEBUG: First booking full_name: ${bookingsList[0]['full_name']}');
              DebugLogger.ui('🔍 DEBUG: First booking user_name: ${bookingsList[0]['user_name']}');
            }
            
            _residentBookings = List<Map<String, dynamic>>.from(bookingsList)
            .where((booking) {
                // Enhanced date comparison - handle both string and DateTime
                final bookingDate = booking['booking_date'];
                bool dateMatch = false;
                
                DebugLogger.ui('🔍 DEBUG: Date comparison - booking_date: $bookingDate (type: ${bookingDate.runtimeType}) vs targetDate: $targetDate');
                
                if (bookingDate is String) {
                  dateMatch = bookingDate == targetDate;
                  DebugLogger.ui('🔍 DEBUG: String date comparison: "$bookingDate" == "$targetDate" -> $dateMatch');
                } else if (bookingDate is DateTime) {
                  final bookingDateString = bookingDate.toString().split(' ')[0]; // Get YYYY-MM-DD part
                  dateMatch = bookingDateString == targetDate;
                  DebugLogger.ui('🔍 DEBUG: DateTime date comparison: "$bookingDateString" == "$targetDate" -> $dateMatch');
                } else {
                  DebugLogger.ui('🔍 DEBUG: Unknown date type: ${bookingDate.runtimeType}');
                }
                
                final facilityMatch = booking['facility_id'].toString() == targetFacilityId;
                // For officials, show ALL resident bookings regardless of status
                final statusMatch = true; // Don't filter by status for officials
                final userRole = booking['user_role'];
                DebugLogger.ui('🔍 DEBUG: Role check - user_role: $userRole (type: ${userRole.runtimeType})');
                
                final roleMatch = (userRole == 'resident' || 
                                 userRole == null || 
                                 userRole == '0' ||
                                 userRole == 0 ||  // Handle integer 0
                                 userRole.toString().startsWith('0.') ||
                                 userRole == 0.05 ||  // Handle double 0.05
                                 userRole == '0.05' ||
                                 userRole == 0.1 ||   // Handle double 0.1
                                 userRole == '0.1');
                
                DebugLogger.ui('🔍 DEBUG: Role details - == "resident": ${userRole == 'resident'}, == null: ${userRole == null}, == "0": ${userRole == '0'}, == 0 (int): ${userRole == 0}, toString().startsWith("0."): ${userRole.toString().startsWith('0.')}, == "0.05": ${userRole == '0.05'}, == 0.05 (double): ${userRole == 0.05}, == "0.1": ${userRole == '0.1'}, == 0.1 (double): ${userRole == 0.1}');
                
                DebugLogger.ui('🔍 DEBUG: Filtering - Date: $dateMatch, Facility: $facilityMatch, Status: $statusMatch, Role: $roleMatch');
                
                return dateMatch && facilityMatch && statusMatch && roleMatch;
            })
            .toList();
        
        DebugLogger.ui('🔍 DEBUG: After filtering - _residentBookings length: ${_residentBookings.length}');
        
        DebugLogger.ui('🔍 Loaded ${_residentBookings.length} resident bookings for official view');
        
        // Debug: Print filtered bookings
        for (int i = 0; i < _residentBookings.length && i < 3; i++) {
          final booking = _residentBookings[i];
          DebugLogger.ui('🔍 Filtered booking $i: ${booking['start_time']} - ${booking['status']} - ${booking['user_email']} - Facility: ${booking['facility_id']} - Date: ${booking['booking_date']} - Role: ${booking['user_role']}');
        }
        
        // Debug: Check if any bookings are being filtered out incorrectly
        final facilityDateBookings = bookingsList.where((booking) => 
            booking['booking_date']?.toString() == targetDate &&
            booking['facility_id'].toString() == targetFacilityId
        ).toList();
        
        DebugLogger.ui('🔍 DEBUG: All bookings for this facility/date: ${facilityDateBookings.length}');
        for (int i = 0; i < facilityDateBookings.length; i++) {
          final booking = facilityDateBookings[i];
          final status = booking['status'];
          final role = booking['user_role'];
          final statusMatch = (status == 'pending' || status == 'approved');
          
          // Debug role matching in detail
          final isResidentString = booking['user_role'] == 'resident';
          final isNull = booking['user_role'] == null;
          final isZeroString = booking['user_role'] == '0';
          final isZeroNum = booking['user_role'] == 0;
          final startsWithZero = booking['user_role'].toString().startsWith('0.');
          final is005 = booking['user_role'] == '0.05';
          final is01 = booking['user_role'] == '0.1';
          
          final roleMatch = isResidentString || isNull || isZeroString || isZeroNum || startsWithZero || is005 || is01 || 
                       booking['user_role'] == 0.05 || booking['user_role'] == 0.1;  // Handle double values
          
          DebugLogger.ui('🔍 DEBUG: Role matching details - role: $role (type: ${role.runtimeType})');
          DebugLogger.ui('🔍 DEBUG: isResidentString: $isResidentString, isNull: $isNull, isZeroString: $isZeroString, isZeroNum: $isZeroNum');
          DebugLogger.ui('🔍 DEBUG: startsWithZero: $startsWithZero, is005: $is005, is01: $is01');
          DebugLogger.ui('🔍 DEBUG: Final roleMatch: $roleMatch');
          
          DebugLogger.ui('🔍 DEBUG: Booking $i - Status: $status (match: $statusMatch), Role: $role (match: $roleMatch), Final: ${statusMatch && roleMatch}');
          DebugLogger.ui('🔍 DEBUG: Full booking data: $booking');
        }
        
        // Also print some sample bookings that didn't match for debugging
        final sampleBookings = List<Map<String, dynamic>>.from(bookingsList).take(5).toList();
        DebugLogger.ui('🔍 Sample bookings from API:');
        for (int i = 0; i < sampleBookings.length; i++) {
          final booking = sampleBookings[i];
          DebugLogger.ui('🔍 Sample $i: ${booking['start_time']} - ${booking['status']} - ${booking['user_email']} - Facility: ${booking['facility_id']} - Date: ${booking['booking_date']} - Role: ${booking['user_role']}');
        }
      } else {
        DebugLogger.ui('🔍 API call failed: ${bookingsData['error']}');
      }
    } catch (e) {
      DebugLogger.error('Error loading resident bookings: $e');
    }
  }

  void _showResidentBookingDetails(Map<String, dynamic> timeSlot) {
    if (timeSlot['has_resident_booking'] != true) return;
    
    final allResidentBookings = timeSlot['all_resident_bookings'] as List<Map<String, dynamic>>;
    final residentCount = timeSlot['resident_count'] as int;
    
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: Row(
          children: [
            Icon(
              Icons.warning,
              color: allResidentBookings.first['status'] == 'approved' ? Colors.green : Colors.orange,
              size: 24,
            ),
            const SizedBox(width: 8),
            Expanded(
              child: Text('Resident Booking Details${residentCount > 1 ? ' ($residentCount)' : ''}'),
            ),
          ],
        ),
        content: SingleChildScrollView(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            mainAxisSize: MainAxisSize.min,
            children: [
              // Show all resident bookings for this time slot
              ...allResidentBookings.asMap().entries.map((entry) {
                final index = entry.key;
                final residentBooking = entry.value;
                final isLast = index == allResidentBookings.length - 1;
                
                return Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    if (residentCount > 1) ...[
                      Container(
                        width: double.infinity,
                        padding: const EdgeInsets.all(8),
                        margin: const EdgeInsets.only(bottom: 8),
                        decoration: BoxDecoration(
                          color: Colors.grey.shade100,
                          borderRadius: BorderRadius.circular(6),
                          border: Border.all(color: Colors.grey.shade300),
                        ),
                        child: Text(
                          'Resident ${index + 1}',
                          style: TextStyle(
                            fontWeight: FontWeight.bold,
                            color: Colors.grey.shade700,
                          ),
                        ),
                      ),
                    ],
                    _buildDetailRow('Name', residentBooking['full_name'] ?? residentBooking['user_name'] ?? 'N/A'),
                    _buildDetailRow('Email', residentBooking['user_email'] ?? 'N/A'),
                    _buildDetailRow('Contact', residentBooking['contact_number'] ?? 'N/A'),
                    _buildDetailRow('Address', residentBooking['contact_address'] ?? 'N/A'),
                    _buildDetailRow('Status', residentBooking['status'] ?? 'N/A'),
                    _buildDetailRow('Purpose', residentBooking['purpose'] ?? 'N/A'),
                    if (residentBooking['receipt_base64'] != null) ...[
                      const SizedBox(height: 12),
                      const Text('Receipt:', style: TextStyle(fontWeight: FontWeight.bold)),
                      const SizedBox(height: 8),
                      Container(
                        height: 200,
                        width: double.infinity,
                        decoration: BoxDecoration(
                          border: Border.all(color: Colors.grey.shade300),
                          borderRadius: BorderRadius.circular(8),
                        ),
                        child: ClipRRect(
                          borderRadius: BorderRadius.circular(8),
                          child: Builder(
                            builder: (context) {
                              try {
                                final base64String = residentBooking['receipt_base64'].toString();
                                final cleanBase64 = base64String.contains(',') 
                                    ? base64String.split(',')[1] 
                                    : base64String;
                                final imageBytes = base64Decode(cleanBase64);
                                return Image.memory(
                                  imageBytes,
                                  fit: BoxFit.contain,
                                  errorBuilder: (context, error, stackTrace) {
                                    return Container(
                                      height: 200,
                                      child: const Center(
                                        child: Column(
                                          mainAxisAlignment: MainAxisAlignment.center,
                                          children: [
                                            Icon(Icons.error, color: Colors.red),
                                            SizedBox(height: 8),
                                            Text('Error loading receipt'),
                                          ],
                                        ),
                                      ),
                                    );
                                  },
                                );
                              } catch (e) {
                                return Container(
                                  height: 200,
                                  child: const Center(
                                    child: Column(
                                      mainAxisAlignment: MainAxisAlignment.center,
                                      children: [
                                        Icon(Icons.error, color: Colors.red),
                                        SizedBox(height: 8),
                                        Text('Invalid receipt format'),
                                      ],
                                    ),
                                  ),
                                );
                              }
                            },
                          ),
                        ),
                      ),
                    ],
                    if (!isLast) const SizedBox(height: 16),
                  ],
                );
              }).toList(),
            ],
          ),
        ),
        actions: [
          // Only show Reject button for pending bookings
          if (allResidentBookings.first['status'] == 'pending')
            TextButton.icon(
              onPressed: () {
                Navigator.pop(context); // Close details dialog
                _rejectResidentBooking(allResidentBookings.first); // Reject the booking
              },
              icon: const Icon(Icons.cancel, color: Colors.red),
              label: const Text('Reject', style: TextStyle(color: Colors.red)),
            ),
          TextButton(
            onPressed: () => Navigator.pop(context),
            child: const Text('Close'),
          ),
        ],
      ),
    );
  }

  // NEW: Reject resident booking with violation tracking dialog
  Future<void> _rejectResidentBooking(Map<String, dynamic> residentBooking) async {
    final bookingId = residentBooking['id'];
    final userEmail = residentBooking['user_email'];
    
    // Show rejection reason dialog
    String? selectedRejectionType;
    
    await showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text('Reject Booking'),
        content: Column(
          mainAxisSize: MainAxisSize.min,
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text('Reject booking for ${residentBooking['full_name']}?'),
            const SizedBox(height: 16),
            const Text(
              'Select rejection reason:',
              style: TextStyle(fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 8),
            StatefulBuilder(
              builder: (context, setState) {
                return Column(
                  children: [
                    RadioListTile<String>(
                      title: const Text('Rejected (because of incorrect amount of downpayment)'),
                      value: 'incorrect_downpayment',
                      groupValue: selectedRejectionType,
                      onChanged: (value) {
                        setState(() => selectedRejectionType = value);
                      },
                    ),
                    RadioListTile<String>(
                      title: const Text('Rejected (because of fake receipt/no downpayment/payment)'),
                      value: 'fake_receipt',
                      groupValue: selectedRejectionType,
                      onChanged: (value) {
                        setState(() => selectedRejectionType = value);
                      },
                    ),
                  ],
                );
              },
            ),
          ],
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context),
            child: const Text('Cancel'),
          ),
          ElevatedButton(
            onPressed: selectedRejectionType != null
                ? () {
                    Navigator.pop(context);
                    _executeRejection(residentBooking, selectedRejectionType!);
                  }
                : null,
            child: const Text('Reject'),
          ),
        ],
      ),
    );
  }

  // NEW: Execute the rejection with proper reason and type
  Future<void> _executeRejection(Map<String, dynamic> residentBooking, String rejectionType) async {
    try {
      final bookingId = residentBooking['id'];
      
      String rejectionReason;
      if (rejectionType == 'incorrect_downpayment') {
        rejectionReason = 'The amount of your down payment is incorrect, please verify your payment and try again.';
      } else {
        rejectionReason = 'Your payment receipt is fake or shown no payment in our payment history/records, ⚠️ know that this violation will be recorded and you will only have three chances before getting your account banned!';
      }
      
      DebugLogger.ui('🔍 Rejecting resident booking: ID=$bookingId, Type=$rejectionType');
      
      final response = await api_service.ApiService.updateBookingStatus(
        bookingId,
        'rejected',
        rejectionReason: rejectionReason,
        rejectionType: rejectionType,
      );
      
      if (response['success'] == true) {
        _showSuccessSnackBar('Booking rejected successfully');
        // Refresh the time slots to update the UI
        _loadTimeSlots();
      } else {
        _showErrorSnackBar('Failed to reject booking: ${response['error'] ?? response['message']}');
      }
    } catch (e) {
      _showErrorSnackBar('Error rejecting booking: $e');
    }
  }

  Widget _buildDetailRow(String label, String value) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 8),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          SizedBox(
            width: 80,
            child: Text(
              '$label:',
              style: const TextStyle(fontWeight: FontWeight.bold),
            ),
          ),
          Expanded(
            child: Text(value),
          ),
        ],
      ),
    );
  }

  Future<void> _submitBooking() async {
    // Officials can book entire day - no time slot selection needed
    setState(() => _isSubmitting = true);

    try {
      final bookingData = {
        'facility_id': widget.facility['id'],
        'user_email': _officialUserData['user_email'] ?? 'captain@barangay.gov',
        'date': DateFormat('yyyy-MM-dd').format(widget.selectedDate),
        'timeslot': 'ALL DAY', // Officials book entire day
        'total_amount': 0, // Official bookings are free
        'full_name': _officialUserData['full_name'] ?? 'Barangay Official',
        'contact_number': _officialUserData['contact_number'] ?? '09123456789',
        'address': 'Barangay Hall',
        'purpose': 'Official barangay business',
        'user_role': 'official',
      };

      DebugLogger.ui('Official booking data: $bookingData');

      // Create the official booking (backend will auto-reject ALL resident bookings for this date)
      final response = await api_service.ApiService.createBooking(bookingData);

      if (response['success'] == true) {
        // Check if any resident bookings were auto-rejected
        final rejectedBookings = response['rejected_resident_bookings'] as List<dynamic>? ?? [];
        
        String message = response['message'] ?? 'Official booking created successfully!';
        
        if (rejectedBookings.isNotEmpty) {
          // Show detailed success message with ALL rejected bookings info
          DebugLogger.ui('🎯 Showing success dialog with ${rejectedBookings.length} rejected bookings');
          await _showDetailedSuccessDialog(message, rejectedBookings.cast<Map<String, dynamic>>());
          DebugLogger.ui('🎯 Dialog closed - navigating back');
          // Navigate after dialog is closed
          if (mounted) {
            DebugLogger.ui('🎯 Navigating back from official booking form');
            Navigator.of(context).pop();
          }
        } else {
          DebugLogger.ui('🎯 Showing simple success snackbar');
          _showSuccessSnackBar(message);
          // Navigate immediately for simple success
          if (mounted) {
            DebugLogger.ui('🎯 Navigating back from official booking form (simple)');
            Navigator.of(context).pop();
          }
        }
      } else {
        _showErrorSnackBar(response['message'] ?? 'Failed to create booking');
      }
    } catch (e) {
      DebugLogger.error('Error submitting official booking: $e');
      _showErrorSnackBar('An error occurred while creating booking');
    } finally {
      setState(() => _isSubmitting = false);
    }
  }

  Future<void> _rejectOverlappingResidentBookings() async {
    try {
      DebugLogger.ui('🔍 Checking for overlapping resident bookings...');
      
      // Retry logic for network issues
      int retryCount = 0;
      const maxRetries = 3;
      
      while (retryCount < maxRetries) {
        try {
          // Get ALL bookings without any filters (to avoid backend filtering issues)
          final bookingsData = await DataService.fetchBookings(
            excludeUserRole: true, // Completely exclude user_role parameter
          );
          
          DebugLogger.ui('🔍 _rejectOverlappingResidentBookings - API Response: ${bookingsData.keys.toList()}');
          DebugLogger.ui('🔍 _rejectOverlappingResidentBookings - Response success: ${bookingsData['success']}');
          
          if (bookingsData['success'] == true) {
            // Check both possible response keys: 'bookings' or 'data'
            List<dynamic> bookingsList = [];
            if (bookingsData['bookings'] != null) {
              bookingsList = bookingsData['bookings'];
              DebugLogger.ui('🔍 _rejectOverlappingResidentBookings - Using bookings key: ${bookingsList.length} total bookings');
            } else if (bookingsData['data'] != null) {
              bookingsList = bookingsData['data'];
              DebugLogger.ui('🔍 _rejectOverlappingResidentBookings - Using data key: ${bookingsList.length} total bookings');
            } else {
              DebugLogger.ui('🔍 _rejectOverlappingResidentBookings - No bookings found in response');
            }
            
            // Filter client-side for resident bookings with matching date and facility
            final targetDate = DateFormat('yyyy-MM-dd').format(widget.selectedDate);
            final targetFacilityId = widget.facility['id'].toString();
            
            DebugLogger.ui('🔍 _rejectOverlappingResidentBookings - Filtering for facility: $targetFacilityId, date: $targetDate');
            DebugLogger.ui('🔍 _rejectOverlappingResidentBookings - All bookings count: ${bookingsList.length}');
            
            // Debug: Show first few bookings to understand structure
            for (int i = 0; i < bookingsList.length && i < 5; i++) {
              final booking = bookingsList[i];
              DebugLogger.ui('🔍 All booking $i: ${booking['start_time']} - ${booking['status']} - ${booking['user_email']} - Facility: ${booking['facility_id']} - Date: ${booking['booking_date']} - Role: ${booking['user_role']}');
            }
            
            final residentBookings = List<Map<String, dynamic>>.from(bookingsList)
                .where((booking) => 
                    // Handle user_role being null, 'resident', or numeric values (0, 0.05, 0.1, etc from database)
                    (booking['user_role'] == 'resident' || 
                     booking['user_role'] == null || 
                     booking['user_role'] == '0' ||
                     booking['user_role'] == 0 ||  // Handle integer 0
                     booking['user_role'].toString().startsWith('0.') ||
                     booking['user_role'] == '0.05' ||
                     booking['user_role'] == 0.05 ||  // Handle double 0.05
                     booking['user_role'] == '0.1' ||
                     booking['user_role'] == 0.1) &&  // Handle double 0.1
                    (booking['status'] == 'pending' || booking['status'] == 'approved') &&
                    booking['facility_id'].toString() == targetFacilityId &&
                    booking['booking_date']?.toString() == targetDate
                )
                .toList();
            
            DebugLogger.ui('🔍 Found ${residentBookings.length} resident bookings to potentially reject');
            
            // Debug: Print resident bookings found
            for (int i = 0; i < residentBookings.length && i < 5; i++) {
              final booking = residentBookings[i];
              DebugLogger.ui('🔍 Resident booking to reject $i: ID=${booking['id']}, Status=${booking['status']}, Email=${booking['user_email']}, Time=${booking['start_time']}');
            }
            
            // Reject each overlapping resident booking with retry
            int rejectedCount = 0;
            for (final booking in residentBookings) {
              final success = await _rejectResidentBookingWithRetry(booking);
              if (success) rejectedCount++;
            }
            
            DebugLogger.ui('🔍 Successfully rejected $rejectedCount out of ${residentBookings.length} resident bookings');
            return; // Success, exit retry loop
            
          } else {
            DebugLogger.ui('🔍 _rejectOverlappingResidentBookings - API call failed: ${bookingsData['error']}');
          }
          
          break; // Success or non-network error, exit retry loop
          
        } catch (e) {
          retryCount++;
          DebugLogger.warning('🔍 Network error (attempt $retryCount/$maxRetries): $e');
          
          if (retryCount < maxRetries) {
            DebugLogger.ui('🔍 Retrying in 2 seconds...');
            await Future.delayed(const Duration(seconds: 2));
          } else {
            DebugLogger.error('❌ Failed to fetch resident bookings after $maxRetries attempts');
            _showErrorSnackBar('Network error: Some resident bookings may not be rejected. Please check manually.');
          }
        }
      }
    } catch (e) {
      DebugLogger.error('Error rejecting overlapping resident bookings: $e');
      _showErrorSnackBar('Error rejecting resident bookings: $e');
    }
  }

  Future<bool> _rejectResidentBookingWithRetry(Map<String, dynamic> residentBooking) async {
    int retryCount = 0;
    const maxRetries = 3;
    
    while (retryCount < maxRetries) {
      try {
        final bookingId = residentBooking['id'];
        final rejectionReason = 'This date has been booked by the Officials, refund of your payments will be done shortly, check your email or SMS for further details.';

        DebugLogger.ui('🔍 Rejecting resident booking: ID=$bookingId, Email=${residentBooking['user_email']}, Status=${residentBooking['status']}');
        DebugLogger.ui('🔍 Booking ID type: ${bookingId.runtimeType}, value: $bookingId');
        
        // Convert bookingId to int if it's a string
        final intBookingId = bookingId is int ? bookingId : int.tryParse(bookingId.toString()) ?? 0;
        
        if (intBookingId == 0) {
          DebugLogger.error('❌ Invalid booking ID: $bookingId');
          return false;
        }
        
        // Call API to update resident booking status
        final response = await api_service.ApiService.updateBookingStatus(
          intBookingId, 
          'rejected', 
          rejectionReason: rejectionReason,
          rejectionType: 'official_overlap'  // This doesn't count as violation
        );
        
        DebugLogger.ui('🔍 _rejectResidentBooking response: $response');
        
        if (response['success'] == true) {
          DebugLogger.ui('✅ Successfully rejected resident booking $intBookingId');
          return true;
        } else {
          DebugLogger.error('❌ Failed to reject resident booking $intBookingId: ${response['error'] ?? response['message']}');
          return false;
        }
      } catch (e) {
        retryCount++;
        DebugLogger.warning('🔍 Network error rejecting booking (attempt $retryCount/$maxRetries): $e');
        
        if (retryCount < maxRetries) {
          DebugLogger.ui('🔍 Retrying booking rejection in 2 seconds...');
          await Future.delayed(const Duration(seconds: 2));
        } else {
          DebugLogger.error('❌ Failed to reject resident booking ${residentBooking['id']} after $maxRetries attempts');
          return false;
        }
      }
    }
    
    return false;
  }

  Future<void> _showDetailedSuccessDialog(String message, List<Map<String, dynamic>> rejectedBookings) async {
    return showDialog<void>(
      context: context,
      builder: (BuildContext context) {
        return AlertDialog(
          title: Row(
            children: [
              Icon(Icons.check_circle, color: Colors.green, size: 24),
              const SizedBox(width: 8),
              Expanded(
                child: const Text(
                  'Booking Successful!',
                  style: TextStyle(fontSize: 16),
                  overflow: TextOverflow.ellipsis,
                ),
              ),
            ],
          ),
          content: SizedBox(
            width: double.maxFinite,
            child: SingleChildScrollView(
              child: Column(
                mainAxisSize: MainAxisSize.min,
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    message,
                    style: const TextStyle(fontSize: 14),
                  ),
                  const SizedBox(height: 16),
                  const Text(
                    'Auto-rejected Resident Bookings:',
                    style: TextStyle(fontWeight: FontWeight.bold, fontSize: 16),
                  ),
                  const SizedBox(height: 8),
                  ...rejectedBookings.asMap().entries.map((entry) {
                    final index = entry.key;
                    final booking = entry.value;
                    return Container(
                      margin: const EdgeInsets.only(bottom: 8),
                      padding: const EdgeInsets.all(12),
                      decoration: BoxDecoration(
                        color: Colors.red.shade50,
                        borderRadius: BorderRadius.circular(8),
                        border: Border.all(color: Colors.red.shade200),
                      ),
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Text(
                            '${index + 1}. ${booking['resident_name']}',
                            style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 12),
                            overflow: TextOverflow.ellipsis,
                          ),
                          Text(
                            'Email: ${booking['resident_email']}',
                            style: const TextStyle(fontSize: 11),
                            overflow: TextOverflow.ellipsis,
                          ),
                          Text(
                            'Time: ${booking['timeslot']}',
                            style: const TextStyle(fontSize: 11),
                            overflow: TextOverflow.ellipsis,
                          ),
                          const Text(
                            'Status: Rejected with apology',
                            style: TextStyle(
                              color: Colors.red,
                              fontWeight: FontWeight.w500,
                              fontSize: 11,
                            ),
                          ),
                        ],
                      ),
                    );
                  }).toList(),
                  const SizedBox(height: 8),
                  const Text(
                    'Note: Residents will receive an apology message and refund notification.',
                    style: TextStyle(
                      fontSize: 12,
                      color: Colors.grey,
                      fontStyle: FontStyle.italic,
                    ),
                  ),
                ],
              ),
            ),
          ),
          actions: [
            TextButton(
              onPressed: () {
                DebugLogger.ui('🎯 Dialog OK button pressed - closing dialog');
                Navigator.of(context).pop(); // Just close the dialog
              },
              child: const Text('OK'),
            ),
          ],
        );
      },
    );
  }

  void _showErrorSnackBar(String message) {
    if (mounted) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text(message),
          backgroundColor: Colors.red,
        ),
      );
    }
  }

  void _showSuccessSnackBar(String message) {
    if (mounted) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text(message),
          backgroundColor: Colors.green,
        ),
      );
    }
  }

  String _formatTimeForDisplay(String time) {
    // Format time for consistent display
    return time.replaceAll(' AM', ' AM').replaceAll(' PM', ' PM');
  }

  Widget _buildFacilityDetails() {
    return Container(
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(12),
        boxShadow: [
          BoxShadow(
            color: Colors.black.withOpacity(0.1),
            blurRadius: 4,
            offset: const Offset(0, 2),
          ),
        ],
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              Icon(
                Icons.business,
                color: Colors.red.shade800,
                size: 24,
              ),
              const SizedBox(width: 12),
              Text(
                'Selected Date: ${DateFormat('MMMM dd, yyyy').format(widget.selectedDate)}',
                style: const TextStyle(
                  fontSize: 16,
                  fontWeight: FontWeight.w500,
                ),
              ),
            ],
          ),
          const SizedBox(height: 12),
          Text(
            widget.facility['name'] ?? 'Facility',
            style: const TextStyle(
              fontSize: 18,
              fontWeight: FontWeight.bold,
            ),
          ),
          if (widget.facility['description'] != null) ...[
            const SizedBox(height: 8),
            Text(
              widget.facility['description'],
              style: const TextStyle(
                fontSize: 14,
                color: Colors.grey,
              ),
            ),
          ],
        ],
      ),
    );
  }

  Widget _buildDateSection() {
    return Container(
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(12),
        boxShadow: [
          BoxShadow(
            color: Colors.black.withOpacity(0.1),
            blurRadius: 4,
            offset: const Offset(0, 2),
          ),
        ],
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              Icon(
                Icons.calendar_today,
                color: Colors.red.shade800,
                size: 24,
              ),
              const SizedBox(width: 12),
              Text(
                'Selected Date: ${DateFormat('MMMM dd, yyyy').format(widget.selectedDate)}',
                style: const TextStyle(
                  fontSize: 16,
                  fontWeight: FontWeight.w500,
                ),
              ),
            ],
          ),
        ],
      ),
    );
  }

  Widget _buildTimeSlotsSection() {
    if (_allTimeSlots.isEmpty) {
      return const Center(child: Text('No time slots available'));
    }

    return Container(
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(12),
        boxShadow: [
          BoxShadow(
            color: Colors.black.withOpacity(0.1),
            blurRadius: 4,
            offset: const Offset(0, 2),
          ),
        ],
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              Icon(
                Icons.access_time,
                color: Colors.red.shade800,
                size: 24,
              ),
              const SizedBox(width: 12),
              Expanded(
                child: const Text(
                  'Resident Bookings for This Date',
                  style: TextStyle(
                    fontSize: 18,
                    fontWeight: FontWeight.bold,
                  ),
                  overflow: TextOverflow.ellipsis,
                ),
              ),
            ],
          ),
          const SizedBox(height: 8),
          Text(
            'Review resident bookings for this date. Your official booking will automatically reject all resident bookings.',
            style: TextStyle(
              fontSize: 12,
              color: Colors.grey.shade600,
            ),
          ),
          const SizedBox(height: 16),
          GridView.builder(
            shrinkWrap: true,
            physics: const NeverScrollableScrollPhysics(),
            gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
              crossAxisCount: 2,
              crossAxisSpacing: 12,
              mainAxisSpacing: 12,
              childAspectRatio:1.1, // Increased aspect ratio to give more height
            ),
            itemCount: _allTimeSlots.length,
            itemBuilder: (context, index) {
              final timeSlot = _allTimeSlots[index];
              final hasResidentBooking = timeSlot['has_resident_booking'] == true;
              
              return InkWell(
                onTap: () {
                  // Only show resident booking details - no selection needed for officials
                  if (hasResidentBooking) {
                    _showResidentBookingDetails(timeSlot);
                  }
                },
                borderRadius: BorderRadius.circular(8),
                child: Container(
                  padding: const EdgeInsets.all(8), // Reduced padding
                  decoration: BoxDecoration(
                    color: timeSlot['background_color'],
                    borderRadius: BorderRadius.circular(8),
                    border: Border.all(color: timeSlot['border_color']),
                  ),
                  child: Center(
                    child: Column(
                      mainAxisAlignment: MainAxisAlignment.center,
                      mainAxisSize: MainAxisSize.min, // Added to minimize space
                      children: [
                        Text(
                          timeSlot['time_slot'],
                          style: TextStyle(
                            fontSize: 10, // Reduced font size
                            color: timeSlot['text_color'],
                            fontWeight: FontWeight.bold,
                          ),
                          textAlign: TextAlign.center,
                        ),
                        if (hasResidentBooking) ...[
                          const SizedBox(height: 2), // Reduced spacing
                          Container(
                            padding: const EdgeInsets.symmetric(horizontal: 4, vertical: 1), // Reduced padding
                            decoration: BoxDecoration(
                              color: timeSlot['border_color'].withOpacity(0.2),
                              borderRadius: BorderRadius.circular(4),
                            ),
                            child: Row(
                              mainAxisSize: MainAxisSize.min,
                              children: [
                                Text(
                                  timeSlot['resident_count'] > 1 
                                      ? '${timeSlot['resident_count']} ${timeSlot['resident_booking']['status'] == 'approved' ? 'Approved' : 'Pending'}'
                                      : (timeSlot['resident_booking']['status'] == 'approved' ? 'Approved' : 'Pending'),
                                  style: TextStyle(
                                    fontSize: 8, // Reduced font size
                                    color: timeSlot['border_color'],
                                    fontWeight: FontWeight.bold,
                                  ),
                                ),
                              ],
                            ),
                          ),
                        ],
                      ],
                    ),
                  ),
                ),
              );
            },
          ),
        ],
      ),
    );
  }

  Widget _buildSubmitButton() {
    return SizedBox(
      width: double.infinity,
      child: ElevatedButton(
        onPressed: _isSubmitting ? null : _submitBooking,
        style: ElevatedButton.styleFrom(
          backgroundColor: Colors.red.shade800,
          foregroundColor: Colors.white,
          padding: const EdgeInsets.symmetric(vertical: 16),
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(8),
          ),
        ),
        child: _isSubmitting
            ? const Row(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  SizedBox(
                    width: 20,
                    height: 20,
                    child: CircularProgressIndicator(
                      strokeWidth: 2,
                      valueColor: AlwaysStoppedAnimation<Color>(Colors.white),
                    ),
                  ),
                  const SizedBox(width: 8),
                  Text('Creating Booking...'),
                ],
              )
            : const Text('Book Entire Day'),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Official Booking - ${widget.facility['name']}'),
        backgroundColor: Colors.red.shade800,
        foregroundColor: Colors.white,
      ),
      body: _isLoadingTimeSlots
          ? const LoadingWidget(message: 'Loading time slots...')
          : SingleChildScrollView(
              padding: const EdgeInsets.all(16),
              child: Form(
                key: _formKey,
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    _buildFacilityDetails(),
                    const SizedBox(height: 24),
                    _buildDateSection(),
                    const SizedBox(height: 24),
                    _buildTimeSlotsSection(),
                    const SizedBox(height: 32),
                    _buildSubmitButton(),
                  ],
                ),
              ),
          ),
    );
  }
}
