import React, { useState, useEffect, useRef } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { useNotification } from '../contexts/NotificationContext';
import apiService from '../services/api';

const AIChat = () => {
  const { user } = useAuth();
  const { showNotification } = useNotification();
  const [messages, setMessages] = useState([]);
  const [inputMessage, setInputMessage] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const [loading, setLoading] = useState(false);
  const [selectedPersonality, setSelectedPersonality] = useState('supportive');
  const [conversationId, setConversationId] = useState(null);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  useEffect(() => {
    // Initial greeting message with personality-based content
    const greetings = {
      supportive: `Hello ${user?.username || 'there'}! 👋 I'm Elaichi, your supportive AI companion. I'm here to provide a safe, caring space where you can explore your thoughts and feelings. Whether you're dealing with stress, need emotional support, or just want someone to listen - I'm here for you. What would you like to talk about today?`,
      humorous: `Hey ${user?.username || 'there'}! 😄 I'm Elaichi, your AI companion with a sense of humor! Life's too short to be serious all the time, right? I'm here to chat, share some laughs, and maybe help you see the lighter side of things. What's on your mind today?`,
      motivational: `Hello ${user?.username || 'there'}! 🌟 I'm Elaichi, your motivational AI companion! I believe in your strength and potential. Every challenge is an opportunity to grow, and I'm here to help you discover the amazing person you already are. Ready to tackle today together?`,
      professional: `Good day ${user?.username || 'there'}. I'm Elaichi, your professional AI companion. I'm here to provide thoughtful, evidence-based guidance and support. My approach focuses on practical solutions and professional insights. How may I assist you today?`,
      sarcastic: `Well hello there ${user?.username || 'friend'}! 😏 I'm Elaichi, your AI companion with a bit of an edge. Don't worry, I'm here to help - I just might do it with a smirk. Life's complicated enough without taking it too seriously, right? What's bothering you today?`
    };

    const initialMessage = {
      id: 1,
      text: greetings[selectedPersonality] || greetings.supportive,
      sender: 'ai',
      timestamp: new Date().toISOString()
    };
    setMessages([initialMessage]);
    setConversationId(Date.now().toString()); // Create new conversation ID
  }, [user, selectedPersonality]);

  const handleSendMessage = async (e) => {
    e.preventDefault();
    
    if (!inputMessage.trim() || loading) return;

    const userMessage = {
      id: Date.now(),
      text: inputMessage,
      sender: 'user',
      timestamp: new Date().toISOString()
    };

    setMessages(prev => [...prev, userMessage]);
    const currentMessage = inputMessage;
    setInputMessage('');
    setIsTyping(true);
    setLoading(true);

    try {
      // Call the real AI API using Gemini with enhanced parameters
      console.log('🤖 Sending message to AI:', currentMessage);
      console.log('🤖 Using personality:', selectedPersonality);
      console.log('🤖 Conversation ID:', conversationId);
      
      const response = await apiService.chatWithAI(currentMessage, conversationId, selectedPersonality);
      console.log('🤖 AI Response received:', response);
      
      // Validate response
      if (!response || !response.response) {
        throw new Error('Invalid response from AI service');
      }
      
      const aiMessage = {
        id: Date.now() + 1,
        text: response.response,
        sender: 'ai',
        timestamp: new Date().toISOString(),
        personality: selectedPersonality
      };

      setMessages(prev => [...prev, aiMessage]);
      
      // Show success feedback
      if (Math.random() < 0.3) { // Occasionally show positive feedback
        showNotification('💭 AI is thinking deeply about your message...', 'info');
      }
      
    } catch (error) {
      console.error('AI Chat Error:', error);
      
      // Enhanced error handling with specific messages
      let errorMessage = "I'm sorry, I'm having trouble connecting right now. Please try again in a moment! 🤖";
      
      if (error.message?.includes('token')) {
        errorMessage = "It looks like your session has expired. Please refresh the page and try again! 🔄";
        showNotification('Session expired - please refresh the page 🔄', 'error');
      } else if (error.message?.includes('network')) {
        errorMessage = "I'm having network connectivity issues. Please check your connection and try again! 🌐";
        showNotification('Network connection issue 🌐', 'error');
      } else {
        showNotification('Failed to get AI response 😞 Please try again.', 'error');
      }
      
      // Fallback message with personality
      const personalityFallbacks = {
        supportive: "I'm here for you, even when technology isn't cooperating. Take a deep breath, and let's try again when you're ready. 💙",
        humorous: "Well, that's awkward! Even AI has bad days apparently. 😅 Give me a moment to get my digital act together!",
        motivational: "Every setback is a setup for a comeback! Let's try this again - you've got this! 💪",
        professional: "I apologize for the technical difficulty. Please attempt your request again momentarily.",
        sarcastic: "Oh great, even the AI is having technical difficulties now. What's next? 🙄 Let's try that again, shall we?"
      };
      
      const fallbackMessage = {
        id: Date.now() + 1,
        text: personalityFallbacks[selectedPersonality] || errorMessage,
        sender: 'ai',
        timestamp: new Date().toISOString(),
        isError: true
      };
      setMessages(prev => [...prev, fallbackMessage]);
    } finally {
      setIsTyping(false);
      setLoading(false);
    }
  };

  const formatTime = (timestamp) => {
    const date = new Date(timestamp);
    return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  };

  const quickReplies = {
    supportive: [
      "I'm feeling stressed 😰",
      "Help me understand my emotions 🧠",
      "I need someone to talk to 💭",
      "What coping strategies do you recommend? 🌱",
      "Can you help me feel better? 💙",
      "How can I process these feelings? 🤔"
    ],
    humorous: [
      "Tell me a joke to cheer me up! 😄",
      "What's the funniest thing about life? 🤣",
      "Make me laugh please! 😂",
      "Give me a funny perspective on stress 😅",
      "What would make you smile today? 😊",
      "Share something amusing! 🎭"
    ],
    motivational: [
      "I need some motivation today! 💪",
      "Help me believe in myself 🌟",
      "What can I achieve today? 🚀",
      "Inspire me to keep going! ⚡",
      "Remind me of my strength 💎",
      "What's possible for me? ✨"
    ],
    professional: [
      "What are evidence-based coping strategies? 📚",
      "How can I improve my mental wellness? 🧠",
      "What does research say about stress? 📊",
      "Provide professional guidance please 👔",
      "What are best practices for anxiety? 📋",
      "Give me practical solutions 🔧"
    ],
    sarcastic: [
      "Life is great, isn't it? 🙄",
      "Why is everything so complicated? 😏",
      "Make fun of my problems please 😈",
      "Give me some sassy advice 💅",
      "What's your take on modern life? 🎭",
      "Roast my daily struggles 🔥"
    ]
  };

  const personalities = [
    { id: 'supportive', name: 'Supportive', icon: '💙', desc: 'Caring and empathetic' },
    { id: 'humorous', name: 'Humorous', icon: '😄', desc: 'Fun and light-hearted' },
    { id: 'motivational', name: 'Motivational', icon: '💪', desc: 'Inspiring and energetic' },
    { id: 'professional', name: 'Professional', icon: '👔', desc: 'Evidence-based guidance' },
    { id: 'sarcastic', name: 'Sarcastic', icon: '😏', desc: 'Witty with an edge' }
  ];

  const handleQuickReply = (reply) => {
    setInputMessage(reply);
  };

  const handlePersonalityChange = (personalityId) => {
    setSelectedPersonality(personalityId);
    showNotification(`Switched to ${personalities.find(p => p.id === personalityId)?.name} mode! 🎭`, 'success');
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-900 via-blue-900 to-indigo-900 pt-20 pb-8">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 h-full">
        <div className="text-center mb-6">
          <h1 className="text-4xl font-bold text-white mb-2">🤖 Elaichi - AI Companion</h1>
          <p className="text-xl text-gray-300">Adaptive AI personality for personalized support</p>
          
          {/* Personality Selector */}
          <div className="mt-4 flex flex-wrap justify-center gap-2">
            {personalities.map((personality) => (
              <button
                key={personality.id}
                onClick={() => handlePersonalityChange(personality.id)}
                className={`px-3 py-1 rounded-full text-sm transition-all duration-300 ${
                  selectedPersonality === personality.id
                    ? 'bg-purple-600 text-white'
                    : 'bg-white/10 text-gray-300 hover:bg-white/20'
                }`}
                title={personality.desc}
              >
                {personality.icon} {personality.name}
              </button>
            ))}
          </div>
        </div>

        <div className="backdrop-blur-lg bg-white/10 border border-white/20 rounded-2xl p-6 h-[70vh] flex flex-col">
          {/* Messages Area */}
          <div className="flex-1 overflow-y-auto mb-4 space-y-4">
            {messages.map((message) => (
              <div
                key={message.id}
                className={`flex ${message.sender === 'user' ? 'justify-end' : 'justify-start'}`}
              >
                <div
                  className={`max-w-xs lg:max-w-md px-4 py-2 rounded-2xl ${
                    message.sender === 'user'
                      ? 'bg-gradient-to-r from-purple-600 to-pink-600 text-white'
                      : message.isError 
                        ? 'bg-red-600/20 text-red-200 border border-red-500/30'
                        : 'bg-white/20 text-white border border-white/30'
                  }`}
                >
                  <p className="text-sm leading-relaxed">{message.text}</p>
                  <p className="text-xs opacity-70 mt-1">{formatTime(message.timestamp)}</p>
                </div>
              </div>
            ))}
            
            {isTyping && (
              <div className="flex justify-start">
                <div className="bg-white/20 text-white border border-white/30 px-4 py-2 rounded-2xl max-w-xs">
                  <div className="flex items-center space-x-1">
                    <div className="w-2 h-2 bg-white rounded-full animate-bounce"></div>
                    <div className="w-2 h-2 bg-white rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
                    <div className="w-2 h-2 bg-white rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                  </div>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          {/* Quick Replies */}
          {messages.length === 1 && (
            <div className="mb-4">
              <p className="text-sm text-gray-300 mb-2">Quick replies for {personalities.find(p => p.id === selectedPersonality)?.name} mode:</p>
              <div className="flex flex-wrap gap-2">
                {quickReplies[selectedPersonality]?.map((reply, index) => (
                  <button
                    key={index}
                    onClick={() => handleQuickReply(reply)}
                    className="bg-white/10 hover:bg-white/20 text-white text-xs px-3 py-1 rounded-full border border-white/30 transition-all duration-300"
                  >
                    {reply}
                  </button>
                ))}
              </div>
            </div>
          )}

          {/* Input Area */}
          <form onSubmit={handleSendMessage} className="flex space-x-2">
            <input
              type="text"
              value={inputMessage}
              onChange={(e) => setInputMessage(e.target.value)}
              placeholder="Type your message..."
              className="flex-1 px-4 py-3 bg-white/20 border border-white/30 rounded-xl text-white placeholder-gray-300 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all duration-300"
              disabled={loading}
            />
            <button
              type="submit"
              disabled={loading || !inputMessage.trim()}
              className="bg-gradient-to-r from-purple-600 to-pink-600 text-white px-6 py-3 rounded-xl font-medium hover:from-purple-700 hover:to-pink-700 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:ring-offset-2 focus:ring-offset-transparent transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {loading ? (
                <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
              ) : (
                'Send'
              )}
            </button>
          </form>
        </div>

        {/* Features */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mt-6">
          <div className="backdrop-blur-lg bg-white/10 border border-white/20 rounded-xl p-4 text-center">
            <div className="text-2xl mb-2">🎭</div>
            <h3 className="text-white font-medium mb-1">Adaptive Personality</h3>
            <p className="text-xs text-gray-400">AI adjusts to your preferred communication style</p>
          </div>
          <div className="backdrop-blur-lg bg-white/10 border border-white/20 rounded-xl p-4 text-center">
            <div className="text-2xl mb-2">�</div>
            <h3 className="text-white font-medium mb-1">Emotional Processing</h3>
            <p className="text-xs text-gray-400">Safe space to explore feelings</p>
          </div>
          <div className="backdrop-blur-lg bg-white/10 border border-white/20 rounded-xl p-4 text-center">
            <div className="text-2xl mb-2">�</div>
            <h3 className="text-white font-medium mb-1">Coping Strategies</h3>
            <p className="text-xs text-gray-400">Practical tools for mental wellness</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AIChat;
