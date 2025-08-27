import React from 'react';
import { Navigate, useLocation } from 'react-router-dom';
import { Box, CircularProgress, Typography } from '@mui/material';
import { useAuth } from './AuthContext';

const ProtectedRoute = ({ 
  children, 
  requiredRoles = [], 
  requiredPermissions = [],
  fallbackPath = '/login',
  showLoading = true 
}) => {
  const { user, isAuthenticated, loading } = useAuth();
  const location = useLocation();

  // Show loading spinner while checking authentication
  if (loading && showLoading) {
    return (
      <Box
        sx={{
          display: 'flex',
          flexDirection: 'column',
          justifyContent: 'center',
          alignItems: 'center',
          minHeight: '100vh',
          background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)'
        }}
      >
        <CircularProgress size={60} sx={{ color: 'white', mb: 2 }} />
        <Typography variant="h6" color="white">
          Loading...
        </Typography>
      </Box>
    );
  }

  // Redirect to login if not authenticated
  if (!isAuthenticated) {
    return <Navigate to={fallbackPath} state={{ from: location }} replace />;
  }

  // Check role-based access
  if (requiredRoles.length > 0 && user) {
    const hasRequiredRole = requiredRoles.includes(user.role);
    if (!hasRequiredRole) {
      return (
        <Box
          sx={{
            display: 'flex',
            flexDirection: 'column',
            justifyContent: 'center',
            alignItems: 'center',
            minHeight: '100vh',
            background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
            padding: 3
          }}
        >
          <Typography variant="h4" color="white" gutterBottom>
            Access Denied
          </Typography>
          <Typography variant="body1" color="white" textAlign="center">
            You don't have permission to access this page.
          </Typography>
          <Typography variant="body2" color="white" textAlign="center" sx={{ mt: 1 }}>
            Required roles: {requiredRoles.join(', ')}
          </Typography>
        </Box>
      );
    }
  }

  // Check permission-based access (if implemented)
  if (requiredPermissions.length > 0 && user) {
    // This would need to be implemented based on your permission system
    // For now, we'll just check if user has admin role for all permissions
    const hasRequiredPermissions = user.role === 'admin' || 
      requiredPermissions.every(permission => {
        // Add your permission checking logic here
        return true; // Placeholder
      });
    
    if (!hasRequiredPermissions) {
      return (
        <Box
          sx={{
            display: 'flex',
            flexDirection: 'column',
            justifyContent: 'center',
            alignItems: 'center',
            minHeight: '100vh',
            background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
            padding: 3
          }}
        >
          <Typography variant="h4" color="white" gutterBottom>
            Access Denied
          </Typography>
          <Typography variant="body1" color="white" textAlign="center">
            You don't have the required permissions to access this page.
          </Typography>
          <Typography variant="body2" color="white" textAlign="center" sx={{ mt: 1 }}>
            Required permissions: {requiredPermissions.join(', ')}
          </Typography>
        </Box>
      );
    }
  }

  // User is authenticated and has required access
  return children;
};

// Convenience components for common role checks
export const AdminRoute = ({ children, ...props }) => (
  <ProtectedRoute requiredRoles={['admin']} {...props}>
    {children}
  </ProtectedRoute>
);

export const AgentRoute = ({ children, ...props }) => (
  <ProtectedRoute requiredRoles={['agent', 'admin']} {...props}>
    {children}
  </ProtectedRoute>
);

export const EmployeeRoute = ({ children, ...props }) => (
  <ProtectedRoute requiredRoles={['employee', 'admin']} {...props}>
    {children}
  </ProtectedRoute>
);

export const ClientRoute = ({ children, ...props }) => (
  <ProtectedRoute requiredRoles={['client', 'agent', 'employee', 'admin']} {...props}>
    {children}
  </ProtectedRoute>
);

export default ProtectedRoute;
