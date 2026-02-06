// SQLite-based User Model - Migrated from Firestore
// This model now uses SQLite backend instead of Firebase Firestore

class User {
  final String id;
  final String email;
  final String fullName;
  final String role;
  final bool verified;
  final double discountRate;
  final String contactNumber;
  final String address;
  final String? profilePhotoUrl;
  final DateTime createdAt;
  final DateTime? updatedAt;

  User({
    required this.id,
    required this.email,
    required this.fullName,
    required this.role,
    this.verified = false,
    this.discountRate = 0.0,
    this.contactNumber = '',
    this.address = '',
    this.profilePhotoUrl,
    required this.createdAt,
    this.updatedAt,
  });

  // Factory constructor for SQLite data
  factory User.fromMap(Map<String, dynamic> map) {
    return User(
      id: map['id']?.toString() ?? '',
      email: map['email'] ?? '',
      fullName: map['full_name'] ?? map['fullName'] ?? '',
      role: map['role'] ?? '',
      verified: map['verified'] == true || map['verified'] == 1,
      discountRate: (map['discount_rate'] ?? map['discountRate'] ?? 0.0).toDouble(),
      contactNumber: map['contact_number'] ?? map['contactNumber'] ?? '',
      address: map['address'] ?? '',
      profilePhotoUrl: map['profile_photo_url'] ?? map['profilePhotoUrl'],
      createdAt: map['created_at'] != null 
          ? (map['created_at'] is String ? DateTime.parse(map['created_at']) : map['created_at'])
          : DateTime.now(),
      updatedAt: map['updated_at'] != null 
          ? (map['updated_at'] is String ? DateTime.parse(map['updated_at']) : map['updated_at'])
          : null,
    );
  }

  // Convert to map for SQLite operations
  Map<String, dynamic> toMap() {
    return {
      'id': id,
      'email': email,
      'full_name': fullName,
      'role': role,
      'verified': verified ? 1 : 0,
      'discount_rate': discountRate,
      'contact_number': contactNumber,
      'address': address,
      'profile_photo_url': profilePhotoUrl,
      'created_at': createdAt.toIso8601String(),
      'updated_at': updatedAt?.toIso8601String(),
    };
  }

  // Helper methods
  bool get isResident => role == 'resident';
  bool get isOfficial => role == 'official';
  bool get isVerified => verified;
  
  String get displayName => fullName.isNotEmpty ? fullName : email;
  
  // Verification status helpers
  bool get isVerifiedResident => verified && role == 'resident';
  bool get isVerifiedNonResident => verified && role != 'resident';
  
  // Discount helpers
  double get discountPercentage => discountRate * 100;
  String get discountDisplay => '${discountPercentage.toInt()}%';

  @override
  String toString() {
    return 'User(id: $id, email: $email, fullName: $fullName, role: $role, verified: $verified)';
  }

  @override
  bool operator ==(Object other) {
    if (identical(this, other)) return true;
    return other is User && other.id == id;
  }

