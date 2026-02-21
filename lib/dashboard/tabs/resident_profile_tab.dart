import 'package:flutter/material.dart';
import 'dart:convert';
import '../../../services/data_service.dart';
import '../../../services/auth_api_service.dart';
import '../../../screens/resident_account_settings_new.dart';
import '../../../screens/resident_verification_new.dart';
import '../../../main.dart';

class ResidentProfileTab extends StatefulWidget {
  final Function(BuildContext)? onLogout;
  final Map<String, dynamic>? userData;
  const ResidentProfileTab({super.key, this.onLogout, this.userData});

  @override
  State<ResidentProfileTab> createState() => _ResidentProfileTabState();
}

class _ResidentProfileTabState extends State<ResidentProfileTab> {
  final AuthApiService _authApiService = AuthApiService();
  Map<String, dynamic>? _currentUser;
  bool _isLoading = true;
  String? _profilePhotoUrl;

  @override
  void initState() {
    super.initState();
    _loadUserData();
  }

  @override
  void didChangeDependencies() {
    super.didChangeDependencies();
    // Refresh data when tab becomes visible again
    _refreshUserData();
  }

  Future<void> _refreshUserData() async {
    try {
      print('🔄 Refreshing user data in Profile Tab...');
      await _loadUserData();
    } catch (e) {
      print('❌ Error refreshing user data: $e');
    }
  }

  Future<void> _loadUserData() async {
    try {
      print('🔄 Loading fresh user data in Profile Tab...');
      
      // Force refresh from server to get latest data
      await _authApiService.restoreUserFromToken();
      final currentUser = await _authApiService.getCurrentUser();
      
      setState(() {
        _currentUser = currentUser;
        _isLoading = false;
      });
      
      // Load profile photo from verification request
      if (_currentUser != null) {
        _profilePhotoUrl = _currentUser!['profile_photo_url'] ?? '';
        
        print('🔍 ResidentProfileTab - User profile loaded from DataService: $currentUser');
        print('🔍 ResidentProfileTab - Verified status: ${_currentUser?['verified']}');
        print('🔍 ResidentProfileTab - Discount rate: ${_currentUser?['discount_rate']}');
        print('🔍 ResidentProfileTab - Profile photo URL: $_profilePhotoUrl');
        print('🔍 ResidentProfileTab - isVerifiedResident: ${_authApiService.isVerifiedResident()}');
        print('🔍 ResidentProfileTab - isVerifiedNonResident: ${_authApiService.isVerifiedNonResident()}');
      }
    } catch (e) {
      print('❌ ResidentProfileTab - Error loading user data: $e');
      if (mounted) {
        setState(() {
          _isLoading = false;
        });
      }
    }
  }

