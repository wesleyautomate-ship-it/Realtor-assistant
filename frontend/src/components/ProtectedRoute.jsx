import React from 'react';
import { Navigate, useLocation } from 'react-router-dom';
import { useAppContext } from '../context/AppContext';
import {
  Box,
  CircularProgress,
  useTheme,
  Fade,
  useMediaQuery,
  Stack,
  Skeleton,
  Grow,
  Divider
} from '@mui/material';

const ProtectedRoute = ({ children }) => {
  const theme = useTheme();
  const { currentUser, isLoading } = useAppContext();
  const location = useLocation();

  // Show loading spinner while checking authentication
  if (isLoading) {
    return (
      <Fade in={true} timeout={500}>
        <Box
          sx={{
            display: 'flex',
            justifyContent: 'center',
            alignItems: 'center',
            minHeight: '100vh',
            backgroundColor: 'background.default'
          }}
        >
          <CircularProgress size={60} />
        </Box>
      </Fade>
    );
  }

  // If not authenticated, redirect to login
  if (!currentUser) {
    return <Navigate to="/login" state={{ from: location }} replace />;
  }

  // If authenticated, render the protected content
  return children;
};

export default ProtectedRoute;
