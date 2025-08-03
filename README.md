# RantSmith AI - Agentic AI for Emotional Expression & Creative Transformation

RantSmith AI is an advanced agentic AI system that transforms emotional rants into creative content and actionable insights.

## 🚀 Features

### Core Functionality
- **Multi-Modal Rant Input**: Text, voice, and video rant submission
- **AI Emotion Analysis**: Advanced emotion detection and sentiment analysis
- **Creative Content Generation**: Transform rants into memes, tweets, songs, scripts, and more
- **Personalized AI Agent**: Customizable AI personality (supportive, sarcastic, humorous, etc.)
- **Action Suggestions**: AI-powered recommendations for emotional wellness
- **Content History & Analytics**: Track emotional patterns and content over time

### AI Services Integration
- **LLM Engine**: OpenAI GPT-3.5/4 for text analysis and generation
- **Text-to-Audio**: ElevenLabs for voice synthesis
- **Video Generation**: RunwayML/Pika for video content creation
- **Speech-to-Text**: Whisper for audio transcription

## 🏗️ Architecture

```
User Client (Web/Mobile)
           ↓
    Flask Backend API
    ├── Rant Ingestion
    ├── AI Processing Layer
    ├── Content Generation
    ├── Action Suggestion Engine
    └── User Customization
           ↓
External AI Services
├── OpenAI (LLM)
├── ElevenLabs (TTS)
└── RunwayML (Video)
```

## 📁 Project Structure

```
RantAi/
├── app/
│   ├── __init__.py              # Flask app factory
│   ├── models/                  # Database models
│   │   ├── user.py             # User model
│   │   ├── rant.py             # Rant model
│   │   └── content.py          # Generated content models
│   ├── routes/                  # API endpoints
│   │   ├── auth.py             # Authentication routes
│   │   ├── rant_api.py         # Rant management
│   │   ├── ai_processing.py    # AI processing endpoints
│   │   └── user_customization.py # User preferences
│   ├── services/               # Business logic
│   │   ├── ai_service.py       # Core AI processing
│   │   ├── content_generator.py # Content generation
│   │   └── rant_processor.py   # Rant processing pipeline
│   └── utils/                  # Utilities
│       ├── validators.py       # Input validation
│       └── helpers.py          # Helper functions
├── config.py                   # Configuration
├── run.py                      # Application entry point
├── requirements.txt            # Dependencies
└── README.md                   # This file
```

## 🎨 Enhanced CSS & UI Features

### Modern Design System
- **Glassmorphism Effects**: Beautiful frosted glass aesthetics with backdrop blur
- **Neon & Cyber Styling**: Futuristic neon glows and cyber-inspired elements
- **Advanced Animations**: Smooth gradient shifts, floating elements, and loading states
- **Responsive Design**: Mobile-first approach with adaptive components

### Component Library
- **Buttons**: Primary, secondary, ghost, and neon variants with hover animations
- **Inputs**: Glassmorphism-styled inputs with focus states and validation
- **Cards**: Interactive cards with lift effects and glowing borders
- **Loading States**: Dots, spinners, waves, and skeleton placeholders

### Typography & Effects
- **Font Stack**: Inter (primary), Space Grotesk (display), Orbitron (cyber), JetBrains Mono (code)
- **Text Effects**: Gradient text, glitch effects, neon glow, and shadow styling
- **Accessibility**: WCAG AA compliant colors, reduced motion support, screen reader friendly

### Visual Features
- **Particle Effects**: Animated background particles for immersive experience
- **Gradient Backgrounds**: Multi-layered gradient meshes with blur effects
- **Interactive Elements**: Hover states, focus indicators, and touch feedback
- **Status Indicators**: Animated dots for online/offline/busy states

### Demo & Testing
- **Style Demo Page**: Comprehensive showcase of all CSS components (`/style-demo`)
- **Cross-Browser Support**: Chrome/Edge 88+, Firefox 78+, Safari 14+
- **Performance Optimized**: GPU-accelerated animations, efficient selectors

For detailed CSS documentation, see [CSS_DOCUMENTATION.md](CSS_DOCUMENTATION.md).

## 🛠️ Installation & Setup

