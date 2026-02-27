import 'dart:async';
import 'package:flutter/material.dart';
import '../services/api_service.dart';

class AutoRefreshService {
  static final AutoRefreshService _instance = AutoRefreshService._internal();
  factory AutoRefreshService() => _instance;
  AutoRefreshService._internal();

  final Map<String, StreamController<Map<String, dynamic>>> _refreshControllers = {};
  final Map<String, VoidCallback> _refreshCallbacks = {};
  
  /// Register a refresh callback for a specific screen/component
  void registerRefreshCallback(String componentId, VoidCallback callback) {
    _refreshCallbacks[componentId] = callback;
    print('🔄 Registered refresh callback for: $componentId');
  }
  
  /// Unregister a refresh callback
  void unregisterRefreshCallback(String componentId) {
    _refreshCallbacks.remove(componentId);
    print('🔄 Unregistered refresh callback for: $componentId');
  }
  
  /// Get a stream for refresh events
  Stream<Map<String, dynamic>> getRefreshStream(String componentId) {
    _refreshControllers.putIfAbsent(componentId, () => StreamController<Map<String, dynamic>>.broadcast());
    return _refreshControllers[componentId]!.stream;
  }
  
  /// Trigger auto-refresh based on API response refresh_data
  void triggerAutoRefresh(Map<String, dynamic> refreshData) {
    print('🔄 Auto-refresh triggered: ${refreshData['trigger']}');
    
    final String trigger = refreshData['trigger'] ?? 'unknown';
    final List<String> requiresRefresh = List<String>.from(refreshData['requires_refresh'] ?? []);
    
    // Execute refresh callbacks for each required component
    for (String component in requiresRefresh) {
      if (_refreshCallbacks.containsKey(component)) {
        print('🔄 Executing refresh for: $component');
        _refreshCallbacks[component]!();
        
        // Send refresh event to stream
        if (_refreshControllers.containsKey(component)) {
          _refreshControllers[component]!.add({
            'trigger': trigger,
            'timestamp': refreshData['timestamp'],
            'data': refreshData,
          });
        }
      } else {
        print('⚠️ No refresh callback registered for: $component');
      }
    }
    
    // Handle special cases
    _handleSpecialRefreshCases(refreshData);
  }
  
  /// Handle special refresh cases with cross-implications
  void _handleSpecialRefreshCases(Map<String, dynamic> refreshData) {
    final String trigger = refreshData['trigger'] ?? '';
    
    switch (trigger) {
      case 'booking_created':
        _handleBookingCreatedRefresh(refreshData);
        break;
      case 'booking_updated':
        _handleBookingUpdatedRefresh(refreshData);
        break;
      case 'booking_cancelled':
        _handleBookingCancelledRefresh(refreshData);
        break;
      case 'profile_updated':
        _handleProfileUpdatedRefresh(refreshData);
        break;
      case 'verification_submitted':
        _handleVerificationSubmittedRefresh(refreshData);
        break;
    }
  }
  
  /// Handle booking creation refresh with cross-implications
  void _handleBookingCreatedRefresh(Map<String, dynamic> refreshData) {
    final String facilityId = refreshData['facility_id']?.toString() ?? '';
    final String bookingDate = refreshData['booking_date'] ?? '';
    final String user_email = refreshData['user_email'] ?? '';
    
    print('🔄 Handling booking creation refresh:');
    print('  - Facility ID: $facilityId');
    print('  - Booking Date: $bookingDate');
    print('  - User Email: $user_email');
    
    // If there are rejected bookings, trigger additional refreshes
    if (refreshData.containsKey('rejected_bookings')) {
      final List<dynamic> rejectedBookings = refreshData['rejected_bookings'];
      print('🔄 Refreshing for ${rejectedBookings.length} rejected bookings');
      
      for (var rejectedBooking in rejectedBookings) {
        final String residentEmail = rejectedBooking['resident_email'] ?? '';
        if (residentEmail.isNotEmpty) {
          // Trigger refresh for affected residents
          _refreshCallbacks['user_notifications']?.call();
        }
      }
    }
  }
  