  // Refresh data method
  Future<void> _refreshData() async {
    setState(() {
      _isLoading = true;
    });
    
    // Reload user data
    await _loadUserData();
    
    if (mounted) {
      setState(() {
        _isLoading = false;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: SafeArea(
        child: Column(
          children: [
            // Header
            Container(
              width: double.infinity,
              padding: const EdgeInsets.all(20),
              decoration: BoxDecoration(
                color: Colors.blue,
                borderRadius: const BorderRadius.only(
                  bottomLeft: Radius.circular(20),
                  bottomRight: Radius.circular(20),
                ),
                boxShadow: [
                  BoxShadow(
                    color: Colors.blue.withOpacity(0.3),
                    spreadRadius: 2,
                    blurRadius: 10,
                    offset: const Offset(0, 4),
                  ),
                ],
              ),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Row(
                    children: [
                      Stack(
                        children: [
                          Container(
                            width: 80,
                            height: 80,
                            decoration: BoxDecoration(
                              shape: BoxShape.circle,
                              color: Colors.white,
                              border: Border.all(color: Colors.white, width: 3),
                              boxShadow: [
                                BoxShadow(
                                  color: Colors.black.withOpacity(0.2),
                                  spreadRadius: 2,
                                  blurRadius: 8,
                                  offset: const Offset(0, 2),
                                ),
                              ],
                            ),
                            child: (_profilePhotoUrl?.isNotEmpty == true ||
                                    _currentUser?['profile_photo_url']?.isNotEmpty == true ||
                                    _currentUser?['profilePhotoUrl']?.isNotEmpty == true ||
                                    _currentUser?['profilePhoto']?.isNotEmpty == true ||
                                    _currentUser?['profile_image']?.isNotEmpty == true ||
                                    _currentUser?['profileImage']?.isNotEmpty == true ||
                                    _currentUser?['avatar']?.isNotEmpty == true ||
                                    _currentUser?['photo_url']?.isNotEmpty == true ||
                                    _currentUser?['imageUrl']?.isNotEmpty == true)
                              ? ClipRRect(
                                  borderRadius: BorderRadius.circular(40),
                                  child: _buildProfileImage(
                                    _profilePhotoUrl ??
                                    _currentUser!['profile_photo_url'] ?? 
                                    _currentUser!['profilePhotoUrl'] ?? 
                                    _currentUser!['profilePhoto'] ??
                                    _currentUser!['profile_image'] ??
                                    _currentUser!['profileImage'] ??
                                    _currentUser!['avatar'] ??
                                    _currentUser!['photo_url'] ??
                                    _currentUser!['imageUrl'] ?? ''
                                  ),
                                )
                              : Icon(
                                  Icons.person,
                                  size: 40,
                                  color: Colors.grey[600],
                                ),
                          ),
                        ],
                      ),
                      const SizedBox(width: 20),
                      Expanded(
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Text(
                              _authApiService.getUserFullName(),
                              style: const TextStyle(
                                fontSize: 24,
                                fontWeight: FontWeight.bold,
                                color: Colors.white,
                                shadows: [
                                  Shadow(
                                    color: Colors.black26,
                                    offset: Offset(0, 1),
                                    blurRadius: 2,
                                  ),
                                ],
                              ),
                            ),
                            const SizedBox(height: 4),
                            Text(
                              _currentUser?['email'] ?? '',
                              style: TextStyle(
                                fontSize: 14,
                                color: Colors.white.withOpacity(0.9),
                                shadows: [
                                  Shadow(
                                    color: Colors.black26,
                                    offset: Offset(0, 1),
                                    blurRadius: 2,
                                  ),
                                ],
                              ),
                            ),
                            const SizedBox(height: 8),
                            if (_authApiService.isUserVerified())
                              Container(
                                padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
                                decoration: BoxDecoration(
                                  color: Colors.white.withOpacity(0.2),
                                  borderRadius: BorderRadius.circular(20),
                                  border: Border.all(color: Colors.white.withOpacity(0.3)),
                                ),
                                child: Row(
                                  mainAxisSize: MainAxisSize.min,
                                  children: [
                                    Icon(
                                      Icons.verified,
                                      size: 16,
                                      color: Colors.white,
                                    ),
                                    const SizedBox(width: 6),
                                    Text(
                                      _authApiService.isVerifiedResident() 
                                          ? 'Verified Resident' 
                                          : 'Verified Non-Resident',
                                      style: const TextStyle(
                                        color: Colors.white,
                                        fontWeight: FontWeight.w600,
                                        fontSize: 12,
                                      ),
                                    ),
                                  ],
                                ),
                              ),
                          ],
                        ),
                      ),
                      
                      // Refresh button in header
                      IconButton(
                        onPressed: _refreshUserData,
                        icon: const Icon(Icons.refresh, color: Colors.white),
                        tooltip: 'Refresh Profile',
                      ),
                    ],
                  ),
                ],
              ),
            ),

            const SizedBox(height: 32),

            // Profile Options
            Expanded(
              child: ListView(
                padding: const EdgeInsets.symmetric(horizontal: 16),
                children: [
                  // Account Settings
                  _buildProfileOption(
                    icon: Icons.settings,
                    title: 'Account Settings',
                    subtitle: 'Update your profile information',
                    onTap: () {
                      Navigator.push(
                        context,
                        MaterialPageRoute(
                          builder: (context) => ResidentAccountSettingsScreen(userData: _currentUser),
                        ),
                      );
                    },
                  ),

                  const SizedBox(height: 16),

                  // Account Verification
                  _buildProfileOption(
                    icon: Icons.verified_user,
                    title: 'Account Verification',
                    subtitle: _authApiService.isVerifiedResident() 
                        ? 'Already verified as Barangay Resident (10% discount)' 
                        : (_authApiService.isVerifiedNonResident()
                            ? 'Verified as Non-Resident (5% discount) - Tap to upgrade'
                            : 'Get verified for discount benefits'),
                    onTap: () {
                      // Check if user is already verified as BARANGAY RESIDENT only
                      // Non-residents can still access verification to potentially upgrade to resident status
                      if (_authApiService.isVerifiedResident()) {
                        // Show "Already Verified" popup for barangay residents only
                        showDialog(
                          context: context,
                          builder: (context) => AlertDialog(
                            title: const Text('Already Verified'),
                            content: const Text('Your account is already verified as a Barangay Resident. You enjoy 10% discount benefits on all facilities!'),
                            actions: [
                              TextButton(
                                onPressed: () => Navigator.of(context).pop(),
                                child: const Text('OK'),
                              ),
                            ],
                          ),
                        );
                      } else {
                        // Allow unverified users and non-residents to access verification screen
                        Navigator.push(
                          context,
                          MaterialPageRoute(
                            builder: (context) => ResidentVerificationScreen(
                              userData: _currentUser,
                            ),
                          ),
                        ).then((_) {
                          // Refresh user data when returning from verification screen
                          _loadUserData();
                        });
                      }
                    },
                  ),

                  const SizedBox(height: 32),

                  // Simple Logout Button
                  Container(
                    width: double.infinity,
                    child: ElevatedButton.icon(
                      onPressed: () {
                        print('🔥 Logout button pressed - using official logout method');
                        widget.onLogout?.call(context);
                      },
                      icon: const Icon(Icons.logout),
                      label: const Text('Logout'),
                      style: ElevatedButton.styleFrom(
                        backgroundColor: Colors.red,
                        foregroundColor: Colors.white,
                        padding: const EdgeInsets.symmetric(vertical: 16),
                        shape: RoundedRectangleBorder(
                          borderRadius: BorderRadius.circular(8),
                        ),
                      ),
                    ),
                  ),

                  const SizedBox(height: 32),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildProfileOption({
    required IconData icon,
    required String title,
    required String subtitle,
    required VoidCallback onTap,
  }) {
    return Container(
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(12),
        boxShadow: [
          BoxShadow(
            color: Colors.blue.withOpacity(0.1),
            spreadRadius: 2,
            blurRadius: 8,
            offset: const Offset(0, 4),
          ),
        ],
      ),
      child: ListTile(
        leading: Container(
          padding: const EdgeInsets.all(8),
          decoration: BoxDecoration(
            color: Colors.blue[50],
            borderRadius: BorderRadius.circular(8),
          ),
          child: Icon(
            icon,
            color: Colors.blue[600],
          ),
        ),
        title: Text(
          title,
          style: const TextStyle(
            fontSize: 16,
            fontWeight: FontWeight.bold,
            color: Colors.black87,
          ),
        ),
        subtitle: Text(
          subtitle,
          style: TextStyle(
            fontSize: 14,
            color: Colors.grey[600],
          ),
        ),
        trailing: Icon(
          Icons.arrow_forward_ios,
          color: Colors.blue[600],
          size: 20,
        ),
        onTap: onTap,
      ),
    );
  }

  void _showCustomerService() {
   
  }

  Widget _buildProfileImage(String imageUrl) {
    print('🔍 DEBUG: _buildProfileImage called with: $imageUrl');
    
    // Use the actual profile photo URL
    String finalUrl = imageUrl.isNotEmpty ? imageUrl : '';
    
    print('🔍 DEBUG: Final image URL: $finalUrl');
    
    // Check if it's a URL (starts with http) or base64 data
    if (finalUrl.startsWith('http')) {
      print('🔍 DEBUG: Loading image from URL: $finalUrl');
      // It's a URL, use NetworkImage
      return ClipRRect(
        borderRadius: BorderRadius.circular(40),
        child: Image.network(
          finalUrl,
          width: 80,
          height: 80,
          fit: BoxFit.cover,
          errorBuilder: (context, error, stackTrace) {
            print('❌ Error loading profile image from URL: $error');
            print('❌ Stack trace: $stackTrace');
            return Icon(Icons.person, size: 40, color: Colors.blue[600]);
          },
          loadingBuilder: (context, child, loadingProgress) {
            if (loadingProgress == null) return child;
            return Center(
              child: CircularProgressIndicator(
                value: loadingProgress.expectedTotalBytes != null
                    ? loadingProgress.cumulativeBytesLoaded / loadingProgress.expectedTotalBytes!
                    : null,
                strokeWidth: 2,
              ),
            );
          },
        ),
      );
    } else {
      print('🔍 DEBUG: Loading image from base64 data');
      // It's base64 data, use existing method
      return ClipRRect(
        borderRadius: BorderRadius.circular(40),
        child: _buildBase64Image(finalUrl),
      );
    }
  }

  Widget _buildBase64Image(String base64String) {
    try {
      // Remove data URL prefix if present
      String cleanBase64 = base64String;
      if (base64String.startsWith('data:image/')) {
        cleanBase64 = base64String.split(',')[1];
      }
      
      final decodedBytes = base64Decode(cleanBase64);
      return Image.memory(
        decodedBytes,
        width: 80,
        height: 80,
        fit: BoxFit.cover,
        errorBuilder: (context, error, stackTrace) {
          print('❌ Error loading profile image: $error');
          return Icon(Icons.person, size: 40, color: Colors.blue[600]);
        },
      );
    } catch (e) {
      print('❌ Error decoding base64 image: $e');
      return Icon(Icons.person, size: 40, color: Colors.blue[600]);
    }
  }
}
