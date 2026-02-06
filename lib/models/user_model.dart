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
