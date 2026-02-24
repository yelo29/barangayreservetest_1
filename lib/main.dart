import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'utils/debug_logger.dart';
import 'services/auth_api_service.dart';
import 'services/ban_detection_service.dart';
import 'screens/selection_screen.dart';
import 'config/app_config.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  
  try {
    // Using computer IP from server log
    DebugLogger.ui('Using computer IP for development');
    DebugLogger.ui('Server URL: ${AppConfig.baseUrl}');
    DebugLogger.ui('Computer IP server ready for barangay operations');
    
    // Initialize user session
    await AuthApiService.instance.initializeUser();
    DebugLogger.ui('User session initialized');
  } catch (e) {
    DebugLogger.error('Initialization error: $e');
  }
  
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Barangay Reserve',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(fontFamily: 'Roboto'),
      home: SelectionScreen(
        navigatorKey: GlobalKey<NavigatorState>(), // Pass navigator key to selection screen
      ),
    );
  }
}

/// Shared enum for account type
enum AccountType { resident, official }
