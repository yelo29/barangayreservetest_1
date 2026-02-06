import 'package:cloud_firestore/cloud_firestore.dart';
import 'dart:io';

class Booking {
  final String id;
  final String userId;
  final String facilityId;
  final String facilityName;
  final String userName;
  final String userEmail;
  final String userPhone;
  final String date;
  final Timestamp dateTimestamp;
  final String timeslot;
  final String purpose;
  final String status; // 'pending', 'approved', 'rejected', 'cancelled'
  final double originalPrice;
  final double discountedPrice;
  final double discountPercentage;
  final double downpaymentAmount;
  final String? receiptImageUrl;
  final Timestamp createdAt;
  final Timestamp? updatedAt;
  final String? approvedBy;
  final String? rejectionReason;
  final Map<String, dynamic>? facilityDetails;

  Booking({
    required this.id,
    required this.userId,
    required this.facilityId,
    required this.facilityName,
    required this.userName,
    required this.userEmail,
    required this.userPhone,
    required this.date,
    required this.dateTimestamp,
    required this.timeslot,
    required this.purpose,
    required this.status,
    required this.originalPrice,
    required this.discountedPrice,
    required this.discountPercentage,
    required this.downpaymentAmount,
    this.receiptImageUrl,
    required this.createdAt,
    this.updatedAt,
    this.approvedBy,
    this.rejectionReason,
    this.facilityDetails,
  });

  // Factory constructor for creating Booking from Firestore document
  factory Booking.fromFirestore(DocumentSnapshot doc) {
    final data = doc.data() as Map<String, dynamic>;
    
    return Booking(
      id: doc.id,
      userId: data['userId'] ?? '',
      facilityId: data['facilityId'] ?? '',
      facilityName: data['facilityName'] ?? '',
      userName: data['userName'] ?? '',
      userEmail: data['userEmail'] ?? '',
      userPhone: data['userPhone'] ?? '',
      date: data['date'] ?? '',
      dateTimestamp: data['dateTimestamp'] ?? Timestamp.now(),
      timeslot: data['timeslot'] ?? '',
      purpose: data['purpose'] ?? '',
      status: data['status'] ?? 'pending',
      originalPrice: (data['originalPrice'] ?? 0.0).toDouble(),
      discountedPrice: (data['discountedPrice'] ?? 0.0).toDouble(),
      discountPercentage: (data['discountPercentage'] ?? 0.0).toDouble(),
      downpaymentAmount: (data['downpaymentAmount'] ?? 0.0).toDouble(),
      receiptImageUrl: data['receiptImageUrl'],
      createdAt: data['createdAt'] ?? Timestamp.now(),
      updatedAt: data['updatedAt'],
      approvedBy: data['approvedBy'],
      rejectionReason: data['rejectionReason'],
      facilityDetails: data['facilityDetails'],
    );
  }

  // Convert Booking to Map for Firestore
  Map<String, dynamic> toMap() {
    return {
      'userId': userId,
      'facilityId': facilityId,
      'facilityName': facilityName,
      'userName': userName,
      'userEmail': userEmail,
      'userPhone': userPhone,
      'date': date,
      'dateTimestamp': dateTimestamp,
      'timeslot': timeslot,
      'purpose': purpose,
      'status': status,
      'originalPrice': originalPrice,
      'discountedPrice': discountedPrice,
      'discountPercentage': discountPercentage,
      'downpaymentAmount': downpaymentAmount,
      'receiptImageUrl': receiptImageUrl,
      'createdAt': createdAt,
      'updatedAt': updatedAt ?? Timestamp.now(),
      'approvedBy': approvedBy,
      'rejectionReason': rejectionReason,
      'facilityDetails': facilityDetails,
    };
  }