### 1. Clone the Repository
```bash
git clone <repository-url>
cd RantAi
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Environment Configuration
Create a `.env` file in the root directory:
```env
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///rantsmith.db
OPENAI_API_KEY=your-openai-api-key
ELEVENLABS_API_KEY=your-elevenlabs-api-key
RUNWAYML_API_KEY=your-runwayml-api-key
FLASK_ENV=development
```

### 5. Initialize Database
```bash
python create_db.py
```

### 6. Run the Application
```bash
python run.py
```

The application will be available at `http://localhost:5000`

## 📡 API Endpoints

### Authentication
- `POST /auth/register` - Register new user
- `POST /auth/login` - User login
- `POST /auth/logout` - User logout
- `GET /auth/profile` - Get user profile
- `PUT /auth/profile` - Update user profile

### Rant Management
- `POST /api/rant/submit` - Submit new rant
- `GET /api/rant/history` - Get rant history
- `GET /api/rant/<id>` - Get specific rant
- `DELETE /api/rant/<id>` - Delete rant
- `GET /api/rant/analytics` - Get rant analytics

### AI Processing
- `POST /api/ai/process/<rant_id>` - Process rant with AI
- `POST /api/ai/generate-content/<rant_id>` - Generate content
- `POST /api/ai/suggest-actions/<rant_id>` - Get action suggestions
- `GET /api/ai/content-history` - Get generated content history

### User Customization
- `GET /api/user/preferences` - Get user preferences
- `PUT /api/user/preferences` - Update preferences
- `GET /api/user/favorites` - Get favorite content
- `POST /api/user/favorites/<content_id>` - Add to favorites
- `GET /api/user/dashboard` - Get dashboard data

## 🤖 AI Features

### Emotion Detection
- Analyzes text, audio, and video inputs
- Detects emotions: angry, frustrated, sad, anxious, excited, happy, confused, neutral
- Provides confidence scores and sentiment analysis

### Content Generation
- **Text**: Supportive responses and reframed perspectives
- **Memes**: Relatable meme templates with custom text
- **Tweets**: Social media ready posts with hashtags
- **Songs**: Custom lyrics based on emotional content
- **Scripts**: Comedy scripts and dialogues
- **Audio**: Text-to-speech with emotional tone
- **Video**: AI-generated video content

### Action Suggestions
- Personalized recommendations based on emotional state
- Health and wellness suggestions
- Social connection prompts
- Professional help recommendations

## 🎨 Customization

### AI Personalities
- **Supportive**: Empathetic and understanding
- **Sarcastic**: Witty but caring responses
- **Humorous**: Light-hearted and funny
- **Motivational**: Energetic and inspiring
- **Professional**: Thoughtful counselor-style guidance

### Output Formats
- **Text**: Written responses and content
- **Audio**: Voice-generated content
- **Video**: Visual content with animations
- **Meme**: Image-based humor

## 🧪 Testing

Run the test suite:
```bash
pytest
```

Run specific tests:
```bash
pytest tests/test_models.py
pytest tests/test_routes.py
pytest tests/test_services.py
```

## 🚀 Deployment

### Development
```bash
flask run --debug
```

### Production
```bash
gunicorn -w 4 -b 0.0.0.0:5000 run:app
```

### Docker (Optional)
```bash
docker build -t rantsmith-ai .
docker run -p 5000:5000 rantsmith-ai
```

## 🔒 Security Features

- Password hashing with Werkzeug
- JWT token authentication
- Input validation and sanitization
- File upload security
- Rate limiting (configurable)
- CORS protection

## 📊 Analytics & Monitoring

- User emotion tracking over time
- Content generation statistics
- AI model performance metrics
- User engagement analytics

## 🛣️ Roadmap

### Phase 1 (Current)
- ✅ Core rant processing
- ✅ Basic AI integration
- ✅ Text content generation
- ✅ User authentication

### Phase 2
- 🔄 Advanced emotion AI
- 🔄 Audio/video processing
- 🔄 Real-time chat interface
- 🔄 Mobile app support

### Phase 3
- ⏳ Social features
- ⏳ Community sharing
- ⏳ Therapist integration
- ⏳ Advanced analytics

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 💬 Support

For support, email support@rantsmith.ai or join our Discord community.

## 🏷️ Version

Current Version: 1.0.0

---

**RantSmith AI** - Transform your rants, transform your life! 🚀✨
