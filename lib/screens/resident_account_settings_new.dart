import 'package:flutter/material.dart';
import '../../../services/auth_api_service.dart';
import '../../../services/data_service.dart';
import '../../../services/api_service_updated.dart' as api_service;
import '../../../utils/debug_logger.dart';

class ResidentAccountSettingsScreen extends StatefulWidget {
  final Map<String, dynamic>? userData;
  
  const ResidentAccountSettingsScreen({super.key, this.userData});

  @override
  State<ResidentAccountSettingsScreen> createState() => _ResidentAccountSettingsScreenState();
}

class _ResidentAccountSettingsScreenState extends State<ResidentAccountSettingsScreen> {
  final _formKey = GlobalKey<FormState>();
  final _nameController = TextEditingController();
  bool _isLoading = false;
  bool _isLoadingContact = false;
  List<Map<String, dynamic>> _officials = [];

  @override
  void initState() {
    super.initState();
    _loadUserData();
    _loadOfficialContact();
  }

  void _loadUserData() {
    if (widget.userData != null) {
      _nameController.text = widget.userData!['full_name'] ?? '';
    }
  }

  Future<void> _loadOfficialContact() async {
    setState(() {
      _isLoadingContact = true;
    });

    try {
      // Fetch real officials from server using DataService
      final result = await DataService.fetchOfficials();
      
      if (result['success'] == true) {
        final List<Map<String, dynamic>> officials = result['data'] ?? [];
        
        setState(() {
          _officials = officials;
          _isLoadingContact = false;
          DebugLogger.ui('Loaded ${_officials.length} officials from server');
        });
      } else {
        throw Exception(result['error'] ?? 'Failed to fetch officials');
      }
    } catch (e) {
      DebugLogger.error('❌ Error loading officials: $e');
      setState(() {
        _isLoadingContact = false;
      });
      
      // Fallback to hardcoded officials if server fails
      final officials = [
        {'full_name': 'Barangay Captain', 'contact_number': '09123456789'},
        {'full_name': 'Barangay Secretary', 'contact_number': '09123456788'},
        {'full_name': 'Barangay Treasurer', 'contact_number': '09123456787'},
        {'full_name': 'Barangay Councilor', 'contact_number': '09123456786'},
      ];
      
      setState(() {
        _officials = officials;
        _isLoadingContact = false;
        DebugLogger.ui('Loaded ${officials.length} fallback officials');
      });
    }
  }

