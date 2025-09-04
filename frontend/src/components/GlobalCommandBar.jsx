import React, { useState, useEffect, useRef } from 'react';
import {
  Dialog,
  DialogContent,
  DialogTitle,
  TextField,
  InputAdornment,
  Button,
  IconButton,
  Typography,
  Box,
  Snackbar,
  Alert,
  Stack,
  Chip,
  Divider,
} from '@mui/material';
import {
  Search as SearchIcon,
  Close as CloseIcon,
  Send as SendIcon,
  Keyboard as KeyboardIcon,
  Lightbulb as LightbulbIcon,
} from '@mui/icons-material';
import { apiUtils, handleApiError } from '../utils/api';

const GlobalCommandBar = ({ 
  open, 
  onClose, 
  onCommandExecuted 
}) => {
  const [command, setCommand] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(null);
  const inputRef = useRef(null);

  // Sample command suggestions
  const commandSuggestions = [
    {
      label: 'Generate CMA',
      command: 'Generate a Comparative Market Analysis for 123 Main St',
      icon: <LightbulbIcon />,
      category: 'Analysis'
    },
    {
      label: 'Client Follow-up',
      command: 'Help me prepare a follow-up email for client John Smith',
      icon: <LightbulbIcon />,
      category: 'Communication'
    },
    {
      label: 'Market Report',
      command: 'Create a market report for Downtown area properties',
      icon: <LightbulbIcon />,
      category: 'Reports'
    },
    {
      label: 'Property Research',
      command: 'Research recent sales in the Marina district',
      icon: <LightbulbIcon />,
      category: 'Research'
    }
  ];

  useEffect(() => {
    if (open && inputRef.current) {
      // Focus the input when dialog opens
      setTimeout(() => {
        inputRef.current?.focus();
      }, 100);
    }
  }, [open]);

  useEffect(() => {
    if (open) {
      setCommand('');
      setError(null);
      setSuccess(null);
    }
  }, [open]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!command.trim()) return;

    try {
      setLoading(true);
      setError(null);
      setSuccess(null);

      const result = await apiUtils.sendGlobalCommand(command.trim());
      
      setSuccess('Command executed successfully!');
      
      if (onCommandExecuted) {
        onCommandExecuted(result);
      }

      // Auto-close after a short delay
      setTimeout(() => {
        onClose();
      }, 1500);

    } catch (error) {
      console.error('Error executing command:', error);
      const errorMessage = handleApiError(error);
      setError(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  const handleSuggestionClick = (suggestion) => {
    setCommand(suggestion.command);
    inputRef.current?.focus();
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Escape') {
      onClose();
    }
  };

  const groupedSuggestions = commandSuggestions.reduce((acc, suggestion) => {
    if (!acc[suggestion.category]) {
      acc[suggestion.category] = [];
    }
    acc[suggestion.category].push(suggestion);
    return acc;
  }, {});

  return (
    <>
      <Dialog
        open={open}
        onClose={onClose}
        maxWidth="md"
        fullWidth
        PaperProps={{
          sx: {
            borderRadius: 2,
            boxShadow: '0 8px 32px rgba(0,0,0,0.12)',
          }
        }}
      >
        <DialogTitle sx={{ pb: 1 }}>
          <Stack direction="row" alignItems="center" justifyContent="space-between">
            <Stack direction="row" alignItems="center" spacing={1}>
              <SearchIcon color="primary" />
              <Typography variant="h6">
                AI Command Center
              </Typography>
            </Stack>
            <Stack direction="row" alignItems="center" spacing={1}>
              <Chip
                icon={<KeyboardIcon />}
                label="Ctrl+K"
                size="small"
                variant="outlined"
                sx={{ fontSize: '0.75rem' }}
              />
              <IconButton onClick={onClose} size="small">
                <CloseIcon />
              </IconButton>
            </Stack>
          </Stack>
          <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
            Ask me anything about your real estate business
          </Typography>
        </DialogTitle>

        <DialogContent sx={{ pt: 0 }}>
          <form onSubmit={handleSubmit}>
            <TextField
              ref={inputRef}
              fullWidth
              variant="outlined"
              placeholder="e.g., Generate a CMA for 123 Main St, Help me prepare for a client meeting..."
              value={command}
              onChange={(e) => setCommand(e.target.value)}
              onKeyDown={handleKeyDown}
              disabled={loading}
              InputProps={{
                startAdornment: (
                  <InputAdornment position="start">
                    <SearchIcon color="action" />
                  </InputAdornment>
                ),
                endAdornment: (
                  <InputAdornment position="end">
                    {loading ? (
                      <Box sx={{ display: 'flex', alignItems: 'center' }}>
                        <Typography variant="caption" color="text.secondary" sx={{ mr: 1 }}>
                          Processing...
                        </Typography>
                      </Box>
                    ) : (
                      <Button
                        type="submit"
                        variant="contained"
                        size="small"
                        disabled={!command.trim()}
                        startIcon={<SendIcon />}
                        sx={{ minWidth: 'auto' }}
                      >
                        Send
                      </Button>
                    )}
                  </InputAdornment>
                ),
              }}
              sx={{
                '& .MuiOutlinedInput-root': {
                  borderRadius: 2,
                  fontSize: '1rem',
                }
              }}
            />
          </form>

          {error && (
            <Alert severity="error" sx={{ mt: 2 }}>
              {error}
            </Alert>
          )}

          {success && (
            <Alert severity="success" sx={{ mt: 2 }}>
              {success}
            </Alert>
          )}

          <Divider sx={{ my: 3 }} />

          <Box>
            <Typography variant="subtitle2" gutterBottom sx={{ mb: 2 }}>
              Quick Commands
            </Typography>
            
            {Object.entries(groupedSuggestions).map(([category, suggestions]) => (
              <Box key={category} sx={{ mb: 3 }}>
                <Typography variant="caption" color="text.secondary" sx={{ mb: 1, display: 'block' }}>
                  {category}
                </Typography>
                <Stack direction="row" flexWrap="wrap" gap={1}>
                  {suggestions.map((suggestion, index) => (
                    <Chip
                      key={index}
                      label={suggestion.label}
                      icon={suggestion.icon}
                      onClick={() => handleSuggestionClick(suggestion)}
                      variant="outlined"
                      clickable
                      sx={{
                        '&:hover': {
                          backgroundColor: 'action.hover',
                        }
                      }}
                    />
                  ))}
                </Stack>
              </Box>
            ))}
          </Box>

          <Box sx={{ mt: 3, p: 2, bgcolor: 'action.hover', borderRadius: 1 }}>
            <Typography variant="caption" color="text.secondary">
              <strong>Tip:</strong> You can ask me to analyze documents, generate reports, 
              prepare for meetings, research properties, and much more. Just describe what you need!
            </Typography>
          </Box>
        </DialogContent>
      </Dialog>

      <Snackbar
        open={!!success}
        autoHideDuration={3000}
        onClose={() => setSuccess(null)}
      >
        <Alert onClose={() => setSuccess(null)} severity="success">
          {success}
        </Alert>
      </Snackbar>
    </>
  );
};

export default GlobalCommandBar;
