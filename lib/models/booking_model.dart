// SQLite-based Booking Model - Migrated from Firestore
// This model now uses SQLite backend instead of Firebase Firestore

import 'dart:io';

class Booking {
  final String id;
  final String facilityId;
  final String userEmail;
  final String date;
  final String timeslot;
  final String purpose;
  final String status; // 'pending', 'approved', 'rejected'
  final String? paymentDetails;
  final String? receiptBase64;
  final String contactNumber;
  final String address;
  final DateTime createdAt;
  final DateTime? updatedAt;
  final String? facilityName;
  final String? userName;
  final bool? userVerified;
  final double? userDiscountRate;
  final double? totalAmount;
  final double? downpayment;

  Booking({
    required this.id,
    required this.facilityId,
    required this.userEmail,
    required this.date,
    required this.timeslot,
    required this.purpose,
    this.status = 'pending',
    this.paymentDetails,
    this.receiptBase64,
    this.contactNumber = '',
    this.address = '',
    required this.createdAt,
    this.updatedAt,
    this.facilityName,
    this.userName,
    this.userVerified,
    this.userDiscountRate,
    this.totalAmount,
    this.downpayment,
  });

  // Factory constructor for SQLite data
  factory Booking.fromMap(Map<String, dynamic> map) {
    return Booking(
      id: map['id']?.toString() ?? '',
      facilityId: map['facility_id']?.toString() ?? '',
      userEmail: map['user_email'] ?? '',
      date: map['date'] ?? '',
      timeslot: map['timeslot'] ?? '',
      purpose: map['purpose'] ?? '',
      status: map['status'] ?? 'pending',
      paymentDetails: map['payment_details'],
      receiptBase64: map['receipt_base64'],
      contactNumber: map['contact_number'] ?? '',
      address: map['address'] ?? '',
      createdAt: map['created_at'] != null 
          ? (map['created_at'] is String ? DateTime.parse(map['created_at']) : map['created_at'])
          : DateTime.now(),
      updatedAt: map['updated_at'] != null 
          ? (map['updated_at'] is String ? DateTime.parse(map['updated_at']) : map['updated_at'])
          : null,
      facilityName: map['facility_name'],
      userName: map['user_name'],
      userVerified: map['verified'] == true || map['verified'] == 1,
      userDiscountRate: (map['discount_rate'] ?? map['userDiscountRate'] ?? 0.0).toDouble(),
      totalAmount: (map['total_amount'] ?? 0.0).toDouble(),
      downpayment: (map['downpayment'] ?? 0.0).toDouble(),
    );
  }

  // Convert to map for SQLite operations
  Map<String, dynamic> toMap() {
    return {
      'id': id,
      'facility_id': facilityId,
      'user_email': userEmail,
      'date': date,
      'timeslot': timeslot,
      'purpose': purpose,
      'status': status,
      'payment_details': paymentDetails,
      'receipt_base64': receiptBase64,
      'contact_number': contactNumber,
      'address': address,
      'created_at': createdAt.toIso8601String(),
      'updated_at': updatedAt?.toIso8601String(),
    };
  }

  // Helper methods
  bool get isPending => status == 'pending';
  bool get isApproved => status == 'approved';
  bool get isRejected => status == 'rejected';
  
  String get statusDisplay {
    switch (status) {
      case 'pending':
        return 'Pending';
      case 'approved':
        return 'Approved';
      case 'rejected':
        return 'Rejected';
      default:
        return status;
    }
  }

  // Discount calculation helper
  double get discountedAmount {
    if (totalAmount == null || userDiscountRate == null) return 0.0;
    return totalAmount! * (1 - userDiscountRate!);
  }

  @override
  String toString() {
    return 'Booking(id: $id, facility: $facilityId, user: $userEmail, status: $status)';
  }

  @override
  bool operator ==(Object other) {
    if (identical(this, other)) return true;
    return other is Booking && other.id == id;
  }

  @override
  int get hashCode => id.hashCode;
}