  @override
  int get hashCode => id.hashCode;
}
      'createdAt': createdAt,
      'updatedAt': updatedAt ?? Timestamp.now(),
      'lastLoginAt': lastLoginAt,
      'isActive': isActive,
      'preferences': preferences,
    };
  }

  // Create a copy with updated fields
  User copyWith({
    String? id,
    String? email,
    String? fullName,
    String? address,
    String? profileImageUrl,
    String? role,
    String? authenticationStatus,
    String? verificationType,
    double? discountPercentage,
    Timestamp? createdAt,
    Timestamp? updatedAt,
    Timestamp? lastLoginAt,
    bool? isActive,
    Map<String, dynamic>? preferences,
  }) {
    return User(
      id: id ?? this.id,
      email: email ?? this.email,
      fullName: fullName ?? this.fullName,
      address: address ?? this.address,
      profileImageUrl: profileImageUrl ?? this.profileImageUrl,
      role: role ?? this.role,
      authenticationStatus: authenticationStatus ?? this.authenticationStatus,
      verificationType: verificationType ?? this.verificationType,
      discountPercentage: discountPercentage ?? this.discountPercentage,
      createdAt: createdAt ?? this.createdAt,
      updatedAt: updatedAt ?? this.updatedAt,
      lastLoginAt: lastLoginAt ?? this.lastLoginAt,
      isActive: isActive ?? this.isActive,
      preferences: preferences ?? this.preferences,
    );
  }

  // Get display name
  String get displayName => fullName ?? email.split('@')[0];

  // Check if user is verified
  bool get isVerified => authenticationStatus == 'approved';

  // Check if user has discount
  bool get hasDiscount => discountPercentage > 0;

  // Get discount display text
  String get discountDisplayText {
    if (!hasDiscount) return 'No discount';
    return '${discountPercentage.toInt()}% discount';
  }

  // Get verification status display text
  String get verificationStatusText {
    switch (authenticationStatus) {
      case 'pending':
        return 'Verification Pending';
      case 'approved':
        return verificationType == 'resident' ? 'Verified Resident' : 'Verified Non-Resident';
      case 'rejected':
        return 'Verification Rejected';
      default:
        return 'Not Verified';
    }
  }

  // Get status color
  String get statusColor {
    switch (authenticationStatus) {
      case 'pending':
        return 'orange';
      case 'approved':
        return 'green';
      case 'rejected':
        return 'red';
      default:
        return 'grey';
    }
  }

  // Check if user can book facilities
  bool get canBook => isActive && role == 'resident';

  // Check if user is official
  bool get isOfficial => role == 'official';

  // Check if user is resident
  bool get isResident => role == 'resident';
}

class AuthenticationRequest {
  final String id;
  final String userId;
  final String fullName;
  final String address;
  final String profileImageUrl;
  final String idImageUrl;
  final String verificationType; // 'resident' or 'non-resident'
  final String status; // 'pending', 'approved', 'rejected'
  final Timestamp requestDate;
  final Timestamp? reviewDate;
  final String? reviewedBy;
  final String? rejectionReason;
  final String email;

  AuthenticationRequest({
    required this.id,
    required this.userId,
    required this.fullName,
    required this.address,
    required this.profileImageUrl,
    required this.idImageUrl,
    required this.verificationType,
    required this.status,
    required this.requestDate,
    this.reviewDate,
    this.reviewedBy,
    this.rejectionReason,
    required this.email,
  });

  // Factory constructor for creating AuthenticationRequest from Firestore document
  factory AuthenticationRequest.fromFirestore(DocumentSnapshot doc) {
    final data = doc.data() as Map<String, dynamic>;
    
    return AuthenticationRequest(
      id: doc.id,
      userId: data['userId'] ?? '',
      fullName: data['fullName'] ?? '',
      address: data['address'] ?? '',
      profileImageUrl: data['profileImageUrl'] ?? '',
      idImageUrl: data['idImageUrl'] ?? '',
      verificationType: data['verificationType'] ?? 'non-resident',
      status: data['status'] ?? 'pending',
      requestDate: data['requestDate'] ?? Timestamp.now(),
      reviewDate: data['reviewDate'],
      reviewedBy: data['reviewedBy'],
      rejectionReason: data['rejectionReason'],
      email: data['email'] ?? '',
    );
  }

  // Convert AuthenticationRequest to Map for Firestore
  Map<String, dynamic> toMap() {
    return {
      'userId': userId,
      'fullName': fullName,
      'address': address,
      'profileImageUrl': profileImageUrl,
      'idImageUrl': idImageUrl,
      'verificationType': verificationType,
      'status': status,
      'requestDate': requestDate,
      'reviewDate': reviewDate,
      'reviewedBy': reviewedBy,
      'rejectionReason': rejectionReason,
      'email': email,
    };
  }

  // Get discount percentage based on verification type
  double get discountPercentage {
    if (status != 'approved') return 0.0;
    return verificationType == 'resident' ? 10.0 : 5.0;
  }

  // Get status display text
  String get statusDisplayText {
    switch (status) {
      case 'pending':
        return 'Pending Review';
      case 'approved':
        return 'Approved';
      case 'rejected':
        return 'Rejected';
      default:
        return 'Unknown';
    }
  }

  // Get verification type display text
  String get verificationTypeDisplayText {
    switch (verificationType) {
      case 'resident':
        return 'Barangay Resident';
      case 'non-resident':
        return 'Non-Resident';
      default:
        return 'Unknown';
    }
  }
}
