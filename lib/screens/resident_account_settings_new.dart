import 'package:flutter/material.dart';
import '../../../services/auth_api_service.dart';
import '../../../services/data_service.dart';
import '../../../services/api_service_updated.dart' as api_service;
import '../../../services/api_service.dart';
import '../../../utils/debug_logger.dart';
import 'package:image_picker/image_picker.dart';

class ResidentAccountSettingsScreen extends StatefulWidget {
  final Map<String, dynamic>? userData;
  
  const ResidentAccountSettingsScreen({super.key, this.userData});

  @override
  State<ResidentAccountSettingsScreen> createState() => _ResidentAccountSettingsScreenState();
}

class _ResidentAccountSettingsScreenState extends State<ResidentAccountSettingsScreen> {
  final _formKey = GlobalKey<FormState>();
  final _nameController = TextEditingController();
  final _contactController = TextEditingController();
  final _addressController = TextEditingController();
  bool _isLoading = false;
  bool _isLoadingContact = false;
  bool _isUploadingPhoto = false;
  String? _profilePhotoUrl;
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
      _contactController.text = widget.userData!['contact_number'] ?? '';
      _addressController.text = widget.userData!['address'] ?? '';
      _profilePhotoUrl = widget.userData!['profile_photo_url'] ?? '';
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
      final result = await ApiService.updateUserProfile({
        'email': currentUser['email'],
        'full_name': _nameController.text.trim(),
        'contact_number': _contactController.text.trim(),
        'address': _addressController.text.trim(),
      });

