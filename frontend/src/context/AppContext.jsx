import React, { createContext, useContext, useReducer, useEffect, useCallback, useMemo } from 'react';
import { api } from '../utils/apiClient';

// Initial state
const initialState = {
  currentUser: null,
  conversations: [],
  currentSessionId: null,
  isLoading: true,
  error: null,
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



  // Check authentication status on app load
  useEffect(() => {
    const checkAuthStatus = async () => {
      const token = localStorage.getItem('authToken');
      
      if (token) {
        try {
          // Try to validate token with backend
          const response = await apiClient.get('/auth/me');
          dispatch({ type: ACTIONS.SET_CURRENT_USER, payload: response });
        } catch (error) {
          // Token is invalid, clear it
          localStorage.removeItem('authToken');
          dispatch({ type: ACTIONS.SET_CURRENT_USER, payload: null });
        }
      }
      
      dispatch({ type: ACTIONS.SET_LOADING, payload: false });
    };

    checkAuthStatus();
  }, [apiClient]); // Add apiClient dependency since it's now memoized

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
      const response = await apiClient.get(`/sessions?page=${page}&limit=${limit}`);
      
      // Cache the result
      const cacheData = {
        data: response,
        timestamp: Date.now()
      };
      localStorage.setItem(cacheKey, JSON.stringify(cacheData));
      
      dispatch({ type: ACTIONS.SET_CONVERSATIONS, payload: response.sessions });
      return response;
    } catch (error) {
      console.error('Error fetching conversations:', error);
      dispatch({ 
        type: ACTIONS.SET_ERROR, 
        payload: 'Failed to fetch conversations' 
      });
    } finally {
      dispatch({ type: ACTIONS.SET_LOADING, payload: false });
    }
  }, [apiClient, state.isLoading]);

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
      dispatch({ 
        type: ACTIONS.SET_ERROR, 
        payload: 'Failed to fetch recent conversations' 
      });
    } finally {
      dispatch({ type: ACTIONS.SET_LOADING, payload: false });
    }
  }, [apiClient, state.isLoading]);

  // Create new conversation with optimized state management
  const createNewConversation = async () => {
    try {
      // Don't set global loading for conversation creation to avoid UI freezing
      const response = await apiClient.post('/sessions', {
        title: "New Chat",
        role: state.currentUser?.role || "agent",
        user_preferences: {}
      });
      const newConversation = response;
      
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
      
      // Batch state updates to prevent multiple re-renders
      dispatch({ 
        type: ACTIONS.ADD_CONVERSATION, 
        payload: conversationData 
      });
      
      return conversationData;
    } catch (error) {
      console.error('Error creating conversation:', error);
      dispatch({ 
        type: ACTIONS.SET_ERROR, 
        payload: 'Failed to create new conversation' 
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
      dispatch({ 
        type: ACTIONS.SET_ERROR, 
        payload: 'Failed to update conversation title' 
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
      dispatch({ 
        type: ACTIONS.SET_ERROR, 
        payload: 'Failed to delete conversation' 
      });
    }
  };

  // Clear error
  const clearError = () => {
    dispatch({ type: ACTIONS.CLEAR_ERROR });
  };

  // Set current user
  const setCurrentUser = (user) => {
    dispatch({ type: ACTIONS.SET_CURRENT_USER, payload: user });
  };

  // Logout function
  const logout = () => {
    localStorage.removeItem('authToken');
    dispatch({ type: ACTIONS.SET_CURRENT_USER, payload: null });
    dispatch({ type: ACTIONS.SET_CONVERSATIONS, payload: [] });
    dispatch({ type: ACTIONS.SET_CURRENT_SESSION, payload: null });
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
