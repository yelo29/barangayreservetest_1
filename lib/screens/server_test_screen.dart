import 'package:flutter/material.dart';
import '../services/api_service.dart';

class ServerTestScreen extends StatefulWidget {
  const ServerTestScreen({super.key});

  @override
  State<ServerTestScreen> createState() => _ServerTestScreenState();
}

class _ServerTestScreenState extends State<ServerTestScreen> {
  bool _isLoading = false;
  String _testResult = '';
  List<Map<String, dynamic>> _facilities = [];

  Future<void> _testConnection() async {
    setState(() {
      _isLoading = true;
      _testResult = 'Testing connection...';
    });

    try {
      // Test basic connection
      bool isConnected = await ApiService.testConnection();
      
      if (isConnected) {
        _testResult = '✅ Server connected successfully!';
        
        // Get facilities
        _facilities = await ApiService.getFacilities();
        _testResult += '\n✅ Found ${_facilities.length} facilities';
        
        // Test login
        var loginResult = await ApiService.login('resident@barangay.com', 'password123');
        if (loginResult['success']) {
          _testResult += '\n✅ Login test successful';
        } else {
          _testResult += '\n❌ Login test failed';
        }
      } else {
        _testResult = '❌ Cannot connect to server';
      }
    } catch (e) {
      _testResult = '❌ Error: $e';
    }

    setState(() {
      _isLoading = false;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Server Connection Test'),
        backgroundColor: Colors.red,
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text(
              'Testing Your Server:',
              style: TextStyle(
                fontSize: 20,
                fontWeight: FontWeight.bold,
              ),
            ),
            const SizedBox(height: 16),
            const Text(
              'Server URL: http://17e7be97-c49c-4e8b-8a8a-be09070d6354.duckdns.org:8080',
              style: TextStyle(fontSize: 14, color: Colors.grey),
            ),
            const SizedBox(height: 24),
            ElevatedButton(
              onPressed: _isLoading ? null : _testConnection,
              style: ElevatedButton.styleFrom(
                backgroundColor: Colors.red,
                foregroundColor: Colors.white,
                padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 12),
              ),
              child: _isLoading 
                ? const CircularProgressIndicator(color: Colors.white)
                : const Text('Test Connection'),
            ),
            const SizedBox(height: 24),
            Container(
              width: double.infinity,
              padding: const EdgeInsets.all(16),
              decoration: BoxDecoration(
                color: Colors.grey.shade100,
                borderRadius: BorderRadius.circular(8),
                border: Border.all(color: Colors.grey.shade300),
              ),
              child: Text(
                _testResult.isEmpty ? 'Click "Test Connection" to start' : _testResult,
                style: const TextStyle(fontFamily: 'monospace'),
              ),
            ),
            if (_facilities.isNotEmpty) ...[
              const SizedBox(height: 24),
              const Text(
                'Available Facilities:',
                style: TextStyle(
                  fontSize: 18,
                  fontWeight: FontWeight.bold,
                ),
              ),
              const SizedBox(height: 8),
              Expanded(
                child: ListView.builder(
                  itemCount: _facilities.length,
                  itemBuilder: (context, index) {
                    final facility = _facilities[index];
                    return Card(
                      child: ListTile(
                        title: Text(facility['name'] ?? 'Unknown'),
                        subtitle: Text(facility['description'] ?? ''),
                        trailing: Text('₱${facility['price'] ?? 0}'),
                      ),
                    );
                  },
                ),
              ),
            ],
          ],
        ),
      ),
    );
  }
}
