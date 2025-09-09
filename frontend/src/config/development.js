/**
 * Development Configuration
 * ========================
 * 
 * This file contains development-specific configuration and utilities.
 * These features should NEVER be available in production builds.
 */

// Check if we're in development mode
export const isDevelopment = () => {
  return process.env.NODE_ENV === 'development' || 
         process.env.REACT_APP_ENVIRONMENT === 'development' ||
         window.location.hostname === 'localhost' ||
         window.location.hostname.includes('127.0.0.1') ||
         window.location.hostname.includes('ngrok');
};

// Development user configurations
export const DEV_USERS = {
  admin: {
    id: 1,
    email: 'admin@dubai-estate.com',
    first_name: 'Development',
    last_name: 'Admin',
    role: 'admin',
    is_active: true,
    email_verified: true
  },
  agent: {
    id: 2,
    email: 'agent@dubai-estate.com',
    first_name: 'Development',
    last_name: 'Agent', 
    role: 'agent',
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

// Development API endpoints
export const DEV_ENDPOINTS = {
  devLogin: '/auth/dev-login',
  devUsers: '/auth/dev-users'
};

// Auto-login configuration
export const AUTO_LOGIN_CONFIG = {
  enabled: isDevelopment() && localStorage.getItem('dev-auto-login') === 'true',
  defaultRole: localStorage.getItem('dev-default-role') || 'agent',
  rememberChoice: localStorage.getItem('dev-remember-choice') === 'true'
};

/**
 * Perform development auto-login
 * @param {string} role - User role (admin, agent, employee)
 * @returns {Promise<Object>} Login response data
 */
export const performDevLogin = async (role = 'agent') => {
  if (!isDevelopment()) {
    throw new Error('Development login not available in production');
  }

  try {
    const response = await fetch(`${process.env.REACT_APP_API_URL || 'http://localhost:8003'}${DEV_ENDPOINTS.devLogin}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ role })
    });

    if (!response.ok) {
      throw new Error(`Development login failed: ${response.statusText}`);
    }

    const data = await response.json();
    
    // Store development token
    localStorage.setItem('authToken', data.access_token);
    localStorage.setItem('dev-user-role', role);
    
    return data;
  } catch (error) {
    console.error('Development login error:', error);
    throw error;
  }
};

/**
 * Get available development users
 * @returns {Promise<Array>} Available development user roles
 */
export const getDevUsers = async () => {
  if (!isDevelopment()) {
    return [];
  }

  try {
    const response = await fetch(`${process.env.REACT_APP_API_URL || 'http://localhost:8003'}${DEV_ENDPOINTS.devUsers}`);
    
    if (!response.ok) {
      throw new Error(`Failed to get dev users: ${response.statusText}`);
    }

    const data = await response.json();
    return data.available_roles || [];
  } catch (error) {
    console.error('Error getting dev users:', error);
    return [];
  }
};

/**
 * Set development auto-login preferences
 * @param {boolean} enabled - Enable auto-login
 * @param {string} role - Default role
 * @param {boolean} remember - Remember choice
 */
export const setDevAutoLogin = (enabled, role = 'agent', remember = true) => {
  if (!isDevelopment()) {
    return;
  }

  localStorage.setItem('dev-auto-login', enabled.toString());
  localStorage.setItem('dev-default-role', role);
  localStorage.setItem('dev-remember-choice', remember.toString());
};

/**
 * Clear development auto-login preferences
 */
export const clearDevAutoLogin = () => {
  if (!isDevelopment()) {
    return;
  }

  localStorage.removeItem('dev-auto-login');
  localStorage.removeItem('dev-default-role');
  localStorage.removeItem('dev-remember-choice');
  localStorage.removeItem('dev-user-role');
};

/**
 * Check if user is currently logged in as a development user
 * @returns {boolean}
 */
export const isDevUser = () => {
  if (!isDevelopment()) {
    return false;
  }

  const token = localStorage.getItem('authToken');
  const devRole = localStorage.getItem('dev-user-role');
  
  return !!(token && devRole && token.includes('dev'));
};

/**
 * Get current development user role
 * @returns {string|null}
 */
export const getCurrentDevRole = () => {
  if (!isDevelopment()) {
    return null;
  }

  return localStorage.getItem('dev-user-role');
};

// Development utilities
export const devUtils = {
  // Log development info
  log: (message, data = null) => {
    if (isDevelopment()) {
      console.log(`[DEV] ${message}`, data);
    }
  },
  
  // Show development banner
  showDevBanner: () => {
    if (isDevelopment() && !document.getElementById('dev-banner')) {
      const banner = document.createElement('div');
      banner.id = 'dev-banner';
      banner.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        background: #ff6b35;
        color: white;
        text-align: center;
        padding: 8px;
        font-size: 14px;
        font-weight: bold;
        z-index: 9999;
        box-shadow: 0 2px 4px rgba(0,0,0,0.2);
      `;
      banner.textContent = '🚧 DEVELOPMENT MODE - Authentication Bypassed';
      document.body.appendChild(banner);
      
      // Adjust body padding to account for banner
      document.body.style.paddingTop = '40px';
    }
  },
  
  // Hide development banner
  hideDevBanner: () => {
    const banner = document.getElementById('dev-banner');
    if (banner) {
      banner.remove();
      document.body.style.paddingTop = '';
    }
  }
};
