const FirebaseService = require('./firebase-service');

async function createAuthRequests() {
  try {
    console.log('🔧 Creating authentication requests...');
    
    const firebaseService = new FirebaseService();
    
    const authRequests = [
      {
        uid: 'auth-req-1',
        name: 'Pedro Cruz',
        email: 'pedro@gmail.com',
        phone: '09123456789',
        address: '123 Main St, Barangay Sample',
        idPhoto: 'https://example.com/id1.jpg',
        verificationType: 'resident',
        status: 'pending',
        requestedAt: new Date().toISOString(),
        createdAt: new Date().toISOString()
      },
      {
        uid: 'auth-req-2',
        name: 'Rosa Lim',
        email: 'rosa@gmail.com',
        phone: '09198765432',
        address: '456 Oak St, Barangay Sample',
        idPhoto: 'https://example.com/id2.jpg',
        verificationType: 'non-resident',
        status: 'pending',
        requestedAt: new Date().toISOString(),
        createdAt: new Date().toISOString()
      },
      {
        uid: 'auth-req-3',
        name: 'Jose Santos',
        email: 'jose@gmail.com',
        phone: '09156789012',
        address: '789 Pine St, Barangay Sample',
        idPhoto: 'https://example.com/id3.jpg',
        verificationType: 'resident',
        status: 'pending',
        requestedAt: new Date().toISOString(),
        createdAt: new Date().toISOString()
      }
    ];
    
    // Create each auth request
    for (const authReq of authRequests) {
      const result = await firebaseService.createAuthenticationRequest(authReq);
      if (result.success) {
        console.log(`✅ Created auth request: ${authReq.name} (${authReq.email})`);
      } else {
        console.error(`❌ Failed to create auth request: ${authReq.email}`, result.error);
      }
    }
    
    console.log('\n🎉 Authentication requests created successfully!');
    console.log('📊 Created 3 authentication requests');
    
  } catch (error) {
    console.error('❌ Error creating authentication requests:', error);
  }
  
  process.exit(0);
}

createAuthRequests();