  /// Handle booking update refresh
  void _handleBookingUpdatedRefresh(Map<String, dynamic> refreshData) {
    print('🔄 Handling booking update refresh');
    // Refresh booking details and status
    _refreshCallbacks['booking_details']?.call();
    _refreshCallbacks['bookings_list']?.call();
  }
  
  /// Handle booking cancellation refresh
  void _handleBookingCancelledRefresh(Map<String, dynamic> refreshData) {
    print('🔄 Handling booking cancellation refresh');
    // Refresh calendar availability and user bookings
    _refreshCallbacks['calendar_view']?.call();
    _refreshCallbacks['bookings_list']?.call();
    _refreshCallbacks['time_slots']?.call();
  }
  
  /// Handle profile update refresh
  void _handleProfileUpdatedRefresh(Map<String, dynamic> refreshData) {
    print('🔄 Handling profile update refresh');
    
    final List<String> updatedFields = List<String>.from(refreshData['updated_fields'] ?? []);
    
    // Refresh user data across all screens
    _refreshCallbacks['user_profile']?.call();
    _refreshCallbacks['account_settings']?.call();
    _refreshCallbacks['resident_dashboard']?.call();
    
    // If profile photo was updated, trigger additional refreshes
    if (updatedFields.contains('profile_photo_url')) {
      print('🔄 Profile photo updated - triggering photo-specific refreshes');
      _refreshCallbacks['profile_photo_display']?.call();
      _refreshCallbacks['official_profile']?.call();
    }
    
    // If name was updated, refresh displays that show user name
    if (updatedFields.contains('full_name')) {
      print('🔄 User name updated - refreshing name displays');
      _refreshCallbacks['user_name_display']?.call();
    }
  }
  
  /// Handle verification submission refresh
  void _handleVerificationSubmittedRefresh(Map<String, dynamic> refreshData) {
    print('🔄 Handling verification submission refresh');
    // Refresh verification status and lock state
    _refreshCallbacks['verification_status']?.call();
    _refreshCallbacks['profile_verification']?.call();
    _refreshCallbacks['account_settings']?.call();
  }
  
  /// Cleanup method to dispose all controllers
  void dispose() {
    for (var controller in _refreshControllers.values) {
      controller.close();
    }
    _refreshControllers.clear();
    _refreshCallbacks.clear();
    print('🔄 AutoRefreshService disposed');
  }
}

/// Mixin for widgets that need auto-refresh functionality
mixin AutoRefreshMixin<T extends StatefulWidget> on State<T> {
  late final String _refreshComponentId;
  StreamSubscription<Map<String, dynamic>>? _refreshSubscription;
  
  /// Initialize auto-refresh for this widget
  void initAutoRefresh(String componentId) {
    _refreshComponentId = componentId;
    
    // Register for refresh events
    _refreshSubscription = AutoRefreshService().getRefreshStream(componentId).listen((refreshData) {
      if (mounted) {
        onAutoRefresh(refreshData);
      }
    });
    
    print('🔄 Auto-refresh initialized for: $componentId');
  }
  
  /// Override this method to handle auto-refresh events
  void onAutoRefresh(Map<String, dynamic> refreshData) {
    // Default implementation - override in widgets
    print('🔄 Auto-refresh received in ${widget.runtimeType}: ${refreshData['trigger']}');
  }
  
  /// Register a refresh callback for this widget
  void registerRefreshCallback(VoidCallback callback) {
    AutoRefreshService().registerRefreshCallback(_refreshComponentId, callback);
  }
  
  /// Unregister refresh callback
  void unregisterRefreshCallback() {
    AutoRefreshService().unregisterRefreshCallback(_refreshComponentId);
  }
  
  @override
  void dispose() {
    _refreshSubscription?.cancel();
    AutoRefreshService().unregisterRefreshCallback(_refreshComponentId);
    super.dispose();
  }
}
