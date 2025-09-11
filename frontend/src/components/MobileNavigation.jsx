import React, { useState } from 'react';
import {
  Box,
  BottomNavigation,
  BottomNavigationAction,
  Paper,
  IconButton,
  Avatar,
  Typography,
  Drawer,
  List,
  ListItem,
  ListItemButton,
  ListItemIcon,
  ListItemText,
  Divider,
  Button,
  Chip,
  useTheme,
  useMediaQuery,
  Stack,
  CircularProgress,
} from '@mui/material';
import {
  Home as HomeIcon,
  Chat as ChatIcon,
  Dashboard as DashboardIcon,
  People as PeopleIcon,
  Description as DescriptionIcon,
  Menu as MenuIcon,
  Close as CloseIcon,
  Add as AddIcon,
  Logout as LogoutIcon,
  SmartToy as SmartToyIcon,
} from '@mui/icons-material';
import { useNavigate, useLocation } from 'react-router-dom';
import { useAppContext } from '../context/AppContext';

const MobileNavigation = () => {
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('md'));
  const navigate = useNavigate();
  const location = useLocation();
  const { 
    currentUser, 
    conversations, 
    currentSessionId,
    createNewConversation,
    setCurrentSessionId,
    logout,
    isLoading 
  } = useAppContext();

  const [drawerOpen, setDrawerOpen] = useState(false);
  const [isCreatingChat, setIsCreatingChat] = useState(false);

  // Navigation items for bottom navigation - matching the mockup exactly
  const navigationItems = [
    {
      label: 'Home',
      icon: <HomeIcon />,
      path: '/dashboard',
      value: 'home'
    },
    {
      label: 'People',
      icon: <PeopleIcon />,
      path: '/contacts',
      value: 'people'
    },
    {
      label: 'Chat',
      icon: <ChatIcon />,
      path: '/chat',
      value: 'chat'
    },
    {
      label: 'Reports',
      icon: <DescriptionIcon />,
      path: '/reports',
      value: 'reports'
    },
    {
      label: 'List',
      icon: <DashboardIcon />,
      path: '/hub',
      value: 'list'
    }
  ];

  // Get current navigation value based on path
  const getCurrentValue = () => {
    const path = location.pathname;
    if (path.startsWith('/dashboard')) return 'home';
    if (path.startsWith('/contacts')) return 'people';
    if (path.startsWith('/chat')) return 'chat';
    if (path.startsWith('/reports')) return 'reports';
    if (path.startsWith('/hub')) return 'list';
    return 'home'; // Default to home
  };

  const handleNavigationChange = (event, newValue) => {
    const item = navigationItems.find(item => item.value === newValue);
    if (item) {
      navigate(item.path);
    }
  };

  const handleNewChat = async () => {
    if (isCreatingChat) return;

    try {
      setIsCreatingChat(true);
      const newConversation = await createNewConversation();
      navigate(`/chat/${newConversation.id}`);
      setDrawerOpen(false);
    } catch (error) {
      console.error('Failed to create new chat:', error);
    } finally {
      setIsCreatingChat(false);
    }
  };

  const handleConversationSelect = (sessionId) => {
    setCurrentSessionId(sessionId);
    navigate(`/chat/${sessionId}`);
    setDrawerOpen(false);
  };

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  // Conversations list
  const conversationsList = Array.isArray(conversations) ? conversations : [];

  // Side drawer content
  const drawerContent = (
    <Box sx={{ width: 280, height: '100%', display: 'flex', flexDirection: 'column' }}>
      {/* Header */}
      <Box sx={{ p: 2, borderBottom: 1, borderColor: 'divider' }}>
        <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
          <Typography variant="h6" sx={{ fontWeight: 600, color: 'primary.main' }}>
            Laura
          </Typography>
          <IconButton onClick={() => setDrawerOpen(false)} size="small">
            <CloseIcon />
          </IconButton>
        </Box>
      </Box>

      {/* New Chat Button */}
      <Box sx={{ p: 2 }}>
        <Button
          fullWidth
          variant="contained"
          startIcon={isCreatingChat ? <CircularProgress size={16} /> : <AddIcon />}
          onClick={handleNewChat}
          disabled={isLoading || isCreatingChat}
          sx={{
            borderRadius: 2,
            py: 1.5,
            textTransform: 'none',
            fontWeight: 600,
            boxShadow: '0 2px 8px rgba(0,0,0,0.1)',
            '&:hover': {
              boxShadow: '0 4px 12px rgba(0,0,0,0.15)',
            },
          }}
        >
          New Chat
        </Button>
      </Box>

      {/* AI Command Button */}
      <Box sx={{ px: 2, mb: 2 }}>
        <Button
          fullWidth
          variant="contained"
          startIcon={<SmartToyIcon />}
          onClick={() => {
            navigate('/chat');
            setDrawerOpen(false);
          }}
          sx={{
            borderRadius: 2,
            py: 2,
            textTransform: 'none',
            fontWeight: 700,
            fontSize: '1rem',
            background: 'linear-gradient(135deg, #1976d2 0%, #42a5f5 100%)',
            boxShadow: '0 4px 12px rgba(25, 118, 210, 0.3)',
            '&:hover': {
              background: 'linear-gradient(135deg, #1565c0 0%, #1976d2 100%)',
              boxShadow: '0 6px 16px rgba(25, 118, 210, 0.4)',
            },
          }}
        >
          AI COMMAND
        </Button>
        <Typography 
          variant="caption" 
          color="text.secondary" 
          sx={{ 
            display: 'block', 
            textAlign: 'center', 
            mt: 0.5,
            fontSize: '0.75rem',
            fontWeight: 500
          }}
        >
          Your AI Copilot awaits
        </Typography>
      </Box>

      <Divider />

      {/* Recent Conversations */}
      <Box sx={{ flex: 1, overflow: 'hidden', display: 'flex', flexDirection: 'column' }}>
        <Box sx={{ px: 2, py: 1.5 }}>
          <Typography variant="subtitle2" color="text.secondary" sx={{ fontWeight: 600 }}>
            Recent Chats
          </Typography>
        </Box>
        
        <Box sx={{ flex: 1, overflow: 'auto' }}>
          <List dense>
            {conversationsList.length === 0 ? (
              <ListItem>
                <ListItemText
                  primary={
                    <Typography variant="body2" color="text.secondary" align="center">
                      No conversations yet
                    </Typography>
                  }
                />
              </ListItem>
            ) : (
              conversationsList.map((conversation, index) => (
                <ListItem key={conversation.id || index} disablePadding>
                  <ListItemButton
                    onClick={() => handleConversationSelect(conversation.id)}
                    selected={currentSessionId === conversation.id}
                    sx={{
                      borderRadius: 1,
                      mx: 1,
                      mb: 0.5,
                      '&.Mui-selected': {
                        backgroundColor: 'primary.light',
                        color: 'primary.contrastText',
                        '&:hover': {
                          backgroundColor: 'primary.main',
                        },
                      },
                    }}
                  >
                    <ListItemIcon
                      sx={{
                        color: currentSessionId === conversation.id ? 'inherit' : 'text.secondary',
                        minWidth: 36,
                      }}
                    >
                      <ChatIcon fontSize="small" />
                    </ListItemIcon>
                    <ListItemText
                      primary={
                        <Typography
                          variant="body2"
                          sx={{
                            fontWeight: currentSessionId === conversation.id ? 600 : 400,
                            overflow: 'hidden',
                            textOverflow: 'ellipsis',
                            whiteSpace: 'nowrap',
                          }}
                        >
                          {conversation.title || 'New conversation'}
                        </Typography>
                      }
                      secondary={
                        conversation.created_at && (
                          <Typography variant="caption" color="text.secondary">
                            {(() => {
                              const timestampStr = conversation.created_at;
                              let utcDate;
                              
                              if (timestampStr.includes('T')) {
                                utcDate = new Date(timestampStr);
                              } else {
                                utcDate = new Date(timestampStr + 'Z');
                              }
                              
                              const now = new Date();
                              const diffInMs = now.getTime() - utcDate.getTime();
                              const diffInHours = diffInMs / (1000 * 60 * 60);
                              
                              if (diffInHours < 1) {
                                return 'Just now';
                              } else if (diffInHours < 24) {
                                const hours = Math.floor(diffInHours);
                                return `${hours} hour${hours > 1 ? 's' : ''} ago`;
                              } else if (diffInHours < 168) {
                                const days = Math.floor(diffInHours / 24);
                                return `${days} day${days > 1 ? 's' : ''} ago`;
                              } else {
                                return utcDate.toLocaleDateString();
                              }
                            })()}
                          </Typography>
                        )
                      }
                    />
                  </ListItemButton>
                </ListItem>
              ))
            )}
          </List>
        </Box>
      </Box>

      <Divider />

      {/* User Profile Section */}
      <Box sx={{ p: 2 }}>
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1.5, mb: 2 }}>
          <Avatar
            sx={{
              width: 32,
              height: 32,
              bgcolor: currentUser?.role === 'admin' ? 'secondary.main' : 'primary.main',
              fontSize: '0.875rem',
            }}
          >
            {currentUser?.name?.charAt(0) || currentUser?.first_name?.charAt(0) || 'U'}
          </Avatar>
          <Box sx={{ flex: 1, minWidth: 0 }}>
            <Typography variant="body2" sx={{ fontWeight: 600, overflow: 'hidden', textOverflow: 'ellipsis' }}>
              {currentUser?.name || `${currentUser?.first_name} ${currentUser?.last_name}` || 'User'}
            </Typography>
            <Chip
              label={currentUser?.role || 'user'}
              size="small"
              color={currentUser?.role === 'admin' ? 'secondary' : 'primary'}
              sx={{ 
                height: 20, 
                fontSize: '0.75rem',
                fontWeight: 600,
                textTransform: 'capitalize'
              }}
            />
          </Box>
        </Box>
        
        <Button
          fullWidth
          variant="outlined"
          startIcon={<LogoutIcon />}
          onClick={handleLogout}
          size="small"
          sx={{
            borderRadius: 1,
            textTransform: 'none',
            borderColor: 'divider',
            color: 'text.secondary',
            '&:hover': {
              borderColor: 'error.main',
              color: 'error.main',
            },
          }}
        >
          Logout
        </Button>
      </Box>
    </Box>
  );

  if (!isMobile) {
    return null; // Don't render on desktop
  }

  return (
    <>
      {/* Mobile Bottom Navigation */}
      <Paper 
        sx={{ 
          position: 'fixed', 
          bottom: 0, 
          left: 0, 
          right: 0, 
          zIndex: theme.zIndex.appBar,
          borderTop: 1,
          borderColor: 'divider',
          boxShadow: '0 -2px 8px rgba(0,0,0,0.1)'
        }} 
        elevation={3}
      >
        <BottomNavigation
          value={getCurrentValue()}
          onChange={handleNavigationChange}
          sx={{
            '& .MuiBottomNavigationAction-root': {
              minWidth: 'auto',
              padding: '6px 8px 8px',
              '&.Mui-selected': {
                color: 'primary.main',
              },
            },
            '& .MuiBottomNavigationAction-label': {
              fontSize: '0.7rem',
              fontWeight: 500,
              '&.Mui-selected': {
                fontSize: '0.7rem',
                fontWeight: 600,
              },
            },
          }}
        >
          {navigationItems.map((item) => (
            <BottomNavigationAction
              key={item.value}
              label={item.label}
              icon={item.icon}
              value={item.value}
            />
          ))}
        </BottomNavigation>
      </Paper>

      {/* Mobile Menu Button */}
      <Box
        sx={{
          position: 'fixed',
          top: 16,
          left: 16,
          zIndex: theme.zIndex.drawer + 1,
        }}
      >
        <IconButton
          onClick={() => setDrawerOpen(true)}
          sx={{
            backgroundColor: 'background.paper',
            boxShadow: '0 2px 8px rgba(0,0,0,0.1)',
            '&:hover': {
              backgroundColor: 'background.paper',
              boxShadow: '0 4px 12px rgba(0,0,0,0.15)',
            },
          }}
        >
          <MenuIcon />
        </IconButton>
      </Box>

      {/* Mobile Drawer */}
      <Drawer
        variant="temporary"
        open={drawerOpen}
        onClose={() => setDrawerOpen(false)}
        ModalProps={{
          keepMounted: true,
        }}
        sx={{
          '& .MuiDrawer-paper': {
            width: 280,
            boxSizing: 'border-box',
          },
        }}
      >
        {drawerContent}
      </Drawer>
    </>
  );
};

export default MobileNavigation;