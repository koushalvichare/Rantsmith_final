// Debug script for frontend
console.log('=== Frontend Debug Info ===');
console.log('Current token:', localStorage.getItem('authToken'));
console.log('API Base URL:', 'http://localhost:5000');

// Test if we can reach the backend
fetch('http://localhost:5000/health')
  .then(response => response.json())
  .then(data => console.log('Health check:', data))
  .catch(error => console.error('Health check failed:', error));

// Test login
const testLogin = async () => {
  try {
    const response = await fetch('http://localhost:5000/auth/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        email: 'chat@example.com',
        password: 'password123'
      })
    });
    
    const data = await response.json();
    console.log('Test login result:', data);
    
    if (data.token) {
      localStorage.setItem('authToken', data.token);
      console.log('Token saved to localStorage');
      
      // Test AI chat with this token
      const chatResponse = await fetch('http://localhost:5000/api/ai/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${data.token}`
        },
        body: JSON.stringify({
          message: 'Hello from debug script!'
        })
      });
      
      const chatData = await chatResponse.json();
      console.log('Test AI chat result:', chatData);
    }
  } catch (error) {
    console.error('Test login failed:', error);
  }
};

// Run the test
testLogin();
