import 'package:flutter/material.dart';

/// Stub service - ban detection logic removed
/// User will implement new approach for handling banned users
class BanDetectionService {
  static final BanDetectionService _instance = BanDetectionService._internal();
  factory BanDetectionService() => _instance;
  BanDetectionService._internal();

  static GlobalKey<NavigatorState>? _navigatorKey;

  /// Set navigator key for showing dialogs (kept for compatibility)
  static void setNavigatorKey(GlobalKey<NavigatorState> navigatorKey) {
    _navigatorKey = navigatorKey;
  }

  /// Stub method - ban detection removed
  static Future<bool> checkAndHandleBanStatus() async {
    // Ban detection logic removed - user will implement new approach
    return false;
  }

  /// Stub method - ban detection removed
  static Future<void> _forceLogoutForBannedUser(String banReason) async {
    // Forced logout logic removed - user will implement new approach
    print('Ban detection and forced logout removed - user will implement new approach');
  }

  /// Stub method - ban dialog removed
  static void _showBanDialog(String banReason) {
    // Ban dialog logic removed - user will implement new approach
    print('Ban dialog logic removed - user will implement new approach');
  }
}
