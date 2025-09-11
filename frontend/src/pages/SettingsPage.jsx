import React, { useState } from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  Switch,
  FormControlLabel,
  Divider,
  Alert,
  Snackbar,
  useTheme,
  Grid,
  Paper,
  Stack,
} from '@mui/material';
import {
  Notifications as NotificationsIcon,
  Security as SecurityIcon,
  Language as LanguageIcon,
  Palette as PaletteIcon,
  VolumeUp as VolumeIcon,
} from '@mui/icons-material';
import { useAppContext } from '../context/AppContext';

const SettingsPage = () => {
  const theme = useTheme();
  const { currentUser } = useAppContext();
  const [snackbar, setSnackbar] = useState({ open: false, message: '', severity: 'info' });
  
  // Settings state
  const [settings, setSettings] = useState({
    notifications: {
      email: true,
      push: true,
      sms: false,
    },
    privacy: {
      profileVisibility: 'public',
      dataSharing: false,
    },
    appearance: {
      theme: 'light',
      language: 'en',
    },
    audio: {
      soundEffects: true,
      voiceCommands: true,
    },
  });

  const handleSettingChange = (category, setting) => (event) => {
    const value = event.target.type === 'checkbox' ? event.target.checked : event.target.value;
    setSettings(prev => ({
      ...prev,
      [category]: {
        ...prev[category],
        [setting]: value
      }
    }));
    
    setSnackbar({
      open: true,
      message: 'Setting updated successfully!',
      severity: 'success'
    });
  };

  const handleCloseSnackbar = () => {
    setSnackbar({ ...snackbar, open: false });
  };

  return (
    <Box sx={{ p: 3, maxWidth: 800, mx: 'auto' }}>
      {/* Header */}
      <Box sx={{ mb: 4 }}>
        <Typography variant="h4" sx={{ fontWeight: 700, mb: 1 }}>
          Settings
        </Typography>
        <Typography variant="body1" color="text.secondary">
          Customize your experience and preferences
        </Typography>
      </Box>

      <Grid container spacing={3}>
        {/* Notifications Settings */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent sx={{ p: 3 }}>
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 3 }}>
                <NotificationsIcon color="primary" />
                <Typography variant="h6" sx={{ fontWeight: 600 }}>
                  Notifications
                </Typography>
              </Box>
              
              <Stack spacing={2}>
                <FormControlLabel
                  control={
                    <Switch
                      checked={settings.notifications.email}
                      onChange={handleSettingChange('notifications', 'email')}
                      color="primary"
                    />
                  }
                  label="Email Notifications"
                />
                
                <FormControlLabel
                  control={
                    <Switch
                      checked={settings.notifications.push}
                      onChange={handleSettingChange('notifications', 'push')}
                      color="primary"
                    />
                  }
                  label="Push Notifications"
                />
                
                <FormControlLabel
                  control={
                    <Switch
                      checked={settings.notifications.sms}
                      onChange={handleSettingChange('notifications', 'sms')}
                      color="primary"
                    />
                  }
                  label="SMS Notifications"
                />
              </Stack>
            </CardContent>
          </Card>
        </Grid>

        {/* Privacy Settings */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent sx={{ p: 3 }}>
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 3 }}>
                <SecurityIcon color="primary" />
                <Typography variant="h6" sx={{ fontWeight: 600 }}>
                  Privacy & Security
                </Typography>
              </Box>
              
              <Stack spacing={2}>
                <FormControlLabel
                  control={
                    <Switch
                      checked={settings.privacy.dataSharing}
                      onChange={handleSettingChange('privacy', 'dataSharing')}
                      color="primary"
                    />
                  }
                  label="Allow Data Sharing for Analytics"
                />
                
                <Alert severity="info" sx={{ mt: 2 }}>
                  Your personal data is encrypted and secure. We never share your information with third parties.
                </Alert>
              </Stack>
            </CardContent>
          </Card>
        </Grid>

        {/* Appearance Settings */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent sx={{ p: 3 }}>
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 3 }}>
                <PaletteIcon color="primary" />
                <Typography variant="h6" sx={{ fontWeight: 600 }}>
                  Appearance
                </Typography>
              </Box>
              
              <Stack spacing={2}>
                <Alert severity="info">
                  Theme and language settings will be available in a future update.
                </Alert>
              </Stack>
            </CardContent>
          </Card>
        </Grid>

        {/* Audio Settings */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent sx={{ p: 3 }}>
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 3 }}>
                <VolumeIcon color="primary" />
                <Typography variant="h6" sx={{ fontWeight: 600 }}>
                  Audio & Voice
                </Typography>
              </Box>
              
              <Stack spacing={2}>
                <FormControlLabel
                  control={
                    <Switch
                      checked={settings.audio.soundEffects}
                      onChange={handleSettingChange('audio', 'soundEffects')}
                      color="primary"
                    />
                  }
                  label="Sound Effects"
                />
                
                <FormControlLabel
                  control={
                    <Switch
                      checked={settings.audio.voiceCommands}
                      onChange={handleSettingChange('audio', 'voiceCommands')}
                      color="primary"
                    />
                  }
                  label="Voice Commands"
                />
              </Stack>
            </CardContent>
          </Card>
        </Grid>

        {/* Future Features */}
        <Grid item xs={12}>
          <Card>
            <CardContent sx={{ p: 3 }}>
              <Typography variant="h6" sx={{ fontWeight: 600, mb: 2 }}>
                Coming Soon
              </Typography>
              <Alert severity="info" sx={{ mb: 2 }}>
                Additional settings and customization options will be available in future updates.
              </Alert>
              <Typography variant="body2" color="text.secondary">
                Planned features include:
              </Typography>
              <Box component="ul" sx={{ mt: 1, pl: 2 }}>
                <Typography component="li" variant="body2" color="text.secondary">
                  Dark/Light theme toggle
                </Typography>
                <Typography component="li" variant="body2" color="text.secondary">
                  Multi-language support
                </Typography>
                <Typography component="li" variant="body2" color="text.secondary">
                  Advanced notification preferences
                </Typography>
                <Typography component="li" variant="body2" color="text.secondary">
                  Keyboard shortcuts customization
                </Typography>
                <Typography component="li" variant="body2" color="text.secondary">
                  Data export and backup options
                </Typography>
              </Box>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

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
    </Box>
  );
};

export default SettingsPage;
