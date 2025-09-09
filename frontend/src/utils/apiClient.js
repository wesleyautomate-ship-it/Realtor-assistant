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
