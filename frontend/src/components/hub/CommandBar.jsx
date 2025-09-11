import React, { useState, useRef, useEffect } from 'react';
import {
  Box,
  TextField,
  IconButton,
  Paper,
  Typography,
  InputAdornment,
  useTheme,
  Fade,
  Grow,
  Chip,
  Stack,
  Menu,
  MenuItem,
  Divider,
  Tooltip,
} from '@mui/material';
import { useNavigate } from 'react-router-dom';
import { useAppContext } from '../../context/AppContext';
import {
  Mic as MicIcon,
  MicOff as MicOffIcon,
  Send as SendIcon,
  Keyboard as KeyboardIcon,
  SmartToy as SmartToyIcon,
  AutoAwesome as MagicIcon,
  Assessment as CMAAIcon,
  Home as PropertyIcon,
  TrendingUp as AnalyticsIcon,
  Security as ComplianceIcon,
  Schedule as ScheduleIcon,
  ExpandMore as ExpandMoreIcon,
} from '@mui/icons-material';

const CommandBar = ({ onSendMessage, suggestions = [], placeholder = "Ask me to generate a CMA, compare properties, or analyze compliance..." }) => {
  const theme = useTheme();
  const navigate = useNavigate();
  const { logout } = useAppContext();
  const [input, setInput] = useState('');
  const [isListening, setIsListening] = useState(false);
  const [isFocused, setIsFocused] = useState(false);
  const [currentHint, setCurrentHint] = useState(0);
  const [templateMenuAnchor, setTemplateMenuAnchor] = useState(null);
  const inputRef = useRef(null);

  // Rotating hints for AI command center feel
  const rotatingHints = [
    "Generate a CMA for Dubai Marina properties",
    "Compare investment opportunities in Downtown Dubai",
    "Check RERA compliance for new listing",
    "Analyze market trends for 3-bedroom villas",
    "Create client follow-up sequence",
    "Find properties under 2M AED with high ROI potential",
    "Try: 'Log me out' or 'Update profile'",
    "Voice commands: 'Go to profile' or 'Open settings'"
  ];

  // Quick action templates
  const quickTemplates = [
    { icon: <CMAAIcon />, label: "Create CMA", command: "Generate a comparative market analysis for" },
    { icon: <PropertyIcon />, label: "Find Properties", command: "Find properties in" },
    { icon: <AnalyticsIcon />, label: "Market Analysis", command: "Analyze market trends for" },
    { icon: <ComplianceIcon />, label: "Compliance Check", command: "Check RERA compliance for" },
    { icon: <ScheduleIcon />, label: "Schedule Viewing", command: "Schedule a property viewing for" },
  ];

  // Rotate hints every 3 seconds
  useEffect(() => {
    const interval = setInterval(() => {
      setCurrentHint((prev) => (prev + 1) % rotatingHints.length);
    }, 3000);
    return () => clearInterval(interval);
  }, []);

  // Handle keyboard shortcuts
  useEffect(() => {
    const handleKeyDown = (event) => {
      if (event.ctrlKey && event.key === 'k') {
        event.preventDefault();
        inputRef.current?.focus();
      }
    };

    document.addEventListener('keydown', handleKeyDown);
    return () => document.removeEventListener('keydown', handleKeyDown);
  }, []);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (input.trim()) {
      processCommand(input.trim());
      setInput('');
    }
  };

  // Process voice and text commands
  const processCommand = (command) => {
    const lowerCommand = command.toLowerCase();
    
    // Voice commands for logout
    if (lowerCommand.includes('log me out') || lowerCommand.includes('logout') || lowerCommand.includes('sign out')) {
      handleLogout();
      return;
    }
    
    // Voice commands for profile
    if (lowerCommand.includes('update profile') || lowerCommand.includes('edit profile') || lowerCommand.includes('go to profile')) {
      navigate('/profile');
      return;
    }
    
    // Voice commands for settings
    if (lowerCommand.includes('settings') || lowerCommand.includes('preferences')) {
      navigate('/settings');
      return;
    }
    
    // Default: send to AI assistant
    if (onSendMessage) {
      onSendMessage(command);
    }
  };

  const handleLogout = async () => {
    try {
      // Call backend logout endpoint
      const { api } = await import('../../utils/apiClient');
      await api.post('/auth/logout');
    } catch (error) {
      console.error('Logout API call failed:', error);
      // Continue with logout even if API call fails
    } finally {
      // Clear local storage and state
      logout();
      navigate('/login');
    }
  };

  const handleVoiceToggle = () => {
    setIsListening(!isListening);
    // TODO: Implement voice recognition
    console.log('Voice recognition:', !isListening ? 'started' : 'stopped');
  };

  const handleSuggestionClick = (suggestion) => {
    setInput(suggestion);
    inputRef.current?.focus();
  };

  const handleTemplateClick = (template) => {
    setInput(template.command + ' ');
    setTemplateMenuAnchor(null);
    inputRef.current?.focus();
  };

  const handleTemplateMenuOpen = (event) => {
    setTemplateMenuAnchor(event.currentTarget);
  };

  const handleTemplateMenuClose = () => {
    setTemplateMenuAnchor(null);
  };

  return (
    <Box sx={{ width: '100%', maxWidth: 1000, mx: 'auto' }}>
      {/* AI Command Center Header */}
      <Box sx={{ textAlign: 'center', mb: 3 }}>
        <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: 1, mb: 1 }}>
          <MagicIcon sx={{ color: 'primary.main', fontSize: 28 }} />
          <Typography variant="h5" sx={{ fontWeight: 700, color: 'text.primary' }}>
            AI Command Center
          </Typography>
        </Box>
        <Typography variant="body1" color="text.secondary">
          Your intelligent assistant for real estate operations
        </Typography>
      </Box>

      {/* Main Command Bar */}
      <Paper
        elevation={isFocused ? 12 : 4}
        sx={{
          borderRadius: 4,
          overflow: 'hidden',
          transition: 'all 0.3s ease',
          border: isFocused ? `3px solid ${theme.palette.primary.main}` : '3px solid transparent',
          background: isFocused 
            ? 'linear-gradient(135deg, #f8f9ff 0%, #ffffff 100%)'
            : 'linear-gradient(135deg, #ffffff 0%, #f8f9ff 100%)',
        }}
      >
        <Box
          component="form"
          onSubmit={handleSubmit}
          sx={{
            display: 'flex',
            alignItems: 'center',
            p: 2,
            minHeight: 80,
          }}
        >
          <InputAdornment position="start" sx={{ ml: 1 }}>
            <SmartToyIcon sx={{ color: 'primary.main', fontSize: 28 }} />
          </InputAdornment>
          
          <TextField
            ref={inputRef}
            fullWidth
            variant="standard"
            placeholder={placeholder}
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onFocus={() => setIsFocused(true)}
            onBlur={() => setIsFocused(false)}
            InputProps={{
              disableUnderline: true,
              sx: {
                fontSize: '1.2rem',
                fontWeight: 500,
                '&::placeholder': {
                  color: 'text.secondary',
                  opacity: 0.8,
                },
              },
            }}
            sx={{ flex: 1, mx: 2 }}
          />

          <Stack direction="row" spacing={1}>
            <Tooltip title="Quick Templates">
              <IconButton
                onClick={handleTemplateMenuOpen}
                sx={{
                  backgroundColor: 'primary.light',
                  color: 'primary.contrastText',
                  '&:hover': {
                    backgroundColor: 'primary.main',
                  },
                }}
              >
                <ExpandMoreIcon />
              </IconButton>
            </Tooltip>

            <Tooltip title={isListening ? "Stop Voice" : "Start Voice"}>
              <IconButton
                onClick={handleVoiceToggle}
                color={isListening ? 'error' : 'default'}
                sx={{
                  backgroundColor: isListening ? 'error.light' : 'action.hover',
                  '&:hover': {
                    backgroundColor: isListening ? 'error.main' : 'action.selected',
                  },
                }}
              >
                {isListening ? <MicOffIcon /> : <MicIcon />}
              </IconButton>
            </Tooltip>

            <Tooltip title="Send Command">
              <IconButton
                type="submit"
                disabled={!input.trim()}
                sx={{
                  backgroundColor: input.trim() ? 'primary.main' : 'action.hover',
                  color: input.trim() ? 'primary.contrastText' : 'text.secondary',
                  '&:hover': {
                    backgroundColor: input.trim() ? 'primary.dark' : 'action.selected',
                  },
                }}
              >
                <SendIcon />
              </IconButton>
            </Tooltip>
          </Stack>
        </Box>
      </Paper>

      {/* Rotating Hint */}
      <Fade key={currentHint} in={true} timeout={500}>
        <Box sx={{ mt: 2, textAlign: 'center' }}>
          <Typography variant="body2" color="primary.main" sx={{ fontWeight: 500 }}>
            💡 {rotatingHints[currentHint]}
          </Typography>
        </Box>
      </Fade>

      {/* Quick Actions Bar */}
      <Box sx={{ mt: 3, mb: 2 }}>
        <Typography variant="subtitle2" color="text.secondary" sx={{ mb: 1, textAlign: 'center' }}>
          Quick Actions
        </Typography>
        <Stack direction="row" spacing={1} justifyContent="center" flexWrap="wrap">
          {quickTemplates.map((template, index) => (
            <Grow in={true} timeout={300 + index * 100} key={index}>
              <Chip
                icon={template.icon}
                label={template.label}
                onClick={() => handleTemplateClick(template)}
                variant="outlined"
                sx={{
                  cursor: 'pointer',
                  borderColor: 'primary.main',
                  color: 'primary.main',
                  '&:hover': {
                    backgroundColor: 'primary.light',
                    color: 'primary.contrastText',
                    borderColor: 'primary.main',
                  },
                }}
              />
            </Grow>
          ))}
        </Stack>
      </Box>

      {/* Template Menu */}
      <Menu
        anchorEl={templateMenuAnchor}
        open={Boolean(templateMenuAnchor)}
        onClose={handleTemplateMenuClose}
        PaperProps={{
          sx: {
            mt: 1,
            minWidth: 200,
            borderRadius: 2,
            boxShadow: '0 8px 32px rgba(0,0,0,0.12)',
          },
        }}
      >
        {quickTemplates.map((template, index) => (
          <MenuItem
            key={index}
            onClick={() => handleTemplateClick(template)}
            sx={{
              display: 'flex',
              alignItems: 'center',
              gap: 1,
              py: 1.5,
            }}
          >
            {template.icon}
            <Typography variant="body2">{template.label}</Typography>
          </MenuItem>
        ))}
      </Menu>

      {/* Keyboard shortcut hint */}
      <Box sx={{ mt: 2, textAlign: 'center' }}>
        <Typography variant="caption" color="text.secondary">
          <KeyboardIcon sx={{ fontSize: 12, mr: 0.5, verticalAlign: 'middle' }} />
          Press Ctrl+K to focus • Voice commands available
        </Typography>
      </Box>
    </Box>
  );
};

export default CommandBar;