      if (result['success'] == true) {
        // Update local user data
        authApiService.updateCurrentUser({
          ...currentUser,
          'full_name': _nameController.text.trim(),
          'contact_number': _contactController.text.trim(),
          'address': _addressController.text.trim(),
        });

        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(
            content: Text('Profile updated successfully!'),
            backgroundColor: Colors.green,
          ),
        );
      } else {
        throw Exception(result['message'] ?? 'Failed to update profile');
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

  Future<void> _pickAndUploadPhoto() async {
    try {
      final ImagePicker picker = ImagePicker();
      final XFile? image = await picker.pickImage(
        source: ImageSource.gallery,
        maxWidth: 800,
        maxHeight: 800,
        imageQuality: 85,
      );

      if (image == null) return;

      setState(() {
        _isUploadingPhoto = true;
      });

      // Get current user email
      final authApiService = AuthApiService();
      final currentUser = await authApiService.ensureUserLoaded();
      
      if (currentUser == null) {
        throw Exception('User not logged in');
      }

      // Upload photo to server
      final result = await ApiService.uploadProfilePhoto(
        currentUser['email'],
        image,
      );

      if (result['success'] == true) {
        setState(() {
          _profilePhotoUrl = result['photo_url'];
        });

        // Update local user data
        authApiService.updateCurrentUser({
          ...currentUser,
          'profile_photo_url': result['photo_url'],
        });

        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(
            content: Text('Profile photo updated successfully!'),
            backgroundColor: Colors.green,
          ),
        );
      } else {
        throw Exception(result['message'] ?? 'Failed to upload photo');
      }
    } catch (e) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Error uploading photo: $e')),
      );
    } finally {
      setState(() {
        _isUploadingPhoto = false;
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

            // Profile Photo Section
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
                  children: [
                    Row(
                      children: [
                        // Profile Photo
                        Container(
                          width: 80,
                          height: 80,
                          decoration: BoxDecoration(
                            shape: BoxShape.circle,
                            color: Colors.grey[200],
                            image: _profilePhotoUrl != null && _profilePhotoUrl!.isNotEmpty
                                ? DecorationImage(
                                    image: NetworkImage(_profilePhotoUrl!),
                                    fit: BoxFit.cover,
                                  )
                                : null,
                          ),
                          child: _profilePhotoUrl == null || _profilePhotoUrl!.isEmpty
                              ? const Icon(
                                  Icons.person,
                                  size: 40,
                                  color: Colors.grey,
                                )
                              : null,
                        ),
                        const SizedBox(width: 16),
                        // Email and Change Photo Button
                        Expanded(
                          child: Column(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              Text(
                                widget.userData?['email'] ?? 'user@example.com',
                                style: const TextStyle(
                                  fontSize: 16,
                                  fontWeight: FontWeight.w600,
                                  color: Colors.black87,
                                ),
                              ),
                              const SizedBox(height: 8),
                              ElevatedButton.icon(
                                onPressed: _isUploadingPhoto ? null : _pickAndUploadPhoto,
                                icon: _isUploadingPhoto
                                    ? const SizedBox(
                                        width: 16,
                                        height: 16,
                                        child: CircularProgressIndicator(
                                          color: Colors.white,
                                          strokeWidth: 2,
                                        ),
                                      )
                                    : const Icon(Icons.camera_alt),
                                label: Text(_isUploadingPhoto ? 'Uploading...' : 'Change Photo'),
                                style: ElevatedButton.styleFrom(
                                  backgroundColor: Colors.blue,
                                  foregroundColor: Colors.white,
                                  padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
                                  shape: RoundedRectangleBorder(
                                    borderRadius: BorderRadius.circular(8),
                                  ),
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
            ),

            const SizedBox(height: 24),

            // Personal Information Section (renamed from "Update Name")
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
                        'Personal Information',
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
                      TextFormField(
                        controller: _contactController,
                        decoration: InputDecoration(
                          labelText: 'Contact Number',
                          prefixIcon: const Icon(Icons.phone),
                          border: OutlineInputBorder(
                            borderRadius: BorderRadius.circular(8),
                          ),
                          filled: true,
                          fillColor: Colors.grey[50],
                        ),
                        validator: (value) {
                          if (value == null || value.isEmpty) {
                            return 'Please enter your contact number';
                          }
                          return null;
                        },
                      ),
                      const SizedBox(height: 16),
                      TextFormField(
                        controller: _addressController,
                        decoration: InputDecoration(
                          labelText: 'Address',
                          prefixIcon: const Icon(Icons.home),
                          border: OutlineInputBorder(
                            borderRadius: BorderRadius.circular(8),
                          ),
                          filled: true,
                          fillColor: Colors.grey[50],
                        ),
                        maxLines: 3,
                        validator: (value) {
                          if (value == null || value.isEmpty) {
                            return 'Please enter your address';
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
                          label: Text(_isLoading ? 'Updating...' : 'Update Information'),
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
            'Your privacy is important to us. This policy explains how we collect, use, and protect your information when you use the Barangay Reserve application, in compliance with Philippine laws.\n\n'
            '1. Information We Collect\n'
            '- Personal information (name, email, contact number)\n'
            '- Booking history and preferences\n'
            '- Verification documents\n'
            '- Residential address and proof of residence\n'
            '- Profile photographs and ID images\n'
            '- Login history and usage patterns\n'
            '\n2. How We Use Your Information\n'
            '- To process booking requests and reservations\n'
            '- To verify user accounts for discount eligibility under Local Government Code\n'
            '- To communicate with you about your bookings\n'
            '- To improve our services and facility management\n'
            '- To ensure security and prevent misuse\n'
            '\n3. Data Protection\n'
            '- All data is encrypted and stored securely under Data Privacy Act of 2012\n'
            '- Only authorized personnel can access your information\n'
            '- We never share your data with third parties without your written consent\n'
            '- Regular security audits and updates\n'
            '- Secure backup systems for data protection\n'
            '\n4. How Long We Keep Your Data\n'
            '- Personal information: Until you delete your account\n'
            '- Booking history: 5 years for legal compliance under Civil Code\n'
            '- Verification documents: 1 year after approval\n'
            '- Login logs: 2 years from last activity\n'
            '- Inactive accounts deleted after 2 years\n'
            '\n5. Your Rights under Data Privacy Act of 2012\n'
            '- Right to be informed what personal data we collect\n'
            '- Right to access your personal data upon request\n'
            '- Right to correct inaccurate or incomplete data\n'
            '- Right to delete your personal data (unless legally required)\n'
            '- Right to data portability - receive your data in machine-readable format\n'
            '- Right to file complaint with National Privacy Commission\n'
            '\n6. Security Measures\n'
            '- Multi-factor authentication for account protection\n'
            '- Encrypted data transmission and storage\n'
            '- Regular security monitoring and threat detection\n'
            '- Staff training on Data Privacy Act compliance\n'
            '- Immediate response to security incidents\n'
            '\n7. Contact Information\n'
            '- For privacy questions: privacy@barangay.gov\n'
            '- Phone: 0967-669-6767\n'
            '- Office: Barangay Hall, 2nd Floor, Main Street\n'
            '- Hours: Monday-Friday, 8:00 AM - 5:00 PM\n'
            '- National Privacy Commission: privacy@npc.gov.ph\n'
            '\n8. Policy Updates\n'
            '- This policy is reviewed annually\n'
            '- Changes posted on barangay bulletin board as required by Local Government Code\n'
            '- 30-day notice for significant changes\n'
            '- Effective date: January 1, 2026\n'
            '\nBy using this application, you consent to collection and processing of your information as described in this policy, in accordance with Republic Act No. 10173 (Data Privacy Act of 2012).\n\n'
            'Thank you for trusting us with your information as we work together to serve our community better!',
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
            'Barangay Reserve App - Help & Support\n\n'
            '1. App Navigation & Features\n'
            '- Bottom Navigation: Home, Facilities, Bookings, Profile, Account\n'
            '- Home Tab: View facilities and quick actions\n'
            '- Facilities Tab: Browse and select venues\n'
            '- Bookings Tab: View your current and past reservations\n'
            '- Profile Tab: Manage personal information and verification\n'
            '- Account Tab: Settings, privacy policy, help & support\n'
            '\n2. Making a Reservation\n'
            '- Tap Facilities tab\n'
            '- Select desired facility (Hall, Court, Pool, Shooting Range)\n'
            '- Choose date from calendar (green = available)\n'
            '- Select time slot\n'
            '- Set duration and number of participants\n'
            '- Submit booking request\n'
            '- Wait for approval notification\n'
            '\n3. Account Verification for Discount\n'
            '- Go to Profile tab\n'
            '- Tap "Get Verified" button\n'
            '- Upload clear photo of government ID\n'
            '- Upload proof of residence (utility bill, barangay clearance)\n'
            '- Submit for processing\n'
            '- Receive 10% resident discount upon approval\n'
            '\n4. Payment Process in App\n'
            '- After booking approval, pay at barangay treasury\n'
            '- Go to Bookings tab\n'
            '- Tap your approved booking\n'
            '- Tap "Upload Receipt"\n'
            '- Take clear photo of payment receipt\n'
            '- Include booking reference number\n'
            '- Submit and wait for confirmation\n'
            '\n5. Managing Your Bookings\n'
            '- View all bookings in Bookings tab\n'
            '- Green cards = your bookings (tappable for details)\n'
            '- Gray cards = others bookings (locked)\n'
            '- Tap your booking to view details\n'
            '- Upload receipts, view status, cancel if needed\n'
            '\n6. Common App Issues & Solutions\n'
            '- App crashes: Restart phone and check updates\n'
            '- Cannot login: Use "Forgot Password" option\n'
            '- Photos not uploading: Check app permissions\n'
            '- Calendar not loading: Check internet connection\n'
            '- Notifications not working: Enable in phone settings\n'
            '- Booking not showing: Pull down to refresh\n'
            '\n7. App Settings & Preferences\n'
            '- Account Tab → Settings\n'
            '- Enable/disable notifications\n'
            '- Change language preference\n'
            '- Clear app cache\n'
            '- Update profile information\n'
            '- Change password\n'
            '\n8. Contact App Support\n'
            '- Technical issues: app@barangay.gov\n'
            '- Booking problems: bookings@barangay.gov\n'
            '- Payment help: payments@barangay.gov\n'
            '- Account issues: accounts@barangay.gov\n'
            '- Hotline: 0967-669-6767\n'
            '- Office: Barangay Hall, 2nd Floor\n'
            '- Hours: Monday-Friday, 8:00 AM - 5:00 PM\n'
            '\n9. App Permissions Required\n'
            '- Camera: For uploading receipts and verification photos\n'
            '- Storage: To save photos and app data\n'
            '- Notifications: For booking updates and alerts\n'
            '- Phone: For account verification\n'
            '- Location: For showing nearby facilities (optional)\n'
            '\n10. Tips for Better Experience\n'
            '- Keep app updated for latest features\n'
            '- Use strong Wi-Fi for uploading photos\n'
            '- Enable notifications for booking updates\n'
            '- Complete verification early for discount benefits\n'
            '- Book facilities in advance for better availability\n'
            '\nThank you for using Barangay Reserve to serve our community better!',
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
