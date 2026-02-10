import 'dart:async';
import 'package:flutter/material.dart';
import 'auth_api_service.dart';
import 'api_service.dart';

/// Service for detecting and handling banned user automatic logout
class BanDetectionService {
  static final BanDetectionService _instance = BanDetectionService._internal();
  factory BanDetectionService() => _instance;
  BanDetectionService._internal();

  static GlobalKey<NavigatorState>? _navigatorKey;
  static bool _isShowingBanDialog = false;

  /// Set navigator key for showing dialogs
  static void setNavigatorKey(GlobalKey<NavigatorState> navigatorKey) {
    _navigatorKey = navigatorKey;
  }

  /// Check if current user is banned and handle automatic logout
  static Future<bool> checkAndHandleBanStatus() async {
    final currentUser = AuthApiService().currentUser;
    
    if (currentUser == null || currentUser['email'] == null) {
      return false;
    }

    try {
      print('🔍 BanDetectionService: Checking ban status for user: ${currentUser['email']}');
      
      // Get fresh user profile from server
      final profileResponse = await ApiService.getUserProfile(currentUser['email']);
      
      if (profileResponse['success'] == true && profileResponse['user'] != null) {
        final userData = profileResponse['user'];
        
        // Check ban status - handle both boolean and integer formats
        dynamic bannedValue = userData['is_banned'] ?? false;
        bool isCurrentlyBanned = bannedValue is bool ? bannedValue : (bannedValue == 1 || bannedValue == true);
        
        print('🔍 BanDetectionService: Ban check result:');
        print('  - User email: ${currentUser['email']}');
        print('  - is_banned value: $bannedValue');
        print('  - is_banned type: ${bannedValue.runtimeType}');
        print('  - isCurrentlyBanned: $isCurrentlyBanned');
        print('  - Previous cached ban status: ${currentUser['is_banned']}');
        
        // CRITICAL: If user is now banned but wasn't before, force logout
        if (isCurrentlyBanned && !(currentUser['is_banned'] == true)) {
          print('🚨 BanDetectionService: USER BANNED DETECTED - FORCING AUTOMATIC LOGOUT');
          await _forceLogoutForBannedUser(userData['ban_reason'] ?? 'Your account has been banned');
          return true; // User was banned and logged out
        }
        
        // Update local ban status
        currentUser['is_banned'] = isCurrentlyBanned;
        
        return false; // User is not newly banned
      } else {
        print('🔍 BanDetectionService: Failed to fetch user profile: ${profileResponse['error']}');
        return false;
      }
    } catch (e) {
      print('🔍 BanDetectionService: Error checking ban status: $e');
      return false;
    }
  }

  /// Force logout for banned user with proper UI notification
  static Future<void> _forceLogoutForBannedUser(String banReason) async {
    if (_isShowingBanDialog) {
      print('🔍 BanDetectionService: Ban dialog already showing, skipping');
      return;
    }

    _isShowingBanDialog = true;
    
    print('🚨 BanDetectionService: FORCING LOGOUT FOR BANNED USER');
    print('🚨 Ban reason: $banReason');
    
    try {
      // Logout user through AuthApiService
      await AuthApiService().signOut();
      
      print('🚨 BanDetectionService: User logged out successfully');
      
      // Show ban dialog to user
      _showBanDialog(banReason);
      
    } catch (e) {
      print('🚨 BanDetectionService: Error during forced logout: $e');
    } finally {
      _isShowingBanDialog = false;
    }
  }

  /// Show ban notification dialog to user
  static void _showBanDialog(String banReason) {
    if (_navigatorKey == null) {
      print('🔍 BanDetectionService: No navigator key available, cannot show dialog');
      return;
    }

    final context = _navigatorKey!.currentContext;
    if (context == null) {
      print('🔍 BanDetectionService: No context available, cannot show dialog');
      return;
    }

    showDialog(
      context: context!,
      barrierDismissible: false, // Prevent dialog from being dismissed
      builder: (context) => AlertDialog(
        title: Row(
          children: [
            Icon(Icons.block, color: Colors.red, size: 28),
            SizedBox(width: 8),
            Text('Account Banned', style: TextStyle(color: Colors.red)),
          ],
        ),
        content: Column(
          mainAxisSize: MainAxisSize.min,
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              'Your account has been banned!',
              style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
            ),
            SizedBox(height: 12),
            Text(
              banReason.isNotEmpty 
                  ? banReason 
                  : 'Your account has been banned due to policy violations. Please contact the barangay office for assistance.',
              style: TextStyle(fontSize: 14),
            ),
            SizedBox(height: 12),
            Text(
              'You have been automatically logged out for security reasons.',
              style: TextStyle(fontSize: 12, fontStyle: FontStyle.italic),
            ),
          ],
        ),
        actions: [
          TextButton(
            onPressed: () {
              Navigator.of(context).pop(); // Close dialog
              // Navigate to login screen
              Navigator.of(context).pushNamedAndRemoveUntil('/login', (route) => false);
            },
            child: Text('OK'),
          ),
        ],
      ),
    );
  }

  /// Check ban status before critical operations
  static Future<bool> checkBanBeforeOperation(String operation) async {
    print('🔍 BanDetectionService: Checking ban status before operation: $operation');
    
    final isBanned = await checkAndHandleBanStatus();
    
    if (isBanned) {
      print('🚨 BanDetectionService: Operation blocked due to ban status: $operation');
    }
    
    return !isBanned; // Return true if operation can proceed
  }
}
