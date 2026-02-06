import 'package:flutter/material.dart';
import '../../../services/data_service.dart';
import '../../../services/auth_api_service.dart';
import '../../../widgets/loading_widget.dart';
import '../../../widgets/error_widget.dart';

class ResidentBookingsTab extends StatefulWidget {
  final Map<String, dynamic>? userData;
  
  const ResidentBookingsTab({super.key, this.userData});

  @override
  State<ResidentBookingsTab> createState() => _ResidentBookingsTabState();
}

class _ResidentBookingsTabState extends State<ResidentBookingsTab> {
  List<Map<String, dynamic>> _bookings = [];
  bool _isLoading = true;
  String? _error;

  @override
  void initState() {
    super.initState();
    _loadBookings();
  }

  @override
  void didUpdateWidget(ResidentBookingsTab oldWidget) {
    super.didUpdateWidget(oldWidget);
    // Refresh data when widget is updated (e.g., when navigating back)
    _loadBookings();
  }

  Future<void> _loadBookings() async {
    if (mounted) {
      setState(() {
        _isLoading = true;
        _error = null;
      });
    }

    try {
      final currentUser = await AuthApiService().getCurrentUser();
      if (currentUser == null || currentUser.isEmpty) {
        if (mounted) {
          setState(() {
            _isLoading = false;
            _error = 'User not logged in';
          });
        }
        return;
      }

      print('🔍 Loading bookings for user: ${currentUser['email']}');
      
      // Use DataService for consistent data fetching
      final bookingsResponse = await DataService.fetchBookings();
      
      if (bookingsResponse['success'] == true) {
        final List<Map<String, dynamic>> bookings = bookingsResponse['data'] ?? [];
        print('🔍 Received ${bookings.length} bookings from DataService');
        
        // Debug: Show booking structure
        if (bookings.isNotEmpty) {
          print('🔍 DEBUG: First booking structure: ${bookings.first}');
          print('🔍 DEBUG: Booking keys: ${bookings.first.keys.toList()}');
        }
        
        // Filter bookings for current user (double privacy protection)
        final userBookings = bookings.where((booking) {
          return booking['user_email'] == currentUser['email'];
        }).toList();
        
        if (mounted) {
          setState(() {
            _bookings = userBookings;
            _isLoading = false;
          });
        }
      } else {
        throw Exception(bookingsResponse['error'] ?? 'Failed to fetch bookings');
      }
    } catch (e) {
      print('❌ Error loading bookings: $e');
      if (mounted) {
        setState(() {
          _isLoading = false;
          _error = 'Failed to load bookings: ${e.toString()}';
        });
      }
    }
  }