  // Create a copy with updated fields
  Booking copyWith({
    String? id,
    String? userId,
    String? facilityId,
    String? facilityName,
    String? userName,
    String? userEmail,
    String? userPhone,
    String? date,
    Timestamp? dateTimestamp,
    String? timeslot,
    String? purpose,
    String? status,
    double? originalPrice,
    double? discountedPrice,
    double? discountPercentage,
    double? downpaymentAmount,
    String? receiptImageUrl,
    Timestamp? createdAt,
    Timestamp? updatedAt,
    String? approvedBy,
    String? rejectionReason,
    Map<String, dynamic>? facilityDetails,
  }) {
    return Booking(
      id: id ?? this.id,
      userId: userId ?? this.userId,
      facilityId: facilityId ?? this.facilityId,
      facilityName: facilityName ?? this.facilityName,
      userName: userName ?? this.userName,
      userEmail: userEmail ?? this.userEmail,
      userPhone: userPhone ?? this.userPhone,
      date: date ?? this.date,
      dateTimestamp: dateTimestamp ?? this.dateTimestamp,
      timeslot: timeslot ?? this.timeslot,
      purpose: purpose ?? this.purpose,
      status: status ?? this.status,
      originalPrice: originalPrice ?? this.originalPrice,
      discountedPrice: discountedPrice ?? this.discountedPrice,
      discountPercentage: discountPercentage ?? this.discountPercentage,
      downpaymentAmount: downpaymentAmount ?? this.downpaymentAmount,
      receiptImageUrl: receiptImageUrl ?? this.receiptImageUrl,
      createdAt: createdAt ?? this.createdAt,
      updatedAt: updatedAt ?? this.updatedAt,
      approvedBy: approvedBy ?? this.approvedBy,
      rejectionReason: rejectionReason ?? this.rejectionReason,
      facilityDetails: facilityDetails ?? this.facilityDetails,
    );
  }

  // Get formatted price
  String get formattedOriginalPrice => '₱${originalPrice.toStringAsFixed(2)}';
  String get formattedDiscountedPrice => '₱${discountedPrice.toStringAsFixed(2)}';
  String get formattedDownpayment => '₱${downpaymentAmount.toStringAsFixed(2)}';

  // Get savings amount
  double get savingsAmount => originalPrice - discountedPrice;
  String get formattedSavings => '₱${savingsAmount.toStringAsFixed(2)}';

  // Check if booking has discount
  bool get hasDiscount => discountPercentage > 0;

  // Get status display text
  String get statusDisplayText {
    switch (status) {
      case 'pending':
        return 'Pending Approval';
      case 'approved':
        return 'Approved';
      case 'rejected':
        return 'Rejected';
      case 'cancelled':
        return 'Cancelled';
      default:
        return 'Unknown';
    }
  }

  // Get status color
  String get statusColor {
    switch (status) {
      case 'pending':
        return 'orange';
      case 'approved':
        return 'green';
      case 'rejected':
        return 'red';
      case 'cancelled':
        return 'grey';
      default:
        return 'grey';
    }
  }

  // Check if booking can be cancelled
  bool get canBeCancelled => status == 'pending';

  // Check if booking is active
  bool get isActive => status == 'approved';

  // Check if booking is past
  bool get isPast {
    final now = DateTime.now();
    final bookingDate = bookingDateTimestamp.toDate();
    return bookingDate.isBefore(now);
  }
}

class BookingRequest {
  final String facilityId;
  final String facilityName;
  final String userName;
  final String userEmail;
  final String userPhone;
  final String date;
  final String timeslot;
  final String purpose;
  final double originalPrice;
  final double discountedPrice;
  final double discountPercentage;
  final double downpaymentAmount;
  final File? receiptImage;

  BookingRequest({
    required this.facilityId,
    required this.facilityName,
    required this.userName,
    required this.userEmail,
    required this.userPhone,
    required this.date,
    required this.timeslot,
    required this.purpose,
    required this.originalPrice,
    required this.discountedPrice,
    required this.discountPercentage,
    required this.downpaymentAmount,
    this.receiptImage,
  });

  // Convert to Booking object (for Firestore)
  Booking toBooking(String userId, String receiptImageUrl) {
    return Booking(
      id: '', // Will be set by Firestore
      userId: userId,
      facilityId: facilityId,
      facilityName: facilityName,
      userName: userName,
      userEmail: userEmail,
      userPhone: userPhone,
      date: date,
      dateTimestamp: Timestamp.now(), // Will be updated with actual date
      timeslot: timeslot,
      purpose: purpose,
      status: 'pending',
      originalPrice: originalPrice,
      discountedPrice: discountedPrice,
      discountPercentage: discountPercentage,
      downpaymentAmount: downpaymentAmount,
      receiptImageUrl: receiptImageUrl,
      createdAt: Timestamp.now(),
    );
  }
}
