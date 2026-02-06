// STUB FIREBASE SERVICE - Prevents crashes during migration
// This file prevents Firebase-related crashes while we migrate to server

class FirebaseService {
  // Stub methods to prevent crashes
  Future<void> init() async {
    // Do nothing - server-based now
  }
  
  dynamic get currentUser => null;
  dynamic get currentUserData => null;
  
  Future<Map<String, dynamic>> signInWithEmailAndPassword({
    required String email,
    required String password,
    required String role,
  }) async {
    return {'success': false, 'error': 'Use server login instead'};
  }
  
  Future<Map<String, dynamic>> signUpWithEmailAndPassword({
    required String email,
    required String password,
    required String fullName,
    required String contactNumber,
    required String address,
    required String role,
  }) async {
    return {'success': false, 'error': 'Use server registration instead'};
  }
  
  Future<List<Map<String, dynamic>>> getAllFacilities() async {
    return []; // Use server instead
  }
  
  Future<List<Map<String, dynamic>>> getPendingBookings() async {
    return []; // Use server instead
  }
  
  Future<List<Map<String, dynamic>>> getAllBookings() async {
    return []; // Use server instead
  }
  
  Future<Map<String, dynamic>> updateBookingStatus({
    required String bookingId,
    required String status,
  }) async {
    return {'success': false, 'error': 'Use server API instead'};
  }
  
  Future<Map<String, dynamic>> createBooking({
    required String facilityId,
    required String facilityName,
    required String date,
    required String timeSlot,
    required String purpose,
    required Map<String, dynamic> paymentDetails,
    required String receiptImageUrl,
  }) async {
    return {'success': false, 'error': 'Use server API instead'};
  }
  
  Future<void> signOut() async {
    // Do nothing - server handles logout
  }
  
  Future<Map<String, dynamic>> updateUserProfile(Map<String, dynamic> userData) async {
    return {'success': false, 'error': 'Use server API instead'};
  }
  
  Future<List<Map<String, dynamic>>> getAllOfficials() async {
    return []; // Use server instead
  }
  
  Future<Map<String, dynamic>> createVerificationRequest({
    required String verificationType,
    required String userPhotoUrl,
    required String validIdUrl,
  }) async {
    return {'success': false, 'error': 'Use server API instead'};
  }
}