  Future<void> _updateName() async {
    if (!_formKey.currentState!.validate()) return;

    setState(() {
      _isLoading = true;
    });

    try {
      // Get current user data
      final authApiService = AuthApiService();
      final currentUser = await authApiService.ensureUserLoaded();
      
      if (currentUser == null) {
        throw Exception('User not logged in');
      }

      // Update profile using server API
      // TODO: Implement proper profile update in DataService
      // For now, just update local data
      final result = {'success': true};

      if (result['success'] == true) {
        // Update local user data
        authApiService.updateCurrentUser({
          ...currentUser,
          'full_name': _nameController.text.trim(),
        });

        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(
            content: Text('Profile updated successfully!'),
            backgroundColor: Colors.green,
          ),
        );
      } else {
        throw Exception(result['error'] ?? 'Failed to update profile');
      }
    } catch (e) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Error updating profile: $e')),
      );
    } finally {
      setState(() {
        _isLoading = false;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.blue[50],
      appBar: AppBar(
        title: const Text('Account Settings'),
        backgroundColor: Colors.blue,
        foregroundColor: Colors.white,
        elevation: 0,
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // User Info Card
            Container(
              padding: const EdgeInsets.all(20),
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
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Row(
                    children: [
                      Container(
                        width: 60,
                        height: 60,
                        decoration: BoxDecoration(
                          color: Colors.blue[50],
                          borderRadius: BorderRadius.circular(30),
                        ),
                        child: Icon(
                          Icons.person,
                          size: 30,
                          color: Colors.blue[600],
                        ),
                      ),
                      const SizedBox(width: 16),
                      Expanded(
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Text(
                              widget.userData?['email'] ?? 'resident@example.com',
                              style: const TextStyle(
                                fontSize: 16,
                                fontWeight: FontWeight.bold,
                                color: Colors.black87,
                              ),
                            ),
                            const SizedBox(height: 4),
                            if (widget.userData?['verified'] == true)
                              Container(
                                padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                                decoration: BoxDecoration(
                                  color: Colors.green,
                                  borderRadius: BorderRadius.circular(12),
                                ),
                                child: const Row(
                                  mainAxisSize: MainAxisSize.min,
                                  children: [
                                    Icon(
                                      Icons.verified,
                                      color: Colors.white,
                                      size: 14,
                                    ),
                                    SizedBox(width: 4),
                                    Text(
                                      'Verified',
                                      style: TextStyle(
                                        color: Colors.white,
                                        fontSize: 12,
                                        fontWeight: FontWeight.bold,
                                      ),
                                    ),
                                  ],
                                ),
                              ),
                          ],
                        ),
                      ),
                    ],
                  ),
                ],
              ),
            ),

            const SizedBox(height: 24),

            // Update Name Section
            Container(
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
              child: Padding(
                padding: const EdgeInsets.all(20),
                child: Form(
                  key: _formKey,
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      const Text(
                        'Update Name',
                        style: TextStyle(
                          fontSize: 18,
                          fontWeight: FontWeight.bold,
                          color: Colors.black87,
                        ),
                      ),
                      const SizedBox(height: 16),
                      TextFormField(
                        controller: _nameController,
                        decoration: InputDecoration(
                          labelText: 'Full Name',
                          prefixIcon: const Icon(Icons.person),
                          border: OutlineInputBorder(
                            borderRadius: BorderRadius.circular(8),
                          ),
                          filled: true,
                          fillColor: Colors.grey[50],
                        ),
                        validator: (value) {
                          if (value == null || value.isEmpty) {
                            return 'Please enter your full name';
                          }
                          return null;
                        },
                      ),
                      const SizedBox(height: 16),
                      SizedBox(
                        width: double.infinity,
                        child: ElevatedButton.icon(
                          onPressed: _isLoading ? null : _updateName,
                          icon: _isLoading 
                              ? const SizedBox(
                                  width: 16,
                                  height: 16,
                                  child: CircularProgressIndicator(
                                    color: Colors.white,
                                    strokeWidth: 2,
                                  ),
                                )
                              : const Icon(Icons.save),
                          label: Text(_isLoading ? 'Updating...' : 'Update Name'),
                          style: ElevatedButton.styleFrom(
                            backgroundColor: Colors.blue,
                            foregroundColor: Colors.white,
                            padding: const EdgeInsets.symmetric(vertical: 12),
                            shape: RoundedRectangleBorder(
                              borderRadius: BorderRadius.circular(8),
                            ),
                          ),
                        ),
                      ),
                    ],
                  ),
                ),
              ),
            ),

            const SizedBox(height: 24),

            // Customer Service Section
            Container(
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
              child: Padding(
                padding: const EdgeInsets.all(20),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    const Text(
                      'Customer Service',
                      style: TextStyle(
                        fontSize: 18,
                        fontWeight: FontWeight.bold,
                        color: Colors.black87,
                      ),
                    ),
                    const SizedBox(height: 8),
                    Text(
                      'Contact barangay officials for assistance',
                      style: TextStyle(
                        fontSize: 14,
                        color: Colors.grey[600],
                      ),
                    ),
                    const SizedBox(height: 16),
                    // Show loading, officials, or fallback immediately
                    if (_isLoadingContact)
                      Container(
                        padding: const EdgeInsets.all(16),
                        decoration: BoxDecoration(
                          color: Colors.grey[50],
                          borderRadius: BorderRadius.circular(8),
                          border: Border.all(color: Colors.grey[300]!),
                        ),
                        child: const Row(
                          children: [
                            CircularProgressIndicator(),
                            SizedBox(width: 12),
                            Text('Loading officials...'),
                          ],
                        ),
                      )
                    else if (_officials.isNotEmpty)
                      Column(
                        children: _officials.map((official) {
                          return Container(
                            margin: const EdgeInsets.only(bottom: 12),
                            padding: const EdgeInsets.all(12),
                            decoration: BoxDecoration(
                              color: Colors.grey[50],
                              borderRadius: BorderRadius.circular(8),
                              border: Border.all(color: Colors.grey[300]!),
                            ),
                            child: Row(
                              children: [
                                Container(
                                  padding: const EdgeInsets.all(8),
                                  decoration: BoxDecoration(
                                    color: Colors.blue[50],
                                    borderRadius: BorderRadius.circular(6),
                                  ),
                                  child: const Icon(
                                    Icons.person,
                                    color: Colors.blue,
                                    size: 20,
                                  ),
                                ),
                                const SizedBox(width: 12),
                                Expanded(
                                  child: Column(
                                    crossAxisAlignment: CrossAxisAlignment.start,
                                    children: [
                                      Text(
                                        official['full_name'] ?? 'Unknown Official',
                                        style: const TextStyle(
                                          fontWeight: FontWeight.w600,
                                          fontSize: 14,
                                        ),
                                      ),
                                      const SizedBox(height: 2),
                                      Text(
                                        official['contact_number']?.toString() ?? 'No contact available',
                                        style: TextStyle(
                                          fontSize: 12,
                                          color: Colors.grey[600],
                                        ),
                                      ),
                                    ],
                                  ),
                                ),
                              ],
                            ),
                          );
                        }).toList(),
                      )
                    else
                      Container(
                        padding: const EdgeInsets.all(16),
                        decoration: BoxDecoration(
                          color: Colors.grey[50],
                          borderRadius: BorderRadius.circular(8),
                          border: Border.all(color: Colors.grey[300]!),
                        ),
                        child: Row(
                          children: [
                            Icon(
                              Icons.info_outline,
                              color: Colors.grey[600],
                            ),
                            const SizedBox(width: 8),
                            Expanded(
                              child: Text(
                                'Contact barangay office for assistance',
                                style: TextStyle(
                                  color: Colors.grey[600],
                                  fontSize: 14,
                                ),
                              ),
                            ),
                          ],
                        ),
                      ),
                  ],
                ),
              ),
            ),

            const SizedBox(height: 24),

            // Privacy Policy Section
            _buildActionCard(
              title: 'Privacy Policy',
              subtitle: 'View our privacy and data policies',
              icon: Icons.privacy_tip,
              onTap: () => _showPrivacyPolicy(),
            ),

            const SizedBox(height: 16),

            // Help and Support Section
            _buildActionCard(
              title: 'Help and Support',
              subtitle: 'Learn how to use the application',
              icon: Icons.help_outline,
              onTap: () => _showHelpAndSupport(),
            ),

            const SizedBox(height: 32),
          ],
        ),
      ),
    );
  }

  Widget _buildActionCard({
    required String title,
    required String subtitle,
    required IconData icon,
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

  void _showPrivacyPolicy() {
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text('Privacy Policy'),
        content: const SingleChildScrollView(
          child: Text(
            'Your privacy is important to us. This policy explains how we collect, use, and protect your information when you use the Barangay Reserve application.\n\n'
            '1. Information We Collect\n'
            '- Personal information (name, email, contact number)\n'
            '- Booking history and preferences\n'
            '- Verification documents\n'
            '\n2. How We Use Your Information\n'
            '- To process booking requests\n'
            '- To verify user accounts\n'
            '- To communicate with you about your bookings\n'
            '\n3. Data Protection\n'
            '- All data is encrypted and stored securely\n'
            '- Only authorized personnel can access your information\n'
            '- We never share your data with third parties without consent\n'
            '\n4. Your Rights\n'
            '- You can request to view your data\n'
            '- You can request to delete your account\n'
            '- You can update your information anytime\n'
            '\nFor questions about privacy, contact your barangay office.',
          ),
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context),
            child: const Text('Close'),
          ),
        ],
      ),
    );
  }

  void _showHelpAndSupport() {
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text('Help and Support'),
        content: const SingleChildScrollView(
          child: Text(
            'Welcome to Barangay Reserve!\n\n'
            'What is Barangay Reserve?\n'
            'Barangay Reserve is a facility booking system that allows residents to easily book barangay facilities for events and activities.\n\n'
            'How to Use:\n\n'
            '1. Browse Facilities\n'
            '- Go to the Home tab to see available facilities\n'
            '- Tap on any facility to view details and availability\n\n'
            '2. Book a Facility\n'
            '- Select an available date (white dates)\n'
            '- Fill out the booking form with your details\n'
            '- Upload payment receipt\n'
            '- Submit your booking request\n\n'
            '3. Track Your Bookings\n'
            '- Go to My Bookings tab to see all your requests\n'
            '- Status colors: Yellow (Pending), Green (Approved), Red (Rejected)\n\n'
            '4. Get Verified\n'
            '- Go to Profile → Account Verification\n'
            '- Submit your documents for verification\n'
            '- Get discounts on facility bookings (5% for non-residents, 10% for residents)\n\n'
            'Calendar Guide:\n'
            '- White: Available for booking\n'
            '- Yellow: Pending booking\n'
            '- Green: Approved booking or event\n'
            '- Gray: Unavailable (past date)\n\n'
            'Need Help?\n'
            'Contact your barangay office or use the Customer Service option in the Profile tab.\n\n'
            'Thank you for using Barangay Reserve!',
          ),
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context),
            child: const Text('Close'),
          ),
        ],
      ),
    );
  }
}
