import 'package:flutter/material.dart';
import '../../../services/data_service.dart';
import '../../../services/auth_api_service.dart';
import '../../../utils/debug_logger.dart';
import '../resident/my_bookings_page.dart';

class ResidentBookingsTab extends StatefulWidget {
  final Map<String, dynamic>? userData;

  const ResidentBookingsTab({super.key, this.userData});

  @override
  State<ResidentBookingsTab> createState() => _ResidentBookingsTabState();
}

class _ResidentBookingsTabState extends State<ResidentBookingsTab> {
  List<Map<String, dynamic>> _myBookings = [];
  bool _isLoading = true;

  @override
  void initState() {
    super.initState();
    _loadMyBookings();
  }

  Future<void> _loadMyBookings() async {
    try {
      DebugLogger.ui('Loading my bookings for resident...');
      print('🔍 _loadMyBookings() called'); // Debug logging
      
      // Use DataService for consistent data fetching
      final bookingsResponse = await DataService.fetchBookings();
      
      if (bookingsResponse['success'] == true) {
        final List<Map<String, dynamic>> bookings = bookingsResponse['data'] ?? [];
        print('🔍 Received ${bookings.length} bookings from DataService'); // Debug logging
        
        // Filter bookings for current user (DataService already filters by user email for residents)
        final myBookings = bookings.where((booking) => 
          booking['user_email'] != null
        ).toList();
        
        print('🔍 Filtered to ${myBookings.length} bookings for current user'); // Debug logging
        
        setState(() {
          _myBookings = myBookings;
          DebugLogger.ui('Loaded ${_myBookings.length} bookings for resident');
          _isLoading = false;
        });
      } else {
        throw Exception(bookingsResponse['error'] ?? 'Failed to fetch bookings');
      }
    } catch (e) {
      DebugLogger.error('Error loading my bookings: $e');
      print('🔍 Error loading bookings: $e'); // Debug logging
      setState(() {
        _myBookings = [];
        _isLoading = false;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    if (_isLoading) {
      return const Center(
        child: CircularProgressIndicator(),
      );
    }

    return MyBookingsPage(bookings: _myBookings);
  }
}
