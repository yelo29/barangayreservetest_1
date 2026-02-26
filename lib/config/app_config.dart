/// Dynamic App Configuration for Global Server Access
/// Laptop as server with barangay.db database

class AppConfig {
  // Use actual computer IP and correct port from server log
  static String _baseUrl = 'http://192.168.100.46:8000';
  
  /// Get the current base URL
  static String get baseUrl => _baseUrl;
  
  /// Set base URL dynamically (for runtime configuration)
  static void setBaseUrl(String url) {
    _baseUrl = url;
  }
  
  /// Auto-detect server URL from multiple sources
  static String autoDetectServerUrl() {
    // Priority order: Environment variable > stored URL > default
    return _baseUrl;
  }
  
  /// Common server configurations
  static const String loginEndpoint = '/api/auth/login';
  static const String registerEndpoint = '/api/auth/register';
  static const String userProfileEndpoint = '/api/users/profile';
  static const String facilitiesEndpoint = '/api/facilities';
  static const String bookingsEndpoint = '/api/bookings';
  static const String authenticationRequestsEndpoint = '/api/authentication-requests';
  static const String barangayEventsEndpoint = '/api/barangay-events';
  static const String uploadReceiptEndpoint = '/api/upload-receipt';
  
  /// Validate URL format
  static bool isValidUrl(String url) {
    try {
      final uri = Uri.parse(url);
      return uri.hasScheme && (uri.hasAuthority || uri.host.isNotEmpty);
    } catch (e) {
      return false;
    }
  }
  
  /// Extract domain from URL (for DuckDNS)
  static String extractDomain(String url) {
    try {
      final uri = Uri.parse(url);
      return uri.host;
    } catch (e) {
      return '';
    }
  }
  
  /// Check if URL uses DuckDNS
  static bool isDuckDnsUrl(String url) {
    final domain = extractDomain(url);
    return domain.contains('duckdns.org');
  }
  
  /// Convert HTTP to HTTPS for production
  static String toHttps(String url) {
    if (url.startsWith('http://')) {
      return url.replaceFirst('http://', 'https://');
    }
    return url;
  }
  
  /// Get current configuration info
  static Map<String, dynamic> getConfigInfo() {
    return {
      'baseUrl': _baseUrl,
      'isDuckDns': isDuckDnsUrl(_baseUrl),
      'domain': extractDomain(_baseUrl),
      'isValid': isValidUrl(_baseUrl),
    };
  }
}
