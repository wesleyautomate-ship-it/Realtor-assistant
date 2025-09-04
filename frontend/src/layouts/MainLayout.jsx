import React, { useState, useEffect } from 'react';
import { Outlet } from 'react-router-dom';
import { Box, CircularProgress, Skeleton, Fade, Stack } from '@mui/material';
import { useAppContext } from '../context/AppContext';
import GlobalCommandBar from '../components/GlobalCommandBar';

const MainLayout = () => {
  const { currentUser, isLoading } = useAppContext();
  const [commandBarOpen, setCommandBarOpen] = useState(false);

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
    // TODO: Handle command results (e.g., show notifications, navigate, etc.)
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

  return (
    <Box sx={{ height: '100vh', overflow: 'hidden' }}>
      {/* Global Command Bar */}
      <GlobalCommandBar
        open={commandBarOpen}
        onClose={() => setCommandBarOpen(false)}
        onCommandExecuted={handleCommandExecuted}
      />
      
      {/* Content */}
      <Box
        component="main"
        sx={{
          height: '100%',
          backgroundColor: 'background.default',
        }}
      >
        <Outlet />
      </Box>
    </Box>
  );
};

export default MainLayout;