  Future<void> _refreshBookings() async {
    await _loadBookings();
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
              ),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  const Text(
                    'My Bookings',
                    style: TextStyle(
                      fontSize: 24,
                      fontWeight: FontWeight.bold,
                      color: Colors.white,
                    ),
                  ),
                  const SizedBox(height: 8),
                  Text(
                    'Track your booking requests',
                    style: TextStyle(
                      fontSize: 16,
                      color: Colors.blue[100],
                    ),
                  ),
                ],
              ),
            ),

            const SizedBox(height: 20),

            // Bookings List
            Expanded(
              child: _isLoading
                  ? const Center(child: CircularProgressIndicator())
                  : _error != null
                      ? Center(
                          child: Column(
                            mainAxisAlignment: MainAxisAlignment.center,
                            children: [
                              Icon(
                                Icons.error_outline,
                                size: 80,
                                color: Colors.red[400],
                              ),
                              const SizedBox(height: 16),
                              Text(
                                'Error loading bookings',
                                style: TextStyle(
                                  fontSize: 18,
                                  color: Colors.grey[600],
                                ),
                              ),
                              const SizedBox(height: 8),
                              Text(
                                _error!,
                                style: TextStyle(
                                  fontSize: 14,
                                  color: Colors.grey[500],
                                ),
                                textAlign: TextAlign.center,
                              ),
                              const SizedBox(height: 16),
                              ElevatedButton.icon(
                                onPressed: _refreshBookings,
                                icon: const Icon(Icons.refresh),
                                label: const Text('Retry'),
                                style: ElevatedButton.styleFrom(
                                  backgroundColor: Colors.blue,
                                  foregroundColor: Colors.white,
                                ),
                              ),
                            ],
                          ),
                        )
                      : _bookings.isEmpty
                          ? Center(
                              child: Column(
                                mainAxisAlignment: MainAxisAlignment.center,
                                children: [
                                  Icon(
                                    Icons.book_online,
                                    size: 80,
                                    color: Colors.grey[400],
                                  ),
                                  const SizedBox(height: 16),
                                  Text(
                                    'No bookings yet',
                                    style: TextStyle(
                                      fontSize: 18,
                                      color: Colors.grey[600],
                                    ),
                                  ),
                                  const SizedBox(height: 8),
                                  Text(
                                    'Book a facility to get started',
                                    style: TextStyle(
                                      fontSize: 14,
                                      color: Colors.grey[500],
                                    ),
                                  ),
                                  const SizedBox(height: 16),
                                  ElevatedButton.icon(
                                    onPressed: _refreshBookings,
                                    icon: const Icon(Icons.refresh),
                                    label: const Text('Refresh'),
                                    style: ElevatedButton.styleFrom(
                                      backgroundColor: Colors.blue,
                                      foregroundColor: Colors.white,
                                    ),
                                  ),
                                ],
                              ),
                            )
                          : RefreshIndicator(
                              onRefresh: _refreshBookings,
                              child: ListView.builder(
                                padding: const EdgeInsets.symmetric(horizontal: 20),
                                itemCount: _bookings.length,
                                itemBuilder: (context, index) {
                                  final booking = _bookings[index];
                                  return _buildBookingCard(booking);
                                },
                              ),
                            ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildBookingCard(Map<String, dynamic> booking) {
    final status = booking['status'] ?? 'pending';
    final statusColor = _getStatusColor(status);
    final statusIcon = _getStatusIcon(status);
    final facilityName = booking['facility_name'] ?? booking['facilityName'] ?? 'Unknown Facility';
    
    print('🔍 _buildBookingCard: $facilityName'); // Debug logging

    return Container(
      margin: const EdgeInsets.only(bottom: 16),
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
            // Header with status
            Row(
              children: [
                Container(
                  padding: const EdgeInsets.all(8),
                  decoration: BoxDecoration(
                    color: statusColor.withOpacity(0.1),
                    borderRadius: BorderRadius.circular(8),
                  ),
                  child: Icon(
                    statusIcon,
                    color: statusColor,
                    size: 20,
                  ),
                ),
                const SizedBox(width: 12),
                Expanded(
                  child: Text(
                    facilityName,
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
                    color: statusColor.withOpacity(0.1),
                    borderRadius: BorderRadius.circular(20),
                  ),
                  child: Text(
                    status.toUpperCase(),
                    style: TextStyle(
                      fontSize: 12,
                      color: statusColor,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                ),
              ],
            ),

            const SizedBox(height: 16),

            // Booking Details
            _buildDetailRow(
              icon: Icons.calendar_today,
              label: 'Date',
              value: booking['booking_date'] ?? booking['date'] ?? 'Not set',
            ),
            const SizedBox(height: 8),
            _buildDetailRow(
              icon: Icons.access_time,
              label: 'Time Slot',
              value: booking['start_time'] ?? booking['timeslot'] ?? booking['time_slot'] ?? 'Not set',
            ),
            const SizedBox(height: 8),
            _buildDetailRow(
              icon: Icons.attach_money,
              label: 'Total Amount',
              value: '₱${booking['total_amount'] ?? booking['totalAmount'] ?? '0'}',
            ),
            if (booking['downpayment'] != null) ...[
              const SizedBox(height: 8),
              _buildDetailRow(
                icon: Icons.payment,
                label: 'Downpayment',
                value: '₱${booking['downpayment']}',
              ),
            ],

            // Purpose/Notes
            if (booking['purpose'] != null && booking['purpose'].isNotEmpty) ...[
              const SizedBox(height: 12),
              Container(
                padding: const EdgeInsets.all(12),
                decoration: BoxDecoration(
                  color: Colors.grey[50],
                  borderRadius: BorderRadius.circular(8),
                ),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      'Purpose',
                      style: TextStyle(
                        fontSize: 12,
                        color: Colors.grey[600],
                        fontWeight: FontWeight.w500,
                      ),
                    ),
                    const SizedBox(height: 4),
                    Text(
                      booking['purpose'],
                      style: const TextStyle(
                        fontSize: 14,
                        color: Colors.black87,
                      ),
                    ),
                  ],
                ),
              ),
            ],

            // Created Date
            const SizedBox(height: 12),
            Builder(
              builder: (context) {
                final createdAt = booking['created_at'] ?? booking['createdAt'] ?? 'Unknown';
                print('🔍 Booking created_at field: $createdAt'); // Debug logging
                return Text(
                  'Booked on ${_formatDate(createdAt)}',
                  style: TextStyle(
                    fontSize: 12,
                    color: Colors.grey[500],
                  ),
                );
              },
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildDetailRow({
    required IconData icon,
    required String label,
    required String value,
  }) {
    return Row(
      children: [
        Icon(
          icon,
          size: 16,
          color: Colors.grey[600],
        ),
        const SizedBox(width: 8),
        Text(
          '$label:',
          style: TextStyle(
            fontSize: 14,
            color: Colors.grey[600],
            fontWeight: FontWeight.w500,
          ),
        ),
        const SizedBox(width: 8),
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
    );
  }

  Color _getStatusColor(String status) {
    switch (status.toLowerCase()) {
      case 'pending':
        return Colors.yellow;
      case 'approved':
        return Colors.green;
      case 'rejected':
        return Colors.red;
      case 'cancelled':
        return Colors.grey;
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
      case 'cancelled':
        return Icons.not_interested;
      default:
        return Icons.help;
    }
  }

  String _formatDate(dynamic date) {
    if (date == null) return 'Unknown';
    
    DateTime dateTime;
    if (date is DateTime) {
      dateTime = date;
    } else if (date is String) {
      try {
        // Parse string date "2026-02-01 16:51:24"
        dateTime = DateTime.parse(date);
      } catch (e) {
        print('🔍 Error parsing date string: $date - $e');
        return 'Unknown';
      }
    } else if (date is Map && date.containsKey('_seconds')) {
      // Handle Firebase timestamp format
      try {
        final seconds = date['_seconds'] as int;
        final nanoseconds = date['_nanoseconds'] as int? ?? 0;
        dateTime = DateTime.fromMillisecondsSinceEpoch(seconds * 1000 + nanoseconds ~/ 1000000);
      } catch (e) {
        print('🔍 Error parsing Firebase timestamp: $date - $e');
        return 'Unknown';
      }
    } else {
      print('🔍 Unsupported date type: ${date.runtimeType}');
      return 'Unknown';
    }

    // Format to "February 1, 2026"
    final months = [
      'January', 'February', 'March', 'April', 'May', 'June',
      'July', 'August', 'September', 'October', 'November', 'December'
    ];
    
    return '${months[dateTime.month - 1]} ${dateTime.day}, ${dateTime.year}';
  }
}
