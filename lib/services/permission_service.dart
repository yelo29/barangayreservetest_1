import 'package:flutter/material.dart';
import 'package:permission_handler/permission_handler.dart';
import 'package:shared_preferences/shared_preferences.dart';

class PermissionService {
  static const String _permissionsRequestedKey = 'permissions_requested';

  static Future<bool> _requestPermission(Permission permission) async {
    final status = await permission.request();
    return status.isGranted;
  }

  static Future<bool> _checkPermission(Permission permission) async {
    final status = await permission.status;
    return status.isGranted;
  }

  static Future<void> requestAllPermissions(BuildContext context) async {
    final prefs = await SharedPreferences.getInstance();
    final alreadyRequested = prefs.getBool(_permissionsRequestedKey) ?? false;

    if (alreadyRequested) {
      return; // Already requested permissions before
    }

    final permissions = [
      Permission.camera,
      Permission.photos,
      // Removed Permission.storage since we use Base64 encoding
    ];

    List<String> deniedPermissions = [];

    for (final permission in permissions) {
      final isGranted = await _checkPermission(permission);
      if (!isGranted) {
        final granted = await _requestPermission(permission);
        if (!granted) {
          deniedPermissions.add(_getPermissionName(permission));
        }
      }
    }

    // Mark that permissions have been requested
    await prefs.setBool(_permissionsRequestedKey, true);

    // Show dialog if any permissions were denied
    if (deniedPermissions.isNotEmpty && context.mounted) {
      _showPermissionDialog(context, deniedPermissions);
    }
  }

  static String _getPermissionName(Permission permission) {
    switch (permission) {
      case Permission.camera:
        return 'Camera';
      case Permission.photos:
        return 'Photos and Videos';
      default:
        return 'Unknown';
    }
  }

  static void _showPermissionDialog(BuildContext context, List<String> deniedPermissions) {
    showDialog(
      context: context,
      barrierDismissible: false,
      builder: (context) => AlertDialog(
        title: Row(
          children: [
            Icon(Icons.warning_amber_rounded, color: Colors.orange[600]),
            const SizedBox(width: 8),
            Expanded(
              child: Text(
                'Permission Required',
                style: const TextStyle(fontSize: 18),
                overflow: TextOverflow.ellipsis,
                maxLines: 1,
              ),
            ),
          ],
        ),
        content: Column(
          mainAxisSize: MainAxisSize.min,
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text(
              'The following permissions are required for the app to work properly:',
              style: TextStyle(fontSize: 16),
            ),
            const SizedBox(height: 12),
            ...deniedPermissions.map((permission) => Padding(
              padding: const EdgeInsets.only(bottom: 4),
              child: Row(
                children: [
                  Icon(Icons.circle, size: 8, color: Colors.red[600]),
                  const SizedBox(width: 8),
                  Text(
                    permission,
                    style: const TextStyle(fontSize: 14),
                  ),
                ],
              ),
            )),
            const SizedBox(height: 12),
            const Text(
              'Please enable these permissions in your device settings to use all features.',
              style: TextStyle(fontSize: 14, color: Colors.black87), // Changed from gray to black
            ),
          ],
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.of(context).pop(),
            child: const Text('Later'),
          ),
          ElevatedButton(
            onPressed: () {
              Navigator.of(context).pop();
              openAppSettings();
            },
            style: ElevatedButton.styleFrom(
              backgroundColor: Colors.blue,
              foregroundColor: Colors.white,
            ),
            child: const Text('Open Settings'),
          ),
        ],
      ),
    );
  }

  static Future<bool> checkAllPermissions() async {
    final permissions = [
      Permission.camera,
      Permission.photos,
      // Removed Permission.storage since we use Base64 encoding
    ];

    for (final permission in permissions) {
      final isGranted = await _checkPermission(permission);
      if (!isGranted) {
        return false;
      }
    }

    return true;
  }

  static Future<void> resetPermissionRequestFlag() async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.remove(_permissionsRequestedKey);
  }
}
