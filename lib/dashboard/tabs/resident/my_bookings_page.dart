import 'package:flutter/material.dart';

class MyBookingsPage extends StatelessWidget {
  final List<Map<String, dynamic>> bookings;

  const MyBookingsPage({super.key, required this.bookings});

  // Helper function to convert time slot ID to time slot string
  String? _getTimeSlotFromId(dynamic timeSlotId) {
    if (timeSlotId == null) return null;
    
    final Map<int, String> timeSlotMap = {
      1: '6:00 AM - 8:00 AM',
      2: '8:00 AM - 10:00 AM',
      3: '10:00 AM - 12:00 PM',
      4: '12:00 PM - 2:00 PM',
      5: '2:00 PM - 4:00 PM',
      6: '4:00 PM - 6:00 PM',
      7: '6:00 PM - 8:00 PM',
      8: '8:00 PM - 10:00 PM',
    };
    
    final int? slotId = int.tryParse(timeSlotId.toString());
    if (slotId == null) return null;
    
    // Handle wrap-around for IDs > 8
    final int wrappedId = ((slotId - 1) % 8) + 1;
    return timeSlotMap[wrappedId] ?? 'Time Slot $slotId';
  }

  @override
  Widget build(BuildContext context) {
    print('🔍 MyBookingsPage.build() called with ${bookings.length} bookings');
    
    if (bookings.isEmpty) {
      print('🔍 MyBookingsPage: No bookings to display');
      return const Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Icon(Icons.event_busy, size: 60, color: Colors.grey),
            SizedBox(height: 16),
            Text(
              "You have no bookings yet.",
              style: TextStyle(fontSize: 18, color: Colors.grey),
            ),
          ],
        ),
      );
    }

    print('🔍 MyBookingsPage: Building ListView with ${bookings.length} bookings');
    return ListView.builder(
      padding: const EdgeInsets.all(16.0),
      itemCount: bookings.length,
      itemBuilder: (context, index) {
        final booking = bookings[index];
        print('🔍 MyBookingsPage: Building booking card $index - ID: ${booking['id']}');
        print('🔍 Booking data: $booking'); // Debug logging
        
        // Enhanced field mapping with fallbacks
        final facilityName = booking['facility_name'] as String? ?? 
                            booking['facilityName'] as String? ?? 
                            booking['facility']?['name'] as String? ?? 
                            'Unknown Facility';
                            
        final date = booking['booking_date'] as String? ?? 
                    booking['date'] as String? ?? 
                    'Not Set';
                    
        // Enhanced time slot resolution - handle ALL DAY for official bookings
        String? timeslot;
        if (booking['start_time'] == 'ALL DAY') {
          timeslot = 'ALL DAY';
        } else {
          timeslot = booking['start_time'] as String? ?? 
                     booking['time_slot'] as String? ?? 
                     booking['timeslot'] as String? ?? 
                     _getTimeSlotFromId(booking['time_slot_id']) ??
                     'Not Set';
        }
        
        final userEmail = booking['user_email'] as String? ?? 
                        booking['email'] as String? ?? 
                        'Unknown User';
        
        // Additional fields for better display - use total_amount for rate
        final rate = booking['total_amount']?.toString() ?? 
                     booking['base_rate']?.toString() ?? 
                     booking['rate']?.toString() ?? 
                     '0';
        
        final status = booking['status'] as String? ?? 'pending';
        final statusText = status.toUpperCase();
        
        print('🔍🔍🔍 MyBookingsPage: Processing booking ID ${booking['id']}');
        print('🔍🔍🔍 MyBookingsPage: Status: "$status" -> "$statusText"');
        print('🔍🔍🔍 MyBookingsPage: Is REJECTED? ${statusText == 'REJECTED'}');
        print('🔍🔍🔍 MyBookingsPage: Has rejection_reason? ${booking['rejection_reason'] != null}');
        if (booking['rejection_reason'] != null) {
          print('🔍🔍🔍 MyBookingsPage: Rejection reason length: ${booking['rejection_reason'].toString().length}');
          print('🔍🔍🔍 MyBookingsPage: Rejection reason preview: "${booking['rejection_reason'].toString().substring(0, 50)}..."');
        }
        
        // Debug for rejection display
        if (statusText == 'REJECTED') {
          print('🔍🔍🔍 MyBookingsPage: === WILL DISPLAY REJECTION SECTION ===');
          print('🔍🔍🔍 MyBookingsPage: Checking rejection display for booking ID ${booking['id']} - statusText: "$statusText"');
          print('🔍🔍🔍 MyBookingsPage: ENTERING REJECTED DISPLAY for booking ID ${booking['id']}');
        } else {
          print('🔍🔍🔍 MyBookingsPage: === NOT REJECTED - Status: $statusText ===');
        }
        
        print('🔍 Processed booking:'); // Debug logging
        print('  - Facility: $facilityName'); 
        print('  - Date: $date');
        print('  - Time: $timeslot');
        print('  - Status: $status');
        print('  - Rate: ₱$rate');

        // Determine status color
        Color statusColor;
        switch (statusText) {
          case 'APPROVED':
            statusColor = Colors.green.shade400;
            break;
          case 'COMPLETED':
            statusColor = Colors.grey.shade600;
            break;
          case 'REJECTED':
            statusColor = Colors.red.shade400;
            break;
          default: // PENDING
            statusColor = Colors.orange.shade400;
            break;
        }

        return Card(
          elevation: 3,
          margin: const EdgeInsets.only(bottom: 16.0),
          shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
          child: Padding(
            padding: const EdgeInsets.all(16.0),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                // Header with facility name and status
                Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
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
                        color: statusColor.withValues(alpha: 0.1),
                        borderRadius: BorderRadius.circular(20),
                        border: Border.all(color: statusColor.withValues(alpha: 0.3)),
                      ),
                      child: Text(
                        statusText,
                        style: TextStyle(
                          color: statusColor,
                          fontWeight: FontWeight.bold,
                          fontSize: 12,
                        ),
                      ),
                    ),
                  ],
                ),
                const SizedBox(height: 12),
                
                // Date and Time
                Row(
                  children: [
                    Icon(Icons.calendar_today, size: 16, color: Colors.grey.shade600),
                    const SizedBox(width: 6),
                    Text(
                      date,
                      style: TextStyle(
                        fontSize: 14,
                        color: Colors.grey.shade700,
                        fontWeight: FontWeight.w500,
                      ),
                    ),
                    const SizedBox(width: 16),
                    Icon(Icons.access_time, size: 16, color: Colors.grey.shade600),
                    const SizedBox(width: 6),
                    Text(
                      timeslot,
                      style: TextStyle(
                        fontSize: 14,
                        color: Colors.grey.shade700,
                        fontWeight: FontWeight.w500,
                      ),
                    ),
                  ],
                ),
                
                // Additional details
                const SizedBox(height: 8),
                Row(
                  children: [
                    Icon(Icons.attach_money, size: 16, color: Colors.green.shade600),
                    const SizedBox(width: 6),
                    Text(
                      'Rate: ₱$rate',
                      style: TextStyle(
                        fontSize: 14,
                        color: Colors.green.shade700,
                        fontWeight: FontWeight.w500,
                      ),
                    ),
                    const SizedBox(width: 16),
                    Icon(Icons.person, size: 16, color: Colors.grey.shade600),
                    const SizedBox(width: 6),
                    Expanded(
                      child: Text(
                        userEmail,
                        style: TextStyle(
                          fontSize: 12,
                          color: Colors.grey.shade600,
                        ),
                        overflow: TextOverflow.ellipsis,
                      ),
                    ),
                  ],
                ),
                
                // Purpose if available - show official override message for rejected bookings
                if (statusText == 'REJECTED') ...[
                  const SizedBox(height: 8),
                  Builder(
                    builder: (context) {
                      print('🔍🔥🔥 MyBookingsPage: Builder called for booking ID ${booking['id']}');
                      print('🔍🔥🔥 MyBookingsPage: Rejection reason: "${booking['rejection_reason']}"');
                      print('🔍🔥🔥 MyBookingsPage: Rejection reason type: ${booking['rejection_reason'].runtimeType}');
                      return Container(
                        padding: const EdgeInsets.all(12),
                        decoration: BoxDecoration(
                          color: Colors.red.shade50,
                          borderRadius: BorderRadius.circular(8),
                          border: Border.all(color: Colors.red.shade200),
                        ),
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Row(
                              children: [
                                Icon(Icons.warning, size: 16, color: Colors.red.shade600),
                                const SizedBox(width: 6),
                                Text(
                                  'Booking Rejected',
                                  style: TextStyle(
                                    fontSize: 14,
                                    fontWeight: FontWeight.bold,
                                    color: Colors.red.shade700,
                                  ),
                                ),
                              ],
                            ),
                            const SizedBox(height: 4),
                            Text(
                              booking['rejection_reason'] ?? 'This date has been booked by Officials, refund of your payments will be done shortly, check your email or SMS for further details.',
                              style: TextStyle(
                                fontSize: 12,
                                color: Colors.red.shade600,
                              ),
                            ),
                          ],
                        ),
                      );
                    },
                  ),
                ] else if (booking['purpose'] != null && booking['purpose'].toString().isNotEmpty) ...[
                  const SizedBox(height: 8),
                  Row(
                    children: [
                      Icon(Icons.description, size: 16, color: Colors.grey.shade600),
                      const SizedBox(width: 6),
                      Expanded(
                        child: Text(
                          booking['purpose'].toString(),
                          style: TextStyle(
                            fontSize: 13,
                            color: Colors.grey.shade600,
                            fontStyle: FontStyle.italic,
                          ),
                          maxLines: 2,
                          overflow: TextOverflow.ellipsis,
                        ),
                      ),
                    ],
                  ),
                ],
              ],
            ),
          ),
        );
      },
    );
  }
}
