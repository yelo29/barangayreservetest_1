import 'package:flutter/material.dart';
import 'dart:convert';
import 'dart:io';
import 'package:intl/intl.dart';
import '../../../services/api_service_updated.dart' as api_service;
import '../../../services/base64_image_service.dart';

class OfficialAuthenticationTab extends StatefulWidget {
  final Map<String, dynamic>? userData;
  final Function(BuildContext)? onLogout;

  const OfficialAuthenticationTab({super.key, required this.userData, this.onLogout});

  @override
  State<OfficialAuthenticationTab> createState() => _OfficialAuthenticationTabState();
}

class _OfficialAuthenticationTabState extends State<OfficialAuthenticationTab> {
  List<Map<String, dynamic>> _verificationRequests = [];
  List<Map<String, dynamic>> _filteredRequests = [];
  bool _isLoading = true;
  String _selectedFilter = 'all';

  @override
  void initState() {
    super.initState();
    _loadVerificationRequests();
  }

  Future<void> _loadVerificationRequests() async {
    try {
      final response = await api_service.ApiService.getVerificationRequests();

      setState(() {
        if (response['success'] == true) {
          // Server returns data in 'data' field with proper field names
          _verificationRequests = List<Map<String, dynamic>>.from(response['data'] ?? []);
          
          // Count by status for debugging
          final pendingCount = _verificationRequests.where((r) => r['status'] == 'pending').length;
          final approvedCount = _verificationRequests.where((r) => r['status'] == 'approved').length;
          final rejectedCount = _verificationRequests.where((r) => r['status'] == 'rejected').length;
          print('🔍 Status counts: Pending: $pendingCount, Approved: $approvedCount, Rejected: $rejectedCount');
          
          // Normalize field names for consistency
          _verificationRequests = _verificationRequests.map((request) {
            final normalized = {
              'id': request['id'],
              'user_id': request['residentId'] ?? request['user_id'],
              'verification_type': request['verificationType'] ?? request['verification_type'],
              'requested_discount_rate': request['discountRate'] ?? request['requested_discount_rate'],
              'user_photo_base64': request['userPhotoUrl'] ?? request['user_photo_base64'],
              'valid_id_base64': request['validIdUrl'] ?? request['valid_id_base64'],
              'status': request['status'],
              'residential_address': request['address'] ?? request['residential_address'],
              'created_at': request['submittedAt'] ?? request['created_at'],
              'email': request['email'],
              'full_name': request['fullName'] ?? request['full_name'],
              'contact_number': request['contactNumber'] ?? request['contact_number'],
            };
            return normalized;
          }).toList();
          _filteredRequests = _verificationRequests;
          print('🔍 Loaded ${_verificationRequests.length} verification requests');
        } else {
          _verificationRequests = [];
          _filteredRequests = [];
        }
        _isLoading = false;
      });
    } catch (e) {
      print('Error loading verification requests: $e');
      setState(() {
        _verificationRequests = [];
        _filteredRequests = [];
        _isLoading = false;
      });
    }
  }

