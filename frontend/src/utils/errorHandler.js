/**
 * Enhanced Error Handling Utility
 * Provides context-specific error messages and consistent error handling across the application
 */

// Error context types
export const ERROR_CONTEXTS = {
  LOGIN: 'login',
  SESSION: 'session',
  DOCUMENT: 'document',
  LEAD: 'lead',
  ADMIN: 'admin',
  GENERAL: 'general',
  NETWORK: 'network',
  VALIDATION: 'validation',
  UPLOAD: 'upload',
  CHAT: 'chat',
  PROPERTY: 'property',
};

// Context-specific error messages
const ERROR_MESSAGES = {
  [ERROR_CONTEXTS.LOGIN]: {
    401: 'Invalid email or password. Please check your credentials and try again.',
    422: 'Please check your input and try again.',
    429: 'Too many login attempts. Please wait a moment and try again.',
    500: 'Login service is temporarily unavailable. Please try again later.',
  },
  [ERROR_CONTEXTS.SESSION]: {
    401: 'Your session has expired. Please log in again.',
    403: 'You do not have permission to access this session.',
    404: 'The requested chat session was not found.',
    500: 'Unable to load session. Please try again later.',
  },
  [ERROR_CONTEXTS.DOCUMENT]: {
    401: 'Please log in to access documents.',
    403: 'You can only access your own documents.',
    404: 'The requested document was not found or has been deleted.',
    500: 'Unable to load document. Please try again later.',
  },
  [ERROR_CONTEXTS.LEAD]: {
    401: 'Please log in to manage leads.',
    403: 'You can only manage your own leads.',
    404: 'The requested lead was not found.',
    500: 'Unable to process lead data. Please try again later.',
  },
  [ERROR_CONTEXTS.ADMIN]: {
    401: 'Please log in with administrator privileges.',
    403: 'You need administrator privileges to access this feature.',
    404: 'The requested admin resource was not found.',
    500: 'Administrative service is temporarily unavailable.',
  },
  [ERROR_CONTEXTS.UPLOAD]: {
    400: 'Invalid file format or size. Please check your file and try again.',
    401: 'Please log in to upload files.',
    413: 'File is too large. Please choose a smaller file.',
    500: 'Upload failed. Please try again later.',
  },
  [ERROR_CONTEXTS.CHAT]: {
    401: 'Please log in to continue chatting.',
    403: 'You do not have permission to access this chat.',
    404: 'Chat session not found.',
    500: 'Chat service is temporarily unavailable.',
  },
  [ERROR_CONTEXTS.PROPERTY]: {
    401: 'Please log in to view properties.',
    404: 'No properties found matching your criteria.',
    500: 'Unable to load property data. Please try again later.',
  },
  [ERROR_CONTEXTS.GENERAL]: {
    401: 'Please log in to continue.',
    403: 'You do not have permission to perform this action.',
    404: 'The requested resource was not found.',
    422: 'Please check your input and try again.',
    429: 'Too many requests. Please wait a moment and try again.',
    500: 'Server error. Please try again later or contact support if the problem persists.',
  },
  [ERROR_CONTEXTS.NETWORK]: {
    ECONNABORTED: 'Request timed out. Please check your connection and try again.',
    ERR_NETWORK: 'Network error. Please check your connection and try again.',
    ERR_BAD_REQUEST: 'Invalid request. Please check your input and try again.',
    ERR_BAD_RESPONSE: 'Server returned an invalid response. Please try again.',
  },
};

/**
 * Get context-specific error message
 * @param {Error} error - The error object
 * @param {string} context - The error context
 * @returns {string} User-friendly error message
 */
export const getErrorMessage = (error, context = ERROR_CONTEXTS.GENERAL) => {
  // Handle network errors
  if (error.code && ERROR_MESSAGES[ERROR_CONTEXTS.NETWORK][error.code]) {
    return ERROR_MESSAGES[ERROR_CONTEXTS.NETWORK][error.code];
  }

  // Handle HTTP response errors
  if (error.response) {
    const { status, data } = error.response;
    const contextMessages = ERROR_MESSAGES[context] || ERROR_MESSAGES[ERROR_CONTEXTS.GENERAL];
    
    // Check for context-specific message
    if (contextMessages[status]) {
      return contextMessages[status];
    }
    
    // Check for server-provided message
    if (data?.detail) {
      return data.detail;
    }
    
    // Fallback to general message
    return ERROR_MESSAGES[ERROR_CONTEXTS.GENERAL][status] || 
           `Request failed with status ${status}`;
  }

  // Handle request errors (no response received)
  if (error.request) {
    return ERROR_MESSAGES[ERROR_CONTEXTS.NETWORK].ERR_NETWORK;
  }

  // Handle other errors
  return error.message || 'An unexpected error occurred. Please try again.';
};

