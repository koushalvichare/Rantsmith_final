#!/usr/bin/env node

// Quick test script to verify authentication
const API_BASE = 'http://localhost:3001/api';

async function testAuth() {
  console.log('🧪 Testing Authentication Flow...');
  console.log('=' .repeat(50));

  // Test 1: Test registration
  try {
    const testUser = {
      username: `testuser_${Date.now()}`,
      email: `test_${Date.now()}@example.com`,
      password: 'testpassword123'
    };

    console.log('📝 Testing Registration...');
    const registerResponse = await fetch(`${API_BASE}/auth/register`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(testUser)
    });

    if (registerResponse.ok) {
      const registerData = await registerResponse.json();
      console.log('✅ Registration successful!');
      console.log('Token received:', registerData.token ? 'Yes' : 'No');
      
      // Test 2: Test login with same credentials
      console.log('\n🔑 Testing Login...');
      const loginResponse = await fetch(`${API_BASE}/auth/login`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          email: testUser.email,
          password: testUser.password
        })
      });

      if (loginResponse.ok) {
        const loginData = await loginResponse.json();
        console.log('✅ Login successful!');
        console.log('Token received:', loginData.token ? 'Yes' : 'No');
      } else {
        const loginError = await loginResponse.text();
        console.log('❌ Login failed:', loginError);
      }

    } else {
      const registerError = await registerResponse.text();
      console.log('❌ Registration failed:', registerError);
    }

  } catch (error) {
    console.error('💥 Test failed:', error.message);
  }

  console.log('\n' + '=' .repeat(50));
  console.log('🏁 Authentication test complete!');
}

// Run if called directly
if (require.main === module) {
  testAuth();
}

module.exports = { testAuth };
