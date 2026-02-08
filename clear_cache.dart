import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'dart:io';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  
  // Clear all SharedPreferences
  final prefs = await SharedPreferences.getInstance();
  await prefs.clear();
  
  print('✅ All SharedPreferences cleared!');
  
  // Exit
  exit(0);
}
