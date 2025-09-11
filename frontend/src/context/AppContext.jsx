import React, { createContext, useContext, useReducer, useEffect, useCallback, useMemo } from 'react';
import { api } from '../utils/apiClient';

// Initial state
const initialState = {
  currentUser: null,
  conversations: [],
  currentSessionId: null,
  isLoading: true,
  error: null,
  sessionWarning: null, // New: Session expiry warning
  sessionExpiryTime: null, // New: Session expiry timestamp
};

// Action types
const ACTIONS = {
  SET_CURRENT_USER: 'SET_CURRENT_USER',
  SET_CONVERSATIONS: 'SET_CONVERSATIONS',
  SET_CURRENT_SESSION: 'SET_CURRENT_SESSION',
  SET_LOADING: 'SET_LOADING',
  SET_ERROR: 'SET_ERROR',
  ADD_CONVERSATION: 'ADD_CONVERSATION',
  UPDATE_CONVERSATION: 'UPDATE_CONVERSATION',
  CLEAR_ERROR: 'CLEAR_ERROR',
  SET_SESSION_WARNING: 'SET_SESSION_WARNING', // New
  CLEAR_SESSION_WARNING: 'CLEAR_SESSION_WARNING', // New
  SET_SESSION_EXPIRY: 'SET_SESSION_EXPIRY', // New
};

// Reducer function
const appReducer = (state, action) => {
  switch (action.type) {
    case ACTIONS.SET_CURRENT_USER:
      return { ...state, currentUser: action.payload };
    case ACTIONS.SET_CONVERSATIONS:
      return { ...state, conversations: action.payload };
    case ACTIONS.SET_CURRENT_SESSION:
      return { ...state, currentSessionId: action.payload };
    case ACTIONS.SET_LOADING:
      return { ...state, isLoading: action.payload };
    case ACTIONS.SET_ERROR:
      return { ...state, error: action.payload };
    case ACTIONS.ADD_CONVERSATION:
      return { 
        ...state, 
        conversations: [action.payload, ...state.conversations] 
      };
    case ACTIONS.UPDATE_CONVERSATION:
      return {
        ...state,
        conversations: state.conversations.map(conv =>
          conv.id === action.payload.id ? action.payload : conv
        ),
      };
    case ACTIONS.CLEAR_ERROR:
      return { ...state, error: null };
    case ACTIONS.SET_SESSION_WARNING:
      return { ...state, sessionWarning: action.payload };
    case ACTIONS.CLEAR_SESSION_WARNING:
      return { ...state, sessionWarning: null };
    case ACTIONS.SET_SESSION_EXPIRY:
      return { ...state, sessionExpiryTime: action.payload };
    default:
      return state;
  }
};

// Create context
const AppContext = createContext();

