import 'package:flutter/material.dart';
import 'tabs/resident_home_tab.dart';
import 'tabs/resident_bookings_tab.dart';
import 'tabs/resident_profile_tab.dart';

class ResidentDashboard extends StatefulWidget {
  final Function(BuildContext) onLogout; // Callback for logging out
  final Map<String, dynamic>? userData; // User data from server

  const ResidentDashboard({super.key, required this.onLogout, this.userData});

  @override
  State<ResidentDashboard> createState() => _ResidentDashboardState();
}

class _ResidentDashboardState extends State<ResidentDashboard> {
  int _currentIndex = 0;
  final PageController _pageController = PageController();
  
  @override
  void initState() {
    super.initState();
  }

  @override
  Widget build(BuildContext context) {
    final List<Widget> pages = [
      ResidentHomeTab(userData: widget.userData),
      ResidentBookingsTab(userData: widget.userData),
      ResidentProfileTab(
        userData: widget.userData,
        onLogout: widget.onLogout,
      ), 
    ];

    return WillPopScope(
      onWillPop: () async {
        if (_currentIndex != 0) {
          // If not on Home tab, navigate to Home tab
          setState(() {
            _currentIndex = 0;
            _pageController.jumpToPage(0);
          });
          return false; // Prevent default back behavior
        } else {
          // If on Home tab, show logout confirmation dialog
          return await _showLogoutConfirmationDialog();
        }
      },
      child: Scaffold(
        appBar: AppBar(
          title: const Text("Resident Page"),
          automaticallyImplyLeading: false,
          elevation: 1,
          backgroundColor: Colors.blue,
          foregroundColor: Colors.white,
        ),
        body: PageView(
          controller: _pageController,
          onPageChanged: (index) {
            setState(() {
              _currentIndex = index;
            });
          },
          children: pages,
        ),
        bottomNavigationBar: BottomNavigationBar(
          currentIndex: _currentIndex,
          selectedItemColor: Colors.blue,
          unselectedItemColor: Colors.grey,
          onTap: (index) {
            _pageController.jumpToPage(index);
          },
          items: const [
            BottomNavigationBarItem(
              icon: Icon(Icons.home),
              label: 'Home',
            ),
            BottomNavigationBarItem(
              icon: Icon(Icons.list_alt),
              label: 'My Bookings',
            ),
            BottomNavigationBarItem(
              icon: Icon(Icons.person),
              label: 'Profile',
            ),
          ],
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