/**
 * Enhanced error handler with logging and user feedback
 * @param {Error} error - The error object
 * @param {string} context - The error context
 * @param {Object} options - Additional options
 * @returns {Object} Error handling result
 */
export const handleError = (error, context = ERROR_CONTEXTS.GENERAL, options = {}) => {
  const {
    logError = true,
    showUserMessage = true,
    retryable = false,
    retryCount = 0,
  } = options;

  // Log error for debugging
  if (logError) {
    console.error(`[${context.toUpperCase()}] Error:`, {
      message: error.message,
      status: error.response?.status,
      data: error.response?.data,
      url: error.config?.url,
      method: error.config?.method,
      context,
      timestamp: new Date().toISOString(),
    });
  }

  // Get user-friendly message
  const userMessage = getErrorMessage(error, context);

  // Determine if error is retryable
  const isRetryable = retryable || (
    error.response?.status >= 500 || 
    error.code === 'ECONNABORTED' || 
    error.code === 'ERR_NETWORK'
  );

  // Determine if user should be redirected to login
  const shouldRedirectToLogin = error.response?.status === 401;

  return {
    userMessage,
    isRetryable,
    shouldRedirectToLogin,
    status: error.response?.status,
    context,
    retryCount,
    timestamp: new Date().toISOString(),
  };
};

/**
 * Retry function for failed requests
 * @param {Function} apiCall - The API function to retry
 * @param {Object} options - Retry options
 * @returns {Promise} API call result
 */
export const retryApiCall = async (apiCall, options = {}) => {
  const {
    maxRetries = 3,
    delay = 1000,
    backoff = 2,
    context = ERROR_CONTEXTS.GENERAL,
  } = options;

  let lastError;
  
  for (let attempt = 0; attempt <= maxRetries; attempt++) {
    try {
      return await apiCall();
    } catch (error) {
      lastError = error;
      
      // Don't retry on client errors (4xx)
      if (error.response?.status >= 400 && error.response?.status < 500) {
        throw error;
      }
      
      // Don't retry on last attempt
      if (attempt === maxRetries) {
        break;
      }
      
      // Wait before retrying
      const waitTime = delay * Math.pow(backoff, attempt);
      console.log(`[${context.toUpperCase()}] Retry attempt ${attempt + 1}/${maxRetries} in ${waitTime}ms`);
      await new Promise(resolve => setTimeout(resolve, waitTime));
    }
  }
  
  throw lastError;
};

/**
 * Session-specific error handler
 * @param {Error} error - The error object
 * @returns {Object} Session error handling result
 */
export const handleSessionError = (error) => {
  return handleError(error, ERROR_CONTEXTS.SESSION, {
    retryable: false, // Session errors are not retryable
  });
};

/**
 * Upload-specific error handler
 * @param {Error} error - The error object
 * @returns {Object} Upload error handling result
 */
export const handleUploadError = (error) => {
  return handleError(error, ERROR_CONTEXTS.UPLOAD, {
    retryable: true,
  });
};

/**
 * Admin-specific error handler
 * @param {Error} error - The error object
 * @returns {Object} Admin error handling result
 */
export const handleAdminError = (error) => {
  return handleError(error, ERROR_CONTEXTS.ADMIN, {
    retryable: false,
  });
};

/**
 * Create a custom error with context
 * @param {string} message - Error message
 * @param {string} context - Error context
 * @param {Object} details - Additional error details
 * @returns {Error} Custom error object
 */
export const createContextError = (message, context = ERROR_CONTEXTS.GENERAL, details = {}) => {
  const error = new Error(message);
  error.context = context;
  error.details = details;
  error.timestamp = new Date().toISOString();
  return error;
};

export default {
  getErrorMessage,
  handleError,
  retryApiCall,
  handleSessionError,
  handleUploadError,
  handleAdminError,
  createContextError,
  ERROR_CONTEXTS,
};
