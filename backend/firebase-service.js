const admin = require('firebase-admin');
const serviceAccount = require('./firebase-service-account.json');

// Initialize Firebase Admin SDK
admin.initializeApp({
  credential: admin.credential.cert(serviceAccount),
  databaseURL: `https://${process.env.FIREBASE_PROJECT_ID}-default-rtdb.firebaseio.com`,
  storageBucket: `${process.env.FIREBASE_PROJECT_ID}.appspot.com`
});

const db = admin.firestore();

class FirebaseService {
  constructor() {
    this.db = db;
  }

  // User Management
  async createUser(userData) {
    try {
      const userRef = this.db.collection('users').doc(userData.uid);
      await userRef.set({
        ...userData,
        createdAt: admin.firestore.FieldValue.serverTimestamp(),
        updatedAt: admin.firestore.FieldValue.serverTimestamp()
      });
      return { success: true, uid: userData.uid };
    } catch (error) {
      console.error('Error creating user:', error);
      return { success: false, error: error.message };
    }
  }

  async getUser(uid) {
    try {
      const userDoc = await this.db.collection('users').doc(uid).get();
      if (userDoc.exists) {
        return { success: true, data: userDoc.data() };
      }
      return { success: false, error: 'User not found' };
    } catch (error) {
      console.error('Error getting user:', error);
      return { success: false, error: error.message };
    }
  }

  async getUserByEmail(email) {
    try {
      const snapshot = await this.db.collection('users').where('email', '==', email).get();
      if (snapshot.empty) {
        return { success: false, error: 'User not found' };
      }
      
      const userDoc = snapshot.docs[0];
      return { success: true, data: { uid: userDoc.id, ...userDoc.data() } };
    } catch (error) {
      console.error('Error getting user by email:', error);
      return { success: false, error: error.message };
    }
  }

  async updateUserRole(uid, role) {
    try {
      await this.db.collection('users').doc(uid).update({
        role: role,
        updatedAt: admin.firestore.FieldValue.serverTimestamp()
      });
      return { success: true };
    } catch (error) {
      console.error('Error updating user role:', error);
      return { success: false, error: error.message };
    }
  }

  async updateUserProfile(uid, userData) {
    try {
      await this.db.collection('users').doc(uid).update({
        ...userData,
        updatedAt: admin.firestore.FieldValue.serverTimestamp()
      });
      return { success: true };
    } catch (error) {
      console.error('Error updating user profile:', error);
      return { success: false, error: error.message };
    }
  }

  // Facility Management
  async createFacility(facilityData) {
    try {
      const facilityRef = this.db.collection('facilities').doc();
      await facilityRef.set({
        ...facilityData,
        id: facilityRef.id,
        createdAt: admin.firestore.FieldValue.serverTimestamp(),
        updatedAt: admin.firestore.FieldValue.serverTimestamp()
      });
      return { success: true, id: facilityRef.id };
    } catch (error) {
      console.error('Error creating facility:', error);
      return { success: false, error: error.message };
    }
  }

  async getAllFacilities() {
    try {
      const snapshot = await this.db.collection('facilities').get();
      const facilities = [];
      snapshot.forEach(doc => {
        facilities.push({ id: doc.id, ...doc.data() });
      });
      return { success: true, data: facilities };
    } catch (error) {
      console.error('Error getting facilities:', error);
      return { success: false, error: error.message };
    }
  }

  async updateFacility(facilityId, facilityData) {
    try {
      await this.db.collection('facilities').doc(facilityId).update({
        ...facilityData,
        updatedAt: admin.firestore.FieldValue.serverTimestamp()
      });
      return { success: true };
    } catch (error) {
      console.error('Error updating facility:', error);
      return { success: false, error: error.message };
    }
  }

  // Booking Management
  async createBooking(bookingData) {
    try {
      const bookingRef = this.db.collection('bookings').doc();
      await bookingRef.set({
        ...bookingData,
        id: bookingRef.id,
        createdAt: admin.firestore.FieldValue.serverTimestamp(),
        updatedAt: admin.firestore.FieldValue.serverTimestamp()
      });
      return { success: true, id: bookingRef.id };
    } catch (error) {
      console.error('Error creating booking:', error);
      return { success: false, error: error.message };
    }
  }

