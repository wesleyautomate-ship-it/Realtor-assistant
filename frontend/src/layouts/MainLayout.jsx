import React, { useState, useEffect } from 'react';
import { Outlet } from 'react-router-dom';
import { Box, CircularProgress, Skeleton, Fade, Stack, useMediaQuery, useTheme } from '@mui/material';
import { useAppContext } from '../context/AppContext';
import GlobalCommandBar from '../components/GlobalCommandBar';
import HeaderBar from '../components/HeaderBar';
import MobileNavigation from '../components/MobileNavigation';
import AdminLayout from './AdminLayout';

const MainLayout = () => {
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('md'));
  const { currentUser, isLoading } = useAppContext();
  const [commandBarOpen, setCommandBarOpen] = useState(false);

  // Check if user is admin - show admin layout
  const isAdmin = currentUser?.role === 'admin';

  // Global keyboard shortcut for Command Bar (Ctrl+K or Cmd+K)
  useEffect(() => {
    const handleKeyDown = (event) => {
      if ((event.ctrlKey || event.metaKey) && event.key === 'k') {
        event.preventDefault();
        setCommandBarOpen(true);
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, []);

  // Handle command execution
  const handleCommandExecuted = (result) => {
    console.log('Command executed:', result);
    setCommandBarOpen(false);
  };

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

  // Render admin layout for admin users
  if (isAdmin) {
    return <AdminLayout />;
  }

  // Render mobile-first layout for agents and other users
  return (
    <Box sx={{ 
      height: '100vh', 
      overflow: 'hidden', 
      display: 'flex', 
      flexDirection: 'column',
      bgcolor: 'background.default'
    }}>
      {/* Header Bar - Only show on desktop */}
      {!isMobile && <HeaderBar />}
      
      {/* Main Content Area */}
      <Box sx={{ 
        flex: 1, 
        overflow: 'hidden',
        pb: isMobile ? 7 : 0 // Add bottom padding for mobile navigation
      }}>
        {/* Content */}
        <Box
          component="main"
          sx={{
            height: '100%',
            overflow: 'auto',
            backgroundColor: 'background.default',
          }}
        >
          <Outlet />
        </Box>
      </Box>

      {/* Mobile Navigation */}
      <MobileNavigation />

      {/* Global Command Bar */}
      <GlobalCommandBar
        open={commandBarOpen}
        onClose={() => setCommandBarOpen(false)}
        onCommandExecuted={handleCommandExecuted}
      />
    </Box>
  );
};

export default MainLayout;