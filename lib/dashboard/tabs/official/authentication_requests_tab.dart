import 'package:flutter/material.dart';
import '../../../services/api_service_updated.dart' as api_service;

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
          _filteredRequests = _verificationRequests;
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
                            onTap: () {
                              showDialog(
                                context: context,
                                builder: (context) => AlertDialog(
                                  title: const Text('Profile Photo'),
                                  content: const Text(
                                    'Photo viewing features:\n\n'
                                    '• View full-size profile photos\n'
                                    '• Download photo copies\n'
                                    '• Verify photo authenticity\n'
                                    '• Zoom and inspect details\n\n'
                                    'This feature will be available in the next update.',
                                  ),
                                  actions: [
                                    TextButton(
                                      onPressed: () => Navigator.pop(context),
                                      child: const Text('OK'),
                                    ),
                                  ],
                                ),
                              );
                            },
                          ),
                        ),
                        const SizedBox(width: 12),
                        Expanded(
                          child: _buildPhotoCard(
                            title: 'Valid ID',
                            imageUrl: request['valid_id_base64'],
                            onTap: () {
                              showDialog(
                                context: context,
                                builder: (context) => AlertDialog(
                                  title: const Text('Valid ID'),
                                  content: const Text(
                                    'ID viewing features:\n\n'
                                    '• View full-size ID photos\n'
                                    '• Download ID copies\n'
                                    '• Verify ID authenticity\n'
                                    '• Check ID details and information\n\n'
                                    'This feature will be available in the next update.',
                                  ),
                                  actions: [
                                    TextButton(
                                      onPressed: () => Navigator.pop(context),
                                      child: const Text('OK'),
                                    ),
                                  ],
                                ),
                              );
                            },
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
                            backgroundColor: Colors.red,
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
          Center(
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                Icon(
                  imageUrl != null ? Icons.image : Icons.person,
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

  Future<void> _updateVerificationStatus(int requestId, String status) async {
    try {
      final response = await api_service.ApiService.updateVerificationStatus(requestId, status);

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
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
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
              title: const Text('5% (Non-Resident)'),
              value: '0.05',
              groupValue: verificationType == 'non-resident' ? '0.05' : '0.10',
              onChanged: (value) {
                Navigator.pop(context);
                _updateVerificationStatus(requestId, 'approved');
              },
            ),
            RadioListTile<String>(
              title: const Text('10% (Resident)'),
              value: '0.10',
              groupValue: verificationType == 'resident' ? '0.10' : '0.05',
              onChanged: (value) {
                Navigator.pop(context);
                _updateVerificationStatus(requestId, 'approved');
              },
            ),
          ],
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context),
            child: const Text('Cancel'),
          ),
        ],
      ),
    );
  }

  String _formatDate(dynamic date) {
    if (date == null) return 'Unknown';
    
    try {
      DateTime dateTime;
      if (date is String) {
        dateTime = DateTime.parse(date);
      } else if (date is DateTime) {
        dateTime = date;
      } else {
        return 'Unknown';
      }

      return '${dateTime.day}/${dateTime.month}/${dateTime.year}';
    } catch (e) {
      return 'Unknown';
    }
  }
}