  async getUserBookings(userId) {
    try {
      const snapshot = await this.db.collection('bookings')
        .where('userId', '==', userId)
        .orderBy('createdAt', 'desc')
        .get();
      
      const bookings = [];
      snapshot.forEach(doc => {
        bookings.push({ id: doc.id, ...doc.data() });
      });
      return { success: true, data: bookings };
    } catch (error) {
      console.error('Error getting user bookings:', error);
      return { success: false, error: error.message };
    }
  }

  // NEW: Get User Bookings by Email
  async getUserBookingsByEmail(email) {
    try {
      console.log(`🔍 Fetching bookings for email: ${email}`);
      
      const snapshot = await this.db.collection('bookings')
        .where('email', '==', email)
        .get();
      
      const bookings = [];
      snapshot.forEach(doc => {
        bookings.push({ id: doc.id, ...doc.data() });
      });
      
      console.log(`📊 Found ${bookings.length} bookings for email: ${email}`);
      return { success: true, data: bookings };
    } catch (error) {
      console.error('Error getting user bookings by email:', error);
      return { success: false, error: error.message };
    }
  }

  async getAllPendingBookings() {
    try {
      const snapshot = await this.db.collection('bookings')
        .where('status', '==', 'pending')
        .get();
      
      const bookings = [];
      snapshot.forEach(doc => {
        bookings.push({ id: doc.id, ...doc.data() });
      });
      
      // Sort manually on client side for now
      bookings.sort((a, b) => {
        const timeA = a.createdAt?.toMillis?.() || 0;
        const timeB = b.createdAt?.toMillis?.() || 0;
        return timeB - timeA;
      });
      
      return { success: true, data: bookings };
    } catch (error) {
      console.error('Error getting all pending bookings:', error);
      return { success: false, error: error.message };
    }
  }

  async getFacilityBookings(facilityId, date) {
    try {
      const snapshot = await this.db.collection('bookings')
        .where('facilityId', '==', facilityId)
        .where('bookingDate', '==', date)
        .get();
      
      const bookings = [];
      snapshot.forEach(doc => {
        bookings.push({ id: doc.id, ...doc.data() });
      });
      return { success: true, data: bookings };
    } catch (error) {
      console.error('Error getting facility bookings:', error);
      return { success: false, error: error.message };
    }
  }

  async getFacilityBookingsInRange(facilityId, startDate, endDate) {
    try {
      console.log(`🔍 Getting bookings for facility ${facilityId} from ${startDate} to ${endDate}`);
      console.log(`🔍 Date format expected: YYYY-MM-DD`);
      
      // First, let's see ALL bookings to debug
      const allBookingsSnapshot = await this.db.collection('bookings').get();
      console.log(`🔍 DEBUG: All bookings in database:`);
      allBookingsSnapshot.forEach(doc => {
        const booking = { id: doc.id, ...doc.data() };
        console.log(`   ${booking.email} - ${booking.facilityName} - FacilityID: ${booking.facilityId} - ${booking.bookingDate} - ${booking.status}`);
      });
      
      // Get all bookings for the facility first (no date filter)
      const facilityBookingsSnapshot = await this.db.collection('bookings')
        .where('facilityId', '==', facilityId)
        .get();
      
      const bookings = [];
      facilityBookingsSnapshot.forEach(doc => {
        const booking = { id: doc.id, ...doc.data() };
        bookings.push(booking);
      });
      
      // Filter bookings by date range (handle both formats)
      const filteredBookings = bookings.filter(booking => {
        let bookingDate;
        
        // Try to parse the date (handle both formats)
        if (booking.bookingDate.includes('-')) {
          // Format: YYYY-MM-DD
          bookingDate = booking.bookingDate;
        } else {
          // Format: "Month Day, Year" - convert to YYYY-MM-DD
          try {
            const date = new Date(booking.bookingDate);
            bookingDate = date.toISOString().split('T')[0];
          } catch (e) {
            console.log(`   ❌ Cannot parse date: ${booking.bookingDate}`);
            return false;
          }
        }
        
        return bookingDate >= startDate && bookingDate <= endDate;
      });
      
      console.log(`🔍 Found ${filteredBookings.length} bookings for facility ${facilityId} in date range:`);
      filteredBookings.forEach(booking => {
        console.log(`   Raw bookingDate: "${booking.bookingDate}" (type: ${typeof booking.bookingDate})`);
        console.log(`   Formatted date: ${new Date(booking.bookingDate).toDateString()}`);
        console.log(`   Status: ${booking.status} (${booking.facilityName})`);
      });
      
      return { success: true, data: filteredBookings };
    } catch (error) {
      console.error('Error getting facility bookings in range:', error);
      return { success: false, error: error.message };
    }
  }

