import React, { createContext, useContext, useState, useEffect } from 'react';
import axios from 'axios';

const API_BASE_URL = 'http://localhost:8001';

const AuthContext = createContext();

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(localStorage.getItem('access_token'));
  const [refreshToken, setRefreshToken] = useState(localStorage.getItem('refresh_token'));
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Configure axios defaults
  useEffect(() => {
    if (token) {
      axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
    } else {
      delete axios.defaults.headers.common['Authorization'];
    }
  }, [token]);

  // Check if user is authenticated on mount
  useEffect(() => {
    const checkAuth = async () => {
      if (token) {
        try {
          const response = await axios.get(`${API_BASE_URL}/auth/me`);
          setUser(response.data);
        } catch (error) {
          console.error('Auth check failed:', error);
          // Token might be expired, try to refresh
          if (refreshToken) {
            await refreshAccessToken();
          } else {
            logout();
          }
        }
      }
      setLoading(false);
    };

    checkAuth();
  }, []);

  const login = async (email, password) => {
    try {
      setError(null);
      const response = await axios.post(`${API_BASE_URL}/auth/login`, {
        email,
        password
      });

      const { access_token, refresh_token, user: userData } = response.data;

      // Store tokens
      localStorage.setItem('access_token', access_token);
      localStorage.setItem('refresh_token', refresh_token);
      
      // Set state
      setToken(access_token);
      setRefreshToken(refresh_token);
      setUser(userData);

      // Set axios header
      axios.defaults.headers.common['Authorization'] = `Bearer ${access_token}`;

      return { success: true };
    } catch (error) {
      const errorMessage = error.response?.data?.detail || 'Login failed';
      setError(errorMessage);
      return { success: false, error: errorMessage };
    }
  };

  const register = async (userData) => {
    try {
      setError(null);
      const response = await axios.post(`${API_BASE_URL}/auth/register`, userData);

      const { access_token, refresh_token, user: newUser } = response.data;

      // Store tokens
      localStorage.setItem('access_token', access_token);
      localStorage.setItem('refresh_token', refresh_token);
      
      // Set state
      setToken(access_token);
      setRefreshToken(refresh_token);
      setUser(newUser);

      // Set axios header
      axios.defaults.headers.common['Authorization'] = `Bearer ${access_token}`;

      return { success: true };
    } catch (error) {
      const errorMessage = error.response?.data?.detail || 'Registration failed';
      setError(errorMessage);
      return { success: false, error: errorMessage };
    }
  };

  const logout = async () => {
    try {
      // Call logout endpoint if we have a token
      if (token) {
        await axios.post(`${API_BASE_URL}/auth/logout`);
      }
    } catch (error) {
      console.error('Logout error:', error);
    } finally {
      // Clear local storage and state
      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh_token');
      setToken(null);
      setRefreshToken(null);
      setUser(null);
      setError(null);
      
      // Remove axios header
      delete axios.defaults.headers.common['Authorization'];
    }
  };

  const refreshAccessToken = async () => {
    try {
      const response = await axios.post(`${API_BASE_URL}/auth/refresh`, {
        refresh_token: refreshToken
      });

      const { access_token, refresh_token: newRefreshToken, user: userData } = response.data;

      // Update tokens
      localStorage.setItem('access_token', access_token);
      localStorage.setItem('refresh_token', newRefreshToken);
      
      setToken(access_token);
      setRefreshToken(newRefreshToken);
      setUser(userData);

      // Update axios header
      axios.defaults.headers.common['Authorization'] = `Bearer ${access_token}`;

      return true;
    } catch (error) {
      console.error('Token refresh failed:', error);
      logout();
      return false;
    }
  };

  const forgotPassword = async (email) => {
    try {
      setError(null);
      await axios.post(`${API_BASE_URL}/auth/forgot-password`, { email });
      return { success: true };
    } catch (error) {
      const errorMessage = error.response?.data?.detail || 'Password reset request failed';
      setError(errorMessage);
      return { success: false, error: errorMessage };
    }
  };

  const resetPassword = async (token, newPassword) => {
    try {
      setError(null);
      await axios.post(`${API_BASE_URL}/auth/reset-password`, {
        token,
        new_password: newPassword
      });
      return { success: true };
    } catch (error) {
      const errorMessage = error.response?.data?.detail || 'Password reset failed';
      setError(errorMessage);
      return { success: false, error: errorMessage };
    }
  };

  const updateProfile = async (profileData) => {
    try {
      setError(null);
      const response = await axios.put(`${API_BASE_URL}/auth/profile`, profileData);
      setUser(response.data);
      return { success: true };
    } catch (error) {
      const errorMessage = error.response?.data?.detail || 'Profile update failed';
      setError(errorMessage);
      return { success: false, error: errorMessage };
    }
  };

  const clearError = () => {
    setError(null);
  };

  const value = {
    user,
    token,
    loading,
    error,
    login,
    register,
    logout,
    forgotPassword,
    resetPassword,
    updateProfile,
    clearError,
    isAuthenticated: !!user && !!token
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};
