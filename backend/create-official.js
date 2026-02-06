const bcrypt = require('bcryptjs');
const { v4: uuidv4 } = require('uuid');
const FirebaseService = require('./firebase-service');

async function createOfficialAccount() {
  try {
    console.log('🔧 Creating barangay official account...');
    
    const firebaseService = new FirebaseService();
    
    // Official account details
    const officialData = {
      uid: 'official-001',
      name: 'Barangay Official',
      email: 'official@barangay.gov',
      password: await bcrypt.hash('tatalaadmin01', 10),
      role: 'official',
      isAuthenticated: true,
      discount: 0.0,
      verificationType: 'official',
      createdAt: new Date().toISOString()
    };

    // Create the official user
    const result = await firebaseService.createUser(officialData);
    
    if (result.success) {
      console.log('✅ Barangay official account created successfully!');
      console.log('📧 Email: official@barangay.gov');
      console.log('🔑 Password: tatalaadmin01');
      console.log('👤 Role: official');
      console.log('✅ Authenticated: true');
      console.log('');
      console.log('🔐 You can now login with these credentials in the official login screen.');
    } else {
      console.error('❌ Failed to create official account:', result.error);
    }
    
  } catch (error) {
    console.error('❌ Error creating official account:', error);
  }
  
  process.exit(0);
}

createOfficialAccount();
