const bcrypt = require('bcryptjs');
const { v4: uuidv4 } = require('uuid');
const FirebaseService = require('./firebase-service');

async function createSimpleOfficialAccount() {
  try {
    console.log('🔧 Creating simple barangay official account...');
    
    const firebaseService = new FirebaseService();
    
    // Simple official account details
    const officialData = {
      uid: 'official-simple',
      name: 'Barangay Official',
      email: 'admin@barangay.gov',
      password: await bcrypt.hash('admin', 10),
      role: 'official',
      isAuthenticated: true,
      discount: 0.0,
      verificationType: 'official',
      createdAt: new Date().toISOString()
    };

    // Create the official user
    const result = await firebaseService.createUser(officialData);
    
    if (result.success) {
      console.log('✅ Simple barangay official account created successfully!');
      console.log('📧 Email: admin@barangay.gov');
      console.log('🔑 Password: admin');
      console.log('👤 Role: official');
      console.log('✅ Authenticated: true');
      console.log('');
      console.log('🔐 Much simpler! Just use: admin / admin');
    } else {
      console.error('❌ Failed to create simple official account:', result.error);
    }
    
  } catch (error) {
    console.error('❌ Error creating simple official account:', error);
  }
  
  process.exit(0);
}

createSimpleOfficialAccount();
