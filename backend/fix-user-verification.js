const FirebaseService = require('./firebase-service');

async function fixUserVerification() {
  try {
    console.log('🔧 Fixing user verification status...');
    
    const firebaseService = new FirebaseService();
    
    // Update saloestillopez@gmail.com to be verified non-resident
    const userEmail = 'saloestillopez@gmail.com';
    
    // First, get the user by email
    const userResult = await firebaseService.getUserByEmail(userEmail);
    
    if (!userResult.success) {
      console.log('❌ User not found:', userEmail);
      return;
    }
    
    const user = userResult.data;
    console.log('🔍 Found user:', user.email, 'Current verified:', user.verified);
    
    // Update user to be verified non-resident
    const updateData = {
      verified: true,
      verificationType: 'non-resident',
      discountRate: 0.05, // 5% discount
      updatedAt: new Date()
    };
    
    const updateResult = await firebaseService.updateUserProfile(user.uid, updateData);
    
    if (updateResult.success) {
      console.log('✅ User verification updated successfully!');
      console.log('📧 Email:', userEmail);
      console.log('✅ Verified:', true);
      console.log('🏷️  Type: non-resident');
      console.log('💰 Discount: 5%');
    } else {
      console.log('❌ Failed to update user:', updateResult.error);
    }
    
  } catch (error) {
    console.error('❌ Error fixing user verification:', error);
  }
}

// Run the fix
fixUserVerification().then(() => {
  console.log('🎯 User verification fix completed');
  process.exit(0);
}).catch((error) => {
  console.error('❌ Fatal error:', error);
  process.exit(1);
});