  void _filterRequests(String filter) {
    setState(() {
      _selectedFilter = filter;
      if (filter == 'all') {
        _filteredRequests = _verificationRequests;
      } else {
        _filteredRequests = _verificationRequests
            .where((request) => request['status'] == filter)
            .toList();
      }
    });
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
                color: Colors.red,
                borderRadius: const BorderRadius.only(
                  bottomLeft: Radius.circular(20),
                  bottomRight: Radius.circular(20),
                ),
              ),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  const Text(
                    'Authentication Requests',
                    style: TextStyle(
                      fontSize: 24,
                      fontWeight: FontWeight.bold,
                      color: Colors.white,
                    ),
                  ),
                  const SizedBox(height: 8),
                  Text(
                    'Review resident verification requests',
                    style: TextStyle(
                      fontSize: 16,
                      color: Colors.red[100],
                    ),
                  ),
                ],
              ),
            ),

            const SizedBox(height: 20),

            // Filter Tabs
            Container(
              padding: const EdgeInsets.symmetric(horizontal: 16),
              child: Row(
                children: [
                  _buildFilterTab('all', 'All'),
                  const SizedBox(width: 8),
                  _buildFilterTab('pending', 'Pending'),
                  const SizedBox(width: 8),
                  _buildFilterTab('approved', 'Approved'),
                  const SizedBox(width: 8),
                  _buildFilterTab('rejected', 'Rejected'),
                ],
              ),
            ),

            const SizedBox(height: 16),

            // Requests List
            Expanded(
              child: _isLoading
                  ? const Center(child: CircularProgressIndicator())
                  : _filteredRequests.isEmpty
                      ? Center(
                          child: Column(
                            mainAxisAlignment: MainAxisAlignment.center,
                            children: [
                              Icon(
                                Icons.verified_user,
                                size: 80,
                                color: Colors.grey[400],
                              ),
                              const SizedBox(height: 16),
                              Text(
                                'No $_selectedFilter requests',
                                style: TextStyle(
                                  fontSize: 18,
                                  color: Colors.grey[600],
                                ),
                              ),
                            ],
                          ),
                        )
                      : ListView.builder(
                          padding: const EdgeInsets.symmetric(horizontal: 16),
                          itemCount: _filteredRequests.length,
                          itemBuilder: (context, index) {
                            final request = _filteredRequests[index];
                            return _buildRequestCard(request);
                          },
                        ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildFilterTab(String filter, String label) {
    final isSelected = _selectedFilter == filter;
    final Color color = _getFilterColor(filter);

    return Expanded(
      child: GestureDetector(
        onTap: () => _filterRequests(filter),
        child: Container(
          padding: const EdgeInsets.symmetric(vertical: 12),
          decoration: BoxDecoration(
            color: isSelected ? color : Colors.transparent,
            borderRadius: BorderRadius.circular(8),
            border: Border.all(
              color: color.withOpacity(0.3),
              width: 1,
            ),
          ),
          child: Text(
            label,
            textAlign: TextAlign.center,
            style: TextStyle(
              color: isSelected ? Colors.white : color,
              fontWeight: isSelected ? FontWeight.bold : FontWeight.normal,
              fontSize: 14,
            ),
          ),
        ),
      ),
    );
  }

  Widget _buildRequestCard(Map<String, dynamic> request) {
    final status = request['status'] ?? 'pending';
    final statusColor = _getStatusColor(status);

    return Container(
      margin: const EdgeInsets.only(bottom: 16),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(12),
        boxShadow: [
          BoxShadow(
            color: Colors.red.withOpacity(0.1),
            spreadRadius: 2,
            blurRadius: 8,
            offset: const Offset(0, 4),
          ),
        ],
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          // Header
          Container(
            padding: const EdgeInsets.all(16),
            decoration: BoxDecoration(
              color: statusColor.withOpacity(0.1),
              borderRadius: const BorderRadius.only(
                topLeft: Radius.circular(12),
                topRight: Radius.circular(12),
              ),
            ),
            child: Row(
              children: [
                Icon(
                  _getStatusIcon(status),
                  color: statusColor,
                  size: 20,
                ),
                const SizedBox(width: 8),
                Expanded(
                  child: Text(
                    request['full_name'] ?? 'Unknown',
                    style: const TextStyle(
                      fontSize: 18,
                      fontWeight: FontWeight.bold,
                      color: Colors.black87,
                    ),
                  ),
                ),
                Container(
                  padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
                  decoration: BoxDecoration(
                    color: statusColor,
                    borderRadius: BorderRadius.circular(20),
                  ),
                  child: Text(
                    status.toUpperCase(),
                    style: const TextStyle(
                      fontSize: 12,
                      color: Colors.white,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                ),
              ],
            ),
          ),

          // Content
          Padding(
            padding: const EdgeInsets.all(16),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                // Resident Information
                _buildInfoSection(
                  title: 'Resident Information',
                  children: [
                    _buildInfoRow('Full Name', request['full_name'] ?? 'N/A'),
                    _buildInfoRow('Contact', request['contact_number'] ?? 'N/A'),
                    _buildInfoRow('Address', request['residential_address'] ?? 'N/A'),
                    _buildInfoRow('Type', request['verification_type'] ?? 'N/A'),
                  ],
                ),

                const SizedBox(height: 16),

                // Verification Photos
                _buildInfoSection(
                  title: 'Verification Photos',
                  children: [
                    Row(
                      children: [
                        Expanded(
                          child: _buildPhotoCard(
                            title: 'Profile Photo',
                            imageUrl: request['user_photo_base64'],
                            onTap: () => _showPhotoViewer('Profile Photo', request['user_photo_base64']),
                          ),
                        ),
                        const SizedBox(width: 12),
                        Expanded(
                          child: _buildPhotoCard(
                            title: 'Valid ID',
                            imageUrl: request['valid_id_base64'],
                            onTap: () => _showPhotoViewer('Valid ID', request['valid_id_base64']),
                          ),
                        ),
                      ],
                    ),
                  ],
                ),

                // Submitted Date
                const SizedBox(height: 16),
                Text(
                  'Submitted: ${_formatDate(request['created_at'])}',
                  style: TextStyle(
                    fontSize: 12,
                    color: Colors.grey[500],
                  ),
                ),

                // Action Buttons (for pending requests)
                if (status == 'pending') ...[
                  const SizedBox(height: 20),
                  Row(
                    children: [
                      Expanded(
                        child: ElevatedButton.icon(
                          onPressed: () => _updateVerificationStatus(request['id'], 'rejected'),
                          icon: const Icon(Icons.close),
                          label: const Text('Reject'),
                          style: ElevatedButton.styleFrom(
                            backgroundColor: Colors.red,
                            foregroundColor: Colors.white,
                            padding: const EdgeInsets.symmetric(vertical: 12),
                          ),
                        ),
                      ),
                      const SizedBox(width: 12),
                      Expanded(
                        child: ElevatedButton.icon(
                          onPressed: () => _showApproveDialog(request['id'], request['verification_type']),
                          icon: const Icon(Icons.check),
                          label: const Text('Approve'),
                          style: ElevatedButton.styleFrom(
                            backgroundColor: Colors.green,
                            foregroundColor: Colors.white,
                            padding: const EdgeInsets.symmetric(vertical: 12),
                          ),
                        ),
                      ),
                    ],
                  ),
                ],
              ],
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildPhotoCard({
    required String title,
    String? imageUrl,
    required VoidCallback onTap,
  }) {
    return Container(
      height: 120,
      decoration: BoxDecoration(
        color: Colors.grey[100],
        borderRadius: BorderRadius.circular(8),
        border: Border.all(color: Colors.grey[300]!),
      ),
      child: Stack(
        children: [
          // Show actual image if available, otherwise show placeholder
          if (imageUrl != null && imageUrl.isNotEmpty)
            ClipRRect(
              borderRadius: BorderRadius.circular(8),
              child: Image.memory(
                base64.decode(Base64ImageService.extractBase64(imageUrl) ?? ''),
                fit: BoxFit.cover,
                width: double.infinity,
                height: double.infinity,
                errorBuilder: (context, error, stackTrace) {
                  return Center(
                    child: Column(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        Icon(Icons.broken_image, size: 32, color: Colors.grey[600]),
                        const SizedBox(height: 4),
                        Text(
                          title,
                          style: TextStyle(
                            color: Colors.grey[600],
                            fontSize: 12,
                          ),
                        ),
                      ],
                    ),
                  );
                },
              ),
            )
          else
            Center(
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  Icon(
                    Icons.person,
                    size: 32,
                    color: Colors.grey[600],
                  ),
                  const SizedBox(height: 4),
                  Text(
                    title,
                    style: TextStyle(
                      color: Colors.grey[600],
                      fontSize: 12,
                    ),
                  ),
                ],
              ),
            ),
          
          // Overlay for tap functionality
          Positioned.fill(
            child: Material(
              color: Colors.transparent,
              child: InkWell(
                borderRadius: BorderRadius.circular(8),
                onTap: onTap,
                child: Container(),
              ),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildInfoSection({
    required String title,
    required List<Widget> children,
  }) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(
          title,
          style: const TextStyle(
            fontSize: 14,
            fontWeight: FontWeight.bold,
            color: Colors.black87,
          ),
        ),
        const SizedBox(height: 8),
        ...children,
      ],
    );
  }

  Widget _buildInfoRow(String label, String value) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 4),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          SizedBox(
            width: 80,
            child: Text(
              '$label:',
              style: TextStyle(
                fontSize: 14,
                color: Colors.grey[600],
                fontWeight: FontWeight.w500,
              ),
            ),
          ),
          Expanded(
            child: Text(
              value,
              style: const TextStyle(
                fontSize: 14,
                color: Colors.black87,
              ),
            ),
          ),
        ],
      ),
    );
  }

  Color _getFilterColor(String filter) {
    switch (filter) {
      case 'all':
        return Colors.grey;
      case 'pending':
        return Colors.orange;
      case 'approved':
        return Colors.green;
      case 'rejected':
        return Colors.red;
      default:
        return Colors.grey;
    }
  }

  Color _getStatusColor(String status) {
    switch (status.toLowerCase()) {
      case 'pending':
        return Colors.orange;
      case 'approved':
        return Colors.green;
      case 'rejected':
        return Colors.red;
      default:
        return Colors.grey;
    }
  }

  IconData _getStatusIcon(String status) {
    switch (status.toLowerCase()) {
      case 'pending':
        return Icons.pending;
      case 'approved':
        return Icons.check_circle;
      case 'rejected':
        return Icons.cancel;
      default:
        return Icons.help;
    }
  }

  Future<void> _updateVerificationStatus(int requestId, String status, {double? discountRate}) async {
    try {
      print('🔍 Updating verification status: ID=$requestId, status=$status, discountRate=$discountRate');
      
      Map<String, dynamic> updateData = {
        'status': status,
        'updatedAt': DateTime.now().toIso8601String(),
      };
      
      // Add discount rate for approved requests
      if (status == 'approved' && discountRate != null) {
        updateData['discountRate'] = discountRate;
        // Also set profile photo URL if approved
        final request = _verificationRequests.firstWhere((req) => req['id'] == requestId);
        if (request['user_photo_base64'] != null) {
          updateData['profilePhotoUrl'] = request['user_photo_base64'];
        }
      }
      
      final response = await api_service.ApiService.updateVerificationStatus(requestId, status, discountRate: discountRate?.toString());

      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text(response['success'] == true 
                ? 'Verification request ${status} successfully'
                : 'Error: ${response['error'] ?? 'Failed to update request'}'),
            backgroundColor: response['success'] == true ? Colors.green : Colors.red,
          ),
        );
      }

      // Reload requests
      _loadVerificationRequests();
    } catch (e) {
      print('❌ Error updating verification status: $e');
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text('Error updating request: $e'),
            backgroundColor: Colors.red,
          ),
        );
      }
    }
  }

  void _showApproveDialog(int requestId, String? verificationType) {
    String selectedDiscount = '0.10'; // Default to resident
    
    showDialog(
      context: context,
      builder: (context) => StatefulBuilder(
        builder: (context, setState) => AlertDialog(
          title: const Text('Approve Verification'),
          content: Column(
            mainAxisSize: MainAxisSize.min,
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text('Verification Type: ${verificationType ?? 'Unknown'}'),
              const SizedBox(height: 16),
              const Text('Select discount rate:'),
              const SizedBox(height: 8),
              RadioListTile<String>(
                title: const Text('10% (Resident)'),
                value: '0.10',
                groupValue: selectedDiscount,
                onChanged: (value) {
                  setState(() {
                    selectedDiscount = value!;
                  });
                },
              ),
              RadioListTile<String>(
                title: const Text('5% (Non-Resident)'),
                value: '0.05',
                groupValue: selectedDiscount,
                onChanged: (value) {
                  setState(() {
                    selectedDiscount = value!;
                  });
                },
              ),
            ],
          ),
          actions: [
            TextButton(
              onPressed: () => Navigator.pop(context),
              child: const Text('Cancel'),
            ),
            ElevatedButton(
              onPressed: () {
                Navigator.pop(context);
                _updateVerificationStatus(requestId, 'approved', discountRate: double.parse(selectedDiscount));
              },
              style: ElevatedButton.styleFrom(
                backgroundColor: Colors.green,
                foregroundColor: Colors.white,
              ),
              child: const Text('Approve'),
            ),
          ],
        ),
      ),
    );
  }

  String _formatDate(dynamic date) {
    if (date == null) return 'Unknown';
    
    try {
      DateTime dateTime;
      if (date is String) {
        // Handle ISO format and other string formats
        if (date.contains('T')) {
          dateTime = DateTime.parse(date);
        } else {
          // Try to parse as various date formats
          dateTime = DateTime.parse(date); // Simplified for now
        }
      } else if (date is DateTime) {
        dateTime = date;
      } else {
        return 'Unknown';
      }

      return '${dateTime.day}/${dateTime.month}/${dateTime.year}';
    } catch (e) {
      print('❌ Error formatting date: $date, error: $e');
      return 'Unknown';
    }
  }

  // Photo Viewer with Zoom
  void _showPhotoViewer(String title, String? base64Image) {
    if (base64Image == null || base64Image.isEmpty) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text('No photo available'),
          backgroundColor: Colors.orange,
        ),
      );
      return;
    }

    Navigator.push(
      context,
      MaterialPageRoute(
        builder: (context) => PhotoViewerScreen(
          title: title,
          base64Image: base64Image,
        ),
      ),
    );
  }
}

