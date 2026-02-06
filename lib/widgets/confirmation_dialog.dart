import 'package:flutter/material.dart';

class ConfirmationDialog extends StatelessWidget {
  final String title;
  final String message;
  final String? confirmText;
  final String? cancelText;
  final VoidCallback? onConfirm;
  final VoidCallback? onCancel;
  final Color? confirmColor;
  final Color? cancelColor;
  final IconData? icon;
  final Color? iconColor;

  const ConfirmationDialog({
    super.key,
    required this.title,
    required this.message,
    this.confirmText,
    this.cancelText,
    this.onConfirm,
    this.onCancel,
    this.confirmColor,
    this.cancelColor,
    this.icon,
    this.iconColor,
  });

  @override
  Widget build(BuildContext context) {
    return AlertDialog(
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(16),
      ),
      title: Row(
        children: [
          if (icon != null) ...[
            Icon(
              icon,
              color: iconColor ?? Theme.of(context).primaryColor,
              size: 24,
            ),
            const SizedBox(width: 12),
          ],
          Expanded(
            child: Text(
              title,
              style: const TextStyle(
                fontSize: 20,
                fontWeight: FontWeight.bold,
              ),
            ),
          ),
        ],
      ),
      content: Text(
        message,
        style: TextStyle(
          fontSize: 16,
          color: Colors.grey.shade700,
        ),
      ),
      actions: [
        TextButton(
          onPressed: onCancel ?? () => Navigator.pop(context, false),
          style: TextButton.styleFrom(
            foregroundColor: cancelColor ?? Colors.grey.shade600,
            padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 12),
          ),
          child: Text(
            cancelText ?? 'Cancel',
            style: const TextStyle(fontSize: 16),
          ),
        ),
        ElevatedButton(
          onPressed: onConfirm ?? () => Navigator.pop(context, true),
          style: ElevatedButton.styleFrom(
            backgroundColor: confirmColor ?? Colors.red,
            foregroundColor: Colors.white,
            padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 12),
            shape: RoundedRectangleBorder(
              borderRadius: BorderRadius.circular(8),
            ),
          ),
          child: Text(
            confirmText ?? 'Confirm',
            style: const TextStyle(fontSize: 16, fontWeight: FontWeight.w500),
          ),
        ),
      ],
    );
  }

  // Static methods for common confirmation dialogs
  static Future<bool?> showDeleteConfirmation(
    BuildContext context, {
    String itemName = 'item',
    VoidCallback? onConfirm,
  }) {
    return showDialog<bool>(
      context: context,
      builder: (context) => ConfirmationDialog(
        title: 'Delete $itemName',
        message: 'Are you sure you want to delete this $itemName? This action cannot be undone.',
        confirmText: 'Delete',
        cancelText: 'Cancel',
        onConfirm: onConfirm,
        confirmColor: Colors.red,
        icon: Icons.delete,
        iconColor: Colors.red,
      ),
    );
  }

  static Future<bool?> showCancelBookingConfirmation(
    BuildContext context, {
    String facilityName = 'facility',
    String bookingDate = 'date',
    VoidCallback? onConfirm,
  }) {
    return showDialog<bool>(
      context: context,
      builder: (context) => ConfirmationDialog(
        title: 'Cancel Booking',
        message: 'Are you sure you want to cancel your booking for $facilityName on $bookingDate?',
        confirmText: 'Cancel Booking',
        cancelText: 'Keep Booking',
        onConfirm: onConfirm,
        confirmColor: Colors.orange,
        icon: Icons.cancel,
        iconColor: Colors.orange,
      ),
    );
  }

  static Future<bool?> showRejectBookingConfirmation(
    BuildContext context, {
    String userName = 'user',
    String facilityName = 'facility',
    String bookingDate = 'date',
    VoidCallback? onConfirm,
  }) {
    return showDialog<bool>(
      context: context,
      builder: (context) => ConfirmationDialog(
        title: 'Reject Booking Request',
        message: 'Are you sure you want to reject $userName\'s booking request for $facilityName on $bookingDate?',
        confirmText: 'Reject',
        cancelText: 'Review Again',
        onConfirm: onConfirm,
        confirmColor: Colors.red,
        icon: Icons.block,
        iconColor: Colors.red,
      ),
    );
  }

  static Future<bool?> showLogoutConfirmation(
    BuildContext context, {
    VoidCallback? onConfirm,
  }) {
    return showDialog<bool>(
      context: context,
      builder: (context) => ConfirmationDialog(
        title: 'Logout',
        message: 'Are you sure you want to logout?',
        confirmText: 'Logout',
        cancelText: 'Stay Logged In',
        onConfirm: onConfirm,
        confirmColor: Colors.blue,
        icon: Icons.logout,
        iconColor: Colors.blue,
      ),
    );
  }

  static Future<bool?> showDiscardChangesConfirmation(
    BuildContext context, {
    VoidCallback? onConfirm,
  }) {
    return showDialog<bool>(
      context: context,
      builder: (context) => ConfirmationDialog(
        title: 'Discard Changes',
        message: 'Are you sure you want to discard your changes? Any unsaved data will be lost.',
        confirmText: 'Discard',
        cancelText: 'Keep Editing',
        onConfirm: onConfirm,
        confirmColor: Colors.orange,
        icon: Icons.warning,
        iconColor: Colors.orange,
      ),
    );
  }

  static Future<bool?> showApproveBookingConfirmation(
    BuildContext context, {
    String userName = 'user',
    String facilityName = 'facility',
    String bookingDate = 'date',
    VoidCallback? onConfirm,
  }) {
    return showDialog<bool>(
      context: context,
      builder: (context) => ConfirmationDialog(
        title: 'Approve Booking Request',
        message: 'Are you sure you want to approve $userName\'s booking request for $facilityName on $bookingDate?',
        confirmText: 'Approve',
        cancelText: 'Review Again',
        onConfirm: onConfirm,
        confirmColor: Colors.green,
        icon: Icons.check_circle,
        iconColor: Colors.green,
      ),
    );
  }
}

