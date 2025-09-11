import React from 'react';
import { Box, Container, useTheme } from '@mui/material';
import { useNavigate } from 'react-router-dom';
import RequestComposer from '../components/RequestComposer';

const Compose = () => {
  const theme = useTheme();
  const navigate = useNavigate();

  return (
    <Box sx={{ 
      minHeight: '100vh', 
      backgroundColor: 'background.default',
      py: 3
    }}>
      <Container maxWidth="lg">
        <RequestComposer />
      </Container>
    </Box>
  );
};

export default Compose;
