const bcrypt = require('bcryptjs');
const { v4: uuidv4 } = require('uuid');
const FirebaseService = require('./firebase-service');

async function createSampleUsers() {
  try {
    console.log('🔧 Creating sample users...');
    
    const firebaseService = new FirebaseService();
    
    const sampleUsers = [
      {
        uid: 'resident-juan',
        name: 'Juan Santos',
        email: 'juan@barangay.gov',
        password: await bcrypt.hash('juan123', 10),
        role: 'resident',
        isAuthenticated: true,
        discount: 10.0,
        verificationType: 'resident',
        createdAt: new Date().toISOString()
      },
      {
        uid: 'resident-maria',
        name: 'Maria Reyes',
        email: 'maria@barangay.gov',
        password: await bcrypt.hash('maria123', 10),
        role: 'resident',
        isAuthenticated: true,
        discount: 5.0,
        verificationType: 'resident',
        createdAt: new Date().toISOString()
      },
      {
        uid: 'resident-carlos',
        name: 'Carlos Garcia',
        email: 'carlos@barangay.gov',
        password: await bcrypt.hash('carlos123', 10),
        role: 'resident',
        isAuthenticated: false,
        discount: 0.0,
        verificationType: 'unverified',
        createdAt: new Date().toISOString()
      },
      {
        uid: 'official-2',
        name: 'Ana Martinez',
        email: 'ana@barangay.gov',
        password: await bcrypt.hash('official123', 10),
        role: 'official',
        isAuthenticated: true,
        discount: 0.0,
        verificationType: 'official',
        createdAt: new Date().toISOString()
      }
    ];
    
    // Create each user
    for (const user of sampleUsers) {
      const result = await firebaseService.createUser(user);
      if (result.success) {
        console.log(`✅ Created user: ${user.name} (${user.email})`);
      } else {
        console.error(`❌ Failed to create user: ${user.email}`, result.error);
      }
    }
    
    console.log('\n🎉 Sample users created successfully!');
    console.log('📊 Created 4 additional users');
    
  } catch (error) {
    console.error('❌ Error creating sample users:', error);
  }
  
  process.exit(0);
}

createSampleUsers();
