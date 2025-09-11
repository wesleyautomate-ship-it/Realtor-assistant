import axios from 'axios';

// Create a custom axios instance with global configuration
const apiClient = axios.create({
  baseURL: process.env.REACT_APP_API_URL || 'http://localhost:8003',
  timeout: 30000, // 30 seconds timeout
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add auth token
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('authToken');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor for global error handling and retry logic
apiClient.interceptors.response.use(
  (response) => {
    return response;
  },
  async (error) => {
    const originalRequest = error.config;

    // Retry logic for network errors or 5xx server errors
    if (
      !originalRequest._retry &&
      (error.code === 'ECONNABORTED' || 
       error.code === 'ERR_NETWORK' ||
       (error.response && error.response.status >= 500))
    ) {
      originalRequest._retry = true;
      
      // Wait 1 second before retrying
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      console.log(`Retrying request: ${originalRequest.url}`);
      return apiClient(originalRequest);
    }

    // Handle authentication errors
    if (error.response && error.response.status === 401) {
      // Clear invalid token
      localStorage.removeItem('authToken');
      
      // Redirect to login if not already there
      if (window.location.pathname !== '/login') {
        window.location.href = '/login';
      }
    }

    // Handle other errors
    if (error.response) {
      // Server responded with error status
      console.error('API Error Response:', {
        status: error.response.status,
        statusText: error.response.statusText,
        data: error.response.data,
        url: error.config.url,
        method: error.config.method
      });
    } else if (error.request) {
      // Request was made but no response received
      console.error('API Network Error:', {
        message: error.message,
        url: error.config.url,
        method: error.config.method
      });
    } else {
      // Something else happened
      console.error('API Error:', error.message);
    }

    return Promise.reject(error);
  }
);

// Helper functions for common HTTP methods with better error handling
export const api = {
  // GET request
  get: async (url, config = {}) => {
    try {
      const response = await apiClient.get(url, config);
      return response.data;
    } catch (error) {
      throw createApiError(error);
    }
  },

  // POST request
  post: async (url, data = {}, config = {}) => {
    try {
      const response = await apiClient.post(url, data, config);
      return response.data;
    } catch (error) {
      throw createApiError(error);
    }
  },

  // PUT request
  put: async (url, data = {}, config = {}) => {
    try {
      const response = await apiClient.put(url, data, config);
      return response.data;
    } catch (error) {
      throw createApiError(error);
    }
  },

  // DELETE request
  delete: async (url, config = {}) => {
    try {
      const response = await apiClient.delete(url, config);
      return response.data;
    } catch (error) {
      throw createApiError(error);
    }
  },

  // PATCH request
  patch: async (url, data = {}, config = {}) => {
    try {
      const response = await apiClient.patch(url, data, config);
      return response.data;
    } catch (error) {
      throw createApiError(error);
    }
  },

  // File upload with progress tracking
  upload: async (url, formData, onProgress = null, config = {}) => {
    try {
      const response = await apiClient.post(url, formData, {
        ...config,
        headers: {
          'Content-Type': 'multipart/form-data',
          ...config.headers,
        },
        onUploadProgress: onProgress,
      });
      return response.data;
    } catch (error) {
      throw createApiError(error);
    }
  },

  // Health check
  health: async () => {
    try {
      const response = await apiClient.get('/health', { timeout: 5000 });
      return response.data;
    } catch (error) {
      throw createApiError(error);
    }
  },

  // Property Detection API
  detectProperty: async (message) => {
    try {
      const response = await apiClient.post('/property/detect', { message });
      return response.data;
    } catch (error) {
      throw createApiError(error);
    }
  },

  // Document Processing API
  processDocument: async (file, sessionId = null) => {
    try {
      const formData = new FormData();
      formData.append('file', file);
      if (sessionId) {
        formData.append('session_id', sessionId);
      }

      const response = await apiClient.post('/document/process', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      return response.data;
    } catch (error) {
      throw createApiError(error);
    }
  },

  // Property Search API
  searchProperties: async (filters = {}) => {
    try {
      const params = new URLSearchParams();
      Object.entries(filters).forEach(([key, value]) => {
        if (value !== null && value !== undefined && value !== '') {
          params.append(key, value);
        }
      });
      
      const response = await apiClient.get(`/properties/search?${params.toString()}`);
      return response.data;
    } catch (error) {
      throw createApiError(error);
    }
  },

  // Building-Specific Data API
  getBuildingData: async (buildingName, community = null) => {
    try {
      const params = new URLSearchParams();
      params.append('building_name', buildingName);
      if (community) {
        params.append('community', community);
      }
      
      const response = await apiClient.get(`/properties/building?${params.toString()}`);
      return response.data;
    } catch (error) {
      throw createApiError(error);
    }
  },

  // Community Market Data API
  getCommunityMarketData: async (community) => {
    try {
      const response = await apiClient.get(`/market/community/${encodeURIComponent(community)}`);
      return response.data;
    } catch (error) {
      throw createApiError(error);
    }
  },

  // Basic Chat API
  sendMessage: async (message, sessionId = null) => {
    try {
      const payload = { message };
      if (sessionId) {
        payload.session_id = sessionId;
      }
      const response = await apiClient.post('/chat', payload);
      return response.data;
    } catch (error) {
      throw createApiError(error);
    }
  },

  // Session Management API
  createSession: async () => {
    try {
      const response = await apiClient.post('/sessions');
      return response.data;
    } catch (error) {
      throw createApiError(error);
    }
  },

  getConversationHistory: async (sessionId) => {
    try {
      const response = await apiClient.get(`/conversation/${sessionId}`);
      return response.data;
    } catch (error) {
      throw createApiError(error);
    }
  },

  // Enhanced Conversation Management API
  createNewConversation: async () => {
    try {
      const response = await apiClient.post('/sessions', {
        title: null, // Will be auto-generated from first message
        role: 'client'
      });
      return response.data;
    } catch (error) {
      throw createApiError(error);
    }
  },

  getConversations: async () => {
    try {
      const response = await apiClient.get('/sessions');
      return response.data;
    } catch (error) {
      throw createApiError(error);
    }
  },

  getConversation: async (sessionId) => {
    try {
      const response = await apiClient.get(`/sessions/${sessionId}`);
      return response.data;
    } catch (error) {
      throw createApiError(error);
    }
  },

  updateConversation: async (sessionId, updates) => {
    try {
      const response = await apiClient.put(`/sessions/${sessionId}`, updates);
      return response.data;
    } catch (error) {
      throw createApiError(error);
    }
  },

  deleteConversation: async (sessionId) => {
    try {
      const response = await apiClient.delete(`/sessions/${sessionId}`);
      return response.data;
    } catch (error) {
      throw createApiError(error);
    }
  },

  clearConversation: async (sessionId) => {
    try {
      const response = await apiClient.post(`/sessions/${sessionId}/clear`);
      return response.data;
    } catch (error) {
      throw createApiError(error);
    }
  },

  // Enhanced Chat API with Property Detection and Entity Detection
  sendMessageWithPropertyDetection: async (sessionId, message, fileUpload = null, detectEntities = true) => {
    try {
      const payload = {
        message,
        session_id: sessionId,
        enable_property_detection: true,
        detect_entities: detectEntities,
      };

      if (fileUpload) {
        payload.file_upload = { file_id: fileUpload.id };
      }

      const response = await apiClient.post(`/sessions/${sessionId}/chat`, payload);
      return response.data;
    } catch (error) {
      throw createApiError(error);
    }
  },

  // Entity Detection API
  detectEntities: async (message, sessionId) => {
    try {
      if (!sessionId) {
        throw new Error('Session ID is required for entity detection');
      }
      const response = await apiClient.post(`/sessions/${sessionId}/advanced/detect-entities`, { message });
      return response.data;
    } catch (error) {
      throw createApiError(error);
    }
  },

  // Entity Context API
  fetchEntityContext: async (entityType, entityId, sessionId) => {
    try {
      if (!sessionId) {
        throw new Error('Session ID is required for entity context fetching');
      }
      const response = await apiClient.get(`/sessions/${sessionId}/advanced/context/${entityType}/${entityId}`);
      return response.data;
    } catch (error) {
      throw createApiError(error);
    }
  },

  // ML Insights API
  getMarketPredictions: async (area, propertyType, timeframe = '6m') => {
    try {
      const response = await apiClient.post('/ml-insights/market-predictions', {
        area,
        property_type: propertyType,
        timeframe
      });
      return response.data;
    } catch (error) {
      throw createApiError(error);
    }
  },

  getPropertyValuation: async (propertyData) => {
    try {
      const response = await apiClient.post('/ml-insights/property-valuation', propertyData);
      return response.data;
    } catch (error) {
      throw createApiError(error);
    }
  },

  getInvestmentOpportunities: async (criteria) => {
    try {
      const response = await apiClient.post('/ml-insights/investment-opportunities', criteria);
      return response.data;
    } catch (error) {
      throw createApiError(error);
    }
  },

  getMarketTrends: async (area, period = '1y') => {
    try {
      const response = await apiClient.get(`/ml-insights/market-trends?area=${encodeURIComponent(area)}&period=${period}`);
      return response.data;
    } catch (error) {
      throw createApiError(error);
    }
  },

  // Advanced Market Data API
  getMarketOverview: async () => {
    try {
      const response = await apiClient.get('/market/overview');
      return response.data;
    } catch (error) {
      throw createApiError(error);
    }
  },

  getAreaAnalysis: async (areaName) => {
    try {
      const response = await apiClient.get(`/market/areas/${encodeURIComponent(areaName)}`);
      return response.data;
    } catch (error) {
      throw createApiError(error);
    }
  },

  getUsageAnalytics: async (period = '30d') => {
    try {
      const response = await apiClient.get(`/analytics/usage?period=${period}`);
      return response.data;
    } catch (error) {
      throw createApiError(error);
    }
  },

  getPerformanceAnalytics: async () => {
    try {
      const response = await apiClient.get('/analytics/performance');
      return response.data;
    } catch (error) {
      throw createApiError(error);
    }
  },

  // Property Detection API
  detectPropertyFromImage: async (imageFile, sessionId = null) => {
    try {
      const formData = new FormData();
      formData.append('image', imageFile);
      if (sessionId) {
        formData.append('session_id', sessionId);
      }

      const response = await apiClient.post('/property-detection/analyze-image', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      return response.data;
    } catch (error) {
      throw createApiError(error);
    }
  },

  detectPropertyFromText: async (text, sessionId = null) => {
    try {
      const payload = { text };
      if (sessionId) {
        payload.session_id = sessionId;
      }

      const response = await apiClient.post('/property-detection/analyze-text', payload);
      return response.data;
    } catch (error) {
      throw createApiError(error);
    }
  },

  // Lead Nurturing API
  getLeadNurturingCampaigns: async () => {
    try {
      const response = await apiClient.get('/nurturing/campaigns');
      return response.data;
    } catch (error) {
      throw createApiError(error);
    }
  },

  createNurturingCampaign: async (campaignData) => {
    try {
      const response = await apiClient.post('/nurturing/campaigns', campaignData);
      return response.data;
    } catch (error) {
      throw createApiError(error);
    }
  },

  getLeadScoring: async (contactId) => {
    try {
      const response = await apiClient.get(`/nurturing/lead-scoring/${contactId}`);
      return response.data;
    } catch (error) {
      throw createApiError(error);
    }
  },

  scheduleFollowUp: async (contactId, followUpData) => {
    try {
      const response = await apiClient.post(`/nurturing/follow-up/${contactId}`, followUpData);
      return response.data;
    } catch (error) {
      throw createApiError(error);
    }
  },

  getAutomatedFollowUps: async () => {
    try {
      const response = await apiClient.get('/nurturing/automated-follow-ups');
      return response.data;
    } catch (error) {
      throw createApiError(error);
    }
  },

  // Report Generation API
  generateReport: async (reportType, parameters = {}) => {
    try {
      const response = await apiClient.post('/reports/generate', {
        report_type: reportType,
        parameters
      });
      return response.data;
    } catch (error) {
      throw createApiError(error);
    }
  },

  getReportTemplates: async () => {
    try {
      const response = await apiClient.get('/reports/templates');
      return response.data;
    } catch (error) {
      throw createApiError(error);
    }
  },

  downloadReport: async (reportId) => {
    try {
      const response = await apiClient.get(`/reports/${reportId}/download`, {
        responseType: 'blob'
      });
      return response.data;
    } catch (error) {
      throw createApiError(error);
    }
  },

  // AI Request Management API
  createAIRequest: async (requestData) => {
    try {
      const response = await apiClient.post('/ai-requests', requestData);
      return response.data;
    } catch (error) {
      throw createApiError(error);
    }
  },

  getAIRequests: async (status = null) => {
    try {
      const url = status ? `/ai-requests?status=${status}` : '/ai-requests';
      const response = await apiClient.get(url);
      return response.data;
    } catch (error) {
      throw createApiError(error);
    }
  },

  getAIRequestStatus: async (requestId) => {
    try {
      const response = await apiClient.get(`/ai-requests/${requestId}/status`);
      return response.data;
    } catch (error) {
      throw createApiError(error);
    }
  },

  // Performance Monitoring API
  getPerformanceMetrics: async () => {
    try {
      const response = await apiClient.get('/performance/metrics');
      return response.data;
    } catch (error) {
      throw createApiError(error);
    }
  },

  getCacheStats: async () => {
    try {
      const response = await apiClient.get('/performance/cache-stats');
      return response.data;
    } catch (error) {
      throw createApiError(error);
    }
  },

  // Feedback API
  submitFeedback: async (feedbackData) => {
    try {
      const response = await apiClient.post('/feedback/submit', feedbackData);
      return response.data;
    } catch (error) {
      throw createApiError(error);
    }
  },

  getFeedbackSummary: async () => {
    try {
      const response = await apiClient.get('/feedback/summary');
      return response.data;
    } catch (error) {
      throw createApiError(error);
    }
  },
};

// Helper function to create consistent error objects
function createApiError(error) {
  if (error.response) {
    // Server responded with error status
    return {
      type: 'API_ERROR',
      status: error.response.status,
      statusText: error.response.statusText,
      message: error.response.data?.detail || error.response.data?.message || 'API request failed',
      data: error.response.data,
      url: error.config?.url,
      method: error.config?.method,
      originalError: error
    };
  } else if (error.code === 'ECONNABORTED') {
    // Request timeout
    return {
      type: 'TIMEOUT_ERROR',
      message: 'Request timed out. Please try again.',
      url: error.config?.url,
      method: error.config?.method,
      originalError: error
    };
  } else if (error.code === 'ERR_NETWORK') {
    // Network error
    return {
      type: 'NETWORK_ERROR',
      message: 'Network error. Please check your connection and try again.',
      url: error.config?.url,
      method: error.config?.method,
      originalError: error
    };
  } else {
    // Other errors
    return {
      type: 'UNKNOWN_ERROR',
      message: error.message || 'An unexpected error occurred',
      url: error.config?.url,
      method: error.config?.method,
      originalError: error
    };
  }
}

// Export the axios instance for direct use if needed
export default apiClient;
