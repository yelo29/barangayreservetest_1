import 'package:flutter/material.dart';

import 'package:intl/intl.dart';

import '../../../services/api_service.dart';

import '../../../models/facility_model.dart';

import '../../../widgets/enhanced_calendar.dart';

import 'form_screen.dart';



class ResidentHomePage extends StatefulWidget {

  final List<Facility> facilities;

  final ScrollController scrollController;

  final Map<String, Map<String, List<Map<String, dynamic>>>> approvedBookings;

  final Map<String, Map<String, List<Map<String, dynamic>>>> pendingBookings;

  final VoidCallback? onRefresh;

  final Map<String, dynamic>? userData;



  const ResidentHomePage({

    super.key,

    required this.facilities,

    required this.scrollController,

    required this.approvedBookings,

    required this.pendingBookings,

    this.onRefresh,

    this.userData,

  });



  @override

  State<ResidentHomePage> createState() => _ResidentHomePageState();

}



class _ResidentHomePageState extends State<ResidentHomePage> {

  @override

  void initState() {

    super.initState();

    print(

      '🔍 ResidentHomePage initialized with ${widget.facilities.length} facilities',

    );

    widget.facilities.forEach((facility) {

      print('   - ${facility.name} (${facility.icon})');

    });

  }



  @override

  Widget build(BuildContext context) {

    if (widget.facilities.isEmpty) {

      return Center(

        child: Column(

          mainAxisAlignment: MainAxisAlignment.center,

          children: [

            Icon(Icons.business, size: 80, color: Colors.grey[400]),

            const SizedBox(height: 16),

            Text(

              'No Facilities Available',

              style: TextStyle(

                fontSize: 24,

                fontWeight: FontWeight.bold,

                color: Colors.grey[600],

              ),

            ),

            const SizedBox(height: 8),

            Text(

              'Please contact the barangay official to add facilities.',

              style: TextStyle(fontSize: 16, color: Colors.grey[500]),

              textAlign: TextAlign.center,

            ),

            const SizedBox(height: 24),

            ElevatedButton(

              onPressed: () {

                // Just show a simple refresh message

                ScaffoldMessenger.of(context).showSnackBar(

                  const SnackBar(

                    content: Text('Refreshing facilities...'),

                    duration: Duration(seconds: 2),

                  ),

                );

              },

              style: ElevatedButton.styleFrom(

                backgroundColor: Colors.blue,

                foregroundColor: Colors.white,

              ),

              child: const Text('Refresh'),

            ),

          ],

        ),

      );

    }



    return GridView.builder(

      controller: widget.scrollController,

      padding: const EdgeInsets.all(16),

      itemCount: widget.facilities.length,

      gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(

        crossAxisCount: 2,

        mainAxisSpacing: 12,

        crossAxisSpacing: 12,

        childAspectRatio: 1,

      ),

      itemBuilder: (context, index) {

        final facility = widget.facilities[index];

        return GestureDetector(

          onTap: () {

            _showCalendar(context, facility);

          },

          child: Container(

            decoration: BoxDecoration(

              color: Colors.blue.shade50,

              borderRadius: BorderRadius.circular(12),

              border: Border.all(

                color: const Color.from(

                  alpha: 1,

                  red: 1,

                  green: 0.804,

                  blue: 0.824,

                ),

              ),

              boxShadow: const [

                BoxShadow(

                  color: Color.fromARGB(137, 0, 0, 0),

                  blurRadius: 6,

                  offset: Offset(0, 2),

                ),

              ],

            ),

            padding: const EdgeInsets.all(12),

            child: Column(

              mainAxisAlignment: MainAxisAlignment.center,

              children: [

                Icon(Icons.business, size: 42, color: Colors.blue.shade700),

                const SizedBox(height: 8),

                Text(

                  facility.name,

                  style: const TextStyle(fontWeight: FontWeight.bold),

                  textAlign: TextAlign.center,

                  maxLines: 2,

                  overflow: TextOverflow.ellipsis,

                ),

                const SizedBox(height: 4),

                Text(

                  _getPriceDisplay(facility),

                  style: TextStyle(

                    color: widget.userData?['verified'] == true ? Colors.green : Colors.blue,

                    fontWeight: FontWeight.bold,

                  ),

                ),

                const SizedBox(height: 4),

                if (facility.amenities.isNotEmpty)

                  Text(

                    facility.amenities,

                    style: const TextStyle(fontSize: 11, color: Colors.grey),

                    textAlign: TextAlign.center,

                    maxLines: 2,

                    overflow: TextOverflow.ellipsis,

                  ),

                const SizedBox(height: 8),

                const Text(

                  'Tap to book',

                  style: TextStyle(fontSize: 12, color: Colors.grey),

                ),

              ],

            ),

          ),

        );

      },

    );

  }



