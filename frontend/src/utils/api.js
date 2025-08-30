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
        user_id: localStorage.getItem('userId'),
        session_id: sessionId,
        role: localStorage.getItem('userRole') || 'agent',
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
  uploadFile: async (file, sessionId = null, role = 'agent') => {
    try {
      const formData = new FormData();
      formData.append('file', file);
      
      if (sessionId) {
        formData.append('session_id', sessionId);
      }
      
      formData.append('role', role);

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
        role: "client",
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
};

// Error handling utility
// 💡 Enhancement Suggestion: Consider implementing a global error boundary component
// that uses this handleApiError function to provide consistent error messaging
// across the application. This would improve user experience by showing
// user-friendly error messages instead of technical error details.
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
