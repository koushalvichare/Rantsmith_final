import React, { useState, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { useNotification } from '../contexts/NotificationContext';

const ContentHistory = () => {
  const { user } = useAuth();
  const { showNotification } = useNotification();
  const [content, setContent] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState('all');
  const [sortBy, setSortBy] = useState('newest');
  const [selectedContent, setSelectedContent] = useState(null);

  const contentTypes = [
    { value: 'all', label: 'All Content', icon: '📚' },
    { value: 'poem', label: 'Poems', icon: '📝' },
    { value: 'rap', label: 'Rap', icon: '🎤' },
    { value: 'story', label: 'Stories', icon: '📖' },
    { value: 'song', label: 'Songs', icon: '🎵' },
    { value: 'motivational', label: 'Motivational', icon: '💪' },
    { value: 'comedy', label: 'Comedy', icon: '😂' }
  ];

  const sortOptions = [
    { value: 'newest', label: 'Newest First' },
    { value: 'oldest', label: 'Oldest First' },
    { value: 'type', label: 'By Type' },
    { value: 'favorites', label: 'Favorites First' }
  ];

  useEffect(() => {
    fetchContent();
  }, []);

  const fetchContent = async () => {
    try {
      // Simulate API call - replace with actual API endpoint
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      const mockContent = [
        {
          id: 1,
          original: "I'm so tired of Monday mornings and having to wake up early for work. It's like the weekend just flies by and suddenly I'm back to the grind.",
          transformed: "Monday mornings, oh how they taunt,\nWith alarms that ring and dreams that haunt,\nThe weekend's joy has slipped away,\nAs work begins another day.\n\nBut in this rhythm, life unfolds,\nWith stories yet to be told,\nEach Monday brings a chance anew,\nTo chase the dreams that live in you.",
          type: 'poem',
          tone: 'neutral',
          createdAt: '2024-01-15T10:30:00Z',
          isFavorite: true,
          privacy: 'private'
        },
        {
          id: 2,
          original: "Traffic jams are the worst! I've been stuck here for 30 minutes and I'm going to be late for my meeting.",
          transformed: "Yo, check it, I'm stuck in traffic, can't move,\nThirty minutes wasted, ain't got nothing to prove,\nMeeting's waiting, time is slipping away,\nBut I'mma keep my cool, that's how I play.\n\nTraffic jams, they test your patience,\nBut I stay calm, no frustration,\nEvery minute's a chance to think,\nStay focused, don't let your spirit sink.",
          type: 'rap',
          tone: 'positive',
          createdAt: '2024-01-14T16:45:00Z',
          isFavorite: false,
          privacy: 'private'
        },
        {
          id: 3,
          original: "My coffee maker broke this morning and I had to rush to work without my usual caffeine fix. The whole day feels off now.",
          transformed: "Once upon a time, there was a coffee lover who faced their greatest challenge yet - a broken coffee maker on the most important morning of the week.\n\nAs they stood in their kitchen, staring at the lifeless machine, they realized this wasn't just about caffeine. It was about ritual, comfort, and the small things that make each day special.\n\nBut sometimes, the best stories come from the unexpected moments when our usual routines are disrupted, forcing us to discover new strengths within ourselves...",
          type: 'story',
          tone: 'dramatic',
          createdAt: '2024-01-13T08:15:00Z',
          isFavorite: true,
          privacy: 'public'
        },
        {
          id: 4,
          original: "I keep procrastinating on my important project and I know I should just start, but I can't seem to motivate myself.",
          transformed: "Listen up, champion! 💪 That project isn't going to complete itself, but here's the thing - you already have everything you need to succeed.\n\nProcrastination is just fear in disguise. Fear of not being perfect, fear of failure, fear of success. But you know what? Every expert was once a beginner. Every success story started with a single step.\n\nYour future self is counting on the decision you make right now. Stop waiting for the perfect moment - the perfect moment is NOW. Break it down into small steps, celebrate each victory, and remember: progress over perfection, always.\n\nYou've got this! The world needs what you have to offer. ✨",
          type: 'motivational',
          tone: 'positive',
          createdAt: '2024-01-12T14:20:00Z',
          isFavorite: false,
          privacy: 'private'
        },
        {
          id: 5,
          original: "My neighbor's dog barks all night and I can't sleep. I've tried everything but nothing works.",
          transformed: "So there I was, lying in bed at 3 AM, listening to what I can only assume was my neighbor's dog auditioning for America's Got Talent. \n\nThis dog has range, people! From the classic 'mailman alert' bark to the sophisticated 'leaf fell from tree' symphony. I'm pretty sure it's trying to communicate with aliens at this point.\n\nI've considered learning dog language, buying industrial-strength earplugs, or maybe just accepting that I now live in a 24/7 concert venue. Who needs sleep when you can have free entertainment, right? 😂\n\nMaybe I should start charging admission for the 'Midnight Bark Concert Series' happening outside my window!",
          type: 'comedy',
          tone: 'humorous',
          createdAt: '2024-01-11T22:00:00Z',
          isFavorite: true,
          privacy: 'public'
        }
      ];

      setContent(mockContent);
    } catch (error) {
      showNotification('Failed to load content history 😞', 'error');
    } finally {
      setLoading(false);
    }
  };

  const getFilteredAndSortedContent = () => {
    let filtered = content;
    
    if (filter !== 'all') {
      filtered = content.filter(item => item.type === filter);
    }

    switch (sortBy) {
      case 'newest':
        return filtered.sort((a, b) => new Date(b.createdAt) - new Date(a.createdAt));
      case 'oldest':
        return filtered.sort((a, b) => new Date(a.createdAt) - new Date(b.createdAt));
      case 'type':
        return filtered.sort((a, b) => a.type.localeCompare(b.type));
      case 'favorites':
        return filtered.sort((a, b) => b.isFavorite - a.isFavorite);
      default:
        return filtered;
    }
  };

  const toggleFavorite = (id) => {
    setContent(prev => 
      prev.map(item => 
        item.id === id ? { ...item, isFavorite: !item.isFavorite } : item
      )
    );
    showNotification('Updated favorites! ⭐', 'success');
  };

  const deleteContent = (id) => {
    setContent(prev => prev.filter(item => item.id !== id));
    showNotification('Content deleted 🗑️', 'success');
    setSelectedContent(null);
  };

  const shareContent = (content) => {
    if (navigator.share) {
      navigator.share({
        title: `My ${content.type} from RantSmith AI`,
        text: content.transformed,
        url: window.location.href
      });
    } else {
      navigator.clipboard.writeText(content.transformed);
      showNotification('Content copied to clipboard! 📋', 'success');
    }
  };

  const getTimeAgo = (dateString) => {
    const date = new Date(dateString);
    const now = new Date();
    const diffInHours = Math.floor((now - date) / (1000 * 60 * 60));
    
    if (diffInHours < 1) return 'Just now';
    if (diffInHours < 24) return `${diffInHours}h ago`;
    const diffInDays = Math.floor(diffInHours / 24);
    if (diffInDays === 1) return 'Yesterday';
    if (diffInDays < 7) return `${diffInDays}d ago`;
    return date.toLocaleDateString();
  };

  const getTypeIcon = (type) => {
    const typeObj = contentTypes.find(t => t.value === type);
    return typeObj ? typeObj.icon : '✨';
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-purple-900 via-blue-900 to-indigo-900 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-white mx-auto mb-4"></div>
          <p className="text-white">Loading your content history...</p>
        </div>
      </div>
    );
  }

  const filteredContent = getFilteredAndSortedContent();

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-900 via-blue-900 to-indigo-900 pt-20 pb-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-white mb-2">📚 Content History</h1>
          <p className="text-xl text-gray-300">Your collection of AI-transformed creations</p>
        </div>

        {/* Filters and Sort */}
        <div className="backdrop-blur-lg bg-white/10 border border-white/20 rounded-2xl p-6 mb-8">
          <div className="flex flex-col lg:flex-row gap-6">
            {/* Content Type Filter */}
            <div className="flex-1">
              <label className="block text-white font-medium mb-3">Filter by Type:</label>
              <div className="flex flex-wrap gap-2">
                {contentTypes.map((type) => (
                  <button
                    key={type.value}
                    onClick={() => setFilter(type.value)}
                    className={`px-4 py-2 rounded-xl border-2 transition-all duration-300 ${
                      filter === type.value
                        ? 'border-purple-500 bg-purple-600/20 text-white'
                        : 'border-white/20 bg-white/5 text-gray-300 hover:bg-white/10'
                    }`}
                  >
                    {type.icon} {type.label}
                  </button>
                ))}
              </div>
            </div>

            {/* Sort Options */}
            <div className="lg:w-48">
              <label className="block text-white font-medium mb-3">Sort by:</label>
              <select
                value={sortBy}
                onChange={(e) => setSortBy(e.target.value)}
                className="w-full px-4 py-2 bg-white/20 border border-white/30 rounded-xl text-white focus:outline-none focus:ring-2 focus:ring-purple-500"
              >
                {sortOptions.map((option) => (
                  <option key={option.value} value={option.value} className="bg-gray-800">
                    {option.label}
                  </option>
                ))}
              </select>
            </div>
          </div>
        </div>

        {/* Content Grid */}
        {filteredContent.length === 0 ? (
          <div className="text-center py-12">
            <div className="text-6xl mb-4">📭</div>
            <h2 className="text-2xl font-bold text-white mb-2">No content found</h2>
            <p className="text-gray-300 mb-6">
              {filter === 'all' 
                ? "You haven't created any content yet! Start by submitting your first rant."
                : `No ${filter} content found. Try a different filter or create some new content.`}
            </p>
            <button
              onClick={() => window.location.href = '/submit'}
              className="bg-gradient-to-r from-purple-600 to-pink-600 text-white px-6 py-3 rounded-xl font-medium hover:from-purple-700 hover:to-pink-700 transition-all duration-300 transform hover:scale-105"
            >
              Create Your First Rant 🚀
            </button>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {filteredContent.map((item) => (
              <div
                key={item.id}
                className="backdrop-blur-lg bg-white/10 border border-white/20 rounded-2xl p-6 hover:bg-white/15 transition-all duration-300 cursor-pointer"
                onClick={() => setSelectedContent(item)}
              >
                <div className="flex items-start justify-between mb-4">
                  <div className="flex items-center space-x-2">
                    <span className="text-2xl">{getTypeIcon(item.type)}</span>
                    <div>
                      <h3 className="text-white font-medium capitalize">{item.type}</h3>
                      <p className="text-xs text-gray-400">{getTimeAgo(item.createdAt)}</p>
                    </div>
                  </div>
                  <div className="flex items-center space-x-2">
                    <button
                      onClick={(e) => {
                        e.stopPropagation();
                        toggleFavorite(item.id);
                      }}
                      className={`transition-all duration-300 ${
                        item.isFavorite ? 'text-yellow-400 scale-110' : 'text-gray-400 hover:text-yellow-400'
                      }`}
                    >
                      ⭐
                    </button>
                    <span className={`text-xs px-2 py-1 rounded-full ${
                      item.privacy === 'private' ? 'bg-gray-600 text-gray-200' : 'bg-green-600 text-white'
                    }`}>
                      {item.privacy === 'private' ? '🔒' : '🌍'}
                    </span>
                  </div>
                </div>
                
                <p className="text-gray-300 text-sm mb-3 line-clamp-2">
                  {item.original}
                </p>
                
                <div className="bg-white/5 rounded-xl p-3 border border-white/10">
                  <p className="text-white text-sm line-clamp-3">
                    {item.transformed}
                  </p>
                </div>
              </div>
            ))}
          </div>
        )}

        {/* Content Modal */}
        {selectedContent && (
          <div className="fixed inset-0 bg-black/50 flex items-center justify-center p-4 z-50">
            <div className="backdrop-blur-lg bg-white/10 border border-white/20 rounded-2xl p-6 max-w-4xl w-full max-h-[90vh] overflow-y-auto">
              <div className="flex items-start justify-between mb-6">
                <div className="flex items-center space-x-3">
                  <span className="text-3xl">{getTypeIcon(selectedContent.type)}</span>
                  <div>
                    <h2 className="text-2xl font-bold text-white capitalize">{selectedContent.type}</h2>
                    <p className="text-gray-300">{getTimeAgo(selectedContent.createdAt)}</p>
                  </div>
                </div>
                <button
                  onClick={() => setSelectedContent(null)}
                  className="text-gray-400 hover:text-white transition-colors duration-300"
                >
                  ✕
                </button>
              </div>

              <div className="space-y-6">
                <div>
                  <h3 className="text-lg font-bold text-white mb-3">📝 Original Rant</h3>
                  <div className="bg-white/5 border border-white/10 rounded-xl p-4">
                    <p className="text-gray-300 leading-relaxed">{selectedContent.original}</p>
                  </div>
                </div>

                <div>
                  <h3 className="text-lg font-bold text-white mb-3">
                    {getTypeIcon(selectedContent.type)} Transformed {selectedContent.type}
                  </h3>
                  <div className="bg-gradient-to-r from-purple-600/20 to-pink-600/20 border border-purple-500/30 rounded-xl p-4">
                    <p className="text-white leading-relaxed whitespace-pre-line">{selectedContent.transformed}</p>
                  </div>
                </div>

                <div className="flex flex-wrap gap-4 justify-center">
                  <button
                    onClick={() => toggleFavorite(selectedContent.id)}
                    className={`px-6 py-3 rounded-xl font-medium transition-all duration-300 transform hover:scale-105 ${
                      selectedContent.isFavorite
                        ? 'bg-yellow-600 text-white hover:bg-yellow-700'
                        : 'bg-white/20 text-white hover:bg-white/30 border border-white/30'
                    }`}
                  >
                    {selectedContent.isFavorite ? '⭐ Remove from Favorites' : '⭐ Add to Favorites'}
                  </button>
                  <button
                    onClick={() => shareContent(selectedContent)}
                    className="bg-gradient-to-r from-blue-600 to-cyan-600 text-white px-6 py-3 rounded-xl font-medium hover:from-blue-700 hover:to-cyan-700 transition-all duration-300 transform hover:scale-105"
                  >
                    Share 🚀
                  </button>
                  <button
                    onClick={() => deleteContent(selectedContent.id)}
                    className="bg-red-600 text-white px-6 py-3 rounded-xl font-medium hover:bg-red-700 transition-all duration-300 transform hover:scale-105"
                  >
                    Delete 🗑️
                  </button>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default ContentHistory;
