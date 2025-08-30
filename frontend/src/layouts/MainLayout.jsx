import React, { useState, useEffect, useCallback } from 'react';
import { Outlet } from 'react-router-dom';
import { Box, useTheme, useMediaQuery, CircularProgress, Skeleton, Fade, Stack } from '@mui/material';
import Sidebar from '../components/Sidebar';
import { useAppContext } from '../context/AppContext';

const MainLayout = () => {
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('md'));
  const [sidebarOpen, setSidebarOpen] = useState(true); // Always start open
  const { currentUser, isLoading } = useAppContext();

  // Handle responsive sidebar state
  useEffect(() => {
    if (isMobile) {
      // On mobile, load saved state or default to closed
      const savedState = localStorage.getItem('sidebarOpen');
      setSidebarOpen(savedState !== null ? JSON.parse(savedState) : false);
    } else {
      // On desktop, always keep sidebar open
      setSidebarOpen(true);
    }
  }, [isMobile]);

  const handleSidebarToggle = useCallback(() => {
    // Only allow toggle on mobile
    if (isMobile) {
      setSidebarOpen(prev => {
        const newState = !prev;
        localStorage.setItem('sidebarOpen', JSON.stringify(newState));
        return newState;
      });
    }
  }, [isMobile]);

  const handleSidebarClose = useCallback(() => {
    // Only close sidebar on mobile
    if (isMobile) {
      setSidebarOpen(false);
      localStorage.setItem('sidebarOpen', 'false');
    }
  }, [isMobile]);

  if (isLoading) {
    return (
      <Fade in={true} timeout={500}>
        <Box sx={{ 
          display: 'flex', 
          justifyContent: 'center', 
          alignItems: 'center', 
          height: '100vh',
          backgroundColor: 'background.default'
        }}>
          <Stack spacing={2} alignItems="center">
            <CircularProgress size={60} />
            <Skeleton variant="text" width={200} height={24} />
          </Stack>
        </Box>
      </Fade>
    );
  }

  return (
    <Box sx={{ display: 'flex', height: '100vh', overflow: 'hidden' }}>
      {/* Sidebar */}
      {currentUser && (
        <Sidebar
          open={sidebarOpen}
          onToggle={handleSidebarToggle}
          onClose={handleSidebarClose}
          isMobile={isMobile}
        />
      )}

      {/* Main content area */}
      <Box
        component="main"
        sx={{
          flexGrow: 1,
          display: 'flex',
          flexDirection: 'column',
          overflow: 'hidden',
          backgroundColor: 'background.default',
          transition: theme.transitions.create(['margin', 'width'], {
            easing: theme.transitions.easing.sharp,
            duration: theme.transitions.duration.leavingScreen,
          }),
          ...(!isMobile && currentUser && {
            marginLeft: '280px', // Sidebar width
            width: `calc(100% - 280px)`,
          }),
        }}
      >
        {/* Content */}
        <Box
          sx={{
            flex: 1,
            overflow: 'auto',
            p: theme.spacing(3),
            backgroundColor: 'background.default',
          }}
        >
          <Outlet />
        </Box>
      </Box>
    </Box>
  );
};

export default MainLayout;
