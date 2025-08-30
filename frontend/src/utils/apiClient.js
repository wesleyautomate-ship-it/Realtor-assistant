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
