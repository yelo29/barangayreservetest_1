const FirebaseService = require('./firebase-service');

async function createFacilitiesWithIcons() {
  try {
    console.log('🏗️ Creating facilities with proper icons...');
    
    const firebaseService = new FirebaseService();
    
    // Facilities with proper Material Design icons
    const facilities = [
      {
        name: 'Basketball Court',
        icon: 'sports_basketball',
        rate: '50',
        description: 'Full-size basketball court with proper lighting',
        capacity: '20',
        downpayment: '25',
        amenities: 'Basketball hoops, lighting, benches',
        active: true
      },
      {
        name: 'Multi-Purpose Hall',
        icon: 'event_seat',
        rate: '100',
        description: 'Spacious hall for events and meetings',
        capacity: '100',
        downpayment: '50',
        amenities: 'Tables, chairs, sound system, air conditioning',
        active: true
      },
      {
        name: 'Covered Court',
        icon: 'sports_volleyball',
        rate: '75',
        description: 'Covered court for various sports activities',
        capacity: '50',
        downpayment: '35',
        amenities: 'Volleyball net, badminton setup, lighting',
        active: true
      },
      {
        name: 'Meeting Room',
        icon: 'meeting_room',
        rate: '30',
        description: 'Air-conditioned meeting room with projector',
        capacity: '15',
        downpayment: '15',
        amenities: 'Projector, whiteboard, air conditioning, tables',
        active: true
      },
      {
        name: 'Community Garden',
        icon: 'park',
        rate: '20',
        description: 'Open garden space for community events',
        capacity: '30',
        downpayment: '10',
        amenities: 'Garden benches, shaded areas, water access',
        active: true
      }
    ];

    // Clear existing facilities
    console.log('🗑️ Clearing existing facilities...');
    const existingSnapshot = await firebaseService.db.collection('facilities').get();
    const batch = firebaseService.db.batch();
    
    existingSnapshot.docs.forEach(doc => {
      batch.delete(doc.ref);
    });
    
    await batch.commit();
    console.log('✅ Cleared existing facilities');

    // Add new facilities with icons
    for (const facility of facilities) {
      const result = await firebaseService.createFacility(facility);
      if (result.success) {
        console.log(`✅ Created facility: ${facility.name} with icon: ${facility.icon}`);
      } else {
        console.error(`❌ Failed to create facility ${facility.name}:`, result.error);
      }
    }

    console.log('\n🎉 Facilities with icons created successfully!');
    console.log('📱 The app will now show proper Material Design icons instead of placeholder images');
    
  } catch (error) {
    console.error('❌ Error creating facilities:', error);
  }
  
  process.exit(0);
}

createFacilitiesWithIcons();
