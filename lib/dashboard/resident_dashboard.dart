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

    return Scaffold(
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
    );
  }
}
