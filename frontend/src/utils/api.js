import axios from 'axios';

// API base URL
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8003';

// Create axios instance with base configuration
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 30000, // 30 seconds timeout
});

// Add request interceptor for authentication
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('authToken');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Add response interceptor for error handling
api.interceptors.response.use(
  (response) => response,
  (error) => {
    // Handle different types of errors
    if (error.response) {
      // Server responded with error status
      const { status, data } = error.response;
      
      switch (status) {
        case 401:
          // Unauthorized - clear token and redirect to login
          localStorage.removeItem('authToken');
          window.location.href = '/login';
          break;
        case 403:
          // Forbidden
          throw new Error('You do not have permission to perform this action');
        case 404:
          // Not found
          throw new Error('The requested resource was not found');
        case 422:
          // Validation error
          const validationErrors = data.detail || 'Validation failed';
          throw new Error(validationErrors);
        case 500:
          // Server error
          throw new Error('Server error. Please try again later.');
        default:
          // Other server errors
          throw new Error(data.detail || `Request failed with status ${status}`);
      }
    } else if (error.request) {
      // Network error
      throw new Error('Network error. Please check your connection and try again.');
    } else {
      // Other errors
      throw new Error('An unexpected error occurred. Please try again.');
    }
  }
);

// API utility functions
export const apiUtils = {
  // Properties API
  getProperties: async (filters = {}) => {
    try {
      const params = new URLSearchParams();
      Object.entries(filters).forEach(([key, value]) => {
        if (value !== null && value !== undefined && value !== '') {
          params.append(key, value);
        }
      });
      
      const response = await api.get(`/properties?${params.toString()}`);
      return response.data;
    } catch (error) {
      console.error('Error fetching properties:', error);
      throw error;
    }
  },

  // Chat API
  sendMessage: async (sessionId, message, fileUpload = null) => {
    try {
      const payload = {
        message,
        session_id: sessionId,
      };

      if (fileUpload) {
        payload.file_upload = { file_id: fileUpload.id };
      }

      const response = await api.post(`/sessions/${sessionId}/chat`, payload);
      return response.data;
    } catch (error) {
      console.error('Error sending message:', error);
      throw error;
    }
  },

  // File upload API
  uploadFile: async (file, sessionId = null) => {
    try {
      const formData = new FormData();
      formData.append('file', file);
      
      if (sessionId) {
        formData.append('session_id', sessionId);
      }

      const response = await api.post('/ingest/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
        onUploadProgress: (progressEvent) => {
          const progress = Math.round((progressEvent.loaded * 100) / progressEvent.total);
          // You can emit this progress to a callback if needed
          console.log(`Upload progress: ${progress}%`);
        },
      });

      return response.data;
    } catch (error) {
      console.error('Error uploading file:', error);
      throw error;
    }
  },

  // Dashboard API
  getDailyBriefing: async () => {
    try {
      const response = await api.post('/admin/trigger-daily-briefing');
      return response.data;
    } catch (error) {
      console.error('Error fetching daily briefing:', error);
      throw error;
    }
  },

  getMarketOverview: async () => {
    try {
      const response = await api.get('/market/overview');
      return response.data;
    } catch (error) {
      console.error('Error fetching market overview:', error);
      throw error;
    }
  },

  // Sessions API
  getSessions: async () => {
    try {
      const response = await api.get('/sessions');
      return response.data.sessions;
    } catch (error) {
      console.error('Error fetching sessions:', error);
      throw error;
    }
  },

  createSession: async () => {
    try {
      const response = await api.post('/sessions', {
        title: "New Chat",
        user_preferences: {}
      });
      return response.data;
    } catch (error) {
      console.error('Error creating session:', error);
      throw error;
    }
  },

  getConversationHistory: async (sessionId) => {
    try {
      const response = await api.get(`/conversation/${sessionId}`);
      return response.data;
    } catch (error) {
      console.error('Error fetching conversation history:', error);
      throw error;
    }
  },

  // Admin files API
  getAdminFiles: async () => {
    try {
      const response = await api.get('/admin/files');
      return response.data;
    } catch (error) {
      console.error('Error fetching admin files:', error);
      throw error;
    }
  },

  deleteAdminFile: async (fileId) => {
    try {
      await api.delete(`/admin/files/${fileId}`);
      return true;
    } catch (error) {
      console.error('Error deleting admin file:', error);
      throw error;
    }
  },

  // Authentication API
  login: async (email, password) => {
    try {
      const response = await api.post('/auth/login', { email, password });
      return response.data;
    } catch (error) {
      console.error('Error during login:', error);
      throw error;
    }
  },

  getCurrentUser: async () => {
    try {
      const response = await api.get('/auth/me');
      return response.data;
    } catch (error) {
      console.error('Error fetching current user:', error);
      throw error;
    }
  },

  // Action engine API
  executeAction: async (action, parameters = {}) => {
    try {
      const response = await api.post('/actions/execute', {
        action,
        parameters,
      });
      return response.data;
    } catch (error) {
      console.error('Error executing action:', error);
      throw error;
    }
  },

  // Async Processing API
  uploadFileAsync: async (file, instructions = '') => {
    try {
      const formData = new FormData();
      formData.append('file', file);
      formData.append('instructions', instructions);

      const response = await api.post('/async/analyze-file', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      return response.data;
    } catch (error) {
      console.error('Error uploading file for async processing:', error);
      throw error;
    }
  },

  getProcessingStatus: async (taskId) => {
    try {
      const response = await api.get(`/async/processing-status/${taskId}`);
      return response.data;
    } catch (error) {
      console.error('Error getting processing status:', error);
      throw error;
    }
  },

  // Agenda API
  getAgenda: async () => {
    try {
      const response = await api.get('/users/me/agenda');
      return response.data;
    } catch (error) {
      console.error('Error fetching agenda:', error);
      throw error;
    }
  },

  // Global Command API
  sendGlobalCommand: async (message) => {
    try {
      // Create a default session if needed or use existing session
      const response = await api.post('/sessions/default/chat', {
        message,
        session_id: 'default'
      });
      return response.data;
    } catch (error) {
      console.error('Error sending global command:', error);
      throw error;
    }
  },

  // Advanced Chat: Entity Detection and Context API
  detectEntities: async (message, sessionId) => {
    try {
      if (!sessionId) {
        throw new Error('Session ID is required for entity detection');
      }
      const response = await api.post(`/sessions/${sessionId}/advanced/detect-entities`, {
        message,
        session_id: sessionId
      });
      return response.data;
    } catch (error) {
      console.error('Error detecting entities:', error);
      throw error;
    }
  },

  fetchEntityContext: async (entityType, entityId, sessionId) => {
    try {
      if (!sessionId) {
        throw new Error('Session ID is required for entity context fetching');
      }
      const response = await api.get(`/sessions/${sessionId}/advanced/context/${entityType}/${entityId}`);
      return response.data;
    } catch (error) {
      console.error('Error fetching entity context:', error);
      throw error;
    }
  },

  getPropertyDetails: async (propertyId, sessionId) => {
    try {
      if (!sessionId) {
        throw new Error('Session ID is required for property details');
      }
      const response = await api.get(`/sessions/${sessionId}/advanced/properties/${propertyId}/details`);
      return response.data;
    } catch (error) {
      console.error('Error fetching property details:', error);
      throw error;
    }
  },

  getClientInfo: async (clientId, sessionId) => {
    try {
      if (!sessionId) {
        throw new Error('Session ID is required for client info');
      }
      const response = await api.get(`/sessions/${sessionId}/advanced/clients/${clientId}`);
      return response.data;
    } catch (error) {
      console.error('Error fetching client info:', error);
      throw error;
    }
  },

  getMarketContext: async (location, propertyType, sessionId) => {
    try {
      if (!sessionId) {
        throw new Error('Session ID is required for market context');
      }
      const params = new URLSearchParams();
      if (location) params.append('location', location);
      if (propertyType) params.append('property_type', propertyType);
      
      const response = await api.get(`/sessions/${sessionId}/advanced/market/context?${params.toString()}`);
      return response.data;
    } catch (error) {
      console.error('Error fetching market context:', error);
      throw error;
    }
  },

  batchFetchContext: async (entities, sessionId) => {
    try {
      if (!sessionId) {
        throw new Error('Session ID is required for batch context');
      }
      const response = await api.post(`/sessions/${sessionId}/advanced/context/batch`, {
        entities: entities.map(entity => ({
          type: entity.type,
          id: entity.id,
          name: entity.name
        }))
      });
      return response.data;
    } catch (error) {
      console.error('Error batch fetching context:', error);
      throw error;
    }
  },

  clearContextCache: async (sessionId) => {
    try {
      if (!sessionId) {
        throw new Error('Session ID is required for cache clearing');
      }
      const response = await api.delete(`/sessions/${sessionId}/advanced/context/cache/clear`);
      return response.data;
    } catch (error) {
      console.error('Error clearing context cache:', error);
      throw error;
    }
  },

  getAdvancedChatHealth: async (sessionId) => {
    try {
      if (!sessionId) {
        throw new Error('Session ID is required for health check');
      }
      const response = await api.get(`/sessions/${sessionId}/advanced/health`);
      return response.data;
    } catch (error) {
      console.error('Error checking Advanced Chat health:', error);
      throw error;
    }
  },
};

// Error handling utility
export const handleApiError = (error) => {
  if (error.response) {
    // Server responded with error status
    const { status, data } = error.response;
    
    switch (status) {
      case 401:
        return 'Please log in to continue';
      case 403:
        return 'You do not have permission to perform this action';
      case 404:
        return 'The requested resource was not found';
      case 422:
        return data.detail || 'Please check your input and try again';
      case 500:
        return 'Server error. Please try again later.';
      default:
        return data.detail || 'An error occurred. Please try again.';
    }
  } else if (error.request) {
    // Network error
    return 'Network error. Please check your connection and try again.';
  } else {
    // Other errors
    return 'An unexpected error occurred. Please try again.';
  }
};

export default api;
