const API_BASE_URL = 'http://localhost:5000';

class APIService {
  constructor() {
    this.token = localStorage.getItem('authToken');
  }

  setAuthToken(token) {
    this.token = token;
    if (token) {
      localStorage.setItem('authToken', token);
    } else {
      localStorage.removeItem('authToken');
    }
  }

  getAuthHeaders() {
    return {
      'Content-Type': 'application/json',
      ...(this.token && { Authorization: `Bearer ${this.token}` })
    };
  }

  async makeRequest(endpoint, options = {}) {
    const url = `${API_BASE_URL}${endpoint}`;
    const config = {
      headers: this.getAuthHeaders(),
      ...options
    };

    try {
      const response = await fetch(url, config);
      
      if (!response.ok) {
        let errorMessage = 'Request failed';
        try {
          const error = await response.json();
          errorMessage = error.error || error.message || errorMessage;
        } catch (parseError) {
          errorMessage = `HTTP ${response.status}: ${response.statusText}`;
        }
        throw new Error(errorMessage);
      }

      return await response.json();
    } catch (error) {
      console.error('API Request failed:', error);
      throw error;
    }
  }

  // Auth endpoints
  async login(email, password) {
    console.log('🌐 API: Attempting login request to /auth/login');
    const response = await this.makeRequest('/auth/login', {
      method: 'POST',
      body: JSON.stringify({ email, password })
    });
    
    console.log('🌐 API: Login response received:', response);
    
    if (response.token) {
      console.log('🌐 API: Setting auth token');
      this.setAuthToken(response.token);
    }
    
    return response;
  }

  async register(username, email, password) {
    console.log('🌐 API: Attempting register request to /auth/register');
    const response = await this.makeRequest('/auth/register', {
      method: 'POST',
      body: JSON.stringify({ username, email, password })
    });
    
    console.log('🌐 API: Register response received:', response);
    
    if (response.token) {
      console.log('🌐 API: Setting auth token');
      this.setAuthToken(response.token);
    }
    
    return response;
  }

  async logout() {
    try {
      await this.makeRequest('/auth/logout', {
        method: 'POST'
      });
    } finally {
      this.setAuthToken(null);
    }
  }

  async getCurrentUser() {
    return await this.makeRequest('/auth/user');
  }

  // Rant endpoints
  async submitRant(content, transformationType, tone, privacy) {
    return await this.makeRequest('/api/rant', {
      method: 'POST',
      body: JSON.stringify({
        content,
        transformation_type: transformationType,
        tone,
        privacy
      })
    });
  }

  async getRants(page = 1, limit = 10, filter = null) {
    const params = new URLSearchParams({
      page: page.toString(),
      limit: limit.toString(),
      ...(filter && { filter })
    });
    
    return await this.makeRequest(`/api/rant?${params}`);
  }

  async getRant(id) {
    return await this.makeRequest(`/api/rant/${id}`);
  }

  async deleteRant(id) {
    return await this.makeRequest(`/api/rant/${id}`, {
      method: 'DELETE'
    });
  }

  async toggleRantFavorite(id) {
    return await this.makeRequest(`/api/rant/${id}/favorite`, {
      method: 'POST'
    });
  }

  // AI Processing endpoints
  async transformRant(content, transformationType, tone) {
    return await this.makeRequest('/api/ai/transform', {
      method: 'POST',
      body: JSON.stringify({
        content,
        transformation_type: transformationType,
        tone
      })
    });
  }

  async chatWithAI(message, conversationId = null) {
    return await this.makeRequest('/api/ai/chat', {
      method: 'POST',
      body: JSON.stringify({
        message,
        conversation_id: conversationId
      })
    });
  }

  async getChatHistory(conversationId) {
    return await this.makeRequest(`/ai/chat/${conversationId}`);
  }

  // Content endpoints
  async getContentHistory(page = 1, limit = 10, type = null) {
    const params = new URLSearchParams({
      page: page.toString(),
      limit: limit.toString(),
      ...(type && { type })
    });
    
    return await this.makeRequest(`/content?${params}`);
  }

  async getContent(id) {
    return await this.makeRequest(`/content/${id}`);
  }

  async deleteContent(id) {
    return await this.makeRequest(`/content/${id}`, {
      method: 'DELETE'
    });
  }

  async toggleContentFavorite(id) {
    return await this.makeRequest(`/content/${id}/favorite`, {
      method: 'POST'
    });
  }

  // User endpoints
  async getUserProfile() {
    return await this.makeRequest('/api/user/profile');
  }

  async updateUserProfile(profileData) {
    return await this.makeRequest('/api/user/profile', {
      method: 'PUT',
      body: JSON.stringify(profileData)
    });
  }

  async getUserPreferences() {
    return await this.makeRequest('/api/user/preferences');
  }

  async updateUserPreferences(preferences) {
    return await this.makeRequest('/api/user/preferences', {
      method: 'PUT',
      body: JSON.stringify(preferences)
    });
  }

  async deleteUserAccount() {
    return await this.makeRequest('/api/user/account', {
      method: 'DELETE'
    });
  }

  // Stats endpoints
  async getUserStats() {
    return await this.makeRequest('/api/user/stats');
  }

  async getDashboardData() {
    return await this.makeRequest('/dashboard');
  }

  // Health check
  async healthCheck() {
    return await this.makeRequest('/health');
  }
}

export default new APIService();
