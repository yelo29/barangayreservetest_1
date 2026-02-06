const axios = require('axios');

const API_BASE_URL = 'http://192.168.100.4:3000/api';

async function testAuthentication() {
  console.log('🧪 Testing Authentication System...\n');

  try {
    // Test 1: Register a new user
    console.log('1️⃣ Testing Registration...');
    const testUser = {
      name: 'Test Resident',
      email: 'test.resident@gmail.com',
      password: 'password123',
      role: 'resident'
    };

    try {
      const registerResponse = await axios.post(`${API_BASE_URL}/auth/register`, testUser);
      console.log('✅ Registration successful');
      console.log(`   User: ${registerResponse.data.user.name}`);
      console.log(`   Email: ${registerResponse.data.user.email}`);
      console.log(`   Token: ${registerResponse.data.token.substring(0, 20)}...\n`);
    } catch (error) {
      if (error.response?.status === 400 && error.response?.data?.error === 'User already exists') {
        console.log('ℹ️ User already exists, proceeding to login test...\n');
      } else {
        console.log('❌ Registration failed:');
        console.log(`   Status: ${error.response?.status}`);
        console.log(`   Error: ${error.response?.data?.error || error.message}\n`);
        return;
      }
    }

    // Test 2: Login with the user
    console.log('2️⃣ Testing Login...');
    try {
      const loginResponse = await axios.post(`${API_BASE_URL}/auth/login`, {
        email: testUser.email,
        password: testUser.password
      });
      
      console.log('✅ Login successful');
      console.log(`   User: ${loginResponse.data.user.name}`);
      console.log(`   Email: ${loginResponse.data.user.email}`);
      console.log(`   Role: ${loginResponse.data.user.role}`);
      console.log(`   Token: ${loginResponse.data.token.substring(0, 20)}...\n`);
    } catch (error) {
      console.log('❌ Login failed:');
      console.log(`   Status: ${error.response?.status}`);
      console.log(`   Error: ${error.response?.data?.error || error.message}\n`);
      return;
    }

    // Test 3: Test with wrong password
    console.log('3️⃣ Testing Login with wrong password...');
    try {
      await axios.post(`${API_BASE_URL}/auth/login`, {
        email: testUser.email,
        password: 'wrongpassword'
      });
      console.log('❌ Should have failed with wrong password');
    } catch (error) {
      if (error.response?.status === 401) {
        console.log('✅ Correctly rejected wrong password');
      } else {
        console.log('❌ Unexpected error:', error.response?.data?.error || error.message);
      }
    }

    console.log('\n🎉 Authentication test completed!');

  } catch (error) {
    console.error('❌ Test failed:', error.message);
  }
}

// Run the test
testAuthentication().then(() => {
  process.exit(0);
});
