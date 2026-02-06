// SIMPLIFIED PLACEHOLDER WIDGET
import 'package:flutter/material.dart';

class UnifiedCalendarWidget extends StatelessWidget {
  final dynamic facility;
  final bool showDetails;
  final Function(DateTime)? onDateSelected;

  const UnifiedCalendarWidget({
    super.key,
    required this.facility,
    this.showDetails = false,
    this.onDateSelected,
  });

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: EdgeInsets.all(16),
      margin: EdgeInsets.all(8),
      decoration: BoxDecoration(
        color: Colors.grey[100],
        borderRadius: BorderRadius.circular(8),
        border: Border.all(color: Colors.grey[300]!),
      ),
      child: Column(
        children: [
          Icon(Icons.calendar_today, size: 48, color: Colors.grey[600]),
          SizedBox(height: 8),
          Text(
            'Calendar View',
            style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
          ),
          SizedBox(height: 4),
          Text(
            'Calendar temporarily under maintenance',
            style: TextStyle(fontSize: 14, color: Colors.grey[600]),
          ),
          SizedBox(height: 16),
          ElevatedButton(
            onPressed: () {
              if (onDateSelected != null) {
                onDateSelected!(DateTime.now());
              }
            },
            child: Text('Select Today'),
          ),
        ],
      ),
    );
  }
}
