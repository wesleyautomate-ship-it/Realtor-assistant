import React, { useState, useEffect } from 'react';
import {
  Box,
  Container,
  Typography,
  Fab,
  useTheme,
  useMediaQuery,
  Stack,
  Chip,
  IconButton,
  Tooltip,
  Alert,
  Skeleton,
  Paper,
  Card,
  CardContent,
  Button,
  Grid,
} from '@mui/material';
import {
  Add as AddIcon,
  Refresh as RefreshIcon,
  FilterList as FilterIcon,
  Chat as ChatIcon,
  Home as HomeIcon,
  People as PeopleIcon,
  TrendingUp as TrendingUpIcon,
  SmartToy as SmartToyIcon,
} from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';
import { useAppContext } from '../context/AppContext';
import useRequestStore from '../store/requests';

const Hub = () => {
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('md'));
  const navigate = useNavigate();
  const { currentUser } = useAppContext();
  
  const [filter, setFilter] = useState('all');
  const { 
    requests, 
    loading, 
    error, 
    fetchRequests, 
    clearError 
  } = useRequestStore();

  const filters = [
    { id: 'all', label: 'All Requests', count: requests.length },
    { id: 'active', label: 'Active', count: requests.filter(r => ['queued', 'planning', 'generating', 'validating'].includes(r.status)).length },
    { id: 'ready', label: 'Ready', count: requests.filter(r => r.status === 'draft_ready').length },
    { id: 'completed', label: 'Completed', count: requests.filter(r => ['approved', 'delivered'].includes(r.status)).length }
  ];

  // Quick action cards for mobile-first design
  const quickActions = [
    {
      title: 'Start New Chat',
      description: 'Ask questions about Dubai real estate',
      icon: <ChatIcon />,
      color: 'primary',
      action: () => navigate('/chat')
    },
    {
      title: 'Browse Properties',
      description: 'Search and filter properties',
      icon: <HomeIcon />,
      color: 'secondary',
      action: () => navigate('/properties')
    },
    {
      title: 'Manage Clients',
      description: 'View and manage your clients',
      icon: <PeopleIcon />,
      color: 'success',
      action: () => navigate('/clients')
    },
    {
      title: 'Market Insights',
      description: 'Get latest market trends',
      icon: <TrendingUpIcon />,
      color: 'warning',
      action: () => navigate('/market-insights')
    }
  ];

  useEffect(() => {
    loadRequests();
  }, []);

  const loadRequests = async () => {
    try {
      await fetchRequests();
    } catch (error) {
      console.error('Error loading requests:', error);
    }
  };

  const handleRefresh = () => {
    loadRequests();
  };

  const getFilteredRequests = () => {
    if (filter === 'all') return requests;
    if (filter === 'active') return requests.filter(r => ['queued', 'planning', 'generating', 'validating'].includes(r.status));
    if (filter === 'ready') return requests.filter(r => r.status === 'draft_ready');
    if (filter === 'completed') return requests.filter(r => ['approved', 'delivered'].includes(r.status));
    return requests;
  };

  const getActiveRequestsCount = () => {
    return requests.filter(r => ['queued', 'planning', 'generating', 'validating'].includes(r.status)).length;
  };

  return (
    <Box sx={{ 
      minHeight: '100vh', 
      backgroundColor: 'background.default',
      pb: isMobile ? 8 : 4 // Add bottom padding for mobile navigation
    }}>
      <Container maxWidth="xl" sx={{ py: 3 }}>
        {/* Welcome Section */}
        <Box sx={{ mb: 4, textAlign: isMobile ? 'center' : 'left' }}>
          <Typography 
            variant={isMobile ? "h5" : "h4"}
            sx={{ 
              fontWeight: 700, 
              mb: 1, 
              color: 'text.primary',
              background: `linear-gradient(135deg, ${theme.palette.primary.main}, ${theme.palette.secondary.main})`,
              backgroundClip: 'text',
              WebkitBackgroundClip: 'text',
              WebkitTextFillColor: 'transparent'
            }}
          >
            Welcome back, {currentUser?.first_name || 'Laura'}!
          </Typography>
          <Typography 
            variant={isMobile ? "body1" : "h6"}
            sx={{ 
              color: 'text.secondary',
              fontWeight: 400
            }}
          >
            Your AI-powered real estate workspace
          </Typography>
        </Box>

        {/* Quick Actions - Mobile First */}
        <Box sx={{ mb: 4 }}>
          <Typography 
            variant="h6" 
            sx={{ 
              fontWeight: 600, 
              mb: 2,
              color: 'text.primary'
            }}
          >
            Quick Actions
          </Typography>
          <Grid container spacing={2}>
            {quickActions.map((action, index) => (
              <Grid item xs={6} sm={3} key={index}>
                <Card
                  sx={{
                    height: '100%',
                    cursor: 'pointer',
                    transition: 'all 0.3s ease',
                    '&:hover': {
                      transform: 'translateY(-4px)',
                      boxShadow: '0 8px 25px rgba(0,0,0,0.15)',
                    },
                    borderRadius: 3,
                    border: 1,
                    borderColor: 'divider',
                  }}
                  onClick={action.action}
                >
                  <CardContent sx={{ p: 2, textAlign: 'center' }}>
                    <Box
                      sx={{
                        width: 48,
                        height: 48,
                        borderRadius: '50%',
                        bgcolor: `${action.color}.light`,
                        color: `${action.color}.contrastText`,
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center',
                        mx: 'auto',
                        mb: 1.5,
                      }}
                    >
                      {action.icon}
                    </Box>
                    <Typography variant="subtitle2" sx={{ fontWeight: 600, mb: 0.5 }}>
                      {action.title}
                    </Typography>
                    <Typography variant="caption" color="text.secondary">
                      {action.description}
                    </Typography>
                  </CardContent>
                </Card>
              </Grid>
            ))}
          </Grid>
        </Box>

        {/* AI Assistant Card */}
        <Paper
          sx={{
            p: 3,
            mb: 4,
            borderRadius: 3,
            background: 'linear-gradient(135deg, #1976d2 0%, #42a5f5 100%)',
            color: 'white',
            cursor: 'pointer',
            transition: 'all 0.3s ease',
            '&:hover': {
              transform: 'translateY(-2px)',
              boxShadow: '0 8px 25px rgba(25, 118, 210, 0.3)',
            },
          }}
          onClick={() => navigate('/chat')}
        >
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
            <Box
              sx={{
                width: 56,
                height: 56,
                borderRadius: '50%',
                bgcolor: 'rgba(255,255,255,0.2)',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
              }}
            >
              <SmartToyIcon sx={{ fontSize: 28 }} />
            </Box>
            <Box sx={{ flex: 1 }}>
              <Typography variant="h6" sx={{ fontWeight: 600, mb: 0.5 }}>
                AI Assistant
              </Typography>
              <Typography variant="body2" sx={{ opacity: 0.9 }}>
                Get instant answers about Dubai real estate market, properties, and investment opportunities
              </Typography>
            </Box>
            <Button
              variant="contained"
              sx={{
                bgcolor: 'rgba(255,255,255,0.2)',
                color: 'white',
                '&:hover': {
                  bgcolor: 'rgba(255,255,255,0.3)',
                },
                borderRadius: 2,
                px: 3,
              }}
            >
              Start Chat
            </Button>
          </Box>
        </Paper>

        {/* Active Requests Section */}
        <Box sx={{ mb: 4 }}>
          <Box sx={{ 
            display: 'flex', 
            justifyContent: 'space-between', 
            alignItems: 'center', 
            mb: 3,
            flexDirection: isMobile ? 'column' : 'row',
            gap: isMobile ? 2 : 0
          }}>
            <Typography 
              variant="h6" 
              sx={{ 
                fontWeight: 600, 
                color: 'text.primary'
              }}
            >
              Recent Activity
            </Typography>
            
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
              <Chip
                label={`${getActiveRequestsCount()} Active`}
                color="primary"
                variant="outlined"
                size="small"
              />
              
              <Tooltip title="Refresh">
                <IconButton onClick={handleRefresh} disabled={loading} size="small">
                  <RefreshIcon />
                </IconButton>
              </Tooltip>
            </Box>
          </Box>

          {/* Filter Chips */}
          <Stack 
            direction="row" 
            spacing={1} 
            sx={{ 
              mb: 3, 
              flexWrap: 'wrap', 
              gap: 1,
              justifyContent: isMobile ? 'center' : 'flex-start'
            }}
          >
            {filters.map((filterOption) => (
              <Chip
                key={filterOption.id}
                label={`${filterOption.label} (${filterOption.count})`}
                onClick={() => setFilter(filterOption.id)}
                variant={filter === filterOption.id ? 'filled' : 'outlined'}
                color={filter === filterOption.id ? 'primary' : 'default'}
                size="small"
              />
            ))}
          </Stack>

          {/* Error Alert */}
          {error && (
            <Alert severity="error" sx={{ mb: 3 }}>
              {error}
            </Alert>
          )}

          {/* Requests Grid */}
          {loading ? (
            <Box sx={{ 
              display: 'grid', 
              gridTemplateColumns: { xs: '1fr', md: 'repeat(2, 1fr)', lg: 'repeat(3, 1fr)' }, 
              gap: 2 
            }}>
              {[1, 2, 3].map((i) => (
                <Skeleton key={i} variant="rectangular" height={200} sx={{ borderRadius: 3 }} />
              ))}
            </Box>
          ) : getFilteredRequests().length === 0 ? (
            <Paper
              sx={{
                textAlign: 'center',
                py: 6,
                px: 3,
                borderRadius: 3,
                border: `2px dashed ${theme.palette.divider}`,
                bgcolor: 'background.paper'
              }}
            >
              <Box
                sx={{
                  width: 64,
                  height: 64,
                  borderRadius: '50%',
                  bgcolor: 'primary.light',
                  color: 'primary.contrastText',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  mx: 'auto',
                  mb: 2,
                }}
              >
                <SmartToyIcon sx={{ fontSize: 32 }} />
              </Box>
              <Typography variant="h6" sx={{ mb: 1, color: 'text.secondary' }}>
                No requests yet
              </Typography>
              <Typography variant="body2" sx={{ color: 'text.secondary', mb: 3 }}>
                Get started by asking the AI assistant or creating your first request
              </Typography>
              <Button
                variant="contained"
                startIcon={<AddIcon />}
                onClick={() => navigate('/chat')}
                sx={{ borderRadius: 2 }}
              >
                Start Chatting
              </Button>
            </Paper>
          ) : (
            <Box sx={{ 
              display: 'grid', 
              gridTemplateColumns: { 
                xs: '1fr', 
                sm: 'repeat(2, 1fr)', 
                lg: 'repeat(3, 1fr)' 
              }, 
              gap: 2 
            }}>
              {getFilteredRequests().slice(0, 6).map((request) => (
                <Card
                  key={request.id}
                  sx={{
                    borderRadius: 3,
                    border: 1,
                    borderColor: 'divider',
                    transition: 'all 0.3s ease',
                    '&:hover': {
                      transform: 'translateY(-2px)',
                      boxShadow: '0 8px 25px rgba(0,0,0,0.1)',
                    },
                  }}
                >
                  <CardContent sx={{ p: 2 }}>
                    <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 1 }}>
                      <Chip
                        label={request.team}
                        size="small"
                        color="primary"
                        variant="outlined"
                      />
                      <Chip
                        label={request.status}
                        size="small"
                        color={request.status === 'completed' ? 'success' : 'default'}
                        variant="filled"
                      />
                    </Box>
                    <Typography variant="subtitle2" sx={{ fontWeight: 600, mb: 1 }}>
                      {request.title || 'Untitled Request'}
                    </Typography>
                    <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                      {request.description || 'No description available'}
                    </Typography>
                    <Button
                      size="small"
                      variant="outlined"
                      onClick={() => navigate(`/requests/${request.id}`)}
                      sx={{ borderRadius: 2 }}
                    >
                      View Details
                    </Button>
                  </CardContent>
                </Card>
              ))}
            </Box>
          )}
        </Box>
      </Container>

      {/* Floating Action Button - Only show on desktop */}
      {!isMobile && (
        <Fab
          color="primary"
          onClick={() => navigate('/chat')}
          sx={{
            position: 'fixed',
            bottom: 24,
            right: 24,
            backgroundColor: theme.palette.primary.main,
            '&:hover': {
              backgroundColor: theme.palette.primary.dark,
              transform: 'scale(1.1)'
            },
            transition: 'all 0.3s ease-in-out',
            zIndex: 1000
          }}
        >
          <ChatIcon />
        </Fab>
      )}
    </Box>
  );
};

export default Hub;