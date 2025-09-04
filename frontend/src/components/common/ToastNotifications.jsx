import React, { useState, useEffect, useCallback } from 'react';
import {
  Snackbar,
  Alert,
  Box,
  IconButton,
  Collapse,
  useTheme,
  Fade,
  Grow,
} from '@mui/material';
import {
  Close as CloseIcon,
  CheckCircle as CheckCircleIcon,
  Error as ErrorIcon,
  Info as InfoIcon,
  Warning as WarningIcon,
} from '@mui/icons-material';
import { 
  PRIORITY_COLORS, 
  SPACING_SCALE, 
  BORDER_RADIUS, 
  TRANSITIONS,
  SHADOWS 
} from '../../theme/designSystem';

// Toast notification context and provider
const ToastContext = React.createContext();

export const useToast = () => {
  const context = React.useContext(ToastContext);
  if (!context) {
    throw new Error('useToast must be used within a ToastProvider');
  }
  return context;
};

// Toast notification types
export const TOAST_TYPES = {
  SUCCESS: 'success',
  ERROR: 'error',
  WARNING: 'warning',
  INFO: 'info',
};

// Toast notification component
const Toast = ({ 
  id, 
  type, 
  message, 
  title, 
  duration = 6000, 
  onClose, 
  action,
  ...props 
}) => {
  const theme = useTheme();
  const [open, setOpen] = useState(true);
  const [expanded, setExpanded] = useState(false);

  useEffect(() => {
    if (duration > 0) {
      const timer = setTimeout(() => {
        handleClose();
      }, duration);
      return () => clearTimeout(timer);
    }
  }, [duration]);

  const handleClose = useCallback(() => {
    setOpen(false);
    setTimeout(() => {
      onClose(id);
    }, 300); // Allow animation to complete
  }, [id, onClose]);

  const getToastIcon = () => {
    switch (type) {
      case TOAST_TYPES.SUCCESS:
        return <CheckCircleIcon sx={{ color: PRIORITY_COLORS.low.primary }} />;
      case TOAST_TYPES.ERROR:
        return <ErrorIcon sx={{ color: PRIORITY_COLORS.high.primary }} />;
      case TOAST_TYPES.WARNING:
        return <WarningIcon sx={{ color: PRIORITY_COLORS.medium.primary }} />;
      case TOAST_TYPES.INFO:
        return <InfoIcon sx={{ color: PRIORITY_COLORS.ai.primary }} />;
      default:
        return <InfoIcon sx={{ color: PRIORITY_COLORS.neutral.primary }} />;
    }
  };

  const getToastColor = () => {
    switch (type) {
      case TOAST_TYPES.SUCCESS:
        return PRIORITY_COLORS.low.primary;
      case TOAST_TYPES.ERROR:
        return PRIORITY_COLORS.high.primary;
      case TOAST_TYPES.WARNING:
        return PRIORITY_COLORS.medium.primary;
      case TOAST_TYPES.INFO:
        return PRIORITY_COLORS.ai.primary;
      default:
        return PRIORITY_COLORS.neutral.primary;
    }
  };

  const getToastBackground = () => {
    switch (type) {
      case TOAST_TYPES.SUCCESS:
        return PRIORITY_COLORS.low.light;
      case TOAST_TYPES.ERROR:
        return PRIORITY_COLORS.high.light;
      case TOAST_TYPES.WARNING:
        return PRIORITY_COLORS.medium.light;
      case TOAST_TYPES.INFO:
        return PRIORITY_COLORS.ai.light;
      default:
        return PRIORITY_COLORS.neutral.light;
    }
  };

  return (
    <Grow in={open} timeout={300}>
      <Box
        sx={{
          mb: 2,
          borderRadius: BORDER_RADIUS.lg,
          boxShadow: SHADOWS.lg,
          overflow: 'hidden',
          bgcolor: 'background.paper',
          border: `1px solid ${theme.palette.divider}`,
          maxWidth: 400,
          minWidth: 300,
        }}
      >
        <Box
          sx={{
            display: 'flex',
            alignItems: 'flex-start',
            p: 2,
            bgcolor: getToastBackground(),
            borderLeft: `4px solid ${getToastColor()}`,
          }}
        >
          {/* Icon */}
          <Box sx={{ mr: 2, mt: 0.5 }}>
            {getToastIcon()}
          </Box>

          {/* Content */}
          <Box sx={{ flex: 1, minWidth: 0 }}>
            {title && (
              <Box
                sx={{
                  fontWeight: 600,
                  fontSize: '0.875rem',
                  color: 'text.primary',
                  mb: 0.5,
                }}
              >
                {title}
              </Box>
            )}
            
            <Box
              sx={{
                fontSize: '0.875rem',
                color: 'text.secondary',
                lineHeight: 1.4,
              }}
            >
              {message}
            </Box>

            {/* Action */}
            {action && (
              <Box sx={{ mt: 1.5 }}>
                {action}
              </Box>
            )}
          </Box>

          {/* Close Button */}
          <IconButton
            size="small"
            onClick={handleClose}
            sx={{
              ml: 1,
              color: 'text.secondary',
              '&:hover': {
                bgcolor: 'action.hover',
                color: 'text.primary',
              },
            }}
          >
            <CloseIcon fontSize="small" />
          </IconButton>
        </Box>
      </Box>
    </Grow>
  );
};

