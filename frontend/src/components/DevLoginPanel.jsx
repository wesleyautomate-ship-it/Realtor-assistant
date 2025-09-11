import React, { useState, useEffect } from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  Button,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  FormControlLabel,
  Switch,
  Alert,
  Divider,
  Chip,
  Stack
} from '@mui/material';
import {
  DeveloperMode as DevIcon,
  Login as LoginIcon,
  Security as SecurityIcon,
  Info as InfoIcon,
  Logout as LogoutIcon
} from '@mui/icons-material';

import { 
  isDevelopment, 
  performDevLogin, 
  getDevUsers, 
  setDevAutoLogin, 
  clearDevAutoLogin,
  AUTO_LOGIN_CONFIG,
  devUtils
} from '../config/development';
import { useAppContext } from '../context/AppContext';
import { useNavigate } from 'react-router-dom';

const DevLoginPanel = ({ onLoginSuccess, onClose }) => {
  const navigate = useNavigate();
  const { logout, currentUser } = useAppContext();
  const [selectedRole, setSelectedRole] = useState(AUTO_LOGIN_CONFIG.defaultRole);
  const [autoLoginEnabled, setAutoLoginEnabled] = useState(AUTO_LOGIN_CONFIG.enabled);
  const [rememberChoice, setRememberChoice] = useState(AUTO_LOGIN_CONFIG.rememberChoice);
  const [availableRoles, setAvailableRoles] = useState(['admin', 'agent', 'employee']);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    if (!isDevelopment()) {
      setError('Development mode not available');
      return;
    }

    // Load available roles from backend
    loadDevUsers();
  }, []);

  const loadDevUsers = async () => {
    try {
      const roles = await getDevUsers();
      if (roles.length > 0) {
        setAvailableRoles(roles);
      }
    } catch (error) {
      console.error('Failed to load dev users:', error);
    }
  };

  const handleDevLogin = async () => {
    if (!isDevelopment()) {
      setError('Development login not available');
      return;
    }

    setLoading(true);
    setError('');

    try {
      const loginData = await performDevLogin(selectedRole);
      
      // Save preferences if remember choice is enabled
      if (rememberChoice) {
        setDevAutoLogin(autoLoginEnabled, selectedRole, true);
      }

      // Show development banner
      devUtils.showDevBanner();
      
      // Call success callback
      if (onLoginSuccess) {
        onLoginSuccess(loginData);
      }

      devUtils.log('Development login successful', { role: selectedRole });
      
    } catch (error) {
      setError(error.message || 'Development login failed');
      devUtils.log('Development login error', error);
    } finally {
      setLoading(false);
    }
  };

  const handleAutoLoginToggle = (enabled) => {
    setAutoLoginEnabled(enabled);
    if (!enabled) {
      clearDevAutoLogin();
    }
  };

  const handleDevLogout = async () => {
    try {
      // Call backend logout endpoint
      const { api } = await import('../utils/apiClient');
      await api.post('/auth/logout');
    } catch (error) {
      console.error('Dev logout API call failed:', error);
      // Continue with logout even if API call fails
    } finally {
      // Clear development auto-login settings
      clearDevAutoLogin();
      
      // Clear local storage and state
      logout();
      
      // Navigate to login page
      navigate('/login');
      
      devUtils.log('Development logout successful');
    }
  };

  if (!isDevelopment()) {
    return (
      <Alert severity="warning" sx={{ mt: 2 }}>
        Development login is only available in development mode.
      </Alert>
    );
  }

  return (
    <Card sx={{ maxWidth: 500, mx: 'auto', mt: 2 }}>
      <CardContent>
        <Box display="flex" alignItems="center" mb={2}>
          <DevIcon color="primary" sx={{ mr: 1 }} />
          <Typography variant="h6" component="h2">
            Development Login
          </Typography>
          <Chip 
            label="DEV ONLY" 
            color="warning" 
            size="small" 
            sx={{ ml: 'auto' }}
          />
        </Box>

        <Alert severity="info" sx={{ mb: 2 }}>
          <Typography variant="body2">
            This bypasses normal authentication for development purposes. 
            <strong> Never use in production!</strong>
          </Typography>
        </Alert>

        <Stack spacing={2}>
          <FormControl fullWidth>
            <InputLabel>User Role</InputLabel>
            <Select
              value={selectedRole}
              label="User Role"
              onChange={(e) => setSelectedRole(e.target.value)}
            >
              {availableRoles.map((role) => (
                <MenuItem key={role} value={role}>
                  <Box display="flex" alignItems="center">
                    <SecurityIcon sx={{ mr: 1, fontSize: 16 }} />
                    {role.charAt(0).toUpperCase() + role.slice(1)}
                  </Box>
                </MenuItem>
              ))}
            </Select>
          </FormControl>

          <Divider />

          <FormControlLabel
            control={
              <Switch
                checked={autoLoginEnabled}
                onChange={(e) => handleAutoLoginToggle(e.target.checked)}
              />
            }
            label="Enable Auto-Login"
          />

          <FormControlLabel
            control={
              <Switch
                checked={rememberChoice}
                onChange={(e) => setRememberChoice(e.target.checked)}
                disabled={!autoLoginEnabled}
              />
            }
            label="Remember My Choice"
          />

          {error && (
            <Alert severity="error">
              {error}
            </Alert>
          )}

          <Button
            variant="contained"
            fullWidth
            onClick={handleDevLogin}
            disabled={loading}
            startIcon={<LoginIcon />}
            sx={{ mt: 2 }}
          >
            {loading ? 'Logging in...' : 'Quick Dev Login'}
          </Button>

          {/* Logout Button - Only show if user is logged in */}
          {currentUser && (
            <Button
              variant="outlined"
              fullWidth
              onClick={handleDevLogout}
              startIcon={<LogoutIcon />}
              sx={{ 
                mt: 1,
                borderColor: 'error.main',
                color: 'error.main',
                '&:hover': {
                  borderColor: 'error.dark',
                  backgroundColor: 'error.light',
                  color: 'error.contrastText',
                },
              }}
            >
              Dev Logout
            </Button>
          )}

          <Typography variant="caption" color="text.secondary" textAlign="center">
            <InfoIcon sx={{ fontSize: 14, mr: 0.5, verticalAlign: 'middle' }} />
            {currentUser 
              ? `Currently logged in as ${currentUser.role || 'user'}`
              : `This will automatically log you in as a ${selectedRole} user`
            }
          </Typography>
        </Stack>
      </CardContent>
    </Card>
  );
};

export default DevLoginPanel;