  // Shows a dialog with a calendar for selecting a booking date with status indicators
  void _showCalendar(BuildContext context, Facility facility) async {
    final selectedDate = await showDialog<DateTime>(
      context: context,
      builder: (ctx) => Dialog(
        child: SizedBox(
          width: MediaQuery.of(context).size.width * 0.9,
          height: MediaQuery.of(context).size.height * 0.75,
          child: EnhancedCalendar(
            selectedDate: DateTime.now(),
            bookingStatuses: _buildBookingStatusesForFacility(facility.id),
            pendingColor: Colors.orange.shade200,
            bookedColor: Colors.green.shade200,
            availableColor: Colors.grey.shade100,
            selectedColor: Colors.blue,
            showTodayButton: true,
            isDateEnabled: (date) {
              // Check if date is in past
              if (date.isBefore(DateTime.now())) {
                return false;
              }
              
              // Check if date has official booking
              final bookingStatuses = _buildBookingStatusesForFacility(facility.id);
              final dateStr = DateFormat.yMMMMd('en_US').format(date);
              final status = bookingStatuses[dateStr];
              
              // Disable official unavailable dates
              return status != 'official_unavailable';
            },
            onDateSelected: (date) {
              Navigator.pop(ctx, date);
            },
          ),
        ),
      ),
    );



    if (selectedDate != null && context.mounted) {

      // Show full booking form for residents (normal process)

      Navigator.push(

        context,

        MaterialPageRoute(

          builder: (_) => FormScreen(

            facilityName: facility.name,

            facilityId: facility.id,

            selectedDate: DateFormat.yMMMMd('en_US').format(selectedDate),

            facilityRate: facility.rate,

            onBookingSubmitted: widget.onRefresh,

          ),

        ),

      );

    }

  }



  // Build a map of booking statuses for the calendar
  // This should only show bookings for the CURRENT USER and SPECIFIC FACILITY
  Map<String, String> _buildBookingStatusesForFacility(String facilityId) {
    final Map<String, String> statuses = {};
    final currentUserEmail = widget.userData?['email'] ?? '';

    print('🔍 Building booking statuses for user: $currentUserEmail, facility: $facilityId');
    print('🔍 Total pending bookings data: ${widget.pendingBookings.keys.toList()}');
    print('🔍 Total approved bookings data: ${widget.approvedBookings.keys.toList()}');

    // Add pending bookings - ONLY for current user and specific facility
    widget.pendingBookings.forEach((fid, dateMap) {
      print('🔍 Checking facility $fid for pending bookings');
      // Only process bookings for the specific facility
      if (fid != facilityId) {
        print('🔍 Skipping facility $fid (not matching $facilityId)');
        return;
      }
      
      print('🔍 Processing pending bookings for facility $facilityId');
      dateMap.forEach((date, bookings) {
        print('🔍 Checking date $date with ${bookings.length} bookings');
        // Check if any booking on this date belongs to the current user
        bool hasUserBooking = false;
        for (final booking in bookings) {
          print('🔍 Booking email: ${booking['user_email']} vs current: $currentUserEmail');
          if (booking['user_email'] == currentUserEmail) {
            hasUserBooking = true;
            print('🔍 ✅ Found user pending booking: $date for facility $facilityId');
            break;
          }
        }
        if (hasUserBooking) {
          statuses[date] = 'pending';
          print('🔍 ✅ Added pending status for date: $date');
        } else {
          print('🔍 ❌ No user booking found for date: $date');
        }
      });
    });

    // Add approved bookings - CURRENT USER + ALL OFFICIAL BOOKINGS for specific facility
    widget.approvedBookings.forEach((fid, dateMap) {
      print('🔍 Checking facility $fid for approved bookings');
      // Only process bookings for the specific facility
      if (fid != facilityId) {
        print('🔍 Skipping facility $fid (not matching $facilityId)');
        return;
      }
      
      print('🔍 Processing approved bookings for facility $facilityId');
      dateMap.forEach((date, bookings) {
        print('🔍 Checking date $date with ${bookings.length} bookings');
        // Check if any booking on this date belongs to the current user OR is official
        bool hasUserBooking = false;
        bool hasOfficialBooking = false;
        
        for (final booking in bookings) {
          String userEmail = booking['user_email'] ?? '';
          print('🔍 Booking email: $userEmail vs current: $currentUserEmail');
          
          // Check if this is an official booking (from any user)
          if (userEmail.contains('official') || 
              userEmail.contains('barangay') ||
              userEmail.contains('admin')) {
            hasOfficialBooking = true;
            print('🔍 ✅ Found official booking: $date for facility $facilityId by: $userEmail');
          }
          // Check if this is the current user's booking
          else if (userEmail == currentUserEmail) {
            hasUserBooking = true;
            print('🔍 ✅ Found user approved booking: $date for facility $facilityId');
          }
        }
        
        // Priority: Official bookings take precedence (unavailable for all)
        if (hasOfficialBooking) {
          statuses[date] = 'official_unavailable';
          print('🔍 ✅ Added official unavailable status for date: $date');
        } else if (hasUserBooking) {
          statuses[date] = 'approved';
          print('🔍 ✅ Added approved status for date: $date');
        } else {
          print('🔍 ❌ No user or official booking found for date: $date');
        }
      });
    });

    print('🔍 Final statuses for current user on facility $facilityId: ${statuses.keys.toList()}');
    return statuses;
  }

  // Get price display with discount information
  String _getPriceDisplay(Facility facility) {
    if (widget.userData?['verified'] == true) {
      final discountRate = (widget.userData?['discount_rate'] ?? 0.0) as double;
      if (discountRate > 0) {
        final originalPrice = double.tryParse(facility.rate) ?? 0.0;
        final discountedPrice = originalPrice * (1 - discountRate);
        return '₱${discountedPrice.toStringAsFixed(2)} (${(discountRate * 100).toInt()}% off)';
      }
    }
    return '₱${facility.rate}';
  }

}

