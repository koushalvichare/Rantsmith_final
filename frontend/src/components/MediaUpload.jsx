import React, { useState, useRef } from 'react';
import { useNotification } from '../contexts/NotificationContext';
import { motion } from 'framer-motion';

const MediaUpload = ({ onMediaProcessed }) => {
  const [isRecording, setIsRecording] = useState(false);
  const [audioBlob, setAudioBlob] = useState(null);
  const [selectedImage, setSelectedImage] = useState(null);
  const [processing, setProcessing] = useState(false);
  const [recordingTime, setRecordingTime] = useState(0);
  
  const mediaRecorderRef = useRef(null);
  const audioChunksRef = useRef([]);
  const timerRef = useRef(null);
  const fileInputRef = useRef(null);
  const { showNotification } = useNotification();

  // Start audio recording
  const startRecording = async () => {
    try {
      console.log('Attempting to start recording...');
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      console.log('Got media stream:', stream);
      
      const mediaRecorder = new MediaRecorder(stream);
      mediaRecorderRef.current = mediaRecorder;
      audioChunksRef.current = [];

      mediaRecorder.ondataavailable = (event) => {
        console.log('Data available:', event.data.size);
        if (event.data.size > 0) {
          audioChunksRef.current.push(event.data);
        }
      };

      mediaRecorder.onstop = () => {
        console.log('Recording stopped, creating blob...');
        const audioBlob = new Blob(audioChunksRef.current, { type: 'audio/wav' });
        console.log('Audio blob created:', audioBlob, 'Size:', audioBlob.size);
        setAudioBlob(audioBlob);
        stream.getTracks().forEach(track => track.stop());
      };

      mediaRecorder.start();
      setIsRecording(true);
      setRecordingTime(0);
      
      // Start timer
      timerRef.current = setInterval(() => {
        setRecordingTime(prev => prev + 1);
      }, 1000);

      showNotification('Recording started! 🎤', 'success');
    } catch (error) {
      console.error('Error starting recording:', error);
      showNotification('Error accessing microphone. Please check permissions.', 'error');
    }
  };

  // Stop audio recording
  const stopRecording = () => {
    if (mediaRecorderRef.current && isRecording) {
      mediaRecorderRef.current.stop();
      setIsRecording(false);
      clearInterval(timerRef.current);
      showNotification('Recording stopped! 🎵', 'success');
    }
  };

  // Upload audio file
  const uploadAudio = async () => {
    if (!audioBlob) {
      console.log('No audio blob available');
      showNotification('No audio recording to upload', 'error');
      return;
    }

    console.log('Starting audio upload...');
    console.log('Audio blob size:', audioBlob.size);
    setProcessing(true);
    const formData = new FormData();
    formData.append('audio', audioBlob, 'recording.wav');

    try {
      const token = localStorage.getItem('authToken');
      console.log('Auth token:', token ? `present (${token.length} chars)` : 'missing');
      
      // Try relative URL first (for proxy), then absolute URL as fallback
      const urls = ['/api/media/upload-audio', 'http://127.0.0.1:5000/api/media/upload-audio'];
      let response;
      let lastError;
      
      for (const url of urls) {
        try {
          console.log(`Trying URL: ${url}`);
          response = await fetch(url, {
            method: 'POST',
            body: formData,
            headers: {
              'Authorization': `Bearer ${token}`
            }
          });
          
          console.log(`Response status: ${response.status} for URL: ${url}`);
          
          if (response.ok) {
            console.log(`Success with URL: ${url}`);
            break;
          } else {
            const errorText = await response.text();
            console.log(`Failed with URL: ${url}, status: ${response.status}, error: ${errorText}`);
            lastError = new Error(`HTTP ${response.status}: ${errorText}`);
          }
        } catch (error) {
          console.log(`Error with URL: ${url}`, error);
          lastError = error;
        }
      }
      
      if (!response || !response.ok) {
        throw lastError || new Error('All upload attempts failed');
      }

      const data = await response.json();
      console.log('Upload successful:', data);
      showNotification('Audio processed successfully! 🎉', 'success');
      
      if (onMediaProcessed) {
        onMediaProcessed({
          type: 'audio',
          text: data.text,
          rantId: data.rant_id
        });
      }
      
      setAudioBlob(null);
      setRecordingTime(0);
    } catch (error) {
      console.error('Error uploading audio:', error);
      showNotification(`Error processing audio: ${error.message}`, 'error');
    } finally {
      setProcessing(false);
    }
  };

  // Handle image selection
  const handleImageSelect = (event) => {
    const file = event.target.files[0];
    if (file && file.type.startsWith('image/')) {
      setSelectedImage(file);
      showNotification('Image selected! 📸', 'success');
    } else {
      showNotification('Please select a valid image file.', 'error');
    }
  };

  // Upload image file
  const uploadImage = async () => {
    if (!selectedImage) return;

    console.log('Starting image upload...');
    setProcessing(true);
    const formData = new FormData();
    formData.append('image', selectedImage);

    try {
      const token = localStorage.getItem('authToken');
      console.log('Auth token:', token ? 'present' : 'missing');
      
      // Try relative URL first (for proxy), then absolute URL as fallback
      const urls = ['/api/media/upload-image', 'http://127.0.0.1:5000/api/media/upload-image'];
      let response;
      let lastError;
      
      for (const url of urls) {
        try {
          console.log(`Trying URL: ${url}`);
          response = await fetch(url, {
            method: 'POST',
            body: formData,
            headers: {
              'Authorization': `Bearer ${token}`
            }
          });
          
          if (response.ok) {
            console.log(`Success with URL: ${url}`);
            break;
          } else {
            console.log(`Failed with URL: ${url}, status: ${response.status}`);
            lastError = new Error(`HTTP ${response.status}: ${response.statusText}`);
          }
        } catch (error) {
          console.log(`Error with URL: ${url}`, error);
          lastError = error;
        }
      }
      
      if (!response || !response.ok) {
        throw lastError || new Error('All upload attempts failed');
      }

      const data = await response.json();
      console.log('Upload successful:', data);
      showNotification('Image processed successfully! 🎨', 'success');
      
      if (onMediaProcessed) {
        onMediaProcessed({
          type: 'image',
          imageData: data.image_data,
          metadata: data.metadata
        });
      }
      
      setSelectedImage(null);
      if (fileInputRef.current) {
        fileInputRef.current.value = '';
      }
    } catch (error) {
      console.error('Error uploading image:', error);
      showNotification(`Error processing image: ${error.message}`, 'error');
    } finally {
      setProcessing(false);
    }
  };

  // Format time display
  const formatTime = (seconds) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  return (
    <div className="bg-white/5 backdrop-blur-lg rounded-2xl p-6 border border-white/10 relative" style={{ zIndex: 10 }}>
      <h3 className="text-xl font-bold text-white mb-4">
        <i className="fas fa-microphone-alt mr-2"></i>
        Audio & Image Upload
      </h3>
      
      {/* Audio Recording Section */}
      <div className="mb-6">
        <h4 className="text-lg font-semibold text-gray-300 mb-3">
          <i className="fas fa-record-vinyl mr-2"></i>
          Record Audio
        </h4>
        
        <div className="flex items-center space-x-4 mb-4">
          {!isRecording ? (
            <motion.button
              onClick={startRecording}
              disabled={processing}
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              className="bg-red-600 hover:bg-red-700 text-white px-6 py-3 rounded-lg font-semibold transition-all duration-200 flex items-center space-x-2 cursor-pointer"
            >
              <i className="fas fa-microphone"></i>
              <span>Start Recording</span>
            </motion.button>
          ) : (
            <motion.button
              onClick={stopRecording}
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              className="bg-gray-600 hover:bg-gray-700 text-white px-6 py-3 rounded-lg font-semibold transition-all duration-200 flex items-center space-x-2 cursor-pointer"
            >
              <i className="fas fa-stop"></i>
              <span>Stop Recording</span>
            </motion.button>
          )}
          
          {isRecording && (
            <div className="flex items-center space-x-2 text-red-400">
              <div className="w-3 h-3 bg-red-500 rounded-full animate-pulse"></div>
              <span className="font-mono text-lg">{formatTime(recordingTime)}</span>
            </div>
          )}
        </div>
        
        {audioBlob && (
          <div className="bg-white/10 rounded-lg p-4 mb-4">
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-2">
                <i className="fas fa-file-audio text-green-400"></i>
                <span className="text-gray-300">Recording ready ({formatTime(recordingTime)})</span>
              </div>
              <motion.button
                onClick={uploadAudio}
                disabled={processing}
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                className="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded-lg font-semibold transition-all duration-200 flex items-center space-x-2 cursor-pointer"
              >
                {processing ? (
                  <>
                    <i className="fas fa-spinner fa-spin"></i>
                    <span>Processing...</span>
                  </>
                ) : (
                  <>
                    <i className="fas fa-upload"></i>
                    <span>Upload</span>
                  </>
                )}
              </motion.button>
            </div>
            
            <audio controls className="w-full mt-2">
              <source src={URL.createObjectURL(audioBlob)} type="audio/wav" />
              Your browser does not support the audio element.
            </audio>
          </div>
        )}
      </div>
      
      {/* Image Upload Section */}
      <div>
        <h4 className="text-lg font-semibold text-gray-300 mb-3">
          <i className="fas fa-image mr-2"></i>
          Upload Image
        </h4>
        
        <div className="flex items-center space-x-4 mb-4">
          <input
            ref={fileInputRef}
            type="file"
            accept="image/*"
            onChange={handleImageSelect}
            className="hidden"
          />
          
          <motion.button
            onClick={() => fileInputRef.current?.click()}
            disabled={processing}
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            className="bg-purple-600 hover:bg-purple-700 text-white px-6 py-3 rounded-lg font-semibold transition-all duration-200 flex items-center space-x-2 cursor-pointer"
          >
            <i className="fas fa-file-image"></i>
            <span>Select Image</span>
          </motion.button>
        </div>
        
        {selectedImage && (
          <div className="bg-white/10 rounded-lg p-4">
            <div className="flex items-center justify-between mb-2">
              <div className="flex items-center space-x-2">
                <i className="fas fa-image text-blue-400"></i>
                <span className="text-gray-300">{selectedImage.name}</span>
              </div>
              <motion.button
                onClick={uploadImage}
                disabled={processing}
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg font-semibold transition-all duration-200 flex items-center space-x-2 cursor-pointer"
              >
                {processing ? (
                  <>
                    <i className="fas fa-spinner fa-spin"></i>
                    <span>Processing...</span>
                  </>
                ) : (
                  <>
                    <i className="fas fa-upload"></i>
                    <span>Upload</span>
                  </>
                )}
              </motion.button>
            </div>
            
            <div className="mt-2">
              <img
                src={URL.createObjectURL(selectedImage)}
                alt="Preview"
                className="max-w-full max-h-48 rounded-lg object-cover"
              />
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default MediaUpload;
