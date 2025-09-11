import React, { useState, useEffect } from 'react';
import {
  Box,
  Card,
  CardContent,
  TextField,
  Button,
  Typography,
  Alert,
  CircularProgress,
  InputAdornment,
  IconButton,
  Paper,
  useMediaQuery,
  useTheme,
  Stack,
  Fade,
  Grow,
} from '@mui/material';
import {
  Visibility as VisibilityIcon,
  VisibilityOff as VisibilityOffIcon,
  Email as EmailIcon,
  Lock as LockIcon,
  Business as BusinessIcon,
} from '@mui/icons-material';
import { useNavigate, useLocation } from 'react-router-dom';
import { useAppContext } from '../context/AppContext';
import { api } from '../utils/apiClient';
import DevLoginPanel from '../components/DevLoginPanel';
import { isDevelopment, AUTO_LOGIN_CONFIG, performDevLogin, devUtils } from '../config/development';

const LoginPage = () => {
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('md'));
  const isSmallScreen = useMediaQuery(theme.breakpoints.down('sm'));
  
  const navigate = useNavigate();
  const location = useLocation();
  const { currentUser, setCurrentUser, handleApiError } = useAppContext();
  
  const [formData, setFormData] = useState({
    email: '',
    password: '',
  });
  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  // Check if user is already authenticated
  useEffect(() => {
    if (currentUser) {
      setIsAuthenticated(true);
      const from = location.state?.from?.pathname || '/dashboard';
      navigate(from, { replace: true });
    }
  }, [currentUser, navigate, location]);

  // Development auto-login using demo system
  useEffect(() => {
    const performAutoLogin = async () => {
      // Check if auto-login is enabled in localStorage
      const autoLoginEnabled = localStorage.getItem('dev-auto-login') === 'true';
      const defaultRole = localStorage.getItem('dev-default-role') || 'agent';
      
      if (process.env.NODE_ENV === 'development' && autoLoginEnabled && !currentUser) {
        try {
          console.log(`🚀 Auto-login enabled for role: ${defaultRole}`);
          
          // Use the demo login system for auto-login
          await handleDemoLogin(defaultRole);
          
        } catch (error) {
          console.log('Auto-login failed, continuing to normal login page');
        }
      }
    };

    performAutoLogin();
  }, [currentUser]);

  const handleInputChange = (field) => (event) => {
    setFormData(prev => ({
      ...prev,
      [field]: event.target.value,
    }));
    // Clear error when user starts typing
    if (error) {
      setError('');
    }
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    
    if (!formData.email || !formData.password) {
      setError('Please fill in all fields');
      return;
    }

    setLoading(true);
    setError('');

    try {
      const response = await api.post('/auth/login', {
        email: formData.email,
        password: formData.password,
      });

      // The API client returns response.data directly, so access_token and user are at the top level
      const { access_token, user } = response;
      
      // Store token in localStorage
      localStorage.setItem('authToken', access_token);
      
      // Update global state
      setCurrentUser(user);
      setIsAuthenticated(true);
      
      // Redirect to dashboard or intended page
      const from = location.state?.from?.pathname || '/dashboard';
      navigate(from, { replace: true });
      
    } catch (error) {
      console.error('Login error:', error);
      
      // Use enhanced error handling from context
      const userMessage = handleApiError(error, 'login');
      setError(userMessage);
    } finally {
      setLoading(false);
    }
  };

  const handleDemoLogin = async (role = 'agent') => {
    setLoading(true);
    setError('');

    try {
      // Enhanced demo users for development
      const demoUsers = {
        agent: {
          id: 2,
          email: 'wesley@dubai-estate.com',
          first_name: 'Wesley',
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

      const user = demoUsers[role];
      
      // Simulate API delay
      await new Promise(resolve => setTimeout(resolve, 500));
      
      // Store demo token with longer expiry for development
      const demoToken = `demo-token-${role}-${Date.now()}`;
      localStorage.setItem('authToken', demoToken);
      localStorage.setItem('demo-user-role', role);
      
      // Update global state
      setCurrentUser(user);
      setIsAuthenticated(true);
      
      // Show development indicator
      if (process.env.NODE_ENV === 'development') {
        console.log(`🚀 Demo login successful as ${role}`);
      }
      
      // Redirect to dashboard
      navigate('/dashboard', { replace: true });
      
    } catch (error) {
      setError('Demo login failed. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  if (isAuthenticated) {
    return (
      <Box 
        sx={{
          minHeight: '100vh',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          background: 'linear-gradient(135deg, #1976d2 0%, #42a5f5 100%)',
          p: 2,
        }}
      >
        <Card
          sx={{
            maxWidth: 400,
            width: '100%',
            boxShadow: '0 8px 32px rgba(0,0,0,0.1)',
            borderRadius: 3,
          }}
        >
          <CardContent sx={{ p: theme.spacing(4), textAlign: 'center' }}>
            <BusinessIcon sx={{ fontSize: 48, color: 'primary.main', mb: 2 }} />
            <Typography variant="h5" sx={{ fontWeight: 600, mb: 2 }}>
              Already Logged In
            </Typography>
            <Typography variant="body1" color="text.secondary" sx={{ mb: 3 }}>
              You are already authenticated. Redirecting to dashboard...
            </Typography>
            <CircularProgress sx={{ mb: 3 }} />
            <Button
              variant="outlined"
              onClick={async () => {
                try {
                  await api.post('/auth/logout');
                } catch (error) {
                  console.error('Logout API call failed:', error);
                } finally {
                  localStorage.removeItem('authToken');
                  localStorage.removeItem('userId');
                  localStorage.removeItem('userRole');
                  setCurrentUser(null);
                  setIsAuthenticated(false);
                }
              }}
              sx={{ 
                borderColor: 'error.main',
                color: 'error.main',
                '&:hover': {
                  borderColor: 'error.dark',
                  backgroundColor: 'error.light',
                },
              }}
            >
              Logout & Return to Login
            </Button>
          </CardContent>
        </Card>
      </Box>
    );
  }

  return (
    <Box
      sx={{
        minHeight: '100vh',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        background: 'linear-gradient(135deg, #1976d2 0%, #42a5f5 100%)',
        p: 2,
      }}
    >
      <Card
        sx={{
          maxWidth: 400,
          width: '100%',
          boxShadow: '0 8px 32px rgba(0,0,0,0.1)',
          borderRadius: 3,
        }}
      >
        <CardContent sx={{ p: theme.spacing(4) }}>
          {/* Header */}
          <Box sx={{ textAlign: 'center', mb: 4 }}>
            <BusinessIcon sx={{ fontSize: 48, color: 'primary.main', mb: 2 }} />
            <Typography variant="h4" sx={{ fontWeight: 600, mb: 1 }}>
              Dubai RAG System
            </Typography>
            <Typography variant="body1" color="text.secondary">
              Sign in to your account
            </Typography>
          </Box>

          {/* Error Alert */}
          {error && (
            <Alert severity="error" sx={{ mb: theme.spacing(3) }}>
              {error}
            </Alert>
          )}

          {/* Login Form */}
          <Box component="form" onSubmit={handleSubmit} sx={{ mb: theme.spacing(3) }}>
            <TextField
              fullWidth
              label="Email"
              type="email"
              value={formData.email}
              onChange={handleInputChange('email')}
              margin="normal"
              required
              InputProps={{
                startAdornment: (
                  <InputAdornment position="start">
                    <EmailIcon color="action" />
                  </InputAdornment>
                ),
              }}
              disabled={loading}
            />

            <TextField
              fullWidth
              label="Password"
              type={showPassword ? 'text' : 'password'}
              value={formData.password}
              onChange={handleInputChange('password')}
              margin="normal"
              required
              InputProps={{
                startAdornment: (
                  <InputAdornment position="start">
                    <LockIcon color="action" />
                  </InputAdornment>
                ),
                endAdornment: (
                  <InputAdornment position="end">
                    <IconButton
                      onClick={() => setShowPassword(!showPassword)}
                      edge="end"
                      disabled={loading}
                    >
                      {showPassword ? <VisibilityOffIcon /> : <VisibilityIcon />}
                    </IconButton>
                  </InputAdornment>
                ),
              }}
              disabled={loading}
            />

            <Button
              type="submit"
              fullWidth
              variant="contained"
              size="large"
              disabled={loading}
              sx={{ mt: 3, mb: 2, py: 1.5 }}
            >
              {loading ? <CircularProgress size={24} /> : 'Sign In'}
            </Button>
          </Box>

          {/* Demo Login Buttons */}
          <Box sx={{ mb: theme.spacing(3) }}>
            <Typography variant="body2" color="text.secondary" sx={{ mb: 2, textAlign: 'center' }}>
              Or try a demo account:
            </Typography>
            <Box sx={{ display: 'flex', gap: 1, flexWrap: 'wrap' }}>
              <Button
                variant="outlined"
                onClick={() => handleDemoLogin('agent')}
                disabled={loading}
                sx={{ py: theme.spacing(1), flex: 1, minWidth: '120px' }}
              >
                Demo Agent
              </Button>
              <Button
                variant="outlined"
                onClick={() => handleDemoLogin('admin')}
                disabled={loading}
                sx={{ py: theme.spacing(1), flex: 1, minWidth: '120px' }}
              >
                Demo Admin
              </Button>
              <Button
                variant="outlined"
                onClick={() => handleDemoLogin('employee')}
                disabled={loading}
                sx={{ py: theme.spacing(1), flex: 1, minWidth: '120px' }}
              >
                Demo Employee
              </Button>
            </Box>
            
            {/* Development Auto-Login Toggle */}
            {process.env.NODE_ENV === 'development' && (
              <Box sx={{ mt: 2, textAlign: 'center' }}>
                <Button
                  size="small"
                  variant="text"
                  onClick={() => {
                    const enabled = localStorage.getItem('dev-auto-login') === 'true';
                    localStorage.setItem('dev-auto-login', (!enabled).toString());
                    localStorage.setItem('dev-default-role', 'agent');
                    alert(enabled ? 'Auto-login disabled' : 'Auto-login enabled for agent role');
                  }}
                  sx={{ fontSize: '0.75rem' }}
                >
                  {localStorage.getItem('dev-auto-login') === 'true' ? '🔓 Disable Auto-Login' : '🔒 Enable Auto-Login'}
                </Button>
              </Box>
            )}
          </Box>

          {/* Development Login Panel */}
          {isDevelopment() && (
            <Box sx={{ mt: theme.spacing(3) }}>
              <DevLoginPanel 
                onLoginSuccess={(loginData) => {
                  setCurrentUser(loginData.user);
                  setIsAuthenticated(true);
                  const from = location.state?.from?.pathname || '/dashboard';
                  navigate(from, { replace: true });
                }}
              />
            </Box>
          )}

          {/* Footer */}
          <Box sx={{ textAlign: 'center' }}>
            <Typography variant="body2" color="text.secondary">
              Dubai Real Estate RAG System
            </Typography>
            <Typography variant="caption" color="text.secondary">
              AI-Powered Real Estate Intelligence Platform
            </Typography>
          </Box>
        </CardContent>
      </Card>
    </Box>
  );
};

export default LoginPage;
