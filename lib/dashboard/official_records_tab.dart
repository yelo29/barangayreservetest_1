import 'package:flutter/material.dart';

class OfficialRecordsTab extends StatefulWidget {
  const OfficialRecordsTab({super.key});

  @override
  State<OfficialRecordsTab> createState() => _OfficialRecordsTabState();
}

class _OfficialRecordsTabState extends State<OfficialRecordsTab> {
  String _selectedStatus = 'approved'; // approved, rejected, completed

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        // Status filter buttons
        Container(
          padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
          child: Row(
            children: [
              _statusButton('approved', 'Approved'),
              const SizedBox(width: 8),
              _statusButton('rejected', 'Rejected'),
              const SizedBox(width: 8),
              _statusButton('completed', 'Completed'),
            ],
          ),
        ),

        // Records list
        Expanded(
          child: StreamBuilder<QuerySnapshot>(
            stream: FirebaseFirestore.instance
                .collection('bookings')
                .where('status', isEqualTo: _selectedStatus)
                .orderBy('reviewedDate', descending: true)
                .snapshots(),
            builder: (context, snapshot) {
              if (snapshot.hasError) {
                return Center(child: Text('Error: ${snapshot.error}'));
              }

              if (snapshot.connectionState == ConnectionState.waiting) {
                return const Center(child: CircularProgressIndicator());
              }

              final records = snapshot.data?.docs ?? [];

              if (records.isEmpty) {
                return Center(
                  child: Text(
                    'No $_selectedStatus bookings found',
                    style: const TextStyle(fontSize: 16, color: Colors.grey),
                  ),
                );
              }

              return ListView.builder(
                itemCount: records.length,
                itemBuilder: (context, index) {
                  final booking = records[index].data() as Map<String, dynamic>;

                  return Card(
                    margin: const EdgeInsets.symmetric(horizontal: 16, vertical: 4),
                    child: ListTile(
                      title: Text(
                        booking['fullName'] ?? 'Unknown',
                        style: const TextStyle(fontWeight: FontWeight.bold),
                      ),
                      subtitle: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Text('Facility: ${booking['facilityName'] ?? 'N/A'}'),
                          Text('Date: ${booking['date'] ?? 'N/A'}'),
                          Text('Time: ${booking['timeslot'] ?? 'N/A'}'),
                          if (_selectedStatus == 'rejected')
                            Text('Reason: ${booking['rejectionReason'] ?? 'N/A'}'),
                        ],
                      ),
                      trailing: _getStatusIcon(_selectedStatus),
                      onTap: () => _showRecordDetailsDialog(booking),
                    ),
                  );
                },
              );
            },
          ),
        ),
      ],
    );
  }

  Widget _statusButton(String status, String label) {
    final isSelected = _selectedStatus == status;
    return Expanded(
      child: ElevatedButton(
        onPressed: () {
          setState(() {
            _selectedStatus = status;
          });
        },
        style: ElevatedButton.styleFrom(
          backgroundColor: isSelected ? Colors.blue[800] : Colors.white,
          foregroundColor: isSelected ? Colors.white : Colors.blue[800],
          side: BorderSide(color: Colors.blue[200]!),
          padding: const EdgeInsets.symmetric(vertical: 8),
        ),
        child: Text(
          label,
          style: const TextStyle(fontSize: 12),
        ),
      ),
    );
  }

  Widget _getStatusIcon(String status) {
    switch (status.toLowerCase()) {
      case 'approved':
        return const Icon(Icons.check_circle, color: Colors.green);
      case 'rejected':
        return const Icon(Icons.cancel, color: Colors.red);
      case 'completed':
        return const Icon(Icons.done_all, color: Colors.blue);
      default:
        return const Icon(Icons.help, color: Colors.grey);
    }
  }

  void _showRecordDetailsDialog(Map<String, dynamic> booking) {
    showDialog(
      context: context,
      builder: (context) {
        return Dialog(
          insetPadding: const EdgeInsets.all(16),
          child: Container(
            width: double.maxFinite,
            constraints: const BoxConstraints(maxHeight: 500),
            child: Padding(
              padding: const EdgeInsets.all(16),
              child: SingleChildScrollView(
                child: Column(
                  mainAxisSize: MainAxisSize.min,
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Row(
                      children: [
                        const Expanded(
                          child: Text(
                            'Booking Record Details',
                            style: TextStyle(
                              fontSize: 18,
                              fontWeight: FontWeight.bold,
                            ),
                          ),
                        ),
                        IconButton(
                          onPressed: () => Navigator.of(context).pop(),
                          icon: const Icon(Icons.close),
                        ),
                      ],
                    ),
                    const Divider(),
                    const SizedBox(height: 8),

                    // Resident Details
                    const Text(
                      'Resident Information',
                      style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
                    ),
                    const SizedBox(height: 8),
                    Text('Name: ${booking['fullName'] ?? 'N/A'}'),
                    Text('Contact: ${booking['contactNumber'] ?? 'N/A'}'),
                    Text('Address: ${booking['address'] ?? 'N/A'}'),
                    const SizedBox(height: 16),

                    // Booking Details
                    const Text(
                      'Booking Information',
                      style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
                    ),
                    const SizedBox(height: 8),
                    Text('Facility: ${booking['facilityName'] ?? 'N/A'}'),
                    Text('Date: ${booking['date'] ?? 'N/A'}'),
                    Text('Timeslot: ${booking['timeslot'] ?? 'N/A'}'),
                    Text('Status: ${booking['status']?.toUpperCase() ?? 'N/A'}'),
                    const SizedBox(height: 16),

                    // Payment Information
                    const Text(
                      'Payment Details',
                      style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
                    ),
                    const SizedBox(height: 8),
                    Text('Reference Number: ${booking['referenceNumber'] ?? 'N/A'}'),
                    Text('Amount Paid: ₱${booking['amountPaid'] ?? 'N/A'}'),
                    const SizedBox(height: 8),

                    // Dates
                    const Text(
                      'Important Dates',
                      style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
                    ),
                    const SizedBox(height: 8),
                    Text('Submitted: ${_formatDate(booking['submittedDate'])}'),
                    Text('Reviewed: ${_formatDate(booking['reviewedDate'])}'),

                    // Rejection reason if applicable
                    if (booking['status'] == 'rejected' && booking['rejectionReason'] != null) ...[
                      const SizedBox(height: 16),
                      const Text(
                        'Rejection Reason',
                        style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold, color: Colors.red),
                      ),
                      const SizedBox(height: 8),
                      Container(
                        padding: const EdgeInsets.all(12),
                        decoration: BoxDecoration(
                          color: Colors.red[50],
                          border: Border.all(color: Colors.red[200]!),
                          borderRadius: BorderRadius.circular(8),
                        ),
                        child: Text(
                          booking['rejectionReason'],
                          style: const TextStyle(color: Colors.red[800]),
                        ),
                      ),
                    ],

                    const SizedBox(height: 16),
                    Center(
                      child: ElevatedButton(
                        onPressed: () => Navigator.of(context).pop(),
                        child: const Text('Close'),
                      ),
                    ),
                  ],
                ),
              ),
            ),
          ),
        );
      },
    );
  }

  String _formatDate(dynamic date) {
    if (date == null) return 'N/A';
    if (date is Timestamp) {
      return date.toDate().toString().split('.')[0]; // Remove milliseconds
    }
    return date.toString();
  }
}