// Provider component
export const AppProvider = ({ children }) => {
  const [state, dispatch] = useReducer(appReducer, initialState);

  // Use centralized API client
  const apiClient = useMemo(() => api, []);

  // Session management utilities
  const getTokenExpiryTime = useCallback((token) => {
    if (!token) return null;
    try {
      const payload = JSON.parse(atob(token.split('.')[1]));
      return payload.exp * 1000; // Convert to milliseconds
    } catch (error) {
      console.error('Error parsing token:', error);
      return null;
    }
  }, []);

  const isTokenExpiringSoon = useCallback((token, warningMinutes = 5) => {
    const expiryTime = getTokenExpiryTime(token);
    if (!expiryTime) return false;
    
    const warningTime = expiryTime - (warningMinutes * 60 * 1000);
    return Date.now() >= warningTime;
  }, [getTokenExpiryTime]);

  const isTokenExpired = useCallback((token) => {
    const expiryTime = getTokenExpiryTime(token);
    if (!expiryTime) return true;
    return Date.now() >= expiryTime;
  }, [getTokenExpiryTime]);

  // Session warning management
  const checkSessionExpiry = useCallback(() => {
    const token = localStorage.getItem('authToken');
    if (!token || !state.currentUser) {
      dispatch({ type: ACTIONS.CLEAR_SESSION_WARNING });
      return;
    }

    if (isTokenExpired(token)) {
      // Token is expired, logout immediately
      logout();
      return;
    }

    if (isTokenExpiringSoon(token, 5)) { // 5 minutes warning
      const expiryTime = getTokenExpiryTime(token);
      const minutesLeft = Math.ceil((expiryTime - Date.now()) / (60 * 1000));
      
      dispatch({ 
        type: ACTIONS.SET_SESSION_WARNING, 
        payload: {
          message: `Your session will expire in ${minutesLeft} minute${minutesLeft !== 1 ? 's' : ''}. Please save your work.`,
          minutesLeft,
          expiryTime
        }
      });
    } else {
      dispatch({ type: ACTIONS.CLEAR_SESSION_WARNING });
    }
  }, [state.currentUser, isTokenExpired, isTokenExpiringSoon, getTokenExpiryTime]);

  // Auto-refresh token functionality
  const refreshToken = useCallback(async () => {
    try {
      const response = await apiClient.post('/auth/refresh');
      const { access_token } = response;
      
      localStorage.setItem('authToken', access_token);
      
      // Update session expiry time
      const expiryTime = getTokenExpiryTime(access_token);
      dispatch({ type: ACTIONS.SET_SESSION_EXPIRY, payload: expiryTime });
      
      // Clear session warning
      dispatch({ type: ACTIONS.CLEAR_SESSION_WARNING });
      
      console.log('Token refreshed successfully');
      return true;
    } catch (error) {
      console.error('Token refresh failed:', error);
      return false;
    }
  }, [apiClient, getTokenExpiryTime]);

  // Enhanced error handling with context-specific messages
  const handleApiError = useCallback((error, context = 'general') => {
    let userMessage = 'An unexpected error occurred. Please try again.';
    
    if (error.response) {
      const { status, data } = error.response;
      
      switch (status) {
        case 401:
          if (context === 'login') {
            userMessage = 'Invalid email or password. Please check your credentials and try again.';
          } else if (context === 'session') {
            userMessage = 'Your session has expired. Please log in again.';
          } else {
            userMessage = 'Please log in to continue.';
          }
          break;
        case 403:
          if (context === 'admin') {
            userMessage = 'You need administrator privileges to access this feature.';
          } else if (context === 'document') {
            userMessage = 'You can only access your own documents.';
          } else if (context === 'lead') {
            userMessage = 'You can only manage your own leads.';
          } else {
            userMessage = 'You do not have permission to perform this action.';
          }
          break;
        case 404:
          if (context === 'document') {
            userMessage = 'The requested document was not found or has been deleted.';
          } else if (context === 'session') {
            userMessage = 'The requested chat session was not found.';
          } else {
            userMessage = 'The requested resource was not found.';
          }
          break;
        case 422:
          userMessage = data.detail || 'Please check your input and try again.';
          break;
        case 429:
          userMessage = 'Too many requests. Please wait a moment and try again.';
          break;
        case 500:
          userMessage = 'Server error. Please try again later or contact support if the problem persists.';
          break;
        default:
          userMessage = data.detail || `Request failed with status ${status}`;
      }
    } else if (error.request) {
      userMessage = 'Network error. Please check your connection and try again.';
    }
    
    return userMessage;
  }, []);

  // Check authentication status on app load
  useEffect(() => {
    const checkAuthStatus = async () => {
      const token = localStorage.getItem('authToken');
      
      if (token) {
        // Check if this is a demo token
        if (token.startsWith('demo-token-')) {
          // Handle demo token - restore user from localStorage
          const demoRole = localStorage.getItem('demo-user-role') || 'agent';
          const demoUsers = {
            agent: {
              id: 2,
              email: 'laura@dubai-estate.com',
              first_name: 'Laura',
              last_name: 'Agent',
              role: 'agent',
              is_active: true,
              email_verified: true
            },
            admin: {
              id: 1,
              email: 'admin@dubai-estate.com',
              first_name: 'System',
              last_name: 'Administrator',
              role: 'admin',
              is_active: true,
              email_verified: true
            },
            employee: {
              id: 3,
              email: 'employee@dubai-estate.com',
              first_name: 'Development',
              last_name: 'Employee',
              role: 'employee',
              is_active: true,
              email_verified: true
            }
          };
          
          const user = demoUsers[demoRole];
          if (user) {
            dispatch({ type: ACTIONS.SET_CURRENT_USER, payload: user });
            dispatch({ type: ACTIONS.SET_LOADING, payload: false });
            return;
          }
        }
        
        // Check if token is already expired
        if (isTokenExpired(token)) {
          localStorage.removeItem('authToken');
          localStorage.removeItem('userId');
          localStorage.removeItem('userRole');
          localStorage.removeItem('demo-user-role');
          dispatch({ type: ACTIONS.SET_CURRENT_USER, payload: null });
          dispatch({ type: ACTIONS.SET_LOADING, payload: false });
          return;
        }

        try {
          // Try to validate token with backend and get complete user object
          const response = await apiClient.get('/auth/me');
          dispatch({ type: ACTIONS.SET_CURRENT_USER, payload: response });
          
          // Set session expiry time
          const expiryTime = getTokenExpiryTime(token);
          dispatch({ type: ACTIONS.SET_SESSION_EXPIRY, payload: expiryTime });
          
        } catch (error) {
          // Token is invalid, clear it
          localStorage.removeItem('authToken');
          localStorage.removeItem('userId');
          localStorage.removeItem('userRole');
          localStorage.removeItem('demo-user-role');
          dispatch({ type: ACTIONS.SET_CURRENT_USER, payload: null });
        }
      }
      
      dispatch({ type: ACTIONS.SET_LOADING, payload: false });
    };

    checkAuthStatus();
  }, [apiClient, isTokenExpired, getTokenExpiryTime]);

  // Session expiry monitoring
  useEffect(() => {
    if (!state.currentUser) return;

    // Check session expiry every minute
    const interval = setInterval(checkSessionExpiry, 60000);
    
    // Also check immediately
    checkSessionExpiry();

    return () => clearInterval(interval);
  }, [state.currentUser, checkSessionExpiry]);

  // Fetch conversations from the backend with pagination and caching
  const fetchConversations = useCallback(async (page = 1, limit = 20, useCache = true) => {
    // Only prevent multiple simultaneous requests if we're already fetching conversations
    // Don't block if we're just loading from authentication check
    if (state.isLoading && state.conversations.length > 0) {
      return;
    }

    try {
      // Check cache first
      const cacheKey = `conversations_page_${page}_limit_${limit}`;
      const cached = localStorage.getItem(cacheKey);
      
      if (useCache && cached) {
        const cachedData = JSON.parse(cached);
        const cacheAge = Date.now() - cachedData.timestamp;
        
        // Use cache if less than 5 minutes old
        if (cacheAge < 5 * 60 * 1000) {
          dispatch({ type: ACTIONS.SET_CONVERSATIONS, payload: cachedData.data.sessions });
          return cachedData.data;
        }
      }
      
      dispatch({ type: ACTIONS.SET_LOADING, payload: true });
      const response = await apiClient.get('/sessions');
      
      // Handle different response formats
      let conversations = [];
      if (Array.isArray(response)) {
        conversations = response;
      } else if (response && response.sessions) {
        conversations = response.sessions;
      } else if (response && response.conversations) {
        conversations = response.conversations;
      }
      
      // Cache the result
      const cacheData = {
        data: { sessions: conversations },
        timestamp: Date.now()
      };
      localStorage.setItem(cacheKey, JSON.stringify(cacheData));
      
      dispatch({ type: ACTIONS.SET_CONVERSATIONS, payload: conversations });
      return { sessions: conversations };
    } catch (error) {
      console.error('Error fetching conversations:', error);
      const userMessage = handleApiError(error, 'session');
      dispatch({ 
        type: ACTIONS.SET_ERROR, 
        payload: userMessage
      });
    } finally {
      dispatch({ type: ACTIONS.SET_LOADING, payload: false });
    }
  }, [apiClient, state.isLoading, handleApiError]);

  // Fetch recent conversations for quick loading
  const fetchRecentConversations = useCallback(async (days = 7, limit = 20) => {
    // Only prevent multiple simultaneous requests if we're already fetching conversations
    // Don't block if we're just loading from authentication check
    if (state.isLoading && state.conversations.length > 0) {
      return;
    }

    try {
      const cacheKey = `recent_conversations_${days}_${limit}`;
      const cached = localStorage.getItem(cacheKey);
      
      if (cached) {
        const cachedData = JSON.parse(cached);
        const cacheAge = Date.now() - cachedData.timestamp;
        
        // Use cache if less than 2 minutes old
        if (cacheAge < 2 * 60 * 1000) {
          dispatch({ type: ACTIONS.SET_CONVERSATIONS, payload: cachedData.data.sessions });
          return cachedData.data;
        }
      }
      
      dispatch({ type: ACTIONS.SET_LOADING, payload: true });
      const response = await apiClient.get(`/sessions/recent?days=${days}&limit=${limit}`);
      
      // Cache the result
      const cacheData = {
        data: response,
        timestamp: Date.now()
      };
      localStorage.setItem(cacheKey, JSON.stringify(cacheData));
      
      dispatch({ type: ACTIONS.SET_CONVERSATIONS, payload: response.sessions });
      return response;
    } catch (error) {
      console.error('Error fetching recent conversations:', error);
      const userMessage = handleApiError(error, 'session');
      dispatch({ 
        type: ACTIONS.SET_ERROR, 
        payload: userMessage
      });
    } finally {
      dispatch({ type: ACTIONS.SET_LOADING, payload: false });
    }
  }, [apiClient, state.isLoading, handleApiError]);

  // Create new conversation with optimized state management
  const createNewConversation = async () => {
    try {
      // Don't set global loading for conversation creation to avoid UI freezing
      const response = await apiClient.post('/sessions', {
        title: null, // Will be auto-generated from first message
        role: 'client'
      });
      const newConversation = response;
      
      console.log('API Response for new conversation:', newConversation);
      console.log('newConversation.session_id:', newConversation.session_id);
      console.log('newConversation.id:', newConversation.id);
      
      // Ensure the conversation has the correct structure
      const conversationData = {
        id: newConversation.session_id || newConversation.id,
        title: newConversation.title || 'New Chat',
        created_at: newConversation.created_at,
        updated_at: newConversation.updated_at,
        role: newConversation.role || state.currentUser?.role || 'agent',
        message_count: newConversation.message_count || 0,
        is_active: newConversation.is_active !== false,
      };
      
      console.log('Processed conversation data:', conversationData);
      
      // Batch state updates to prevent multiple re-renders
      dispatch({ 
        type: ACTIONS.ADD_CONVERSATION, 
        payload: conversationData 
      });
      
      return conversationData;
    } catch (error) {
      console.error('Error creating conversation:', error);
      const userMessage = handleApiError(error, 'session');
      dispatch({ 
        type: ACTIONS.SET_ERROR, 
        payload: userMessage
      });
      throw error;
    }
  };

  // Set current session
  const setCurrentSessionId = (sessionId) => {
    dispatch({ type: ACTIONS.SET_CURRENT_SESSION, payload: sessionId });
  };

  // Update conversation title
  const updateConversationTitle = async (sessionId, title) => {
    try {
      const response = await apiClient.put(`/sessions/${sessionId}/title`, { title });
      dispatch({ type: ACTIONS.UPDATE_CONVERSATION, payload: response });
    } catch (error) {
      console.error('Error updating conversation title:', error);
      const userMessage = handleApiError(error, 'session');
      dispatch({ 
        type: ACTIONS.SET_ERROR, 
        payload: userMessage
      });
    }
  };

  // Delete conversation
  const deleteConversation = async (sessionId) => {
    try {
      await apiClient.delete(`/sessions/${sessionId}`);
      dispatch({ 
        type: ACTIONS.SET_CONVERSATIONS, 
        payload: state.conversations.filter(conv => conv.id !== sessionId) 
      });
      
      // If deleted conversation was current, clear current session
      if (state.currentSessionId === sessionId) {
        dispatch({ type: ACTIONS.SET_CURRENT_SESSION, payload: null });
      }
    } catch (error) {
      console.error('Error deleting conversation:', error);
      const userMessage = handleApiError(error, 'session');
      dispatch({ 
        type: ACTIONS.SET_ERROR, 
        payload: userMessage
      });
    }
  };

  // Clear error
  const clearError = () => {
    dispatch({ type: ACTIONS.CLEAR_ERROR });
  };

  // Clear session warning
  const clearSessionWarning = () => {
    dispatch({ type: ACTIONS.CLEAR_SESSION_WARNING });
  };

  // Set current user
  const setCurrentUser = (user) => {
    dispatch({ type: ACTIONS.SET_CURRENT_USER, payload: user });
  };

  // Enhanced logout function
  const logout = () => {
    localStorage.removeItem('authToken');
    localStorage.removeItem('userId');
    localStorage.removeItem('userRole');
    localStorage.removeItem('demo-user-role');
    dispatch({ type: ACTIONS.SET_CURRENT_USER, payload: null });
    dispatch({ type: ACTIONS.SET_CONVERSATIONS, payload: [] });
    dispatch({ type: ACTIONS.SET_CURRENT_SESSION, payload: null });
    dispatch({ type: ACTIONS.CLEAR_SESSION_WARNING });
    dispatch({ type: ACTIONS.SET_SESSION_EXPIRY, payload: null });
  };

  // Load conversations when user is authenticated - with proper dependency management
  useEffect(() => {
    if (state.currentUser && !state.isLoading && !state.conversations.length) {
      // Only fetch if user is authenticated, not loading, and no conversations are loaded
      console.log('Fetching conversations for user:', state.currentUser.email);
      fetchConversations();
    }
  }, [state.currentUser, state.isLoading, fetchConversations]);

  // Memoize the context value to prevent unnecessary re-renders
  const value = useMemo(() => ({
    ...state,
    api,
    fetchConversations,
    fetchRecentConversations,
    createNewConversation,
    setCurrentSessionId,
    updateConversationTitle,
    deleteConversation,
    setCurrentUser,
    logout,
    clearError,
    clearSessionWarning,
    refreshToken,
    handleApiError,
    checkSessionExpiry,
  }), [
    state,
    api,
    fetchConversations,
    fetchRecentConversations,
    createNewConversation,
    setCurrentSessionId,
    updateConversationTitle,
    deleteConversation,
    setCurrentUser,
    logout,
    clearError,
    clearSessionWarning,
    refreshToken,
    handleApiError,
    checkSessionExpiry,
  ]);

  return (
    <AppContext.Provider value={value}>
      {children}
    </AppContext.Provider>
  );
};

// Custom hook to use the context
export const useAppContext = () => {
  const context = useContext(AppContext);
  if (!context) {
    throw new Error('useAppContext must be used within an AppProvider');
  }
  return context;
};
