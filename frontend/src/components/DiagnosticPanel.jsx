import React, { useState, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { useNotification } from '../contexts/NotificationContext';
import { motion } from 'framer-motion';

const DiagnosticPanel = () => {
  const { user } = useAuth();
  const { showNotification } = useNotification();
  const [results, setResults] = useState({});
  const [isRunning, setIsRunning] = useState(false);

  const runTest = async (testName, testFunction) => {
    try {
      setResults(prev => ({ ...prev, [testName]: { status: 'running', result: null } }));
      const result = await testFunction();
      setResults(prev => ({ ...prev, [testName]: { status: 'success', result } }));
      return result;
    } catch (error) {
      setResults(prev => ({ ...prev, [testName]: { status: 'error', result: error.message } }));
      throw error;
    }
  };

  const testBackendConnection = async () => {
    console.log('Testing backend connection...');
    const response = await fetch('/api/health', {
      method: 'GET',
      headers: { 'Content-Type': 'application/json' }
    });
    
    if (!response.ok) {
      throw new Error(`Backend connection failed: ${response.status}`);
    }
    
    const data = await response.json();
    return `Backend healthy: ${data.message}`;
  };

  const testAuthentication = async () => {
    console.log('Testing authentication...');
    const token = localStorage.getItem('authToken');
    
    if (!token) {
      throw new Error('No auth token found');
    }
    
    const response = await fetch('/auth/user', {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    });
    
    if (!response.ok) {
      throw new Error(`Auth check failed: ${response.status}`);
    }
    
    const data = await response.json();
    return `User authenticated: ${data.user.email}`;
  };

  const testRantSubmission = async () => {
    console.log('Testing rant submission...');
    const token = localStorage.getItem('authToken');
    
    if (!token) {
      throw new Error('No auth token for rant submission');
    }
    
    const testRant = {
      content: 'This is a diagnostic test rant to check if submission works properly.',
      transformation_type: 'poem',
      tone: 'neutral',
      privacy: 'private',
      input_type: 'text'
    };
    
    const response = await fetch('/api/rant/submit', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(testRant)
    });
    
    if (!response.ok) {
      const errorText = await response.text();
      throw new Error(`Rant submission failed: ${response.status} - ${errorText}`);
    }
    
    const data = await response.json();
    return `Rant submitted successfully: ID ${data.rant_id}`;
  };

  const testAudioUpload = async () => {
    console.log('Testing audio upload...');
    const token = localStorage.getItem('authToken');
    
    if (!token) {
      throw new Error('No auth token for audio upload');
    }
    
    // Create a simple audio blob for testing
    const audioContext = new (window.AudioContext || window.webkitAudioContext)();
    const buffer = audioContext.createBuffer(1, 44100, 44100);
    const audioData = buffer.getChannelData(0);
    
    // Generate a simple sine wave
    for (let i = 0; i < 44100; i++) {
      audioData[i] = Math.sin(2 * Math.PI * 440 * i / 44100) * 0.3;
    }
    
    // Convert to blob
    const audioBlob = new Blob([audioData], { type: 'audio/wav' });
    
    const formData = new FormData();
    formData.append('audio', audioBlob, 'test-audio.wav');
    
    const response = await fetch('/api/media/upload-audio', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`
      },
      body: formData
    });
    
    if (!response.ok) {
      const errorText = await response.text();
      throw new Error(`Audio upload failed: ${response.status} - ${errorText}`);
    }
    
    const audioResult = await response.json();
    return `Audio uploaded successfully: ${audioResult.message}`;
  };

  const testImageUpload = async () => {
    console.log('Testing image upload...');
    const token = localStorage.getItem('authToken');
    
    if (!token) {
      throw new Error('No auth token for image upload');
    }
    
    // Create a simple 1x1 pixel image
    const canvas = document.createElement('canvas');
    canvas.width = 1;
    canvas.height = 1;
    const ctx = canvas.getContext('2d');
    ctx.fillStyle = '#FF0000';
    ctx.fillRect(0, 0, 1, 1);
    
    const imageBlob = await new Promise(resolve => {
      canvas.toBlob(resolve, 'image/jpeg', 0.9);
    });
    
    const formData = new FormData();
    formData.append('image', imageBlob, 'test-image.jpg');
    
    const response = await fetch('/api/media/upload-image', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`
      },
      body: formData
    });
    
    if (!response.ok) {
      const errorText = await response.text();
      throw new Error(`Image upload failed: ${response.status} - ${errorText}`);
    }
    
    const imageResult = await response.json();
    return `Image uploaded successfully: ${imageResult.message}`;
  };

  const runAllTests = async () => {
    setIsRunning(true);
    setResults({});
    
    try {
      await runTest('Backend Connection', testBackendConnection);
      await runTest('Authentication', testAuthentication);
      await runTest('Rant Submission', testRantSubmission);
      await runTest('Audio Upload', testAudioUpload);
      await runTest('Image Upload', testImageUpload);
      
      showNotification('All diagnostic tests completed! 🎉', 'success');
    } catch (error) {
      showNotification(`Diagnostic test failed: ${error.message}`, 'error');
    } finally {
      setIsRunning(false);
    }
  };

  const getStatusIcon = (status) => {
    switch (status) {
      case 'running': return '🔄';
      case 'success': return '✅';
      case 'error': return '❌';
      default: return '⏳';
    }
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'running': return 'text-yellow-400';
      case 'success': return 'text-green-400';
      case 'error': return 'text-red-400';
      default: return 'text-gray-400';
    }
  };

  if (!user) {
    return (
      <div className="bg-red-900/20 border border-red-500/50 rounded-lg p-6 text-center">
        <h2 className="text-xl font-bold text-red-400 mb-2">Authentication Required</h2>
        <p className="text-red-300">Please log in to run diagnostic tests.</p>
      </div>
    );
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="bg-gray-900/50 backdrop-blur-sm border border-gray-700/50 rounded-lg p-6 max-w-4xl mx-auto"
    >
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-2xl font-bold text-white">🔧 Diagnostic Panel</h2>
        <button
          onClick={runAllTests}
          disabled={isRunning}
          className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:bg-gray-600 disabled:cursor-not-allowed transition-colors"
        >
          {isRunning ? 'Running Tests...' : 'Run All Tests'}
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {Object.entries(results).map(([testName, testResult]) => (
          <motion.div
            key={testName}
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            className="bg-gray-800/50 border border-gray-600/50 rounded-lg p-4"
          >
            <div className="flex items-center justify-between mb-2">
              <h3 className="font-semibold text-white">{testName}</h3>
              <span className="text-2xl">{getStatusIcon(testResult.status)}</span>
            </div>
            <div className={`text-sm ${getStatusColor(testResult.status)}`}>
              {testResult.status === 'running' 
                ? 'Running...' 
                : testResult.result || 'Waiting to run...'}
            </div>
          </motion.div>
        ))}
      </div>

      <div className="mt-6 p-4 bg-blue-900/20 border border-blue-500/50 rounded-lg">
        <h3 className="font-semibold text-blue-400 mb-2">How to Use:</h3>
        <ul className="text-sm text-blue-300 space-y-1">
          <li>• Click "Run All Tests" to check all features</li>
          <li>• Green checkmarks indicate working features</li>
          <li>• Red X marks indicate issues that need fixing</li>
          <li>• Check the browser console for detailed error logs</li>
        </ul>
      </div>
    </motion.div>
  );
};

export default DiagnosticPanel;
