import React, { useState, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { useNotification } from '../contexts/NotificationContext';
import { Link } from 'react-router-dom';

const Dashboard = () => {
  const { user } = useAuth();
  const { showNotification } = useNotification();
  const [stats, setStats] = useState({
    totalRants: 0,
    aiTransformations: 0,
    favoriteContent: 0,
    streakDays: 0
  });
  const [recentRants, setRecentRants] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    try {
      // Simulate API call - replace with actual API endpoints
      setTimeout(() => {
        setStats({
          totalRants: 12,
          aiTransformations: 8,
          favoriteContent: 5,
          streakDays: 3
        });
        setRecentRants([
          {
            id: 1,
            content: "Just had the most frustrating day at work...",
            transformedType: "poem",
            createdAt: "2024-01-15T10:30:00Z"
          },
          {
            id: 2,
            content: "Why is traffic always so bad on Mondays?",
            transformedType: "rap",
            createdAt: "2024-01-14T16:45:00Z"
          },
          {
            id: 3,
            content: "My coffee was cold this morning and it ruined my vibe...",
            transformedType: "story",
            createdAt: "2024-01-13T08:15:00Z"
          }
        ]);
        setLoading(false);
      }, 1000);
    } catch (error) {
      showNotification('Failed to load dashboard data 😞', 'error');
      setLoading(false);
    }
  };

  const getTimeAgo = (dateString) => {
    const date = new Date(dateString);
    const now = new Date();
    const diffInHours = Math.floor((now - date) / (1000 * 60 * 60));
    
    if (diffInHours < 1) return 'Just now';
    if (diffInHours < 24) return `${diffInHours}h ago`;
    return `${Math.floor(diffInHours / 24)}d ago`;
  };

  const getTypeIcon = (type) => {
    switch (type) {
      case 'poem': return '📝';
      case 'rap': return '🎤';
      case 'story': return '📚';
      case 'song': return '🎵';
      default: return '✨';
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-purple-900 via-blue-900 to-indigo-900 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-white mx-auto mb-4"></div>
          <p className="text-white">Loading your dashboard...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-900 via-blue-900 to-indigo-900 pt-20 pb-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Welcome Section */}
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-white mb-2">
            Welcome back, {user?.username || 'Ranter'}! 👋
          </h1>
          <p className="text-xl text-gray-300">
            Ready to transform your thoughts into something amazing?
          </p>
        </div>

        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <div className="backdrop-blur-lg bg-white/10 border border-white/20 rounded-2xl p-6 text-center">
            <div className="text-3xl font-bold text-purple-300 mb-2">{stats.totalRants}</div>
            <div className="text-white font-medium mb-1">Total Rants</div>
            <div className="text-sm text-gray-400">Your thoughts expressed</div>
          </div>
          
          <div className="backdrop-blur-lg bg-white/10 border border-white/20 rounded-2xl p-6 text-center">
            <div className="text-3xl font-bold text-pink-300 mb-2">{stats.aiTransformations}</div>
            <div className="text-white font-medium mb-1">AI Transformations</div>
            <div className="text-sm text-gray-400">Magic moments created</div>
          </div>
          
          <div className="backdrop-blur-lg bg-white/10 border border-white/20 rounded-2xl p-6 text-center">
            <div className="text-3xl font-bold text-cyan-300 mb-2">{stats.favoriteContent}</div>
            <div className="text-white font-medium mb-1">Favorite Content</div>
            <div className="text-sm text-gray-400">Your loved creations</div>
          </div>
          
          <div className="backdrop-blur-lg bg-white/10 border border-white/20 rounded-2xl p-6 text-center">
            <div className="text-3xl font-bold text-green-300 mb-2">{stats.streakDays}</div>
            <div className="text-white font-medium mb-1">Day Streak</div>
            <div className="text-sm text-gray-400">Keep it going! 🔥</div>
          </div>
        </div>

        {/* Quick Actions */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <Link
            to="/submit"
            className="backdrop-blur-lg bg-gradient-to-r from-purple-600/20 to-pink-600/20 border border-purple-500/30 rounded-2xl p-6 hover:from-purple-600/30 hover:to-pink-600/30 transition-all duration-300 transform hover:scale-105 group"
          >
            <div className="text-4xl mb-3 group-hover:animate-bounce">🚀</div>
            <h3 className="text-xl font-bold text-white mb-2">New Rant</h3>
            <p className="text-gray-300">Express yourself and let AI work its magic</p>
          </Link>
          
          <Link
            to="/chat"
            className="backdrop-blur-lg bg-gradient-to-r from-blue-600/20 to-cyan-600/20 border border-blue-500/30 rounded-2xl p-6 hover:from-blue-600/30 hover:to-cyan-600/30 transition-all duration-300 transform hover:scale-105 group"
          >
            <div className="text-4xl mb-3 group-hover:animate-bounce">🤖</div>
            <h3 className="text-xl font-bold text-white mb-2">AI Chat</h3>
            <p className="text-gray-300">Have a conversation with our AI assistant</p>
          </Link>
          
          <Link
            to="/history"
            className="backdrop-blur-lg bg-gradient-to-r from-green-600/20 to-teal-600/20 border border-green-500/30 rounded-2xl p-6 hover:from-green-600/30 hover:to-teal-600/30 transition-all duration-300 transform hover:scale-105 group"
          >
            <div className="text-4xl mb-3 group-hover:animate-bounce">📚</div>
            <h3 className="text-xl font-bold text-white mb-2">Content History</h3>
            <p className="text-gray-300">Browse your transformed creations</p>
          </Link>
        </div>

        {/* Recent Rants */}
        <div className="backdrop-blur-lg bg-white/10 border border-white/20 rounded-2xl p-6">
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-2xl font-bold text-white">Recent Rants</h2>
            <Link
              to="/history"
              className="text-purple-300 hover:text-purple-200 transition-colors duration-300"
            >
              View All →
            </Link>
          </div>
          
          {recentRants.length === 0 ? (
            <div className="text-center py-8">
              <div className="text-6xl mb-4">😴</div>
              <p className="text-gray-300 text-lg">No rants yet!</p>
              <p className="text-gray-400 mb-4">Start by sharing what's on your mind</p>
              <Link
                to="/submit"
                className="inline-block bg-gradient-to-r from-purple-600 to-pink-600 text-white px-6 py-3 rounded-xl font-medium hover:from-purple-700 hover:to-pink-700 transition-all duration-300 transform hover:scale-105"
              >
                Create Your First Rant 🚀
              </Link>
            </div>
          ) : (
            <div className="space-y-4">
              {recentRants.map((rant) => (
                <div
                  key={rant.id}
                  className="bg-white/5 border border-white/10 rounded-xl p-4 hover:bg-white/10 transition-all duration-300"
                >
                  <div className="flex items-start justify-between">
                    <div className="flex-1">
                      <p className="text-white text-sm mb-2 line-clamp-2">
                        {rant.content}
                      </p>
                      <div className="flex items-center space-x-4 text-xs text-gray-400">
                        <span className="flex items-center">
                          {getTypeIcon(rant.transformedType)} {rant.transformedType}
                        </span>
                        <span>{getTimeAgo(rant.createdAt)}</span>
                      </div>
                    </div>
                    <button className="text-purple-300 hover:text-purple-200 transition-colors duration-300 ml-4">
                      →
                    </button>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
