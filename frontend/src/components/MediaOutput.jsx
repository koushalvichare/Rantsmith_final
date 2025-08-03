import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { useNotification } from '../contexts/NotificationContext';

const MediaOutput = ({ rantId, transformedContent }) => {
  const [generating, setGenerating] = useState({});
  const { showNotification } = useNotification();

  // Check if transformedContent is multimedia object or just text
  const isMultimediaContent = transformedContent && typeof transformedContent === 'object' && transformedContent.text;
  const textContent = isMultimediaContent ? transformedContent.text : transformedContent;
  const audioContent = isMultimediaContent ? transformedContent.audio : null;
  const imageContent = isMultimediaContent ? transformedContent.image : null;
  const videoContent = isMultimediaContent ? transformedContent.video : null;

  const copyToClipboard = (text) => {
    navigator.clipboard.writeText(text).then(() => {
      showNotification('Copied to clipboard! 📋', 'success');
    });
  };

  const downloadMedia = (mediaData, filename, type) => {
    try {
      const link = document.createElement('a');
      link.href = mediaData;
      link.download = filename;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      showNotification(`${type} downloaded successfully! 📥`, 'success');
    } catch (error) {
      showNotification('Error downloading file.', 'error');
    }
  };

  const renderVideoContent = (videoData) => {
    try {
      // Check if it's our professional video format
      if (videoData.startsWith('data:application/json;base64,')) {
        const jsonData = atob(videoData.split(',')[1]);
        const videoInfo = JSON.parse(jsonData);
        
        // Handle RunwayML processing status
        if (videoInfo.status === 'processing') {
          return (
            <div className="text-center">
              <div className="mb-4">
                <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-white mx-auto mb-4"></div>
                <h4 className="text-lg font-semibold text-white mb-2">🎬 Professional Video Processing</h4>
                <p className="text-gray-300">Your video is being generated using RunwayML's AI...</p>
                <p className="text-sm text-gray-400">Job ID: {videoInfo.job_id}</p>
              </div>
            </div>
          );
        }
        
        // Handle cinematic sequence format
        if (videoInfo.type === 'cinematic_sequence' && videoInfo.frames) {
          return (
            <div className="text-center">
              <div className="mb-4">
                <h4 className="text-lg font-semibold text-white mb-2">🎬 Professional Cinematic Video</h4>
                <div className="bg-black/50 rounded-lg p-4 inline-block">
                  <div className="grid grid-cols-5 gap-2 max-w-2xl">
                    {videoInfo.frames.slice(0, 15).map((frame, index) => (
                      <div key={index} className="relative">
                        <img
                          src={`data:image/png;base64,${frame}`}
                          alt={`Frame ${index + 1}`}
                          className="w-full h-auto rounded border border-white/20 transition-transform hover:scale-110"
                        />
                        <div className="absolute bottom-0 left-0 bg-black/70 text-white text-xs px-1 rounded-tr">
                          {index + 1}
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
              <div className="bg-white/10 rounded-lg p-3 inline-block">
                <p className="text-gray-300 text-sm">
                  <span className="font-semibold text-white">Quality:</span> {videoInfo.quality || 'Full HD'} |{' '}
                  <span className="font-semibold text-white">Duration:</span> {videoInfo.duration}s |{' '}
                  <span className="font-semibold text-white">FPS:</span> {videoInfo.fps} |{' '}
                  <span className="font-semibold text-white">Frames:</span> {videoInfo.frames.length}
                </p>
                <p className="text-xs text-gray-400 mt-1">
                  Resolution: {videoInfo.width}x{videoInfo.height}
                </p>
              </div>
            </div>
          );
        }
        
        // Handle other JSON formats
        return (
          <div className="text-center text-gray-300">
            <p>📊 Video data processed</p>
            <pre className="text-xs bg-black/30 rounded p-2 mt-2 text-left overflow-auto max-h-32">
              {JSON.stringify(videoInfo, null, 2)}
            </pre>
          </div>
        );
      }
      
      // Standard video handling
      return (
        <video controls className="w-full max-w-2xl mx-auto rounded-lg" src={videoData}>
          Your browser does not support the video element.
        </video>
      );
    } catch (error) {
      return (
        <div className="text-center text-gray-400">
          <p>🎬 Video preview not available</p>
          <p className="text-sm">{error.message}</p>
        </div>
      );
    }
  };

  if (!transformedContent) {
    return null;
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="bg-white/5 backdrop-blur-lg rounded-2xl p-6 border border-white/10"
    >
      <h3 className="text-2xl font-bold text-white mb-6 flex items-center">
        <i className="fas fa-magic mr-2 text-purple-400"></i>
        Transformed Content
      </h3>

      {/* Text Content */}
      {textContent && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className="mb-6"
        >
          <div className="bg-white/10 rounded-lg p-4 border border-white/10">
            <div className="flex items-center justify-between mb-3">
              <h4 className="text-lg font-semibold text-white flex items-center">
                <i className="fas fa-file-text mr-2 text-blue-400"></i>
                Text Content
              </h4>
              <button
                onClick={() => copyToClipboard(textContent)}
                className="px-3 py-1 bg-blue-600 hover:bg-blue-700 text-white rounded-lg text-sm transition-colors"
              >
                <i className="fas fa-copy mr-1"></i>
                Copy
              </button>
            </div>
            <div className="bg-black/20 rounded p-4 text-gray-300 whitespace-pre-wrap font-mono text-sm">
              {textContent}
            </div>
          </div>
        </motion.div>
      )}

      {/* Audio Content */}
      {audioContent && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className="mb-6"
        >
          <div className="bg-white/10 rounded-lg p-4 border border-white/10">
            <div className="flex items-center justify-between mb-3">
              <h4 className="text-lg font-semibold text-white flex items-center">
                <i className="fas fa-volume-up mr-2 text-green-400"></i>
                Audio Output
              </h4>
              <button
                onClick={() => downloadMedia(audioContent, 'rant-audio.mp3', 'Audio')}
                className="px-3 py-1 bg-green-600 hover:bg-green-700 text-white rounded-lg text-sm transition-colors"
              >
                <i className="fas fa-download mr-1"></i>
                Download
              </button>
            </div>
            <audio controls className="w-full" src={audioContent}>
              Your browser does not support the audio element.
            </audio>
          </div>
        </motion.div>
      )}

      {/* Image Content */}
      {imageContent && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className="mb-6"
        >
          <div className="bg-white/10 rounded-lg p-4 border border-white/10">
            <div className="flex items-center justify-between mb-3">
              <h4 className="text-lg font-semibold text-white flex items-center">
                <i className="fas fa-image mr-2 text-purple-400"></i>
                Generated Image
              </h4>
              <button
                onClick={() => downloadMedia(imageContent, 'rant-image.png', 'Image')}
                className="px-3 py-1 bg-purple-600 hover:bg-purple-700 text-white rounded-lg text-sm transition-colors"
              >
                <i className="fas fa-download mr-1"></i>
                Download
              </button>
            </div>
            <img 
              src={imageContent} 
              alt="Generated content" 
              className="w-full max-w-md mx-auto rounded-lg"
            />
          </div>
        </motion.div>
      )}

      {/* Video Content */}
      {videoContent && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className="mb-6"
        >
          <div className="bg-white/10 rounded-lg p-4 border border-white/10">
            <div className="flex items-center justify-between mb-3">
              <h4 className="text-lg font-semibold text-white flex items-center">
                <i className="fas fa-video mr-2 text-red-400"></i>
                Generated Video
              </h4>
              <button
                onClick={() => downloadMedia(videoContent, 'rant-video.mp4', 'Video')}
                className="px-3 py-1 bg-red-600 hover:bg-red-700 text-white rounded-lg text-sm transition-colors"
              >
                <i className="fas fa-download mr-1"></i>
                Download
              </button>
            </div>
            {renderVideoContent(videoContent)}
          </div>
        </motion.div>
      )}

      {/* Additional Actions */}
      <div className="pt-4 border-t border-white/10">
        <div className="flex flex-wrap gap-3">
          <button
            onClick={() => copyToClipboard(textContent)}
            className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg text-sm transition-colors flex items-center"
          >
            <i className="fas fa-share mr-2"></i>
            Share
          </button>
          <button
            onClick={() => showNotification('Content saved to history! 📚', 'success')}
            className="px-4 py-2 bg-purple-600 hover:bg-purple-700 text-white rounded-lg text-sm transition-colors flex items-center"
          >
            <i className="fas fa-bookmark mr-2"></i>
            Save
          </button>
          <button
            onClick={() => window.location.reload()}
            className="px-4 py-2 bg-gray-600 hover:bg-gray-700 text-white rounded-lg text-sm transition-colors flex items-center"
          >
            <i className="fas fa-redo mr-2"></i>
            Start Over
          </button>
        </div>
      </div>
    </motion.div>
  );
};

export default MediaOutput;
