const axios = require('axios');

const API_BASE = 'http://localhost:3000/api';

async function setupFacilities() {
  try {
    // First, login to get token
    console.log('🔐 Logging in as admin...');
    const loginResponse = await axios.post(`${API_BASE}/auth/login`, {
      email: 'admin@barangay.test',
      password: 'admin123'
    });

    const token = loginResponse.data.token;
    console.log('✅ Login successful!');

    // Facilities to create
    const facilities = [
      {
        name: "Basketball Court",
        description: "Full-size basketball court with lighting",
        capacity: "20",
        rate: "100",
        downpayment: "50",
        amenities: "Basketball hoops, lights, benches",
        icon: "https://via.placeholder.com/300x200/4CAF50/FFFFFF?text=Basketball+Court"
      },
      {
        name: "Multipurpose Hall",
        description: "Large hall for events and meetings",
        capacity: "100",
        rate: "500",
        downpayment: "200",
        amenities: "Tables, chairs, sound system, projector",
        icon: "https://via.placeholder.com/300x200/2196F3/FFFFFF?text=Multipurpose+Hall"
      },
      {
        name: "Covered Court",
        description: "Covered court for various sports",
        capacity: "50",
        rate: "150",
        downpayment: "75",
        amenities: "Covered area, lighting, benches",
        icon: "https://via.placeholder.com/300x200/FF9800/FFFFFF?text=Covered+Court"
      },
      {
        name: "Meeting Room",
        description: "Air-conditioned meeting room with projector",
        capacity: "30",
        rate: "200",
        downpayment: "100",
        amenities: "Air conditioning, projector, whiteboard, tables",
        icon: "https://via.placeholder.com/300x200/9C27B0/FFFFFF?text=Meeting+Room"
      }
    ];

    // Create each facility
    console.log('🏗️ Creating facilities...');
    for (const facility of facilities) {
      try {
        const response = await axios.post(`${API_BASE}/facilities`, facility, {
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          }
        });
        console.log(`✅ Created: ${facility.name}`);
      } catch (error) {
        console.error(`❌ Failed to create ${facility.name}:`, error.response?.data || error.message);
      }
    }

    console.log('🎉 Facility setup complete!');
    
    // Verify facilities
    console.log('📋 Verifying facilities...');
    const facilitiesResponse = await axios.get(`${API_BASE}/facilities`);
    console.log(`✅ Found ${facilitiesResponse.data.data.length} facilities in database`);

  } catch (error) {
    console.error('❌ Setup failed:', error.response?.data || error.message);
    
    if (error.response?.status === 401) {
      console.log('\n💡 Tip: Make sure the admin account exists first.');
      console.log('Run: curl -X POST http://localhost:3000/api/auth/register -H "Content-Type: application/json" -d \'{"name":"Admin User","email":"admin@barangay.test","password":"admin123","role":"official"}\'');
    }
  }
}

// Run the setup
setupFacilities();