// Toast container component
const ToastContainer = ({ toasts, onClose }) => {
  const theme = useTheme();

  return (
    <Box
      sx={{
        position: 'fixed',
        top: SPACING_SCALE.lg,
        right: SPACING_SCALE.lg,
        zIndex: theme.zIndex.snackbar,
        maxWidth: 400,
        pointerEvents: 'none',
      }}
    >
      {toasts.map((toast) => (
        <Box
          key={toast.id}
          sx={{
            pointerEvents: 'auto',
            mb: 1,
          }}
        >
          <Toast
            {...toast}
            onClose={onClose}
          />
        </Box>
      ))}
    </Box>
  );
};

// Toast provider component
export const ToastProvider = ({ children }) => {
  const [toasts, setToasts] = useState([]);
  const [counter, setCounter] = useState(0);

  const addToast = useCallback((toast) => {
    const id = counter;
    setCounter(prev => prev + 1);
    
    const newToast = {
      id,
      type: TOAST_TYPES.INFO,
      duration: 6000,
      ...toast,
    };

    setToasts(prev => [...prev, newToast]);

    // Auto-remove toast after duration
    if (newToast.duration > 0) {
      setTimeout(() => {
        removeToast(id);
      }, newToast.duration);
    }

    return id;
  }, [counter]);

  const removeToast = useCallback((id) => {
    setToasts(prev => prev.filter(toast => toast.id !== id));
  }, []);

  const clearToasts = useCallback(() => {
    setToasts([]);
  }, []);

  const showSuccess = useCallback((message, options = {}) => {
    return addToast({
      type: TOAST_TYPES.SUCCESS,
      message,
      title: 'Success',
      ...options,
    });
  }, [addToast]);

  const showError = useCallback((message, options = {}) => {
    return addToast({
      type: TOAST_TYPES.ERROR,
      message,
      title: 'Error',
      duration: 8000, // Longer duration for errors
      ...options,
    });
  }, [addToast]);

  const showWarning = useCallback((message, options = {}) => {
    return addToast({
      type: TOAST_TYPES.WARNING,
      message,
      title: 'Warning',
      ...options,
    });
  }, [addToast]);

  const showInfo = useCallback((message, options = {}) => {
    return addToast({
      type: TOAST_TYPES.INFO,
      message,
      title: 'Information',
      ...options,
    });
  }, [addToast]);

  const contextValue = {
    addToast,
    removeToast,
    clearToasts,
    showSuccess,
    showError,
    showWarning,
    showInfo,
    toasts,
  };

  return (
    <ToastContext.Provider value={contextValue}>
      {children}
      <ToastContainer toasts={toasts} onClose={removeToast} />
    </ToastContext.Provider>
  );
};

// Inline notification component for use within components
export const InlineNotification = ({ 
  type = TOAST_TYPES.INFO, 
  message, 
  title, 
  onClose, 
  showClose = true,
  action,
  ...props 
}) => {
  const theme = useTheme();
  const [visible, setVisible] = useState(true);

  const handleClose = () => {
    setVisible(false);
    onClose?.();
  };

  if (!visible) return null;

  const getNotificationColor = () => {
    switch (type) {
      case TOAST_TYPES.SUCCESS:
        return PRIORITY_COLORS.low.primary;
      case TOAST_TYPES.ERROR:
        return PRIORITY_COLORS.high.primary;
      case TOAST_TYPES.WARNING:
        return PRIORITY_COLORS.medium.primary;
      case TOAST_TYPES.INFO:
        return PRIORITY_COLORS.ai.primary;
      default:
        return PRIORITY_COLORS.neutral.primary;
    }
  };

  const getNotificationBackground = () => {
    switch (type) {
      case TOAST_TYPES.SUCCESS:
        return PRIORITY_COLORS.low.light;
      case TOAST_TYPES.ERROR:
        return PRIORITY_COLORS.high.light;
      case TOAST_TYPES.WARNING:
        return PRIORITY_COLORS.medium.light;
      case TOAST_TYPES.INFO:
        return PRIORITY_COLORS.ai.light;
      default:
        return PRIORITY_COLORS.neutral.light;
    }
  };

  return (
    <Collapse in={visible} timeout={300}>
      <Box
        sx={{
          p: 2,
          borderRadius: BORDER_RADIUS.md,
          bgcolor: getNotificationBackground(),
          border: `1px solid ${getNotificationColor()}`,
          borderLeft: `4px solid ${getNotificationColor()}`,
          mb: 2,
          ...props.sx,
        }}
        {...props}
      >
        <Box sx={{ display: 'flex', alignItems: 'flex-start' }}>
          <Box sx={{ flex: 1 }}>
            {title && (
              <Box
                sx={{
                  fontWeight: 600,
                  fontSize: '0.875rem',
                  color: 'text.primary',
                  mb: 0.5,
                }}
              >
                {title}
              </Box>
            )}
            
            <Box
              sx={{
                fontSize: '0.875rem',
                color: 'text.secondary',
                lineHeight: 1.4,
              }}
            >
              {message}
            </Box>

            {action && (
              <Box sx={{ mt: 1.5 }}>
                {action}
              </Box>
            )}
          </Box>

          {showClose && (
            <IconButton
              size="small"
              onClick={handleClose}
              sx={{
                ml: 1,
                color: 'text.secondary',
                '&:hover': {
                  bgcolor: 'action.hover',
                  color: 'text.primary',
                },
              }}
            >
              <CloseIcon fontSize="small" />
            </IconButton>
          )}
        </Box>
      </Box>
    </Collapse>
  );
};

export default ToastProvider;
