import 'package:flutter/material.dart';
import '../utils/debug_logger.dart';

class TimeslotDialog extends StatefulWidget {
  final Map<String, dynamic> facility;
  final Map<String, dynamic>? userBookings; // User's existing bookings
  final Map<String, dynamic>? allBookings; // All bookings for competitive checking

  const TimeslotDialog({
    super.key, 
    required this.facility,
    this.userBookings,
    this.allBookings,
  });

  @override
  State<TimeslotDialog> createState() => _TimeslotDialogState();
}

class _TimeslotDialogState extends State<TimeslotDialog> {
  String? _selectedTimeslot;
  
  // Get timeslot status and color
  Map<String, dynamic> _getTimeslotStatus(String timeslot) {
    // Check if user has approved booking for this timeslot
    final userApproved = widget.userBookings?.containsKey(timeslot) == true && 
                        widget.userBookings?[timeslot]['status'] == 'approved';
    
    // Check if user has pending booking for this timeslot
    final userPending = widget.userBookings?.containsKey(timeslot) == true && 
                       widget.userBookings?[timeslot]['status'] == 'pending';
    
    // Check if timeslot is available (no other bookings)
    final hasOtherBookings = widget.allBookings?.containsKey(timeslot) == true;
    
    if (userApproved) {
      return {'status': 'user_approved', 'color': Colors.green, 'enabled': false};
    } else if (userPending) {
      return {'status': 'user_pending', 'color': Colors.yellow, 'enabled': true};
    } else if (hasOtherBookings) {
      return {'status': 'competitive', 'color': Colors.white, 'enabled': true};
    } else {
      return {'status': 'available', 'color': Colors.white, 'enabled': true};
    }
  }

  // Get timeslot description
  String _getTimeslotDescription(String status) {
    switch (status) {
      case 'user_approved':
        return 'Your approved booking';
      case 'user_pending':
        return 'Your pending booking';
      case 'competitive':
        return 'Competitive slot available';
      case 'available':
        return 'Available';
      default:
        return '';
    }
  }

  // Build timeslot trailing widget
  Widget? _buildTimeslotTrailing(Map<String, dynamic> timeslotStatus, bool isSelected) {
    if (timeslotStatus['status'] == 'user_approved') {
      return const Icon(Icons.check_circle, color: Colors.green);
    } else if (timeslotStatus['status'] == 'user_pending') {
      return const Icon(Icons.pending, color: Colors.orange);
    } else if (isSelected) {
      return const Icon(Icons.check, color: Colors.blue);
    } else if (timeslotStatus['status'] == 'competitive') {
      return const Icon(Icons.people, color: Colors.grey, size: 16);
    }
    return null;
  }

  final List<String> timeslots = [
    '6:00 AM - 8:00 AM',
    '8:00 AM - 10:00 AM',
    '10:00 AM - 12:00 PM',
    '12:00 PM - 2:00 PM',
    '2:00 PM - 4:00 PM',
    '4:00 PM - 6:00 PM',
    '6:00 PM - 8:00 PM',
    '8:00 PM - 10:00 PM',
  ];

  @override
  Widget build(BuildContext context) {
    DebugLogger.ui('TimeslotDialog: Opening dialog for facility: ${widget.facility['name']}');
    
    return AlertDialog(
      title: Text('Select Timeslot - ${widget.facility['name'] ?? 'Facility'}'),
      content: SizedBox(
        width: double.maxFinite,
        child: ListView.builder(
          shrinkWrap: true,
          itemCount: timeslots.length,
          itemBuilder: (context, index) {
            final timeslot = timeslots[index];
            final isSelected = _selectedTimeslot == timeslot;
            final timeslotStatus = _getTimeslotStatus(timeslot);
            
            return ListTile(
              title: Text(timeslot),
              subtitle: Text(
                _getTimeslotDescription(timeslotStatus['status']),
                style: TextStyle(
                  fontSize: 12,
                  color: timeslotStatus['status'] == 'user_approved' ? Colors.green.shade700 : Colors.grey.shade600,
                ),
              ),
              trailing: _buildTimeslotTrailing(timeslotStatus, isSelected),
              tileColor: timeslotStatus['color'],
              enabled: timeslotStatus['enabled'],
              onTap: timeslotStatus['enabled'] ? () {
                setState(() {
                  _selectedTimeslot = timeslot;
                });
              } : null,
            );
          },
        ),
      ),
      actions: [
        TextButton(
          onPressed: () => Navigator.pop(context),
          child: const Text('CANCEL'),
        ),
        ElevatedButton(
          onPressed: _selectedTimeslot != null 
              ? () => Navigator.pop(context, _selectedTimeslot)
              : null,
          child: const Text('SELECT'),
        ),
      ],
    );
  }
}