  async updateBookingStatus(bookingId, status, approvedBy = null) {
    try {
      const updateData = {
        status: status,
        updatedAt: admin.firestore.FieldValue.serverTimestamp()
      };
      
      if (status === 'approved') {
        updateData.approvedDate = admin.firestore.FieldValue.serverTimestamp();
        updateData.approvedBy = approvedBy;
      }
      
      await this.db.collection('bookings').doc(bookingId).update(updateData);
      return { success: true };
    } catch (error) {
      console.error('Error updating booking status:', error);
      return { success: false, error: error.message };
    }
  }

  // Authentication Requests
  async createAuthenticationRequest(requestData) {
    try {
      const requestRef = this.db.collection('authenticationRequests').doc();
      await requestRef.set({
        ...requestData,
        id: requestRef.id,
        createdAt: admin.firestore.FieldValue.serverTimestamp(),
        updatedAt: admin.firestore.FieldValue.serverTimestamp()
      });
      return { success: true, id: requestRef.id };
    } catch (error) {
      console.error('Error creating authentication request:', error);
      return { success: false, error: error.message };
    }
  }

  async getPendingAuthenticationRequests() {
    try {
      const snapshot = await this.db.collection('authenticationRequests')
        .where('status', '==', 'pending')
        .orderBy('createdAt', 'desc')
        .get();
      
      const requests = [];
      snapshot.forEach(doc => {
        requests.push({ id: doc.id, ...doc.data() });
      });
      return { success: true, data: requests };
    } catch (error) {
      console.error('Error getting authentication requests:', error);
      return { success: false, error: error.message };
    }
  }

  async updateAuthenticationRequest(requestId, status, approvedBy = null) {
    try {
      const updateData = {
        status: status,
        updatedAt: admin.firestore.FieldValue.serverTimestamp()
      };
      
      if (status === 'approved') {
        updateData.approvedDate = admin.firestore.FieldValue.serverTimestamp();
        updateData.approvedBy = approvedBy;
      }
      
      await this.db.collection('authenticationRequests').doc(requestId).update(updateData);
      
      // Update user's authentication status if approved
      if (status === 'approved') {
        const requestDoc = await this.db.collection('authenticationRequests').doc(requestId).get();
        if (requestDoc.exists) {
          const requestData = requestDoc.data();
          const discount = requestData.verificationType === 'resident' ? 10 : 5;
          
          await this.db.collection('users').doc(requestData.userId).update({
            isAuthenticated: true,
            discount: discount,
            verificationType: requestData.verificationType,
            updatedAt: admin.firestore.FieldValue.serverTimestamp()
          });
        }
      }
      
      return { success: true };
    } catch (error) {
      console.error('Error updating authentication request:', error);
      return { success: false, error: error.message };
    }
  }

  // Barangay Events
  async createBarangayEvent(eventData) {
    try {
      const eventRef = this.db.collection('barangayEvents').doc();
      await eventRef.set({
        ...eventData,
        id: eventRef.id,
        createdAt: admin.firestore.FieldValue.serverTimestamp(),
        updatedAt: admin.firestore.FieldValue.serverTimestamp()
      });
      return { success: true, id: eventRef.id };
    } catch (error) {
      console.error('Error creating barangay event:', error);
      return { success: false, error: error.message };
    }
  }

  async getBarangayEvents() {
    try {
      const snapshot = await this.db.collection('barangayEvents')
        .orderBy('eventDate', 'asc')
        .get();
      
      const events = [];
      snapshot.forEach(doc => {
        events.push({ id: doc.id, ...doc.data() });
      });
      return { success: true, data: events };
    } catch (error) {
      console.error('Error getting barangay events:', error);
      return { success: false, error: error.message };
    }
  }
}

module.exports = FirebaseService;
