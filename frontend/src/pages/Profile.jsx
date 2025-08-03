import React, { useState, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { useNotification } from '../contexts/NotificationContext';

const Profile = () => {
  const { user, logout } = useAuth();
  const { showNotification } = useNotification();
  const [activeTab, setActiveTab] = useState('profile');
  const [profileData, setProfileData] = useState({
    username: '',
    email: '',
    bio: '',
    favoriteTransformation: 'poem',
    defaultTone: 'neutral',
    privacy: 'private'
  });
  const [stats, setStats] = useState({
    totalRants: 0,
    aiTransformations: 0,
    favoriteContent: 0,
    joinedDate: ''
  });
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);

  useEffect(() => {
    fetchProfileData();
  }, [user]);

  const fetchProfileData = async () => {
    try {
      // Simulate API call - replace with actual API endpoint
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      setProfileData({
        username: user?.username || 'ranter_user',
        email: user?.email || 'user@example.com',
        bio: 'Just someone who loves to transform thoughts into creative expressions! 🌟',
        favoriteTransformation: 'poem',
        defaultTone: 'neutral',
        privacy: 'private'
      });
      
      setStats({
        totalRants: 12,
        aiTransformations: 8,
        favoriteContent: 5,
        joinedDate: '2024-01-01'
      });
    } catch (error) {
      showNotification('Failed to load profile data 😞', 'error');
    } finally {
      setLoading(false);
    }
  };

  const handleSave = async () => {
    setSaving(true);
    try {
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 1000));
      showNotification('Profile updated successfully! 🎉', 'success');
    } catch (error) {
      showNotification('Failed to update profile 😞', 'error');
    } finally {
      setSaving(false);
    }
  };

  const handleDeleteAccount = async () => {
    const confirmed = window.confirm(
      'Are you sure you want to delete your account? This action cannot be undone.'
    );
    
    if (confirmed) {
      try {
        // Simulate API call
        await new Promise(resolve => setTimeout(resolve, 1000));
        showNotification('Account deleted successfully', 'success');
        logout();
      } catch (error) {
        showNotification('Failed to delete account 😞', 'error');
      }
    }
  };

  const transformationTypes = [
    { value: 'poem', label: 'Poetry', icon: '📝' },
    { value: 'rap', label: 'Rap', icon: '🎤' },
    { value: 'story', label: 'Story', icon: '📚' },
    { value: 'song', label: 'Song', icon: '🎵' },
    { value: 'motivational', label: 'Motivational', icon: '💪' },
    { value: 'comedy', label: 'Comedy', icon: '😂' }
  ];

  const tones = [
    { value: 'neutral', label: 'Neutral', icon: '😐' },
    { value: 'positive', label: 'Positive', icon: '😊' },
    { value: 'dramatic', label: 'Dramatic', icon: '🎭' },
    { value: 'sarcastic', label: 'Sarcastic', icon: '😏' },
    { value: 'emotional', label: 'Emotional', icon: '💫' },
    { value: 'humorous', label: 'Humorous', icon: '😄' }
  ];

  const tabs = [
    { id: 'profile', label: 'Profile', icon: '👤' },
    { id: 'preferences', label: 'Preferences', icon: '⚙️' },
    { id: 'privacy', label: 'Privacy', icon: '🔒' },
    { id: 'account', label: 'Account', icon: '🛡️' }
  ];

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-purple-900 via-blue-900 to-indigo-900 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-white mx-auto mb-4"></div>
          <p className="text-white">Loading your profile...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-900 via-blue-900 to-indigo-900 pt-20 pb-8">
      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-white mb-2">👤 Profile Settings</h1>
          <p className="text-xl text-gray-300">Customize your RantSmith AI experience</p>
        </div>

        {/* Profile Stats */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <div className="backdrop-blur-lg bg-white/10 border border-white/20 rounded-2xl p-6 text-center">
            <div className="text-3xl font-bold text-purple-300 mb-2">{stats.totalRants}</div>
            <div className="text-white font-medium">Total Rants</div>
          </div>
          <div className="backdrop-blur-lg bg-white/10 border border-white/20 rounded-2xl p-6 text-center">
            <div className="text-3xl font-bold text-pink-300 mb-2">{stats.aiTransformations}</div>
            <div className="text-white font-medium">AI Transformations</div>
          </div>
          <div className="backdrop-blur-lg bg-white/10 border border-white/20 rounded-2xl p-6 text-center">
            <div className="text-3xl font-bold text-cyan-300 mb-2">{stats.favoriteContent}</div>
            <div className="text-white font-medium">Favorite Content</div>
          </div>
          <div className="backdrop-blur-lg bg-white/10 border border-white/20 rounded-2xl p-6 text-center">
            <div className="text-3xl font-bold text-green-300 mb-2">
              {new Date(stats.joinedDate).toLocaleDateString('en-US', { month: 'short', year: 'numeric' })}
            </div>
            <div className="text-white font-medium">Member Since</div>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
          {/* Sidebar */}
          <div className="backdrop-blur-lg bg-white/10 border border-white/20 rounded-2xl p-6 lg:col-span-1">
            <div className="space-y-2">
              {tabs.map((tab) => (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  className={`w-full flex items-center space-x-3 px-4 py-3 rounded-xl transition-all duration-300 ${
                    activeTab === tab.id
                      ? 'bg-gradient-to-r from-purple-600 to-pink-600 text-white'
                      : 'text-gray-300 hover:bg-white/10'
                  }`}
                >
                  <span className="text-xl">{tab.icon}</span>
                  <span className="font-medium">{tab.label}</span>
                </button>
              ))}
            </div>
          </div>

          {/* Main Content */}
          <div className="backdrop-blur-lg bg-white/10 border border-white/20 rounded-2xl p-6 lg:col-span-3">
            {activeTab === 'profile' && (
              <div className="space-y-6">
                <h2 className="text-2xl font-bold text-white mb-6">Profile Information</h2>
                
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div>
                    <label className="block text-white font-medium mb-2">Username</label>
                    <input
                      type="text"
                      value={profileData.username}
                      onChange={(e) => setProfileData({...profileData, username: e.target.value})}
                      className="w-full px-4 py-3 bg-white/20 border border-white/30 rounded-xl text-white placeholder-gray-300 focus:outline-none focus:ring-2 focus:ring-purple-500"
                    />
                  </div>
                  
                  <div>
                    <label className="block text-white font-medium mb-2">Email</label>
                    <input
                      type="email"
                      value={profileData.email}
                      onChange={(e) => setProfileData({...profileData, email: e.target.value})}
                      className="w-full px-4 py-3 bg-white/20 border border-white/30 rounded-xl text-white placeholder-gray-300 focus:outline-none focus:ring-2 focus:ring-purple-500"
                    />
                  </div>
                </div>

                <div>
                  <label className="block text-white font-medium mb-2">Bio</label>
                  <textarea
                    value={profileData.bio}
                    onChange={(e) => setProfileData({...profileData, bio: e.target.value})}
                    placeholder="Tell us about yourself..."
                    className="w-full h-24 px-4 py-3 bg-white/20 border border-white/30 rounded-xl text-white placeholder-gray-300 focus:outline-none focus:ring-2 focus:ring-purple-500 resize-none"
                  />
                </div>

                <button
                  onClick={handleSave}
                  disabled={saving}
                  className="bg-gradient-to-r from-purple-600 to-pink-600 text-white px-6 py-3 rounded-xl font-medium hover:from-purple-700 hover:to-pink-700 transition-all duration-300 transform hover:scale-105 disabled:opacity-50"
                >
                  {saving ? 'Saving...' : 'Save Changes'}
                </button>
              </div>
            )}

            {activeTab === 'preferences' && (
              <div className="space-y-6">
                <h2 className="text-2xl font-bold text-white mb-6">Preferences</h2>
                
                <div>
                  <label className="block text-white font-medium mb-4">Favorite Transformation Type</label>
                  <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
                    {transformationTypes.map((type) => (
                      <button
                        key={type.value}
                        onClick={() => setProfileData({...profileData, favoriteTransformation: type.value})}
                        className={`p-4 rounded-xl border-2 transition-all duration-300 ${
                          profileData.favoriteTransformation === type.value
                            ? 'border-purple-500 bg-purple-600/20'
                            : 'border-white/20 bg-white/5 hover:bg-white/10'
                        }`}
                      >
                        <div className="text-2xl mb-2">{type.icon}</div>
                        <div className="text-white font-medium">{type.label}</div>
                      </button>
                    ))}
                  </div>
                </div>

                <div>
                  <label className="block text-white font-medium mb-4">Default Tone</label>
                  <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
                    {tones.map((tone) => (
                      <button
                        key={tone.value}
                        onClick={() => setProfileData({...profileData, defaultTone: tone.value})}
                        className={`p-3 rounded-xl border-2 transition-all duration-300 ${
                          profileData.defaultTone === tone.value
                            ? 'border-purple-500 bg-purple-600/20'
                            : 'border-white/20 bg-white/5 hover:bg-white/10'
                        }`}
                      >
                        <div className="text-xl mb-1">{tone.icon}</div>
                        <div className="text-white text-sm font-medium">{tone.label}</div>
                      </button>
                    ))}
                  </div>
                </div>

                <button
                  onClick={handleSave}
                  disabled={saving}
                  className="bg-gradient-to-r from-purple-600 to-pink-600 text-white px-6 py-3 rounded-xl font-medium hover:from-purple-700 hover:to-pink-700 transition-all duration-300 transform hover:scale-105 disabled:opacity-50"
                >
                  {saving ? 'Saving...' : 'Save Preferences'}
                </button>
              </div>
            )}

            {activeTab === 'privacy' && (
              <div className="space-y-6">
                <h2 className="text-2xl font-bold text-white mb-6">Privacy Settings</h2>
                
                <div className="space-y-4">
                  <div className="flex items-center justify-between p-4 bg-white/5 rounded-xl border border-white/10">
                    <div>
                      <h3 className="text-white font-medium">Default Content Privacy</h3>
                      <p className="text-sm text-gray-400">Choose the default privacy setting for your new content</p>
                    </div>
                    <select
                      value={profileData.privacy}
                      onChange={(e) => setProfileData({...profileData, privacy: e.target.value})}
                      className="px-4 py-2 bg-white/20 border border-white/30 rounded-xl text-white focus:outline-none focus:ring-2 focus:ring-purple-500"
                    >
                      <option value="private" className="bg-gray-800">🔒 Private</option>
                      <option value="public" className="bg-gray-800">🌍 Public</option>
                    </select>
                  </div>
                  
                  <div className="flex items-center justify-between p-4 bg-white/5 rounded-xl border border-white/10">
                    <div>
                      <h3 className="text-white font-medium">Profile Visibility</h3>
                      <p className="text-sm text-gray-400">Control who can see your profile</p>
                    </div>
                    <div className="flex items-center">
                      <input
                        type="checkbox"
                        className="mr-2"
                        defaultChecked={false}
                      />
                      <span className="text-white">Public Profile</span>
                    </div>
                  </div>
                  
                  <div className="flex items-center justify-between p-4 bg-white/5 rounded-xl border border-white/10">
                    <div>
                      <h3 className="text-white font-medium">Data Analytics</h3>
                      <p className="text-sm text-gray-400">Help us improve by sharing usage analytics</p>
                    </div>
                    <div className="flex items-center">
                      <input
                        type="checkbox"
                        className="mr-2"
                        defaultChecked={true}
                      />
                      <span className="text-white">Share Analytics</span>
                    </div>
                  </div>
                </div>

                <button
                  onClick={handleSave}
                  disabled={saving}
                  className="bg-gradient-to-r from-purple-600 to-pink-600 text-white px-6 py-3 rounded-xl font-medium hover:from-purple-700 hover:to-pink-700 transition-all duration-300 transform hover:scale-105 disabled:opacity-50"
                >
                  {saving ? 'Saving...' : 'Save Privacy Settings'}
                </button>
              </div>
            )}

            {activeTab === 'account' && (
              <div className="space-y-6">
                <h2 className="text-2xl font-bold text-white mb-6">Account Management</h2>
                
                <div className="space-y-4">
                  <div className="p-4 bg-white/5 rounded-xl border border-white/10">
                    <h3 className="text-white font-medium mb-2">Change Password</h3>
                    <p className="text-sm text-gray-400 mb-4">Update your password to keep your account secure</p>
                    <button className="bg-gradient-to-r from-blue-600 to-cyan-600 text-white px-6 py-3 rounded-xl font-medium hover:from-blue-700 hover:to-cyan-700 transition-all duration-300 transform hover:scale-105">
                      Change Password
                    </button>
                  </div>
                  
                  <div className="p-4 bg-white/5 rounded-xl border border-white/10">
                    <h3 className="text-white font-medium mb-2">Export Data</h3>
                    <p className="text-sm text-gray-400 mb-4">Download all your content and data</p>
                    <button className="bg-gradient-to-r from-green-600 to-teal-600 text-white px-6 py-3 rounded-xl font-medium hover:from-green-700 hover:to-teal-700 transition-all duration-300 transform hover:scale-105">
                      Export Data
                    </button>
                  </div>
                  
                  <div className="p-4 bg-red-500/10 rounded-xl border border-red-500/30">
                    <h3 className="text-red-400 font-medium mb-2">Danger Zone</h3>
                    <p className="text-sm text-gray-400 mb-4">Permanently delete your account and all associated data</p>
                    <button
                      onClick={handleDeleteAccount}
                      className="bg-red-600 text-white px-6 py-3 rounded-xl font-medium hover:bg-red-700 transition-all duration-300 transform hover:scale-105"
                    >
                      Delete Account
                    </button>
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Profile;
