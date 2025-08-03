import React, { useState } from 'react';
import { useNotification } from '../contexts/NotificationContext';

const SimpleMediaUpload = () => {
  const [processing, setProcessing] = useState(false);
  const { showNotification } = useNotification();

  const testButton = () => {
    console.log('Simple test button clicked!');
    alert('Simple test button works!');
    showNotification('Simple test button clicked!', 'success');
  };

  const testAudioUpload = async () => {
    console.log('Testing simple audio upload...');
    setProcessing(true);
    
    try {
      const token = localStorage.getItem('authToken');
      const testBlob = new Blob(['test audio data'], { type: 'audio/wav' });
      const formData = new FormData();
      formData.append('audio', testBlob, 'test.wav');
      
      const response = await fetch('http://localhost:5000/api/media/upload-audio', {
        method: 'POST',
        body: formData,
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      
      if (response.ok) {
        const data = await response.json();
        console.log('Upload successful:', data);
        showNotification('Audio upload successful!', 'success');
      } else {
        console.error('Upload failed:', response.status);
        showNotification('Audio upload failed!', 'error');
      }
    } catch (error) {
      console.error('Upload error:', error);
      showNotification('Upload error: ' + error.message, 'error');
    } finally {
      setProcessing(false);
    }
  };

  return (
    <div style={{ 
      position: 'fixed', 
      top: '100px', 
      left: '20px', 
      zIndex: 9999, 
      backgroundColor: '#333', 
      padding: '20px', 
      borderRadius: '10px',
      color: 'white' 
    }}>
      <h3>Simple Media Upload Test</h3>
      <div style={{ marginBottom: '10px' }}>
        <button 
          onClick={testButton}
          style={{
            backgroundColor: '#4CAF50',
            color: 'white',
            padding: '10px 20px',
            border: 'none',
            borderRadius: '5px',
            cursor: 'pointer',
            marginRight: '10px'
          }}
        >
          Test Button
        </button>
        
        <button 
          onClick={testAudioUpload}
          disabled={processing}
          style={{
            backgroundColor: processing ? '#666' : '#2196F3',
            color: 'white',
            padding: '10px 20px',
            border: 'none',
            borderRadius: '5px',
            cursor: processing ? 'not-allowed' : 'pointer'
          }}
        >
          {processing ? 'Processing...' : 'Test Audio Upload'}
        </button>
      </div>
    </div>
  );
};

export default SimpleMediaUpload;
