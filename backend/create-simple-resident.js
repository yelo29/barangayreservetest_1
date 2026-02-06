const bcrypt = require('bcryptjs');
const { v4: uuidv4 } = require('uuid');
const FirebaseService = require('./firebase-service');

async function createSimpleResidentAccount() {
  try {
    console.log('🔧 Creating simple barangay resident account...');
    
    const firebaseService = new FirebaseService();
    
    // Simple resident account details
    const residentData = {
      uid: 'resident-simple',
      name: 'John Resident',
      email: 'resident@barangay.gov',
      password: await bcrypt.hash('resident', 10),
      role: 'resident',
      isAuthenticated: true,
      discount: 10.0,
      verificationType: 'resident',
      createdAt: new Date().toISOString()
    };

    // Create the resident user
    const result = await firebaseService.createUser(residentData);
    
    if (result.success) {
      console.log('✅ Simple barangay resident account created successfully!');
      console.log('📧 Email: resident@barangay.gov');
      console.log('🔑 Password: resident');
      console.log('👤 Role: resident');
      console.log('✅ Authenticated: true');
      console.log('💰 Discount: 10%');
      console.log('');
      console.log('🔐 Much simpler! Just use: resident / resident');
    } else {
      console.error('❌ Failed to create simple resident account:', result.error);
    }
    
  } catch (error) {
    console.error('❌ Error creating simple resident account:', error);
  }
  
  process.exit(0);
}

createSimpleResidentAccount();
