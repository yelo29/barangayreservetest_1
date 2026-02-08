import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:io';
import 'lib/config/app_config.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  
  print('🔍 Testing direct connection...');
  print('🔍 Base URL: ${AppConfig.baseUrl}');
  
  try {
    final response = await http.post(
      Uri.parse('${AppConfig.baseUrl}/api/auth/login'),
      headers: {'Content-Type': 'application/json'},
      body: '{"email":"test","password":"test"}',
    );
    
    print('🔍 Response status: ${response.statusCode}');
    print('🔍 Response body: ${response.body}');
  } catch (e) {
    print('❌ Error: $e');
  }
  
  exit(0);
}
