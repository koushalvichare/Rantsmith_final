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
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  useEffect(() => {
    // Initial greeting message
    const initialMessage = {
      id: 1,
      text: `Hey ${user?.username || 'there'}! 👋 I'm your AI companion here to help with anything on your mind. Whether you want to vent, brainstorm, or just chat - I'm here for you! What's going on?`,
      sender: 'ai',
      timestamp: new Date().toISOString()
    };
    setMessages([initialMessage]);
  }, [user]);

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
      // Call the real AI API using Gemini
      console.log('🤖 Sending message to AI:', currentMessage);
      const response = await apiService.chatWithAI(currentMessage);
      console.log('🤖 AI Response received:', response);
      
      const aiMessage = {
        id: Date.now() + 1,
        text: response.response,
        sender: 'ai',
        timestamp: new Date().toISOString()
      };

      setMessages(prev => [...prev, aiMessage]);
    } catch (error) {
      console.error('AI Chat Error:', error);
      showNotification('Failed to get AI response 😞 Please try again.', 'error');
      
      // Fallback message if API fails
      const fallbackMessage = {
        id: Date.now() + 1,
        text: "I'm sorry, I'm having trouble connecting right now. Please try again in a moment! 🤖",
        sender: 'ai',
        timestamp: new Date().toISOString()
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

  const quickReplies = [
    "I'm feeling stressed 😰",
    "Work is overwhelming 💼",
    "I need to vent 💭",
    "Help me process my thoughts 🤔",
    "I'm having a rough day 😔",
    "Tell me a joke 😂"
  ];

  const handleQuickReply = (reply) => {
    setInputMessage(reply);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-900 via-blue-900 to-indigo-900 pt-20 pb-8">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 h-full">
        <div className="text-center mb-6">
          <h1 className="text-4xl font-bold text-white mb-2">🤖 AI Chat Companion</h1>
          <p className="text-xl text-gray-300">Your friendly AI assistant for emotional support and conversation</p>
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
              <p className="text-sm text-gray-300 mb-2">Quick replies:</p>
              <div className="flex flex-wrap gap-2">
                {quickReplies.map((reply, index) => (
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
            <h3 className="text-white font-medium mb-1">Emotional Support</h3>
            <p className="text-xs text-gray-400">I'm here to listen and provide support</p>
          </div>
          <div className="backdrop-blur-lg bg-white/10 border border-white/20 rounded-xl p-4 text-center">
            <div className="text-2xl mb-2">💡</div>
            <h3 className="text-white font-medium mb-1">Brainstorming</h3>
            <p className="text-xs text-gray-400">Let's think through problems together</p>
          </div>
          <div className="backdrop-blur-lg bg-white/10 border border-white/20 rounded-xl p-4 text-center">
            <div className="text-2xl mb-2">🌟</div>
            <h3 className="text-white font-medium mb-1">Creative Ideas</h3>
            <p className="text-xs text-gray-400">Explore creative solutions and perspectives</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AIChat;
