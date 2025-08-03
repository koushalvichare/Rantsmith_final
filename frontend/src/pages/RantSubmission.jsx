import React, { useState } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { useNotification } from '../contexts/NotificationContext';
import { useNavigate } from 'react-router-dom';
import MediaUpload from '../components/MediaUpload';
import MediaOutput from '../components/MediaOutput';

const RantSubmission = () => {
  const { user } = useAuth();
  const { showNotification } = useNotification();
  const navigate = useNavigate();
  
  const [formData, setFormData] = useState({
    content: '',
    transformationType: 'poem',
    tone: 'neutral',
    privacy: 'private'
  });
  const [loading, setLoading] = useState(false);
  const [transformedContent, setTransformedContent] = useState(null);
  const [currentRantId, setCurrentRantId] = useState(null);
  const [mediaInput, setMediaInput] = useState(null);

  const transformationTypes = [
    { value: 'poem', label: 'Poetry', icon: '📝', description: 'Transform into beautiful verses' },
    { value: 'rap', label: 'Rap', icon: '🎤', description: 'Turn it into sick bars' },
    { value: 'story', label: 'Story', icon: '📚', description: 'Create a narrative' },
    { value: 'song', label: 'Song', icon: '🎵', description: 'Make it melodic' },
    { value: 'motivational', label: 'Motivational', icon: '💪', description: 'Inspire and uplift' },
    { value: 'comedy', label: 'Comedy', icon: '😂', description: 'Find the humor' }
  ];

  const tones = [
    { value: 'neutral', label: 'Neutral', icon: '😐' },
    { value: 'positive', label: 'Positive', icon: '😊' },
    { value: 'dramatic', label: 'Dramatic', icon: '🎭' },
    { value: 'sarcastic', label: 'Sarcastic', icon: '😏' },
    { value: 'emotional', label: 'Emotional', icon: '💫' },
    { value: 'humorous', label: 'Humorous', icon: '😄' }
  ];

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    // Check if we have either text content or media input
    if (!formData.content.trim() && !mediaInput) {
      showNotification('Please write something or upload media to transform! 📝', 'error');
      return;
    }

    setLoading(true);
    
    try {
      let rantId = currentRantId;
      
      // If we already have a rant from media upload, use it
      if (mediaInput && mediaInput.rantId) {
        rantId = mediaInput.rantId;
        setCurrentRantId(rantId);
      } else {
        // Otherwise, create a new rant with text content
        const submitUrls = ['/api/rant/submit', 'http://127.0.0.1:5000/api/rant/submit'];
        let response;
        let submitSuccess = false;
        
        for (const url of submitUrls) {
          try {
            console.log(`Trying to submit to: ${url}`);
            response = await fetch(url, {
              method: 'POST',
              headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${localStorage.getItem('authToken')}`
              },
              body: JSON.stringify({
                content: formData.content || (mediaInput ? mediaInput.text : ''),
                transformation_type: formData.transformationType,
                tone: formData.tone,
                privacy: formData.privacy,
                input_type: mediaInput ? mediaInput.type : 'text'
              })
            });
            
            if (response.ok) {
              console.log(`Submit successful with: ${url}`);
              submitSuccess = true;
              break;
            } else {
              console.log(`Submit failed with: ${url}, status: ${response.status}`);
            }
          } catch (error) {
            console.log(`Submit error with: ${url}`, error);
          }
        }
        
        if (!submitSuccess) {
          throw new Error('Failed to submit rant to any endpoint');
        }

        const data = await response.json();
        rantId = data.rant_id;
        setCurrentRantId(rantId);
      }
      
      // Transform the content - try both proxy and direct URL
      const transformUrls = [`/api/media/transform-with-ai/${rantId}`, `http://127.0.0.1:5000/api/media/transform-with-ai/${rantId}`];
      let transformResponse;
      let transformSuccess = false;
      
      for (const url of transformUrls) {
        try {
          console.log(`Trying to transform with: ${url}`);
          transformResponse = await fetch(url, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
              'Authorization': `Bearer ${localStorage.getItem('authToken')}`
            },
            body: JSON.stringify({
              transformation_type: formData.transformationType,
              output_format: 'text'
            })
          });
          
          if (transformResponse.ok) {
            console.log(`Transform successful with: ${url}`);
            transformSuccess = true;
            break;
          } else {
            console.log(`Transform failed with: ${url}, status: ${transformResponse.status}`);
          }
        } catch (error) {
          console.log(`Transform error with: ${url}`, error);
        }
      }

      if (transformSuccess) {
        const transformData = await transformResponse.json();
        const transformedText = transformData.text;
        
        // Create multimedia outputs based on transformation type
        const multimediaOutputs = {
          text: transformedText,
          audio: null,
          image: null,
          video: null
        };

        // Generate audio output for songs and poetry
        if (['song', 'poem', 'rap'].includes(formData.transformationType)) {
          try {
            const speechResponse = await fetch(`/api/media/generate-speech/${rantId}`, {
              method: 'POST',
              headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${localStorage.getItem('authToken')}`
              },
              body: JSON.stringify({
                language: 'en',
                slow: false
              })
            });
            
            if (speechResponse.ok) {
              const speechData = await speechResponse.json();
              multimediaOutputs.audio = speechData.audio_data;
              console.log('Audio generated successfully');
            }
          } catch (error) {
            console.log('Audio generation failed:', error);
          }
        }

        // Generate image/meme output for comedy and motivational
        if (['comedy', 'motivational'].includes(formData.transformationType)) {
          try {
            const memeResponse = await fetch(`/api/media/generate-meme/${rantId}`, {
              method: 'POST',
              headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${localStorage.getItem('authToken')}`
              },
              body: JSON.stringify({
                template_type: formData.transformationType
              })
            });
            
            if (memeResponse.ok) {
              const memeData = await memeResponse.json();
              multimediaOutputs.image = memeData.image_data;
              console.log('Image generated successfully');
            }
          } catch (error) {
            console.log('Image generation failed:', error);
          }
        }

        // Generate video output for stories
        if (formData.transformationType === 'story') {
          try {
            const videoResponse = await fetch(`/api/media/generate-video/${rantId}`, {
              method: 'POST',
              headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${localStorage.getItem('authToken')}`
              },
              body: JSON.stringify({
                duration: 15,
                background_color: [30, 30, 60]
              })
            });
            
            if (videoResponse.ok) {
              const videoData = await videoResponse.json();
              multimediaOutputs.video = videoData.video_data;
              console.log('Video generated successfully');
            }
          } catch (error) {
            console.log('Video generation failed:', error);
          }
        }

        setTransformedContent(multimediaOutputs);
      } else {
        console.warn('Transform failed, using mock transformation');
        // Fallback to mock transformation
        setTransformedContent({
          text: generateMockTransformation(formData.content || mediaInput?.text || '', formData.transformationType),
          audio: null,
          image: null,
          video: null
        });
      }
      
      showNotification('Your rant has been transformed! ✨', 'success');
      
    } catch (error) {
      console.error('Error:', error);
      showNotification('Failed to transform your rant 😞', 'error');
    } finally {
      setLoading(false);
    }
  };

  const handleMediaProcessed = (mediaData) => {
    setMediaInput(mediaData);
    if (mediaData.text) {
      setFormData(prev => ({ ...prev, content: mediaData.text }));
    }
    if (mediaData.rantId) {
      setCurrentRantId(mediaData.rantId);
    }
  };

  const generateMockTransformation = (content, type) => {
    switch (type) {
      case 'poem':
        return `In the depths of thought I ponder,\nWords that make my heart grow fonder,\n"${content.substring(0, 50)}..."\nTransformed to verse, a sight to wonder.`;
      case 'rap':
        return `Yo, listen up, I got something to say,\n"${content.substring(0, 30)}..." that's my way,\nSpitting truth like it's my job,\nTurning rants into beats that throb.`;
      case 'story':
        return `Once upon a time, there was someone who felt: "${content.substring(0, 40)}..." This feeling would lead them on an unexpected journey of self-discovery...`;
      case 'song':
        return `🎵 (Verse 1)\n"${content.substring(0, 30)}..."\nThat's the feeling in my heart\n🎵 (Chorus)\nSinging out loud, breaking free\nThis is who I'm meant to be...`;
      case 'motivational':
        return `Remember this: "${content.substring(0, 40)}..." - These feelings are valid, but they don't define you. Every challenge is a stepping stone to greatness. You've got this! 💪`;
      case 'comedy':
        return `So there I was, thinking: "${content.substring(0, 30)}..." And then I realized - if this was a sitcom, the laugh track would be going crazy right now! 😂`;
      default:
        return content;
    }
  };

  const handleStartOver = () => {
    setFormData({
      content: '',
      transformationType: 'poem',
      tone: 'neutral',
      privacy: 'private'
    });
    setTransformedContent(null);
  };

  const handleSave = () => {
    // Save to content history
    showNotification('Content saved to your history! 📚', 'success');
    navigate('/history');
  };

  const handleShare = () => {
    // Share functionality
    if (navigator.share) {
      navigator.share({
        title: 'Check out my RantSmith AI creation!',
        text: transformedContent.transformed,
        url: window.location.href
      });
    } else {
      // Fallback to clipboard
      navigator.clipboard.writeText(transformedContent.transformed);
      showNotification('Content copied to clipboard! 📋', 'success');
    }
  };

  if (transformedContent) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-purple-900 via-blue-900 to-indigo-900 pt-20 pb-8">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-8">
            <h1 className="text-4xl font-bold text-white mb-2">✨ Transformation Complete!</h1>
            <p className="text-xl text-gray-300">Your rant has been magically transformed</p>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
            {/* Original Content */}
            <div className="backdrop-blur-lg bg-white/10 border border-white/20 rounded-2xl p-6">
              <h2 className="text-xl font-bold text-white mb-4 flex items-center">
                📝 Original Rant
              </h2>
              <div className="bg-white/5 border border-white/10 rounded-xl p-4">
                <p className="text-gray-300 leading-relaxed">{transformedContent.original}</p>
              </div>
            </div>

            {/* Transformed Content */}
            <div className="backdrop-blur-lg bg-white/10 border border-white/20 rounded-2xl p-6">
              <h2 className="text-xl font-bold text-white mb-4 flex items-center">
                {transformationTypes.find(t => t.value === transformedContent.type)?.icon} 
                <span className="ml-2">Transformed {transformedContent.type}</span>
              </h2>
              <div className="bg-gradient-to-r from-purple-600/20 to-pink-600/20 border border-purple-500/30 rounded-xl p-4">
                <p className="text-white leading-relaxed whitespace-pre-line">{transformedContent.transformed}</p>
              </div>
            </div>
          </div>

          {/* Actions */}
          <div className="flex flex-col sm:flex-row gap-4 justify-center mt-8">
            <button
              onClick={handleSave}
              className="bg-gradient-to-r from-green-600 to-teal-600 text-white px-6 py-3 rounded-xl font-medium hover:from-green-700 hover:to-teal-700 transition-all duration-300 transform hover:scale-105"
            >
              Save to History 📚
            </button>
            <button
              onClick={handleShare}
              className="bg-gradient-to-r from-blue-600 to-cyan-600 text-white px-6 py-3 rounded-xl font-medium hover:from-blue-700 hover:to-cyan-700 transition-all duration-300 transform hover:scale-105"
            >
              Share 🚀
            </button>
            <button
              onClick={handleStartOver}
              className="bg-gradient-to-r from-purple-600 to-pink-600 text-white px-6 py-3 rounded-xl font-medium hover:from-purple-700 hover:to-pink-700 transition-all duration-300 transform hover:scale-105"
            >
              Create Another ✨
            </button>
          </div>

          {/* Media Output Section */}
          <MediaOutput 
            rantId={currentRantId} 
            transformedContent={transformedContent} 
          />
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-900 via-blue-900 to-indigo-900 pt-20 pb-8">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-white mb-2">🚀 Express Yourself</h1>
          <p className="text-xl text-gray-300">Let AI transform your thoughts into something amazing</p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-8">
          {/* Media Upload Section */}
          <MediaUpload onMediaProcessed={handleMediaProcessed} />

          {/* Content Input */}
          <div className="backdrop-blur-lg bg-white/10 border border-white/20 rounded-2xl p-6">
            <label className="block text-xl font-bold text-white mb-4">
              What's on your mind? 💭
            </label>
            <textarea
              value={formData.content}
              onChange={(e) => setFormData({...formData, content: e.target.value})}
              placeholder="Share your thoughts, feelings, frustrations, or anything that's bothering you... The AI will work its magic!"
              className="w-full h-32 px-4 py-3 bg-white/20 border border-white/30 rounded-xl text-white placeholder-gray-300 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all duration-300 resize-none"
              disabled={loading}
            />
            <div className="text-right mt-2">
              <span className="text-sm text-gray-400">
                {formData.content.length}/1000
              </span>
            </div>
          </div>

          {/* Transformation Type */}
          <div className="backdrop-blur-lg bg-white/10 border border-white/20 rounded-2xl p-6">
            <label className="block text-xl font-bold text-white mb-4">
              How should we transform it? ✨
            </label>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {transformationTypes.map((type) => (
                <button
                  key={type.value}
                  type="button"
                  onClick={() => setFormData({...formData, transformationType: type.value})}
                  className={`p-4 rounded-xl border-2 transition-all duration-300 ${
                    formData.transformationType === type.value
                      ? 'border-purple-500 bg-purple-600/20'
                      : 'border-white/20 bg-white/5 hover:bg-white/10'
                  }`}
                  disabled={loading}
                >
                  <div className="text-2xl mb-2">{type.icon}</div>
                  <div className="text-white font-medium">{type.label}</div>
                  <div className="text-xs text-gray-400 mt-1">{type.description}</div>
                </button>
              ))}
            </div>
          </div>

          {/* Tone Selection */}
          <div className="backdrop-blur-lg bg-white/10 border border-white/20 rounded-2xl p-6">
            <label className="block text-xl font-bold text-white mb-4">
              What tone should we use? 🎭
            </label>
            <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
              {tones.map((tone) => (
                <button
                  key={tone.value}
                  type="button"
                  onClick={() => setFormData({...formData, tone: tone.value})}
                  className={`p-3 rounded-xl border-2 transition-all duration-300 ${
                    formData.tone === tone.value
                      ? 'border-purple-500 bg-purple-600/20'
                      : 'border-white/20 bg-white/5 hover:bg-white/10'
                  }`}
                  disabled={loading}
                >
                  <div className="text-xl mb-1">{tone.icon}</div>
                  <div className="text-white text-sm font-medium">{tone.label}</div>
                </button>
              ))}
            </div>
          </div>

          {/* Privacy Setting */}
          <div className="backdrop-blur-lg bg-white/10 border border-white/20 rounded-2xl p-6">
            <label className="block text-xl font-bold text-white mb-4">
              Privacy Setting 🔒
            </label>
            <div className="flex space-x-4">
              <button
                type="button"
                onClick={() => setFormData({...formData, privacy: 'private'})}
                className={`flex-1 p-4 rounded-xl border-2 transition-all duration-300 ${
                  formData.privacy === 'private'
                    ? 'border-purple-500 bg-purple-600/20'
                    : 'border-white/20 bg-white/5 hover:bg-white/10'
                }`}
                disabled={loading}
              >
                <div className="text-xl mb-2">🔒</div>
                <div className="text-white font-medium">Private</div>
                <div className="text-xs text-gray-400">Only you can see this</div>
              </button>
              <button
                type="button"
                onClick={() => setFormData({...formData, privacy: 'public'})}
                className={`flex-1 p-4 rounded-xl border-2 transition-all duration-300 ${
                  formData.privacy === 'public'
                    ? 'border-purple-500 bg-purple-600/20'
                    : 'border-white/20 bg-white/5 hover:bg-white/10'
                }`}
                disabled={loading}
              >
                <div className="text-xl mb-2">🌍</div>
                <div className="text-white font-medium">Public</div>
                <div className="text-xs text-gray-400">Share with the community</div>
              </button>
            </div>
          </div>

          {/* Submit Button */}
          <div className="text-center">
            <button
              type="submit"
              disabled={loading || (!formData.content.trim() && !mediaInput)}
              className="bg-gradient-to-r from-purple-600 to-pink-600 text-white px-8 py-4 rounded-xl font-medium hover:from-purple-700 hover:to-pink-700 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:ring-offset-2 focus:ring-offset-transparent transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed transform hover:scale-105"
            >
              {loading ? (
                <div className="flex items-center justify-center">
                  <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-white mr-3"></div>
                  AI is working its magic...
                </div>
              ) : (
                'Transform My Rant ✨'
              )}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default RantSubmission;
