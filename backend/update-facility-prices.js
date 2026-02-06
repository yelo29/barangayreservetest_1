const admin = require('firebase-admin');
const serviceAccount = require('./firebase-service-account.json');

// Initialize Firebase Admin
admin.initializeApp({
  credential: admin.credential.cert(serviceAccount),
  databaseURL: 'https://barangay-reserve.firebaseio.com'
});

const db = admin.firestore();

// Facility pricing data
const facilityPrices = {
  'Community Garden': 200,
  'Meeting Room': 200,
  'Multi-Purpose Hall': 500,
  'Basketball Court': 100,
  'Covered Court': 150
};

async function updateFacilityPrices() {
  try {
    console.log('🔄 Fetching facilities...');
    const snapshot = await db.collection('facilities').get();
    
    if (snapshot.empty) {
      console.log('❌ No facilities found');
      process.exit(1);
    }

    console.log(`📍 Found ${snapshot.docs.length} facilities`);
    
    for (const doc of snapshot.docs) {
      const facility = doc.data();
      const facilityName = facility.name;
      const price = facilityPrices[facilityName];
      
      if (price !== undefined) {
        console.log(`💰 Updating ${facilityName}: Price = ₱${price}`);
        await db.collection('facilities').doc(doc.id).update({
          price: price
        });
        console.log(`✅ Updated ${facilityName}`);
      } else {
        console.log(`⚠️ No price defined for ${facilityName}`);
      }
    }

    console.log('🎉 All facilities updated with prices!');
    process.exit(0);
  } catch (error) {
    console.error('❌ Error updating facilities:', error);
    process.exit(1);
  }
}

// Run the update
updateFacilityPrices();
