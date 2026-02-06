import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'utils/debug_logger.dart';
import 'services/auth_api_service.dart';
import 'screens/selection_screen.dart';
import 'config/app_config.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  
  try {
    // Using hardcoded ngrok URL - no need to load config
    DebugLogger.ui('Using hardcoded global server URL');
    DebugLogger.ui('Server URL: ${AppConfig.baseUrl}');
    DebugLogger.ui('Global server ready for barangay operations');
    
    // Initialize user session
    await AuthApiService().initializeUser();
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
      home: const SelectionScreen(),
    );
  }
}

/// Shared enum for account type
enum AccountType { resident, official }
