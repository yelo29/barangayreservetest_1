const FirebaseService = require('./firebase-service');

async function createSampleBookings() {
  try {
    console.log('🔧 Creating sample bookings...');
    
    const firebaseService = new FirebaseService();
    
    // Sample bookings data
    const sampleBookings = [
      {
        uid: 'booking-1',
        facilityId: 'fFKKz9NhfoLbjuEaVQLh', // Basketball Court
        facilityName: 'Basketball Court',
        userEmail: 'resident@barangay.gov',
        userName: 'John Resident',
        date: '2026-02-15',
        timeSlot: '08:00-10:00',
        status: 'approved',
        totalPrice: 100,
        downpayment: 50,
        paymentStatus: 'paid',
        createdAt: new Date().toISOString(),
        updatedAt: new Date().toISOString()
      },
      {
        uid: 'booking-2',
        facilityId: 'KPmWdb2EzuF88VOngosS', // Multi-Purpose Hall
        facilityName: 'Multi-Purpose Hall',
        userEmail: 'resident@barangay.gov',
        userName: 'John Resident',
        date: '2026-02-16',
        timeSlot: '14:00-16:00',
        status: 'pending',
        totalPrice: 500,
        downpayment: 250,
        paymentStatus: 'pending',
        createdAt: new Date().toISOString(),
        updatedAt: new Date().toISOString()
      },
      {
        uid: 'booking-3',
        facilityId: 'BwCsuPV7OXF69FknGSpK', // Meeting Room
        facilityName: 'Meeting Room',
        userEmail: 'admin@barangay.gov',
        userName: 'Barangay Official',
        date: '2026-02-14',
        timeSlot: '10:00-12:00',
        status: 'approved',
        totalPrice: 200,
        downpayment: 100,
        paymentStatus: 'paid',
        isOfficial: true,
        createdAt: new Date().toISOString(),
        updatedAt: new Date().toISOString()
      }
    ];
    
    // Create each booking
    for (const booking of sampleBookings) {
      const result = await firebaseService.createBooking(booking);
      if (result.success) {
        console.log(`✅ Created booking: ${booking.facilityName} on ${booking.date}`);
      } else {
        console.error(`❌ Failed to create booking:`, result.error);
      }
    }
    
    console.log('\n🎉 Sample bookings created successfully!');
    console.log('📊 Created 3 sample bookings with different statuses');
    
  } catch (error) {
    console.error('❌ Error creating sample bookings:', error);
  }
  
  process.exit(0);
}

createSampleBookings();
