import React from 'react';
import {
  Box,
  Drawer,
  List,
  ListItem,
  ListItemButton,
  ListItemIcon,
  ListItemText,
  Typography,
  Button,
  Divider,
  IconButton,
  Avatar,
  Chip,
  useTheme,
  Snackbar,
  Alert,
  CircularProgress,
  useMediaQuery,
  Stack,
  Skeleton,
  Fade,
  Grow
} from '@mui/material';
import {
  Add as AddIcon,
  Dashboard as DashboardIcon,
  Home as HomeIcon,
  Folder as FolderIcon,
  Logout as LogoutIcon,
  Menu as MenuIcon,
  Close as CloseIcon,
  Chat as ChatIcon,
  Keyboard as KeyboardIcon,
} from '@mui/icons-material';
import { useNavigate, useLocation } from 'react-router-dom';
import { useAppContext } from '../context/AppContext';
import { apiUtils, handleApiError } from '../utils/api';

const Sidebar = ({ open, onToggle, onClose, isMobile, onOpenCommandBar }) => {
  const theme = useTheme();
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

  const [snackbar, setSnackbar] = React.useState({ open: false, message: '', severity: 'info' });

  const sidebarWidth = 280;

  const [isCreatingChat, setIsCreatingChat] = React.useState(false);

  // Handle new chat creation with debouncing
  const handleNewChat = async () => {
    if (isCreatingChat) {
      return; // Prevent multiple simultaneous requests
    }

    try {
      setIsCreatingChat(true);
      console.log('Creating new chat...');
      const newConversation = await createNewConversation();
      console.log('New conversation created:', newConversation);
      console.log('newConversation.id:', newConversation.id);
      console.log('newConversation.id type:', typeof newConversation.id);
      console.log('Navigating to:', `/chat/${newConversation.id}`);
      
      if (!newConversation.id) {
        console.error('No valid session ID in newConversation:', newConversation);
        throw new Error('Failed to create session - no session ID returned');
      }
      
      navigate(`/chat/${newConversation.id}`);
    } catch (error) {
      console.error('Failed to create new chat:', error);
      const errorMessage = handleApiError(error);
      setSnackbar({
        open: true,
        message: `Failed to create new chat: ${errorMessage}`,
        severity: 'error',
      });
    } finally {
      setIsCreatingChat(false);
    }
  };

  // Handle command bar opening
  const handleOpenCommandBar = () => {
    if (onOpenCommandBar) {
      onOpenCommandBar();
    }
  };

  // Handle conversation selection
  const handleConversationSelect = (sessionId) => {
    setCurrentSessionId(sessionId);
    navigate(`/chat/${sessionId}`);
    if (isMobile) {
      onClose();
    }
  };

  // Handle navigation
  const handleNavigation = (path) => {
    navigate(path);
    if (isMobile) {
      onClose();
    }
  };

  // Handle logout
  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  // Navigation items based on user role
  const navigationItems = [
    {
      text: 'AI Copilot',
      icon: <DashboardIcon />,
      path: '/hub',
      show: true,
    },
    {
      text: 'Properties',
      icon: <HomeIcon />,
      path: '/properties',
      show: true,
    },
    {
      text: 'File Hub',
      icon: <FolderIcon />,
      path: '/admin/files',
      show: currentUser?.role === 'admin',
    },
    {
      text: 'Client Management',
      icon: <HomeIcon />,
      path: '/clients',
      show: currentUser?.role === 'agent',
    },
  ];

  // Ensure conversations is an array
  const conversationsList = Array.isArray(conversations) ? conversations : [];

  const handleCloseSnackbar = () => {
    setSnackbar({ ...snackbar, open: false });
  };

  // Sidebar content
  const sidebarContent = (
    <Box
      sx={{
        width: sidebarWidth,
        height: '100%',
        display: 'flex',
        flexDirection: 'column',
        backgroundColor: 'background.paper',
        borderRight: `1px solid ${theme.palette.divider}`,
      }}
    >
      {/* Header */}
      <Box
        sx={{
          p: 2,
          borderBottom: `1px solid ${theme.palette.divider}`,
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
        }}
      >
        <Typography variant="h6" sx={{ fontWeight: 600, color: 'primary.main' }}>
          Dubai RAG
        </Typography>
        {isMobile && (
          <IconButton onClick={onClose} size="small">
            <CloseIcon />
          </IconButton>
        )}
      </Box>

      {/* New Chat Button */}
      <Box sx={{ p: theme.spacing(2) }}>
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

      {/* AI Command Bar Button */}
      <Box sx={{ px: theme.spacing(2), mb: theme.spacing(2) }}>
        <Button
          fullWidth
          variant="outlined"
          startIcon={<KeyboardIcon />}
          onClick={handleOpenCommandBar}
          sx={{
            borderRadius: 2,
            py: 1.5,
            textTransform: 'none',
            fontWeight: 600,
            borderColor: 'primary.main',
            color: 'primary.main',
            '&:hover': {
              backgroundColor: 'primary.main',
              color: 'primary.contrastText',
              borderColor: 'primary.main',
            },
          }}
        >
          AI Command Bar
        </Button>
        <Typography 
          variant="caption" 
          color="text.secondary" 
          sx={{ 
            display: 'block', 
            textAlign: 'center', 
            mt: 0.5,
            fontSize: '0.7rem'
          }}
        >
          Press Ctrl+K to open
        </Typography>
      </Box>

      {/* Navigation */}
      <Box sx={{ px: 2, mb: 2 }}>
        <List dense>
          {navigationItems
            .filter(item => item.show)
            .map((item) => (
              <ListItem key={item.text} disablePadding>
                <ListItemButton
                  onClick={() => handleNavigation(item.path)}
                  selected={location.pathname === item.path}
                  sx={{
                    borderRadius: 1,
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
                      color: location.pathname === item.path ? 'inherit' : 'text.secondary',
                    }}
                  >
                    {item.icon}
                  </ListItemIcon>
                  <ListItemText 
                    primary={item.text}
                    primaryTypographyProps={{
                      fontWeight: location.pathname === item.path ? 600 : 400,
                    }}
                  />
                </ListItemButton>
              </ListItem>
            ))}
        </List>
      </Box>

      <Divider />

      {/* Recent Conversations */}
      <Box sx={{ flex: 1, overflow: 'hidden', display: 'flex', flexDirection: 'column' }}>
        <Box sx={{ px: 2, py: 1.5 }}>
          <Typography variant="subtitle2" color="text.secondary" sx={{ fontWeight: 600 }}>
            Recent
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
                              // Parse the UTC timestamp from the database
                              // The database stores UTC timestamps without timezone info
                              // So we need to explicitly treat them as UTC
                              const timestampStr = conversation.created_at;
                              let utcDate;
                              
                              // Handle different timestamp formats
                              if (timestampStr.includes('T')) {
                                // ISO format with T
                                utcDate = new Date(timestampStr);
                              } else {
                                // PostgreSQL format: "2025-08-31 11:32:22.114730"
                                // Add 'Z' to indicate UTC timezone
                                utcDate = new Date(timestampStr + 'Z');
                              }
                              
                              const now = new Date();
                              
                              // Calculate the time difference in milliseconds
                              const diffInMs = now.getTime() - utcDate.getTime();
                              const diffInHours = diffInMs / (1000 * 60 * 60);
                              
                              if (diffInHours < 1) {
                                return 'Just now';
                              } else if (diffInHours < 24) {
                                const hours = Math.floor(diffInHours);
                                return `${hours} hour${hours > 1 ? 's' : ''} ago`;
                              } else if (diffInHours < 168) { // 7 days
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
      <Box sx={{ p: theme.spacing(2) }}>
        <Box
          sx={{
            display: 'flex',
            alignItems: 'center',
            gap: 1.5,
            mb: 1,
          }}
        >
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

  return (
    <>
      {/* Mobile Drawer */}
      {isMobile ? (
        <Drawer
          variant="temporary"
          open={open}
          onClose={onClose}
          ModalProps={{
            keepMounted: true, // Better mobile performance
          }}
          sx={{
            '& .MuiDrawer-paper': {
              width: sidebarWidth,
              boxSizing: 'border-box',
            },
          }}
        >
          {sidebarContent}
        </Drawer>
      ) : (
        /* Desktop Drawer */
        <Drawer
          variant="persistent"
          open={open}
          sx={{
            '& .MuiDrawer-paper': {
              width: sidebarWidth,
              boxSizing: 'border-box',
            },
          }}
        >
          {sidebarContent}
        </Drawer>
      )}

      {/* Mobile Menu Button */}
      {isMobile && (
        <Box
          sx={{
            position: 'fixed',
            top: 16,
            left: 16,
            zIndex: theme.zIndex.drawer + 1,
          }}
        >
          <IconButton
            onClick={onToggle}
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
      )}

      {/* Snackbar for notifications */}
      <Snackbar
        open={snackbar.open}
        autoHideDuration={6000}
        onClose={handleCloseSnackbar}
        anchorOrigin={{ vertical: 'bottom', horizontal: 'right' }}
      >
        <Alert onClose={handleCloseSnackbar} severity={snackbar.severity} sx={{ width: '100%' }}>
          {snackbar.message}
        </Alert>
      </Snackbar>
    </>
  );
};

export default Sidebar;
