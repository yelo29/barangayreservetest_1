import 'package:flutter/material.dart';
import '../dashboard/widgets/option_card.dart';
import '../services/permission_service.dart';
import 'resident_login_screen.dart';
import 'official_login_screen.dart';
import '../config/app_config.dart';

class SelectionScreen extends StatefulWidget {
  const SelectionScreen({super.key});

  @override
  State<SelectionScreen> createState() => _SelectionScreenState();
}

class _SelectionScreenState extends State<SelectionScreen> {
  @override
  void initState() {
    super.initState();
    _requestPermissions();
  }

  Future<void> _requestPermissions() async {
    // Request permissions after a short delay to allow UI to render
    Future.delayed(const Duration(milliseconds: 500), () {
      if (mounted) {
        PermissionService.requestAllPermissions(context);
      }
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Container(
        decoration: const BoxDecoration(
          gradient: LinearGradient(
            colors: [Color(0xFFDBEAFE), Color(0xFFFECACA)],
            begin: Alignment.topLeft,
            end: Alignment.bottomRight,
          ),
        ),
        child: Center(
          child: SingleChildScrollView(
            padding: const EdgeInsets.all(24),
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                // Logo
                Container(
                  height: 120,
                  width: 120,
                  decoration: BoxDecoration(
                    color: Colors.white.withAlpha(230),
                    shape: BoxShape.circle,
                    boxShadow: const [
                      BoxShadow(
                        color: Colors.black26,
                        blurRadius: 12,
                        offset: Offset(0, 6),
                      ),
                    ],
                  ),
                  child: const Center(
                    child: Text("🏛️", style: TextStyle(fontSize: 56)),
                  ),
                ),
                const SizedBox(height: 24),

                // Title
                const Text(
                  "Barangay Reserve",
                  textAlign: TextAlign.center,
                  style: TextStyle(
                    fontSize: 28,
                    fontWeight: FontWeight.w900,
                    color: Colors.black87,
                  ),
                ),
                const SizedBox(height: 12),
                const Text(
                  "Welcome to Barangay Reserve",
                  style: TextStyle(
                    color: Colors.black54,
                    fontWeight: FontWeight.w500,
                  ),
                ),
                const SizedBox(height: 32),

                // Resident option
                OptionCard(
                  title: "Resident",
                  description: "Book facilities and submit requests",
                  icon: "👤",
                  borderColor: Colors.blue,
                  onTap: () {
                    Navigator.push(
                      context,
                      MaterialPageRoute(
                        builder: (_) => const ResidentLoginScreen(),
                      ),
                    );
                  },
                ),
                const SizedBox(height: 20),

                // Official option
                OptionCard(
                  title: "Barangay Official",
                  description: "Manage bookings and approve requests",
                  icon: "👨‍💼",
                  borderColor: Colors.red,
                  onTap: () {
                    Navigator.push(
                      context,
                      MaterialPageRoute(
                        builder: (_) => const OfficialLoginScreen(),
                      ),
                    );
                  },
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}
