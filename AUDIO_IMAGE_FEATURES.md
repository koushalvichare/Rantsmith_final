# RantSmith AI - Audio & Image Features

## Overview
RantSmith AI now supports multimedia input and output, allowing users to:
- Record audio and convert to text
- Upload images for processing
- Generate audio output (text-to-speech)
- Create memes and visual content
- Generate videos with text overlay

## New Features Added

### 🎤 Audio Recording & Processing
- **Audio Recording**: Users can record audio directly in the browser
- **Speech-to-Text**: Audio files are processed and converted to text
- **Supported Formats**: WAV, MP3, OGG, M4A
- **Mock Service**: Currently using a mock transcription service (can be upgraded with actual speech recognition)

### 📸 Image Upload & Processing
- **Image Upload**: Support for PNG, JPG, JPEG, GIF formats
- **Image Analysis**: Basic metadata extraction (dimensions, format, etc.)
- **Preview**: Users can preview uploaded images before processing

### 🔊 Audio Output Generation
- **Text-to-Speech**: Convert any text content to audio
- **Language Support**: Multiple language options (EN, ES, FR, etc.)
- **Speed Control**: Option for slow or normal speech
- **Download**: Generated audio can be downloaded

### 🖼️ Visual Content Generation
- **Meme Generation**: Create memes with custom text overlays
- **Background Gradients**: Attractive gradient backgrounds
- **Text Wrapping**: Automatic text wrapping for readability
- **Customizable**: Different template types and styles

### 🎬 Video Creation
- **Text-to-Video**: Convert text content into video format
- **Custom Backgrounds**: Configurable background colors
- **Duration Control**: Adjustable video length
- **Text Animation**: Professional text overlay with proper formatting

## How to Use

### Recording Audio
1. Go to the "Rant Submission" page
2. Click the "Start Recording" button in the Audio Upload section
3. Speak your thoughts (timer shows recording duration)
4. Click "Stop Recording" when finished
5. Preview the audio and click "Upload" to process

### Uploading Images
1. In the Audio & Image Upload section, click "Select Image"
2. Choose an image file from your device
3. Preview the selected image
4. Click "Upload" to process

### Generating Multimedia Output
1. After submitting a rant (text, audio, or image)
2. Scroll to the "Multimedia Output" section
3. Choose from available options:
   - **Text to Speech**: Convert your content to audio
   - **Generate Meme**: Create a visual meme
   - **Create Video**: Generate a video with text overlay
   - **AI Transform**: Transform content and generate multimedia

### Downloading Content
- All generated content includes download buttons
- Click the download icon to save files locally
- Supported formats: MP3 (audio), PNG (images), MP4 (videos)

## Technical Implementation

### Backend Services
- **SimpleMediaService**: Handles basic media processing
- **Audio Processing**: Mock speech recognition with upgrade path
- **Image Processing**: PIL-based image manipulation
- **Text-to-Speech**: Placeholder service (can integrate gTTS)
- **Video Generation**: Placeholder service (can integrate OpenCV)

### Frontend Components
- **MediaUpload**: Audio recording and file upload interface
- **MediaOutput**: Display and manage generated content
- **Audio Controls**: Native HTML5 audio player
- **File Previews**: Image and video preview functionality

### API Endpoints
- `POST /api/media/upload-audio` - Process audio files
- `POST /api/media/upload-image` - Process image files
- `POST /api/media/generate-speech/{rant_id}` - Generate audio
- `POST /api/media/generate-meme/{rant_id}` - Create memes
- `POST /api/media/generate-video/{rant_id}` - Create videos
- `POST /api/media/transform-with-ai/{rant_id}` - AI transformation

## Future Enhancements

### Planned Features
1. **Real Speech Recognition**: Integrate with Google Speech API or OpenAI Whisper
2. **Advanced TTS**: Use ElevenLabs or Google Cloud TTS for better voice quality
3. **Video Templates**: Multiple video templates and animations
4. **OCR Support**: Extract text from uploaded images
5. **Batch Processing**: Process multiple files simultaneously
6. **Voice Cloning**: Custom voice generation
7. **Advanced Memes**: More template options and customization

### Technical Upgrades
- **FFmpeg Integration**: Better audio/video processing
- **WebRTC**: Real-time audio streaming
- **WebSocket**: Real-time processing updates
- **Cloud Storage**: Store large media files
- **CDN Integration**: Fast media delivery
- **AI Models**: Custom trained models for better transformations

## Configuration

### Environment Variables
```env
# Add these to your .env file for full functionality
OPENAI_API_KEY=your_openai_key_here
GOOGLE_CLOUD_API_KEY=your_google_cloud_key
ELEVENLABS_API_KEY=your_elevenlabs_key
```

### Dependencies
The application now includes these additional Python packages:
- `Pillow` - Image processing
- `speechrecognition` - Audio transcription (optional)
- `gTTS` - Text-to-speech (optional)
- `opencv-python` - Video processing (optional)
- `pydub` - Audio manipulation (optional)

### Browser Requirements
- **Audio Recording**: Requires HTTPS in production for microphone access
- **File Upload**: Modern browsers with File API support
- **Media Playback**: HTML5 audio/video support

## Security Considerations

### File Upload Security
- File type validation
- File size limits (16MB max)
- Secure filename handling
- Temporary file cleanup

### Privacy
- Audio recordings are processed locally when possible
- Temporary files are automatically deleted
- User content is tied to authenticated sessions

## Troubleshooting

### Common Issues
1. **Microphone Access Denied**: Check browser permissions
2. **Audio Not Processing**: Verify file format is supported
3. **Large File Upload**: Check file size limits
4. **Service Unavailable**: Some features use mock services in development

### Error Messages
- "Speech recognition not available" - Optional dependency not installed
- "TTS not available" - Text-to-speech service not configured
- "File too large" - Reduce file size or contact administrator

## Support

For technical support or feature requests, please refer to the main documentation or contact the development team.

---
*Last updated: January 2025*
