import 'package:flutter/material.dart';

class OfficialBookingsPage extends StatelessWidget {
  final List<Map<String, dynamic>> allBookings;

  const OfficialBookingsPage({super.key, required this.allBookings});

  @override
  Widget build(BuildContext context) {
    if (allBookings.isEmpty) {
      return const Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Icon(Icons.event_busy, size: 60, color: Colors.grey),
            SizedBox(height: 16),
            Text(
              "No bookings yet.",
              style: TextStyle(fontSize: 18, color: Colors.grey),
            ),
          ],
        ),
      );
    }

    return ListView.builder(
      padding: const EdgeInsets.all(16.0),
      itemCount: allBookings.length,
      itemBuilder: (context, index) {
        final booking = allBookings[index];
        final facilityName = booking['facilityName'] as String? ?? 'N/A';

        // Determine status color
        Color statusColor;
        String statusText = (booking['status'] as String? ?? 'pending').toUpperCase();
        switch (statusText) {
          case 'APPROVED':
            statusColor = Colors.green.shade400;
            break;
          case 'COMPLETED':
            statusColor = Colors.grey.shade600;
            break;
          default: // PENDING
            statusColor = Colors.orange.shade400;
            break;
        }

        return Card(
          elevation: 2,
          margin: const EdgeInsets.only(bottom: 16.0),
          shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
          child: ListTile(
            contentPadding: const EdgeInsets.symmetric(vertical: 12, horizontal: 16),
            leading: CircleAvatar(
              backgroundColor: Colors.blue.shade100,
              child: const Icon(Icons.event_available, color: Colors.blue),
            ),
            title: Text(
              facilityName,
              style: const TextStyle(fontWeight: FontWeight.bold),
            ),
            subtitle: Text(
              "${booking['date'] as String? ?? ''} at ${booking['time'] as String? ?? ''}\nBooked by: ${booking['name'] as String? ?? ''}",
              style: TextStyle(color: Colors.grey.shade600, height: 1.4),
            ),
            trailing: Chip(
              label: Text(
                statusText,
                style: const TextStyle(color: Colors.white, fontWeight: FontWeight.bold, fontSize: 10),
              ),
              backgroundColor: statusColor,
              padding: const EdgeInsets.symmetric(horizontal: 4),
            ),
          ),
        );
      },
    );
  }
}
