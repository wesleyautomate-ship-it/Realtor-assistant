import React, { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Box, Typography, CircularProgress } from '@mui/material';

const Dashboard = () => {
  const navigate = useNavigate();

  useEffect(() => {
    // Redirect to AgentHub (the new AI Copilot interface)
    navigate('/agent-hub', { replace: true });
  }, [navigate]);

  return (
    <Box sx={{ 
      display: 'flex', 
      flexDirection: 'column', 
      alignItems: 'center', 
      justifyContent: 'center', 
      minHeight: '60vh',
      gap: 2
    }}>
      <CircularProgress size={40} />
      <Typography variant="h6" color="text.secondary">
        Redirecting to AI Copilot...
      </Typography>
    </Box>
  );
};

export default Dashboard;
