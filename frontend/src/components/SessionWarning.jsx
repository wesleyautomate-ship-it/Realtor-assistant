import React from 'react';
import {
  Alert,
  AlertTitle,
  Button,
  Box,
  Stack,
  Typography,
  CircularProgress,
  useTheme,
  Fade,
  Grow,
} from '@mui/material';
import {
  Warning as WarningIcon,
  Refresh as RefreshIcon,
  Close as CloseIcon,
  Timer as TimerIcon,
} from '@mui/icons-material';
import { useAppContext } from '../context/AppContext';

const SessionWarning = () => {
  const theme = useTheme();
  const { sessionWarning, clearSessionWarning, refreshToken } = useAppContext();
  const [isRefreshing, setIsRefreshing] = React.useState(false);

  if (!sessionWarning) {
    return null;
  }

  const handleRefreshSession = async () => {
    setIsRefreshing(true);
    try {
      const success = await refreshToken();
      if (success) {
        // Warning will be cleared automatically by the context
        console.log('Session refreshed successfully');
      } else {
        console.error('Failed to refresh session');
      }
    } catch (error) {
      console.error('Error refreshing session:', error);
    } finally {
      setIsRefreshing(false);
    }
  };

  const handleDismiss = () => {
    clearSessionWarning();
  };

  const getSeverity = () => {
    if (sessionWarning.minutesLeft <= 1) return 'error';
    if (sessionWarning.minutesLeft <= 3) return 'warning';
    return 'info';
  };

  const getIcon = () => {
    if (sessionWarning.minutesLeft <= 1) return <TimerIcon />;
    return <WarningIcon />;
  };

  return (
    <Fade in={true} timeout={500}>
      <Box
        sx={{
          position: 'fixed',
          top: theme.spacing(2),
          right: theme.spacing(2),
          zIndex: theme.zIndex.snackbar + 1,
          maxWidth: 400,
          minWidth: 350,
        }}
      >
        <Grow in={true} timeout={300}>
          <Alert
            severity={getSeverity()}
            icon={getIcon()}
            action={
              <Stack direction="row" spacing={1} alignItems="center">
                <Button
                  size="small"
                  variant="outlined"
                  startIcon={isRefreshing ? <CircularProgress size={16} /> : <RefreshIcon />}
                  onClick={handleRefreshSession}
                  disabled={isRefreshing}
                  sx={{
                    color: 'inherit',
                    borderColor: 'inherit',
                    '&:hover': {
                      backgroundColor: 'rgba(255, 255, 255, 0.1)',
                    },
                  }}
                >
                  {isRefreshing ? 'Refreshing...' : 'Extend Session'}
                </Button>
                <Button
                  size="small"
                  variant="text"
                  onClick={handleDismiss}
                  sx={{
                    color: 'inherit',
                    minWidth: 'auto',
                    p: 0.5,
                  }}
                >
                  <CloseIcon fontSize="small" />
                </Button>
              </Stack>
            }
            sx={{
              boxShadow: theme.shadows[8],
              borderRadius: 2,
              '& .MuiAlert-message': {
                width: '100%',
              },
            }}
          >
            <AlertTitle sx={{ fontWeight: 600, mb: 0.5 }}>
              Session Expiry Warning
            </AlertTitle>
            <Typography variant="body2" sx={{ mb: 1 }}>
              {sessionWarning.message}
            </Typography>
            <Typography variant="caption" color="text.secondary">
              Click "Extend Session" to stay logged in, or save your work and log in again.
            </Typography>
          </Alert>
        </Grow>
      </Box>
    </Fade>
  );
};

export default SessionWarning;