// Photo Viewer Screen with Zoom
class PhotoViewerScreen extends StatefulWidget {
  final String title;
  final String base64Image;

  const PhotoViewerScreen({
    super.key,
    required this.title,
    required this.base64Image,
  });

  @override
  State<PhotoViewerScreen> createState() => _PhotoViewerScreenState();
}

class _PhotoViewerScreenState extends State<PhotoViewerScreen> {
  double _scale = 1.0;
  final TransformationController _transformationController = TransformationController();

  @override
  void dispose() {
    _transformationController.dispose();
    super.dispose();
  }

  void _resetScale() {
    setState(() {
      _scale = 1.0;
      _transformationController.value = Matrix4.identity();
    });
  }

  @override
  Widget build(BuildContext context) {
    ImageProvider imageProvider;
    
    try {
      final cleanBase64 = Base64ImageService.extractBase64(widget.base64Image);
      if (cleanBase64 == null || cleanBase64.isEmpty) {
        throw Exception('Invalid base64 data');
      }
      imageProvider = MemoryImage(base64.decode(cleanBase64));
    } catch (e) {
      print('❌ Error loading image: $e');
      return Scaffold(
        appBar: AppBar(
          title: Text(widget.title),
          backgroundColor: Colors.red,
        ),
        body: const Center(
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Icon(Icons.error, size: 64, color: Colors.red),
              SizedBox(height: 16),
              Text('Failed to load image', style: TextStyle(fontSize: 18)),
              SizedBox(height: 8),
              Text('The image data may be corrupted', style: TextStyle(fontSize: 14, color: Colors.grey)),
            ],
          ),
        ),
      );
    }

    return Scaffold(
      backgroundColor: Colors.black,
      appBar: AppBar(
        title: Text(widget.title),
        backgroundColor: Colors.black,
        iconTheme: const IconThemeData(color: Colors.white),
        actions: [
          IconButton(
            icon: const Icon(Icons.refresh, color: Colors.white),
            onPressed: () {
              _transformationController.value = Matrix4.identity();
            },
          ),
        ],
      ),
      body: Center(
        child: InteractiveViewer(
          transformationController: _transformationController,
          minScale: 0.5,
          maxScale: 5.0,
          boundaryMargin: const EdgeInsets.all(20),
          child: Container(
            constraints: BoxConstraints(
              minHeight: 200,
              minWidth: 200,
              maxHeight: MediaQuery.of(context).size.height - 200,
              maxWidth: MediaQuery.of(context).size.width - 40,
            ),
            child: Image(
              image: imageProvider,
              fit: BoxFit.contain,
              errorBuilder: (context, error, stackTrace) {
                return const Center(
                  child: Column(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      Icon(Icons.error, size: 64, color: Colors.white),
                      SizedBox(height: 16),
                      Text('Failed to load image', style: TextStyle(color: Colors.white)),
                    ],
                  ),
                );
              },
            ),
          ),
        ),
      ),
      bottomNavigationBar: Container(
        color: Colors.black87,
        padding: const EdgeInsets.all(16),
        child: Row(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            const Icon(Icons.zoom_in, color: Colors.white),
            const SizedBox(width: 8),
            Text(
              'Pinch to zoom • Drag to pan',
              style: TextStyle(color: Colors.white.withOpacity(0.8)),
            ),
          ],
        ),
      ),
    );
  }
}
