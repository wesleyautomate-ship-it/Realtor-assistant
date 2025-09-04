import React, { useState, useEffect, useRef, useCallback } from 'react';
import {
  Box,
  Typography,
  List,
  ListItem,
  ListItemText,
  ListItemIcon,
  ListItemSecondaryAction,
  IconButton,
  Chip,
  Badge,
  Collapse,
  Card,
  CardContent,
  Alert,
  Button,
  Snackbar,
  useTheme,
  Fade,
  Slide,
} from '@mui/material';
import {
  Notifications as NotificationsIcon,
  NotificationsActive as NotificationsActiveIcon,
  NotificationsNone as NotificationsNoneIcon,
  Close as CloseIcon,
  CheckCircle as CheckCircleIcon,
  Warning as WarningIcon,
  Error as ErrorIcon,
  Info as InfoIcon,
  PriorityHigh as PriorityHighIcon,
  Refresh as RefreshIcon,
  Settings as SettingsIcon,
} from '@mui/icons-material';
import { useAuth } from '../../context/AuthContext';

const RealTimeNotifications = () => {
  const theme = useTheme();
  const { user } = useAuth();
  const [notifications, setNotifications] = useState([]);
  const [unreadCount, setUnreadCount] = useState(0);
  const [expanded, setExpanded] = useState(false);
  const [connected, setConnected] = useState(false);
  const [lastUpdate, setLastUpdate] = useState(null);
  const [showSnackbar, setShowSnackbar] = useState(false);
  const [snackbarMessage, setSnackbarMessage] = useState('');
  const [snackbarSeverity, setSnackbarSeverity] = useState('info');
  
  const wsRef = useRef(null);
  const reconnectTimeoutRef = useRef(null);
  const pingIntervalRef = useRef(null);

  // WebSocket connection management
  const connectWebSocket = useCallback(() => {
    if (!user) return;

    try {
      // In production, this would be your WebSocket server URL
      const wsUrl = process.env.REACT_APP_WS_URL || `ws://localhost:8000/ws/notifications/${user.id}`;
      
      wsRef.current = new WebSocket(wsUrl);
      
      wsRef.current.onopen = () => {
        console.log('WebSocket connected for real-time notifications');
        setConnected(true);
        setSnackbarMessage('Connected to real-time notifications');
        setSnackbarSeverity('success');
        setShowSnackbar(true);
        
        // Start ping interval to keep connection alive
        pingIntervalRef.current = setInterval(() => {
          if (wsRef.current?.readyState === WebSocket.OPEN) {
            wsRef.current.send(JSON.stringify({ type: 'ping' }));
          }
        }, 30000); // Ping every 30 seconds
      };

      wsRef.current.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data);
          handleWebSocketMessage(data);
        } catch (error) {
          console.error('Failed to parse WebSocket message:', error);
        }
      };

      wsRef.current.onclose = (event) => {
        console.log('WebSocket disconnected:', event.code, event.reason);
        setConnected(false);
        
        // Clear ping interval
        if (pingIntervalRef.current) {
          clearInterval(pingIntervalRef.current);
        }
        
        // Attempt to reconnect
        if (event.code !== 1000) { // Not a normal closure
          reconnectTimeoutRef.current = setTimeout(() => {
            console.log('Attempting to reconnect...');
            connectWebSocket();
          }, 5000);
        }
      };

      wsRef.current.onerror = (error) => {
        console.error('WebSocket error:', error);
        setConnected(false);
        setSnackbarMessage('Connection error. Retrying...');
        setSnackbarSeverity('error');
        setShowSnackbar(true);
      };

    } catch (error) {
      console.error('Failed to create WebSocket connection:', error);
      setConnected(false);
    }
  }, [user]);

  const disconnectWebSocket = useCallback(() => {
    if (wsRef.current) {
      wsRef.current.close(1000, 'User initiated disconnect');
    }
    
    if (reconnectTimeoutRef.current) {
      clearTimeout(reconnectTimeoutRef.current);
    }
    
    if (pingIntervalRef.current) {
      clearInterval(pingIntervalRef.current);
    }
    
    setConnected(false);
  }, []);

  const handleWebSocketMessage = (data) => {
    switch (data.type) {
      case 'notification':
        handleNewNotification(data.notification);
        break;
      case 'notification_update':
        handleNotificationUpdate(data.notification);
        break;
      case 'notification_delete':
        handleNotificationDelete(data.notification_id);
        break;
      case 'pong':
        // Server responded to ping
        break;
      default:
        console.log('Unknown WebSocket message type:', data.type);
    }
  };

  const handleNewNotification = (notification) => {
    setNotifications(prev => [notification, ...prev]);
    setUnreadCount(prev => prev + 1);
    setLastUpdate(new Date());
    
    // Show snackbar for high priority notifications
    if (notification.priority === 'high') {
      setSnackbarMessage(notification.title);
      setSnackbarSeverity('error');
      setShowSnackbar(true);
    }
  };

  const handleNotificationUpdate = (updatedNotification) => {
    setNotifications(prev => 
      prev.map(notif => 
        notif.id === updatedNotification.id ? updatedNotification : notif
      )
    );
    setLastUpdate(new Date());
  };

  const handleNotificationDelete = (notificationId) => {
    setNotifications(prev => prev.filter(notif => notif.id !== notificationId));
    setLastUpdate(new Date());
  };

  const markAsRead = async (notificationId) => {
    try {
      // Update local state immediately for better UX
      setNotifications(prev => 
        prev.map(notif => 
          notif.id === notificationId 
            ? { ...notif, read: true }
            : notif
        )
      );
      
      // Update unread count
      setUnreadCount(prev => Math.max(0, prev - 1));
      
      // Send update to server via WebSocket
      if (wsRef.current?.readyState === WebSocket.OPEN) {
        wsRef.current.send(JSON.stringify({
          type: 'mark_read',
          notification_id: notificationId
        }));
      }
      
      // Also update via REST API as fallback
      // await apiClient.patch(`/ml/notifications/${notificationId}/read`);
      
    } catch (error) {
      console.error('Failed to mark notification as read:', error);
    }
  };

  const markAllAsRead = async () => {
    try {
      // Update local state
      setNotifications(prev => prev.map(notif => ({ ...notif, read: true })));
      setUnreadCount(0);
      
      // Send to server
      if (wsRef.current?.readyState === WebSocket.OPEN) {
        wsRef.current.send(JSON.stringify({ type: 'mark_all_read' }));
      }
      
    } catch (error) {
      console.error('Failed to mark all notifications as read:', error);
    }
  };

  const dismissNotification = async (notificationId) => {
    try {
      // Remove from local state
      setNotifications(prev => prev.filter(notif => notif.id !== notificationId));
      
      // Update unread count if it was unread
      const notification = notifications.find(n => n.id === notificationId);
      if (notification && !notification.read) {
        setUnreadCount(prev => Math.max(0, prev - 1));
      }
      
      // Send to server
      if (wsRef.current?.readyState === WebSocket.OPEN) {
        wsRef.current.send(JSON.stringify({
          type: 'dismiss',
          notification_id: notificationId
        }));
      }
      
    } catch (error) {
      console.error('Failed to dismiss notification:', error);
    }
  };

  const getPriorityIcon = (priority) => {
    switch (priority) {
      case 'high':
        return <PriorityHighIcon color="error" />;
      case 'medium':
        return <WarningIcon color="warning" />;
      case 'low':
        return <InfoIcon color="info" />;
      default:
        return <InfoIcon color="info" />;
    }
  };

  const getPriorityColor = (priority) => {
    switch (priority) {
      case 'high':
        return 'error';
      case 'medium':
        return 'warning';
      case 'low':
        return 'success';
      default:
        return 'default';
    }
  };

  const formatTimestamp = (timestamp) => {
    if (!timestamp) return 'Unknown';
    const date = new Date(timestamp);
    const now = new Date();
    const diffMs = now - date;
    const diffMins = Math.floor(diffMs / 60000);
    
    if (diffMins < 1) return 'Just now';
    if (diffMins < 60) return `${diffMins}m ago`;
    if (diffMins < 1440) return `${Math.floor(diffMins / 60)}h ago`;
    return `${Math.floor(diffMins / 1440)}d ago`;
  };

  // Connection management effects
  useEffect(() => {
    if (user) {
      connectWebSocket();
    }
    
    return () => {
      disconnectWebSocket();
    };
  }, [user, connectWebSocket, disconnectWebSocket]);

  // Cleanup on unmount
  useEffect(() => {
    return () => {
      disconnectWebSocket();
    };
  }, [disconnectWebSocket]);

  const renderNotificationItem = (notification, index) => (
    <Slide direction="left" in={true} timeout={300 + index * 100}>
      <ListItem
        sx={{
          mb: 1,
          borderRadius: 1,
          backgroundColor: notification.read ? 'transparent' : 'action.hover',
          border: notification.read ? '1px solid transparent' : `1px solid ${theme.palette.primary.light}`,
          '&:hover': {
            backgroundColor: 'action.hover',
            transform: 'translateX(4px)',
            transition: 'all 0.2s ease-in-out'
          }
        }}
      >
        <ListItemIcon>
          {getPriorityIcon(notification.priority)}
        </ListItemIcon>
        
        <ListItemText
          primary={
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
              <Typography 
                variant="subtitle2" 
                sx={{ 
                  fontWeight: notification.read ? 400 : 600,
                  color: notification.read ? 'text.secondary' : 'text.primary'
                }}
              >
                {notification.title}
              </Typography>
              {!notification.read && (
                <Chip 
                  label="NEW" 
                  size="small" 
                  color="primary" 
                  variant="outlined"
                  sx={{ height: 20, fontSize: '0.7rem' }}
                />
              )}
            </Box>
          }
          secondary={
            <Box>
              <Typography variant="body2" color="text.secondary" sx={{ mb: 1 }}>
                {notification.message}
              </Typography>
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                <Chip 
                  label={notification.notification_type} 
                  size="small" 
                  variant="outlined"
                  color={getPriorityColor(notification.priority)}
                />
                <Typography variant="caption" color="text.secondary">
                  {formatTimestamp(notification.created_at)}
                </Typography>
              </Box>
            </Box>
          }
        />
        
        <ListItemSecondaryAction>
          <Box sx={{ display: 'flex', gap: 1 }}>
            {!notification.read && (
              <IconButton
                size="small"
                onClick={() => markAsRead(notification.id)}
                sx={{ color: 'primary.main' }}
              >
                <CheckCircleIcon fontSize="small" />
              </IconButton>
            )}
            <IconButton
              size="small"
              onClick={() => dismissNotification(notification.id)}
              sx={{ color: 'text.secondary' }}
            >
              <CloseIcon fontSize="small" />
            </IconButton>
          </Box>
        </ListItemSecondaryAction>
      </ListItem>
    </Slide>
  );

  return (
    <>
      {/* Notification Bell with Badge */}
      <Box sx={{ position: 'relative' }}>
        <IconButton
          onClick={() => setExpanded(!expanded)}
          sx={{ 
            color: connected ? 'primary.main' : 'text.secondary',
            position: 'relative'
          }}
        >
          {connected ? <NotificationsActiveIcon /> : <NotificationsNoneIcon />}
        </IconButton>
        
        {unreadCount > 0 && (
          <Badge
            badgeContent={unreadCount}
            color="error"
            sx={{
              position: 'absolute',
              top: -8,
              right: -8,
              '& .MuiBadge-badge': {
                fontSize: '0.7rem',
                height: 20,
                minWidth: 20
              }
            }}
          />
        )}
      </Box>

      {/* Notifications Panel */}
      <Collapse in={expanded} timeout="auto">
        <Card
          sx={{
            position: 'absolute',
            top: '100%',
            right: 0,
            width: 400,
            maxHeight: 600,
            overflow: 'auto',
            zIndex: 1000,
            boxShadow: 3,
            mt: 1
          }}
        >
          <CardContent sx={{ p: 0 }}>
            {/* Header */}
            <Box sx={{ 
              p: 2, 
              borderBottom: `1px solid ${theme.palette.divider}`,
              backgroundColor: theme.palette.background.default
            }}>
              <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                <Typography variant="h6" sx={{ fontWeight: 600 }}>
                  Real-Time Notifications
                </Typography>
                <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                  <Chip 
                    label={connected ? 'Connected' : 'Disconnected'} 
                    size="small" 
                    color={connected ? 'success' : 'error'}
                    variant="outlined"
                  />
                  <IconButton size="small" onClick={() => setExpanded(false)}>
                    <CloseIcon />
                  </IconButton>
                </Box>
              </Box>
              
              {lastUpdate && (
                <Typography variant="caption" color="text.secondary">
                  Last update: {formatTimestamp(lastUpdate)}
                </Typography>
              )}
            </Box>

            {/* Actions */}
            {notifications.length > 0 && (
              <Box sx={{ p: 2, borderBottom: `1px solid ${theme.palette.divider}` }}>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                  <Typography variant="body2" color="text.secondary">
                    {unreadCount} unread of {notifications.length} total
                  </Typography>
                  <Button
                    size="small"
                    variant="outlined"
                    onClick={markAllAsRead}
                    disabled={unreadCount === 0}
                  >
                    Mark All Read
                  </Button>
                </Box>
              </Box>
            )}

            {/* Notifications List */}
            <Box sx={{ maxHeight: 400, overflow: 'auto' }}>
              {notifications.length === 0 ? (
                <Box sx={{ p: 3, textAlign: 'center' }}>
                  <NotificationsNoneIcon sx={{ fontSize: 48, color: 'text.secondary', mb: 2 }} />
                  <Typography variant="body2" color="text.secondary">
                    No notifications yet
                  </Typography>
                  <Typography variant="caption" color="text.secondary">
                    You'll see real-time updates here
                  </Typography>
                </Box>
              ) : (
                <List sx={{ p: 2 }}>
                  {notifications.map((notification, index) => 
                    renderNotificationItem(notification, index)
                  )}
                </List>
              )}
            </Box>

            {/* Footer */}
            <Box sx={{ 
              p: 2, 
              borderTop: `1px solid ${theme.palette.divider}`,
              backgroundColor: theme.palette.background.default
            }}>
              <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <Typography variant="caption" color="text.secondary">
                  Powered by Phase 4B AI
                </Typography>
                <IconButton size="small" onClick={connectWebSocket} disabled={connected}>
                  <RefreshIcon />
                </IconButton>
              </Box>
            </Box>
          </CardContent>
        </Card>
      </Collapse>

      {/* Connection Status Snackbar */}
      <Snackbar
        open={showSnackbar}
        autoHideDuration={4000}
        onClose={() => setShowSnackbar(false)}
        anchorOrigin={{ vertical: 'bottom', horizontal: 'right' }}
      >
        <Alert 
          onClose={() => setShowSnackbar(false)} 
          severity={snackbarSeverity}
          sx={{ width: '100%' }}
        >
          {snackbarMessage}
        </Alert>
      </Snackbar>
    </>
  );
};

export default RealTimeNotifications;
