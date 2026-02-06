import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:http/http.dart' as http;
import '../config/app_config.dart';

class ServerConfigScreen extends StatefulWidget {
  const ServerConfigScreen({super.key});

  @override
  State<ServerConfigScreen> createState() => _ServerConfigScreenState();
}

class _ServerConfigScreenState extends State<ServerConfigScreen> {
  final TextEditingController _urlController = TextEditingController();
  bool _isLoading = false;
  bool _isTesting = false;

  @override
  void initState() {
    super.initState();
    _loadCurrentConfig();
  }

  Future<void> _loadCurrentConfig() async {
    final prefs = await SharedPreferences.getInstance();
    // Get saved server URL or use default
    final savedUrl = prefs.getString('server_url') ?? AppConfig.baseUrl;
    if (mounted) {
      setState(() {
        _urlController.text = savedUrl;
      });
    }
  }

  Future<void> _saveConfig() async {
    if (mounted) {
      setState(() => _isLoading = true);
    }
    
    try {
      final url = _urlController.text.trim();
      
      if (!AppConfig.isValidUrl(url)) {
        _showError('Please enter a valid URL (e.g., http://192.168.1.100:8080)');
        return;
      }

      // Save to preferences
      final prefs = await SharedPreferences.getInstance();
      await prefs.setString('server_url', url);
      
      // Update app config
      AppConfig.setBaseUrl(url);
      
      _showSuccess('Server configuration saved successfully!');
      
    } catch (e) {
      _showError('Failed to save configuration: $e');
    } finally {
      if (mounted) {
        setState(() => _isLoading = false);
      }
    }
  }

  Future<void> _testConnection() async {
    if (mounted) {
      setState(() => _isTesting = true);
    }
    
    try {
      final url = _urlController.text.trim();
      
      if (!AppConfig.isValidUrl(url)) {
        _showError('Please enter a valid URL first');
        return;
      }

      // Temporarily set URL for testing
      AppConfig.setBaseUrl(url);
      
      // Test API connection
      final testUrl = '${AppConfig.baseUrl}/api/me?email=test@example.com';
      print('🔍 Testing connection to: $testUrl');
      print('🔍 AppConfig.baseUrl is: ${AppConfig.baseUrl}');
      
      final response = await http.get(
        Uri.parse(testUrl),
        headers: {'Content-Type': 'application/json'},
      );
      
      print('🔍 Response status: ${response.statusCode}');
      print('🔍 Response body: ${response.body}');
      
      if (response.statusCode == 200) {
        _showSuccess('Server connection successful!');
      } else {
        _showError('Server responded with error: ${response.statusCode}');
      }
      
    } catch (e) {
      _showError('Failed to connect to server: $e');
    } finally {
      if (mounted) {
        setState(() => _isTesting = false);
      }
      // Restore original config
      await _loadCurrentConfig();
    }
  }

  void _showError(String message) {
    if (mounted) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text(message),
          backgroundColor: Colors.red,
        ),
      );
    }
  }

  void _showSuccess(String message) {
    if (mounted) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text(message),
          backgroundColor: Colors.green,
        ),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Server Configuration'),
        backgroundColor: Colors.blue[600],
        foregroundColor: Colors.white,
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            // Current configuration info
            Card(
              child: Padding(
                padding: const EdgeInsets.all(16.0),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    const Text(
                      'Current Configuration',
                      style: TextStyle(
                        fontSize: 18,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                    const SizedBox(height: 8),
                    Text('URL: ${AppConfig.baseUrl}'),
                    Text('Is DuckDNS: ${AppConfig.isDuckDnsUrl(AppConfig.baseUrl)}'),
                    Text('Domain: ${AppConfig.extractDomain(AppConfig.baseUrl)}'),
                  ],
                ),
              ),
            ),
            
            const SizedBox(height: 16),
            
            // URL input
            TextField(
              controller: _urlController,
              decoration: const InputDecoration(
                labelText: 'Server URL',
                hintText: 'http://192.168.1.100:8080',
                border: OutlineInputBorder(),
                helperText: 'Enter your server URL (DuckDNS or IP address)',
              ),
            ),
            
            const SizedBox(height: 16),
            
            // Quick setup buttons
            const Text(
              'Quick Setup:',
              style: TextStyle(fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 8),
            Wrap(
              spacing: 8,
              children: [
                _buildQuickButton('localhost', AppConfig.commonUrls['localhost']!),
                _buildQuickButton('DuckDNS', AppConfig.commonUrls['duckdns']!),
                _buildQuickButton('HTTPS', AppConfig.commonUrls['production_template']!),
              ],
            ),
            
            const SizedBox(height: 24),
            
            // Action buttons
            Row(
              children: [
                Expanded(
                  child: ElevatedButton(
                    onPressed: _isTesting ? null : _testConnection,
                    child: _isTesting
                        ? const CircularProgressIndicator()
                        : const Text('Test Connection'),
                  ),
                ),
                const SizedBox(width: 16),
                Expanded(
                  child: ElevatedButton(
                    onPressed: _isLoading ? null : _saveConfig,
                    style: ElevatedButton.styleFrom(
                      backgroundColor: Colors.green,
                      foregroundColor: Colors.white,
                    ),
                    child: _isLoading
                        ? const CircularProgressIndicator()
                        : const Text('Save Configuration'),
                  ),
                ),
              ],
            ),
            
            const SizedBox(height: 16),
            
            // Instructions
            const Card(
              child: Padding(
                padding: EdgeInsets.all(16.0),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      'Setup Instructions:',
                      style: TextStyle(fontWeight: FontWeight.bold),
                    ),
                    SizedBox(height: 8),
                    Text('1. Start your server using: python server.py'),
                    Text('2. Find your server IP or use DuckDNS domain'),
                    Text('3. Enter the URL above (e.g., http://192.168.1.100:8080)'),
                    Text('4. Test connection to verify it works'),
                    Text('5. Save configuration to use throughout the app'),
                  ],
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildQuickButton(String label, String url) {
    return ElevatedButton(
      onPressed: () {
        _urlController.text = url;
      },
      child: Text(label),
    );
  }
}
