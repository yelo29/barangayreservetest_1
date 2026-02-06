import 'package:flutter/material.dart';
import '../../services/api_service.dart';

class OfficialHomeTab extends StatefulWidget {
  final Map<String, dynamic>? userData;
  
  const OfficialHomeTab({super.key, this.userData});

  @override
  State<OfficialHomeTab> createState() => _OfficialHomeTabState();
}

class _OfficialHomeTabState extends State<OfficialHomeTab> {
  List<Map<String, dynamic>> _facilities = [];
  bool _isLoading = true;

  @override
  void initState() {
    super.initState();
    _loadFacilities();
  }

  Future<void> _loadFacilities() async {
    try {
      final facilities = await ApiService.getFacilities();
      
      setState(() {
        _facilities = facilities.map((facility) => {
                  'id': facility['id'].toString(),
                  ...facility,
                }).toList();
        _isLoading = false;
      });
    } catch (e) {
      print('Error loading facilities: $e');
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
                color: Colors.red,
                borderRadius: const BorderRadius.only(
                  bottomLeft: Radius.circular(20),
                  bottomRight: Radius.circular(20),
                ),
              ),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    'Welcome, ${widget.userData?['fullName'] ?? 'Official'}!',
                    style: const TextStyle(
                      fontSize: 24,
                      fontWeight: FontWeight.bold,
                      color: Colors.white,
                    ),
                  ),
                  const SizedBox(height: 8),
                  Text(
                    'Manage facilities and bookings',
                    style: TextStyle(
                      fontSize: 16,
                      color: Colors.red[100],
                    ),
                  ),
                ],
              ),
            ),

            const SizedBox(height: 20),

            // Quick Actions
            Padding(
              padding: const EdgeInsets.symmetric(horizontal: 16),
              child: Row(
                children: [
                  Expanded(
                    child: _buildQuickAction(
                      icon: Icons.add_location,
                      label: 'Add Facility',
                      color: Colors.red,
                      onTap: () {
                        // TODO: Navigate to add facility
                        // For now, show facility management info
                        showDialog(
                          context: context,
                          builder: (context) => AlertDialog(
                            title: const Text('Add Facility'),
                            content: const Text(
                              'Facility management features:\n\n'
                              '• Add new barangay facilities\n'
                              '• Set pricing and capacity\n'
                              '• Manage availability schedules\n'
                              '• Upload facility photos\n\n'
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
                    child: _buildQuickAction(
                      icon: Icons.event_available,
                      label: 'Create Event',
                      color: Colors.red,
                      onTap: () {
                        // TODO: Navigate to create instant event
                        // For now, show event creation info
                        showDialog(
                          context: context,
                          builder: (context) => AlertDialog(
                            title: const Text('Create Event'),
                            content: const Text(
                              'Event management features:\n\n'
                              '• Create official barangay events\n'
                              '• Set event dates and times\n'
                              '• Block facility dates for events\n'
                              '• Manage event calendars\n\n'
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
            ),

            const SizedBox(height: 24),

            // Facilities List Header
            Padding(
              padding: const EdgeInsets.symmetric(horizontal: 16),
              child: Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  const Text(
                    'Facilities',
                    style: TextStyle(
                      fontSize: 20,
                      fontWeight: FontWeight.bold,
                      color: Colors.black87,
                    ),
                  ),
                  Text(
                    '${_facilities.length} facilities',
                    style: TextStyle(
                      fontSize: 14,
                      color: Colors.grey[600],
                    ),
                  ),
                ],
              ),
            ),

            const SizedBox(height: 16),

            // Facilities List
            Expanded(
              child: _isLoading
                  ? const Center(child: CircularProgressIndicator())
                  : _facilities.isEmpty
                      ? Center(
                          child: Column(
                            mainAxisAlignment: MainAxisAlignment.center,
                            children: [
                              Icon(
                                Icons.location_city,
                                size: 80,
                                color: Colors.grey[400],
                              ),
                              const SizedBox(height: 16),
                              Text(
                                'No facilities yet',
                                style: TextStyle(
                                  fontSize: 18,
                                  color: Colors.grey[600],
                                ),
                              ),
                              const SizedBox(height: 8),
                              ElevatedButton.icon(
                                onPressed: () {
                                  // TODO: Navigate to add facility
                                  // For now, show facility management info
                                  showDialog(
                                    context: context,
                                    builder: (context) => AlertDialog(
                                      title: const Text('Add Facility'),
                                      content: const Text(
                                        'Facility management features:\n\n'
                                        '• Add new barangay facilities\n'
                                        '• Set pricing and capacity\n'
                                        '• Manage availability schedules\n'
                                        '• Upload facility photos\n\n'
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
                                icon: const Icon(Icons.add),
                                label: const Text('Add First Facility'),
                                style: ElevatedButton.styleFrom(
                                  backgroundColor: Colors.red[50],
                                  foregroundColor: Colors.white,
                                ),
                              ),
                            ],
                          ),
                        )
                      : ListView.builder(
                          padding: const EdgeInsets.symmetric(horizontal: 16),
                          itemCount: _facilities.length,
                          itemBuilder: (context, index) {
                            final facility = _facilities[index];
                            return _buildFacilityCard(facility);
                          },
                        ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildQuickAction({
    required IconData icon,
    required String label,
    required Color color,
    required VoidCallback onTap,
  }) {
    return Container(
      height: 100,
      decoration: BoxDecoration(
        color: color.withOpacity(0.1),
        borderRadius: BorderRadius.circular(12),
        border: Border.all(
          color: color.withOpacity(0.3),
          width: 2,
        ),
      ),
      child: Material(
        color: Colors.transparent,
        child: InkWell(
          borderRadius: BorderRadius.circular(12),
          onTap: onTap,
          child: Padding(
            padding: const EdgeInsets.all(16),
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                Icon(
                  icon,
                  size: 32,
                  color: color,
                ),
                const SizedBox(height: 8),
                Text(
                  label,
                  style: TextStyle(
                    fontSize: 14,
                    fontWeight: FontWeight.bold,
                    color: color,
                  ),
                  textAlign: TextAlign.center,
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }

  Widget _buildFacilityCard(Map<String, dynamic> facility) {
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
      child: Padding(
        padding: const EdgeInsets.all(20),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                Container(
                  padding: const EdgeInsets.all(12),
                  decoration: BoxDecoration(
                    color: Colors.red[50],
                    borderRadius: BorderRadius.circular(8),
                  ),
                  child: Icon(
                    Icons.location_city,
                    color: Colors.red[600],
                    size: 28,
                  ),
                ),
                const SizedBox(width: 16),
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        facility['name'] ?? 'Facility Name',
                        style: const TextStyle(
                          fontSize: 20,
                          fontWeight: FontWeight.bold,
                          color: Colors.black87,
                        ),
                      ),
                      const SizedBox(height: 4),
                      Text(
                        facility['description'] ?? 'Facility description',
                        style: TextStyle(
                          fontSize: 14,
                          color: Colors.grey[600],
                        ),
                      ),
                    ],
                  ),
                ),
                PopupMenuButton<String>(
                  icon: Icon(Icons.more_vert, color: Colors.red[600]),
                  onSelected: (value) {
                    switch (value) {
                      case 'edit':
                        // TODO: Navigate to edit facility
                        // For now, show edit facility info
                        showDialog(
                          context: context,
                          builder: (context) => AlertDialog(
                            title: const Text('Edit Facility'),
                            content: const Text(
                              'Facility editing features:\n\n'
                              '• Update facility information\n'
                              '• Change pricing and capacity\n'
                              '• Modify facility descriptions\n'
                              '• Update facility photos\n\n'
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
                        break;
                      case 'calendar':
                        // TODO: Navigate to facility calendar
                        // For now, show calendar info
                        showDialog(
                          context: context,
                          builder: (context) => AlertDialog(
                            title: const Text('Facility Calendar'),
                            content: const Text(
                              'Calendar management features:\n\n'
                              '• View facility availability\n'
                              '• Manage booking schedules\n'
                              '• Set blackout dates\n'
                              '• View booking history\n\n'
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
                        break;
                      case 'delete':
                        _showDeleteConfirmation(facility);
                        break;
                    }
                  },
                  itemBuilder: (context) => [
                    const PopupMenuItem(
                      value: 'edit',
                      child: Row(
                        children: [
                          Icon(Icons.edit, size: 16),
                          SizedBox(width: 8),
                          Text('Edit'),
                        ],
                      ),
                    ),
                    const PopupMenuItem(
                      value: 'calendar',
                      child: Row(
                        children: [
                          Icon(Icons.calendar_today, size: 16),
                          SizedBox(width: 8),
                          Text('View Calendar'),
                        ],
                      ),
                    ),
                    const PopupMenuItem(
                      value: 'delete',
                      child: Row(
                        children: [
                          Icon(Icons.delete, size: 16, color: Colors.red),
                          SizedBox(width: 8),
                          Text('Delete', style: TextStyle(color: Colors.red)),
                        ],
                      ),
                    ),
                  ],
                ),
              ],
            ),
            const SizedBox(height: 16),
            Row(
              children: [
                _buildInfoChip(
                  icon: Icons.attach_money,
                  label: '₱${facility['price'] ?? '0'}',
                  color: Colors.red,
                ),
                const SizedBox(width: 12),
                _buildInfoChip(
                  icon: Icons.payment,
                  label: '₱${facility['downpayment'] ?? '0'} down',
                  color: Colors.orange,
                ),
                const SizedBox(width: 12),
                _buildInfoChip(
                  icon: Icons.group,
                  label: '${facility['capacity'] ?? '0'} capacity',
                  color: Colors.purple,
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildInfoChip({
    required IconData icon,
    required String label,
    required Color color,
  }) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
      decoration: BoxDecoration(
        color: color.withOpacity(0.1),
        borderRadius: BorderRadius.circular(20),
      ),
      child: Row(
        mainAxisSize: MainAxisSize.min,
        children: [
          Icon(
            icon,
            size: 16,
            color: color,
          ),
          const SizedBox(width: 4),
          Text(
            label,
            style: TextStyle(
              fontSize: 12,
              color: color,
              fontWeight: FontWeight.w500,
            ),
          ),
        ],
      ),
    );
  }

  void _showDeleteConfirmation(Map<String, dynamic> facility) {
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text('Delete Facility'),
        content: Text('Are you sure you want to delete "${facility['name']}"?'),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context),
            child: const Text('Cancel'),
          ),
          ElevatedButton(
            onPressed: () async {
              Navigator.pop(context);
              
              // Show loading indicator
              showDialog(
                context: context,
                barrierDismissible: false,
                builder: (context) => const AlertDialog(
                  content: Row(
                    children: [
                      CircularProgressIndicator(),
                      SizedBox(width: 20),
                      Text('Deleting facility...'),
                    ],
                  ),
                ),
              );
              
              // Perform actual delete
              try {
                final result = await _firebaseService.deleteFacility(facility['id'].toString());
                
                // Close loading dialog
                Navigator.pop(context);
                
                // Show result
                showDialog(
                  context: context,
                  builder: (context) => AlertDialog(
                    title: Text(result['success'] ? 'Success' : 'Error'),
                    content: Text(result['success'] 
                        ? 'Facility deleted successfully!' 
                        : result['error'] ?? 'Failed to delete facility'),
                    actions: [
                      TextButton(
                        onPressed: () => Navigator.pop(context),
                        child: const Text('OK'),
                      ),
                    ],
                  ),
                );
                
                // Refresh facilities list if successful
                if (result['success']) {
                  _loadFacilities();
                }
              } catch (e) {
                // Close loading dialog
                Navigator.pop(context);
                
                // Show error
                showDialog(
                  context: context,
                  builder: (context) => AlertDialog(
                    title: const Text('Error'),
                    content: Text('Failed to delete facility: $e'),
                    actions: [
                      TextButton(
                        onPressed: () => Navigator.pop(context),
                        child: const Text('OK'),
                      ),
                    ],
                  ),
                );
              }
            },
            style: ElevatedButton.styleFrom(
              backgroundColor: Colors.red,
              foregroundColor: Colors.white,
            ),
            child: const Text('Delete'),
          ),
        ],
      ),
    );
  }
}
