import React, { useState, useEffect, useRef } from 'react';
import {
  Dialog,
  DialogTitle,
  DialogContent,
  TextField,
  Box,
  Typography,
  Chip,
  Button,
  IconButton,
  List,
  ListItem,
  ListItemText,
  ListItemIcon,
  Paper,
  Divider,
  useTheme,
  Fade,
  Grow,
} from '@mui/material';
import {
  Close as CloseIcon,
  Search as SearchIcon,
  Mic as MicIcon,
  History as HistoryIcon,
  Star as StarIcon,
  TrendingUp as TrendingUpIcon,
  Schedule as ScheduleIcon,
  Person as PersonIcon,
  Home as HomeIcon,
  Assessment as AssessmentIcon,
} from '@mui/icons-material';

const SmartCommandBar = ({ open, onClose }) => {
  const theme = useTheme();
  const inputRef = useRef(null);
  const [command, setCommand] = useState('');
  const [suggestions, setSuggestions] = useState([]);
  const [commandHistory, setCommandHistory] = useState([]);
  const [favorites, setFavorites] = useState([]);

  // Mock data for development - will be replaced with real API calls
  const mockSuggestions = [
    {
      id: 1,
      icon: PersonIcon,
      category: 'Client Management',
      commands: [
        'Follow up with Ali Khan about the villa viewing',
        'Schedule a call with Jane Doe for tomorrow',
        'Update client preferences for John Smith',
        'Generate client follow-up email template',
      ],
    },
    {
      id: 2,
      icon: HomeIcon,
      category: 'Property Management',
      commands: [
        'Generate CMA for Villa 12 in Emirates Hills',
        'Find similar properties to the one I just viewed',
        'Update property listing status for Marina Apartment',
        'Create property brochure for Downtown Villa',
      ],
    },
    {
      id: 3,
      icon: AssessmentIcon,
      category: 'Market Analysis',
      commands: [
        'Show me current market trends in Dubai Marina',
        'Analyze price changes in Downtown area',
        'Compare property values across different neighborhoods',
        'Generate weekly market report',
      ],
    },
    {
      id: 4,
      icon: ScheduleIcon,
      category: 'Task Management',
      commands: [
        'Schedule follow-up call for next week',
        'Set reminder for property viewing',
        'Create task list for today',
        'Prioritize my pending tasks',
      ],
    },
  ];

  const mockCommandHistory = [
    'Generate CMA for Villa 12',
    'Follow up with Ali Khan',
    'Show market trends in Dubai Marina',
    'Create property brochure',
    'Schedule client call',
  ];

  const mockFavorites = [
    'Generate CMA for {property}',
    'Follow up with {client}',
    'Show market trends in {location}',
    'Create property brochure for {property}',
  ];

  useEffect(() => {
    if (open) {
      // Focus input when dialog opens
      setTimeout(() => {
        inputRef.current?.focus();
      }, 100);
      
      // Load suggestions and history
      setSuggestions(mockSuggestions);
      setCommandHistory(mockCommandHistory);
      setFavorites(mockFavorites);
    }
  }, [open]);

  useEffect(() => {
    // Add global keyboard shortcut listener
    const handleKeyDown = (event) => {
      if ((event.ctrlKey || event.metaKey) && event.key === 'k') {
        event.preventDefault();
        if (!open) {
          // Open command bar
          onClose && onClose();
        }
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [open, onClose]);

  const handleCommandSubmit = async (commandText) => {
    if (!commandText.trim()) return;

    try {
      // TODO: Send command to AI backend
      console.log('Executing command:', commandText);
      
      // Add to history
      setCommandHistory(prev => [commandText, ...prev.slice(0, 9)]);
      
      // Close dialog
      onClose();
      setCommand('');
      
      // Show success feedback
      // TODO: Implement toast notification
      
    } catch (error) {
      console.error('Command execution failed:', error);
      // TODO: Show error feedback
    }
  };

  const handleSuggestionClick = (suggestion) => {
    setCommand(suggestion);
    inputRef.current?.focus();
  };

  const handleFavoriteClick = (favorite) => {
    // Replace placeholders with actual values
    let processedCommand = favorite;
    
    // TODO: Implement smart placeholder replacement
    // For now, just use the template as-is
    setCommand(processedCommand);
    inputRef.current?.focus();
  };

  const handleVoiceInput = () => {
    // TODO: Implement voice input functionality
    console.log('Voice input not implemented yet');
  };

  const renderSuggestions = () => (
    <Box sx={{ mb: 3 }}>
      <Typography variant="subtitle2" sx={{ color: 'text.secondary', mb: 2 }}>
        💡 Smart Suggestions
      </Typography>
      {suggestions.map((category) => (
        <Box key={category.id} sx={{ mb: 2 }}>
          <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
            <category.icon sx={{ mr: 1, fontSize: 18, color: 'primary.main' }} />
            <Typography variant="body2" sx={{ fontWeight: 600, color: 'text.secondary' }}>
              {category.category}
            </Typography>
          </Box>
          <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
            {category.commands.map((cmd, index) => (
              <Chip
                key={index}
                label={cmd}
                size="small"
                variant="outlined"
                onClick={() => handleSuggestionClick(cmd)}
                sx={{
                  cursor: 'pointer',
                  '&:hover': {
                    bgcolor: 'primary.light',
                    color: 'primary.contrastText',
                  },
                }}
              />
            ))}
          </Box>
        </Box>
      ))}
    </Box>
  );

  const renderCommandHistory = () => (
    <Box sx={{ mb: 3 }}>
      <Typography variant="subtitle2" sx={{ color: 'text.secondary', mb: 2 }}>
        📚 Recent Commands
      </Typography>
      <List dense>
        {commandHistory.slice(0, 5).map((cmd, index) => (
          <ListItem
            key={index}
            button
            onClick={() => handleSuggestionClick(cmd)}
            sx={{
              borderRadius: 1,
              mb: 0.5,
              '&:hover': {
                bgcolor: 'action.hover',
              },
            }}
          >
            <ListItemIcon>
              <HistoryIcon sx={{ fontSize: 18, color: 'text.secondary' }} />
            </ListItemIcon>
            <ListItemText
              primary={cmd}
              primaryTypographyProps={{ variant: 'body2' }}
            />
          </ListItem>
        ))}
      </List>
    </Box>
  );

  const renderFavorites = () => (
    <Box sx={{ mb: 3 }}>
      <Typography variant="subtitle2" sx={{ color: 'text.secondary', mb: 2 }}>
        ⭐ Favorite Commands
      </Typography>
      <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
        {favorites.map((fav, index) => (
          <Chip
            key={index}
            icon={<StarIcon />}
            label={fav}
            size="small"
            variant="outlined"
            onClick={() => handleFavoriteClick(fav)}
            sx={{
              cursor: 'pointer',
              '&:hover': {
                bgcolor: 'warning.light',
                color: 'warning.contrastText',
              },
            }}
          />
        ))}
      </Box>
    </Box>
  );

  return (
    <Dialog
      open={open}
      onClose={onClose}
      maxWidth="md"
      fullWidth
      PaperProps={{
        sx: {
          borderRadius: 3,
          maxHeight: '80vh',
        },
      }}
    >
      <DialogTitle sx={{ pb: 1 }}>
        <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
          <Box sx={{ display: 'flex', alignItems: 'center' }}>
            <SearchIcon sx={{ mr: 1, color: 'primary.main' }} />
            <Typography variant="h6" sx={{ fontWeight: 600 }}>
              AI Command Center
            </Typography>
          </Box>
          <IconButton onClick={onClose} size="small">
            <CloseIcon />
          </IconButton>
        </Box>
        <Typography variant="body2" sx={{ color: 'text.secondary', mt: 0.5 }}>
          Your AI Copilot is ready to help. Type your command or choose from suggestions below.
        </Typography>
      </DialogTitle>

      <DialogContent sx={{ pt: 0 }}>
        {/* Command Input */}
        <Box sx={{ mb: 3 }}>
          <TextField
            ref={inputRef}
            fullWidth
            variant="outlined"
            placeholder="Type your command or question..."
            value={command}
            onChange={(e) => setCommand(e.target.value)}
            onKeyPress={(e) => {
              if (e.key === 'Enter') {
                handleCommandSubmit(command);
              }
            }}
            InputProps={{
              startAdornment: (
                <SearchIcon sx={{ mr: 1, color: 'text.secondary' }} />
              ),
              endAdornment: (
                <Box sx={{ display: 'flex', gap: 1 }}>
                  <IconButton
                    size="small"
                    onClick={handleVoiceInput}
                    sx={{ color: 'primary.main' }}
                  >
                    <MicIcon />
                  </IconButton>
                  <Button
                    variant="contained"
                    size="small"
                    onClick={() => handleCommandSubmit(command)}
                    disabled={!command.trim()}
                  >
                    Execute
                  </Button>
                </Box>
              ),
            }}
            sx={{
              '& .MuiOutlinedInput-root': {
                borderRadius: 2,
                fontSize: '1.1rem',
              },
            }}
          />
        </Box>

        {/* Content Area */}
        <Box sx={{ display: 'flex', gap: 3 }}>
          {/* Left Column: Suggestions and History */}
          <Box sx={{ flex: 1 }}>
            <Grow in timeout={200}>
              <Box>
                {renderSuggestions()}
                {renderCommandHistory()}
              </Box>
            </Grow>
          </Box>

          {/* Right Column: Favorites and Quick Actions */}
          <Box sx={{ width: 300 }}>
            <Grow in timeout={400}>
              <Box>
                {renderFavorites()}
                
                {/* Quick Actions */}
                <Box>
                  <Typography variant="subtitle2" sx={{ color: 'text.secondary', mb: 2 }}>
                    ⚡ Quick Actions
                  </Typography>
                  <Box sx={{ display: 'flex', flexDirection: 'column', gap: 1 }}>
                    <Button
                      variant="outlined"
                      size="small"
                      startIcon={<TrendingUpIcon />}
                      onClick={() => handleSuggestionClick('Show me today\'s market insights')}
                      fullWidth
                    >
                      Market Insights
                    </Button>
                    <Button
                      variant="outlined"
                      size="small"
                      startIcon={<ScheduleIcon />}
                      onClick={() => handleSuggestionClick('Show my agenda for today')}
                      fullWidth
                    >
                      Today\'s Agenda
                    </Button>
                    <Button
                      variant="outlined"
                      size="small"
                      startIcon={<PersonIcon />}
                      onClick={() => handleSuggestionClick('Show my active leads')}
                      fullWidth
                    >
                      Active Leads
                    </Button>
                  </Box>
                </Box>
              </Box>
            </Grow>
          </Box>
        </Box>
      </DialogContent>
    </Dialog>
  );
};

export default SmartCommandBar;