class InfoDialog extends StatelessWidget {
  final String title;
  final String message;
  final String? buttonText;
  final IconData? icon;
  final Color? iconColor;

  const InfoDialog({
    super.key,
    required this.title,
    required this.message,
    this.buttonText,
    this.icon,
    this.iconColor,
  });

  @override
  Widget build(BuildContext context) {
    return AlertDialog(
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(16),
      ),
      title: Row(
        children: [
          if (icon != null) ...[
            Icon(
              icon,
              color: iconColor ?? Theme.of(context).primaryColor,
              size: 24,
            ),
            const SizedBox(width: 12),
          ],
          Expanded(
            child: Text(
              title,
              style: const TextStyle(
                fontSize: 20,
                fontWeight: FontWeight.bold,
              ),
            ),
          ),
        ],
      ),
      content: Text(
        message,
        style: TextStyle(
          fontSize: 16,
          color: Colors.grey.shade700,
        ),
      ),
      actions: [
        ElevatedButton(
          onPressed: () => Navigator.pop(context),
          style: ElevatedButton.styleFrom(
            backgroundColor: Theme.of(context).primaryColor,
            foregroundColor: Colors.white,
            padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 12),
            shape: RoundedRectangleBorder(
              borderRadius: BorderRadius.circular(8),
            ),
          ),
          child: Text(
            buttonText ?? 'OK',
            style: const TextStyle(fontSize: 16, fontWeight: FontWeight.w500),
          ),
        ),
      ],
    );
  }

  // Static methods for common info dialogs
  static Future<void> showSuccessInfo(
    BuildContext context, {
    required String title,
    required String message,
  }) {
    return showDialog(
      context: context,
      builder: (context) => InfoDialog(
        title: title,
        message: message,
        icon: Icons.check_circle,
        iconColor: Colors.green,
      ),
    );
  }

  static Future<void> showErrorInfo(
    BuildContext context, {
    required String title,
    required String message,
  }) {
    return showDialog(
      context: context,
      builder: (context) => InfoDialog(
        title: title,
        message: message,
        icon: Icons.error,
        iconColor: Colors.red,
      ),
    );
  }

  static Future<void> showWarningInfo(
    BuildContext context, {
    required String title,
    required String message,
  }) {
    return showDialog(
      context: context,
      builder: (context) => InfoDialog(
        title: title,
        message: message,
        icon: Icons.warning,
        iconColor: Colors.orange,
      ),
    );
  }

  static Future<void> showInfo(
    BuildContext context, {
    required String title,
    required String message,
  }) {
    return showDialog(
      context: context,
      builder: (context) => InfoDialog(
        title: title,
        message: message,
        icon: Icons.info,
        iconColor: Colors.blue,
      ),
    );
  }
}
