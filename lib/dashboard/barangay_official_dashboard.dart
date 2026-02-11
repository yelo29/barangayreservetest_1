import 'package:flutter/material.dart';
import 'tabs/official/official_home_tab.dart';
import 'tabs/official/official_booking_requests_tab.dart';
import 'tabs/official/authentication_requests_tab.dart';
import 'tabs/official/official_profile_tab.dart';

class BarangayOfficialDashboard extends StatefulWidget {
  final Function(BuildContext) onLogout;

  const BarangayOfficialDashboard({super.key, required this.onLogout});

  @override
  State<BarangayOfficialDashboard> createState() => _BarangayOfficialDashboardState();
}

class _BarangayOfficialDashboardState extends State<BarangayOfficialDashboard> {
  int _selectedIndex = 0;

  List<Widget> get _widgetOptions => <Widget>[
    const OfficialHomeTab(),
    const OfficialBookingRequestsTab(),
    const OfficialAuthenticationTab(userData: {}),
    OfficialProfileTab(onLogout: widget.onLogout),
  ];

  void _onItemTapped(int index) {
    setState(() {
      _selectedIndex = index;
    });
  }

  @override
  Widget build(BuildContext context) {
    return WillPopScope(
      onWillPop: () async {
        if (_selectedIndex != 0) {
          // If not on Home tab, navigate to Home tab
          setState(() {
            _selectedIndex = 0;
          });
          return false; // Prevent default back behavior
        } else {
          // If on Home tab, show logout confirmation dialog
          return await _showLogoutConfirmationDialog();
        }
      },
      child: Scaffold(
        appBar: AppBar(
          title: const Text('Barangay Official Dashboard'),
          backgroundColor: Colors.red,
          foregroundColor: Colors.white,
          automaticallyImplyLeading: false,
        ),
        body: _widgetOptions.elementAt(_selectedIndex),
        bottomNavigationBar: BottomNavigationBar(
          type: BottomNavigationBarType.fixed,
          items: const <BottomNavigationBarItem>[
            BottomNavigationBarItem(
              icon: Icon(Icons.home),
              label: 'Home',
            ),
            BottomNavigationBarItem(
              icon: Icon(Icons.pending_actions),
              label: 'Requests',
            ),
            BottomNavigationBarItem(
              icon: Icon(Icons.verified_user),
              label: 'Auth',
            ),
            BottomNavigationBarItem(
              icon: Icon(Icons.person),
              label: 'Profile',
            ),
          ],
          currentIndex: _selectedIndex,
          selectedItemColor: Colors.red,
          unselectedItemColor: Colors.grey,
          onTap: _onItemTapped,
        ),
      ),
    );
  }

  Future<bool> _showLogoutConfirmationDialog() async {
    return await showDialog<bool>(
      context: context,
      builder: (BuildContext context) {
        return AlertDialog(
          title: const Text('Confirm Logout'),
          content: const Text('Are you sure you want to logout?'),
          actions: [
            TextButton(
              onPressed: () {
                Navigator.of(context).pop(false); // Cancel
              },
              child: const Text('Cancel'),
            ),
            TextButton(
              onPressed: () {
                Navigator.of(context).pop(true); // OK
                widget.onLogout(context); // Call logout callback
              },
              child: const Text('OK'),
            ),
          ],
        );
      },
    ) ?? false; // Default to false if dialog is dismissed
  }
}
