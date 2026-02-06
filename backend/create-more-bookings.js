const FirebaseService = require('./firebase-service');

async function createMoreBookings() {
  try {
    console.log('🔧 Creating more sample bookings...');
    
    const firebaseService = new FirebaseService();
    
    const moreBookings = [
      {
        uid: 'booking-4',
        facilityId: 'shoFOwE6Z1vRNXkldvzB', // Covered Court
        facilityName: 'Covered Court',
        userEmail: 'juan@barangay.gov',
        userName: 'Juan Santos',
        date: '2026-02-20',
        timeSlot: '16:00-18:00',
        status: 'pending',
        totalPrice: 150,
        downpayment: 75,
        paymentStatus: 'pending',
        createdAt: new Date().toISOString(),
        updatedAt: new Date().toISOString()
      },
      {
        uid: 'booking-5',
        facilityId: 'BwCsuPV7OXF69FknGSpK', // Meeting Room
        facilityName: 'Meeting Room',
        userEmail: 'maria@barangay.gov',
        userName: 'Maria Reyes',
        date: '2026-02-21',
        timeSlot: '09:00-11:00',
        status: 'approved',
        totalPrice: 200,
        downpayment: 100,
        paymentStatus: 'paid',
        createdAt: new Date().toISOString(),
        updatedAt: new Date().toISOString()
      },
      {
        uid: 'booking-6',
        facilityId: 'KPmWdb2EzuF88VOngosS', // Multi-Purpose Hall
        facilityName: 'Multi-Purpose Hall',
        userEmail: 'admin@barangay.gov',
        userName: 'Barangay Official',
        date: '2026-02-22',
        timeSlot: '13:00-17:00',
        status: 'approved',
        totalPrice: 500,
        downpayment: 250,
        paymentStatus: 'paid',
        isOfficial: true,
        createdAt: new Date().toISOString(),
        updatedAt: new Date().toISOString()
      },
      {
        uid: 'booking-7',
        facilityId: 'fFKKz9NhfoLbjuEaVQLh', // Basketball Court
        facilityName: 'Basketball Court',
        userEmail: 'carlos@barangay.gov',
        userName: 'Carlos Garcia',
        date: '2026-02-23',
        timeSlot: '10:00-12:00',
        status: 'pending',
        totalPrice: 100,
        downpayment: 50,
        paymentStatus: 'pending',
        createdAt: new Date().toISOString(),
        updatedAt: new Date().toISOString()
      },
      {
        uid: 'booking-8',
        facilityId: '1eEEcuXhEMX69DbvtsYo', // Community Garden
        facilityName: 'Community Garden',
        userEmail: 'ana@barangay.gov',
        userName: 'Ana Martinez',
        date: '2026-02-24',
        timeSlot: '08:00-10:00',
        status: 'approved',
        totalPrice: 50,
        downpayment: 25,
        paymentStatus: 'paid',
        isOfficial: true,
        createdAt: new Date().toISOString(),
        updatedAt: new Date().toISOString()
      }
    ];
    
    // Create each booking
    for (const booking of moreBookings) {
      const result = await firebaseService.createBooking(booking);
      if (result.success) {
        console.log(`✅ Created booking: ${booking.facilityName} on ${booking.date} for ${booking.userName}`);
      } else {
        console.error(`❌ Failed to create booking:`, result.error);
      }
    }
    
    console.log('\n🎉 More bookings created successfully!');
    console.log('📊 Created 5 additional bookings');
    
  } catch (error) {
    console.error('❌ Error creating more bookings:', error);
  }
  
  process.exit(0);
}

createMoreBookings();
