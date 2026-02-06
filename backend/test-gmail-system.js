const FirebaseService = require('./firebase-service');

async function testGmailBasedSystem() {
  console.log('🧪 Testing Gmail-based booking system...\n');

  try {
    // Initialize Firebase service
    const firebaseService = new FirebaseService();

    // Test 1: Create a test booking with Gmail
    console.log('1️⃣ Creating test booking with Gmail...');
    const testBooking = {
      userId: 'test_user_123',
      email: 'test.user@gmail.com', // Gmail field
      facilityId: 'facility_1',
      facilityName: 'Basketball Court',
      bookingDate: '2026-01-29',
      timeslot: '09:00-10:00',
      fullName: 'Test User',
      contactNumber: '1234567890',
      address: 'Test Address',
      receiptImageURL: '',
      status: 'pending',
      submittedDate: new Date().toISOString(),
    };

    const createResult = await firebaseService.createBooking(testBooking);
    if (createResult.success) {
      console.log('✅ Test booking created with Gmail');
      console.log(`   Booking ID: ${createResult.id}`);
      console.log(`   Email: ${testBooking.email}\n`);
    } else {
      console.log('❌ Failed to create test booking');
      console.log(`   Error: ${createResult.error}\n`);
      return;
    }

    // Test 2: Fetch bookings by Gmail
    console.log('2️⃣ Fetching bookings by Gmail...');
    const fetchResult = await firebaseService.getUserBookingsByEmail('test.user@gmail.com');
    
    if (fetchResult.success) {
      console.log('✅ Successfully fetched bookings by Gmail');
      console.log(`   Found ${fetchResult.data.length} bookings`);
      fetchResult.data.forEach((booking, index) => {
        console.log(`   ${index + 1}. ${booking.facilityName} - ${booking.bookingDate} - ${booking.email}`);
      });
    } else {
      console.log('❌ Failed to fetch bookings by Gmail');
      console.log(`   Error: ${fetchResult.error}`);
    }

    console.log('\n🎉 Gmail-based system test completed!');

  } catch (error) {
    console.error('❌ Test failed:', error);
  }
}

// Run the test
testGmailBasedSystem().then(() => {
  process.exit(0);
});
