import React, { useState, useEffect, useRef } from 'react';
import {
  Box,
  Paper,
  TextField,
  IconButton,
  Typography,
  List,
  ListItem,
  ListItemText,
  Divider,
  Button,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Chip,
  Avatar,
  Tooltip,
  Fab,
  Drawer,
  ListItemIcon,
  ListItemButton,
  ListItemSecondaryAction,
  IconButton as MuiIconButton,
  Menu,
  MenuItem,
  Snackbar,
  Alert
} from '@mui/material';
import {
  Send as SendIcon,
  Add as AddIcon,
  Delete as DeleteIcon,
  Edit as EditIcon,
  Clear as ClearIcon,
  Settings as SettingsIcon,
  Person as PersonIcon,
  SmartToy as BotIcon,
  MoreVert as MoreVertIcon,
  Refresh as RefreshIcon,
  ContentCopy as CopyIcon,
  Download as DownloadIcon
} from '@mui/icons-material';
import { styled } from '@mui/material/styles';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8001';

// Styled components
const ChatContainer = styled(Box)(({ theme }) => ({
  height: '100vh',
  display: 'flex',
  flexDirection: 'column',
  backgroundColor: theme.palette.background.default,
}));

const Sidebar = styled(Paper)(({ theme }) => ({
  width: 300,
  height: '100%',
  borderRadius: 0,
  borderRight: `1px solid ${theme.palette.divider}`,
  display: 'flex',
  flexDirection: 'column',
  backgroundColor: theme.palette.background.paper,
}));

const ChatArea = styled(Box)(({ theme }) => ({
  flex: 1,
  display: 'flex',
  flexDirection: 'column',
  backgroundColor: theme.palette.background.default,
}));

const MessageContainer = styled(Box)(({ theme, isUser }) => ({
  display: 'flex',
  justifyContent: isUser ? 'flex-end' : 'flex-start',
  marginBottom: theme.spacing(2),
  padding: theme.spacing(0, 2),
}));

const MessageBubble = styled(Paper)(({ theme, isUser }) => ({
  maxWidth: '70%',
  padding: theme.spacing(2),
  backgroundColor: isUser 
    ? theme.palette.primary.main 
    : theme.palette.background.paper,
  color: isUser 
    ? theme.palette.primary.contrastText 
    : theme.palette.text.primary,
  borderRadius: theme.spacing(2),
  boxShadow: theme.shadows[2],
  wordWrap: 'break-word',
  '& pre': {
    backgroundColor: theme.palette.grey[100],
    padding: theme.spacing(1),
    borderRadius: theme.spacing(1),
    overflow: 'auto',
    margin: theme.spacing(1, 0),
  },
  '& code': {
    backgroundColor: theme.palette.grey[100],
    padding: theme.spacing(0.5),
    borderRadius: theme.spacing(0.5),
    fontFamily: 'monospace',
  },
}));

const InputContainer = styled(Box)(({ theme }) => ({
  padding: theme.spacing(2),
  borderTop: `1px solid ${theme.palette.divider}`,
  backgroundColor: theme.palette.background.paper,
}));

const ChatGPTStyleChat = () => {
  const [sessions, setSessions] = useState([]);
  const [currentSession, setCurrentSession] = useState(null);
  const [messages, setMessages] = useState([]);
  const [inputMessage, setInputMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [selectedRole, setSelectedRole] = useState('client');
  const [userPreferences, setUserPreferences] = useState({});
  const [showNewChatDialog, setShowNewChatDialog] = useState(false);
  const [newChatTitle, setNewChatTitle] = useState('');
  const [showSettings, setShowSettings] = useState(false);
  const [anchorEl, setAnchorEl] = useState(null);
  const [snackbar, setSnackbar] = useState({ open: false, message: '', severity: 'info' });

  const messagesEndRef = useRef(null);
  const inputRef = useRef(null);

  // Auto-scroll to bottom
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Load sessions on component mount
  useEffect(() => {
    loadSessions();
  }, []);

  const loadSessions = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/sessions`);
      if (response.ok) {
        const data = await response.json();
        setSessions(data.sessions);
        
        // Auto-select first session if none selected
        if (!currentSession && data.sessions.length > 0) {
          setCurrentSession(data.sessions[0]);
          loadSessionHistory(data.sessions[0].session_id);
        }
      }
    } catch (error) {
      console.error('Error loading sessions:', error);
      showSnackbar('Error loading chat sessions', 'error');
    }
  };

  const loadSessionHistory = async (sessionId) => {
    try {
      const response = await fetch(`${API_BASE_URL}/sessions/${sessionId}`);
      if (response.ok) {
        const data = await response.json();
        setMessages(data.messages);
        setUserPreferences(data.user_preferences || {});
      }
    } catch (error) {
      console.error('Error loading session history:', error);
      showSnackbar('Error loading chat history', 'error');
    }
  };

  const createNewSession = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/sessions`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          title: newChatTitle || 'New Chat',
          role: selectedRole,
          user_preferences: userPreferences
        }),
      });

      if (response.ok) {
        const newSession = await response.json();
        setSessions(prev => [newSession, ...prev]);
        setCurrentSession(newSession);
        setMessages([]);
        setShowNewChatDialog(false);
        setNewChatTitle('');
        showSnackbar('New chat session created', 'success');
      }
    } catch (error) {
      console.error('Error creating new session:', error);
      showSnackbar('Error creating new chat session', 'error');
    }
  };

  const handleSendMessage = async () => {
    if (!inputMessage.trim() || !currentSession) return;

    const userMessage = {
      id: Date.now(),
      role: 'user',
      content: inputMessage,
      timestamp: new Date().toISOString(),
      message_type: 'text'
    };

    setMessages(prev => [...prev, userMessage]);
    setInputMessage('');
    setIsLoading(true);

    try {
      const response = await fetch(`${API_BASE_URL}/sessions/${currentSession.session_id}/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message: inputMessage,
          role: selectedRole,
          session_id: currentSession.session_id
        }),
      });

      if (response.ok) {
        const data = await response.json();
        const assistantMessage = {
          id: Date.now() + 1,
          role: 'assistant',
          content: data.response,
          timestamp: new Date().toISOString(),
          message_type: 'text'
        };

        setMessages(prev => [...prev, assistantMessage]);
        
        // Reload sessions to update message count
        loadSessions();
      } else {
        throw new Error('Failed to send message');
      }
    } catch (error) {
      console.error('Error sending message:', error);
      showSnackbar('Error sending message', 'error');
    } finally {
      setIsLoading(false);
    }
  };

  const deleteSession = async (sessionId) => {
    try {
      const response = await fetch(`${API_BASE_URL}/sessions/${sessionId}`, {
        method: 'DELETE',
      });

      if (response.ok) {
        setSessions(prev => prev.filter(s => s.session_id !== sessionId));
        if (currentSession?.session_id === sessionId) {
          setCurrentSession(null);
          setMessages([]);
        }
        showSnackbar('Chat session deleted', 'success');
      }
    } catch (error) {
      console.error('Error deleting session:', error);
      showSnackbar('Error deleting chat session', 'error');
    }
  };

  const clearSession = async (sessionId) => {
    try {
      const response = await fetch(`${API_BASE_URL}/sessions/${sessionId}/clear`, {
        method: 'POST',
      });

      if (response.ok) {
        setMessages([]);
        showSnackbar('Chat session cleared', 'success');
      }
    } catch (error) {
      console.error('Error clearing session:', error);
      showSnackbar('Error clearing chat session', 'error');
    }
  };

  const updateSessionTitle = async (sessionId, newTitle) => {
    try {
      const response = await fetch(`${API_BASE_URL}/sessions/${sessionId}/title`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ title: newTitle }),
      });

      if (response.ok) {
        setSessions(prev => 
          prev.map(s => 
            s.session_id === sessionId 
              ? { ...s, title: newTitle }
              : s
          )
        );
        if (currentSession?.session_id === sessionId) {
          setCurrentSession(prev => ({ ...prev, title: newTitle }));
        }
        showSnackbar('Session title updated', 'success');
      }
    } catch (error) {
      console.error('Error updating session title:', error);
      showSnackbar('Error updating session title', 'error');
    }
  };

  const showSnackbar = (message, severity = 'info') => {
    setSnackbar({ open: true, message, severity });
  };

  const handleKeyPress = (event) => {
    if (event.key === 'Enter' && !event.shiftKey) {
      event.preventDefault();
      handleSendMessage();
    }
  };

  const formatMessage = (content) => {
    // Simple markdown-like formatting
    return content
      .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
      .replace(/\*(.*?)\*/g, '<em>$1</em>')
      .replace(/`(.*?)`/g, '<code>$1</code>')
      .replace(/\n/g, '<br />');
  };

  return (
    <ChatContainer>
      {/* Sidebar */}
      <Drawer
        variant="persistent"
        anchor="left"
        open={sidebarOpen}
        sx={{
          width: 300,
          flexShrink: 0,
          '& .MuiDrawer-paper': {
            width: 300,
            boxSizing: 'border-box',
          },
        }}
      >
        <Sidebar>
          {/* Header */}
          <Box sx={{ p: 2, borderBottom: 1, borderColor: 'divider' }}>
            <Button
              variant="contained"
              startIcon={<AddIcon />}
              fullWidth
              onClick={() => setShowNewChatDialog(true)}
              sx={{ mb: 1 }}
            >
              New Chat
            </Button>
            <Button
              variant="outlined"
              startIcon={<SettingsIcon />}
              fullWidth
              onClick={() => setShowSettings(true)}
            >
              Settings
            </Button>
          </Box>

          {/* Sessions List */}
          <Box sx={{ flex: 1, overflow: 'auto' }}>
            <List>
              {sessions.map((session) => (
                <ListItem
                  key={session.session_id}
                  disablePadding
                  selected={currentSession?.session_id === session.session_id}
                >
                  <ListItemButton
                    onClick={() => {
                      setCurrentSession(session);
                      loadSessionHistory(session.session_id);
                    }}
                    sx={{ py: 1 }}
                  >
                    <ListItemIcon>
                      <PersonIcon />
                    </ListItemIcon>
                    <ListItemText
                      primary={session.title}
                      secondary={`${session.message_count} messages`}
                      primaryTypographyProps={{
                        noWrap: true,
                        fontSize: '0.9rem'
                      }}
                      secondaryTypographyProps={{
                        fontSize: '0.75rem'
                      }}
                    />
                    <ListItemSecondaryAction>
                      <MuiIconButton
                        edge="end"
                        onClick={(e) => {
                          e.stopPropagation();
                          setAnchorEl(e.currentTarget);
                        }}
                        size="small"
                      >
                        <MoreVertIcon />
                      </MuiIconButton>
                    </ListItemSecondaryAction>
                  </ListItemButton>
                </ListItem>
              ))}
            </List>
          </Box>
        </Sidebar>
      </Drawer>

      {/* Main Chat Area */}
      <Box sx={{ 
        flex: 1, 
        display: 'flex', 
        flexDirection: 'column',
        ml: sidebarOpen ? '300px' : 0,
        transition: 'margin-left 0.3s ease'
      }}>
        {/* Chat Header */}
        <Paper sx={{ p: 2, borderBottom: 1, borderColor: 'divider' }}>
          <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
            <Box sx={{ display: 'flex', alignItems: 'center' }}>
              <IconButton
                onClick={() => setSidebarOpen(!sidebarOpen)}
                sx={{ mr: 1 }}
              >
                <MoreVertIcon />
              </IconButton>
              <Typography variant="h6">
                {currentSession?.title || 'Select a chat session'}
              </Typography>
            </Box>
            {currentSession && (
              <Box>
                <Chip 
                  label={selectedRole} 
                  size="small" 
                  color="primary" 
                  sx={{ mr: 1 }}
                />
                <IconButton
                  onClick={() => clearSession(currentSession.session_id)}
                  size="small"
                >
                  <ClearIcon />
                </IconButton>
              </Box>
            )}
          </Box>
        </Paper>

        {/* Messages Area */}
        <Box sx={{ 
          flex: 1, 
          overflow: 'auto', 
          p: 2,
          backgroundColor: 'background.default'
        }}>
          {messages.length === 0 ? (
            <Box sx={{ 
              display: 'flex', 
              flexDirection: 'column', 
              alignItems: 'center', 
              justifyContent: 'center',
              height: '100%',
              textAlign: 'center'
            }}>
              <BotIcon sx={{ fontSize: 64, color: 'text.secondary', mb: 2 }} />
              <Typography variant="h6" color="text.secondary" gutterBottom>
                Dubai Real Estate AI Assistant
              </Typography>
              <Typography variant="body2" color="text.secondary">
                Start a conversation to get expert advice on Dubai real estate
              </Typography>
            </Box>
          ) : (
            messages.map((message) => (
              <MessageContainer key={message.id} isUser={message.role === 'user'}>
                <MessageBubble isUser={message.role === 'user'}>
                  <Box sx={{ display: 'flex', alignItems: 'flex-start', gap: 1 }}>
                    <Avatar sx={{ width: 32, height: 32, mt: 0.5 }}>
                      {message.role === 'user' ? <PersonIcon /> : <BotIcon />}
                    </Avatar>
                    <Box sx={{ flex: 1 }}>
                      <Typography
                        variant="body1"
                        dangerouslySetInnerHTML={{ 
                          __html: formatMessage(message.content) 
                        }}
                        sx={{ 
                          whiteSpace: 'pre-wrap',
                          '& strong': { fontWeight: 'bold' },
                          '& em': { fontStyle: 'italic' },
                          '& code': { 
                            backgroundColor: 'grey.100',
                            padding: 0.5,
                            borderRadius: 0.5,
                            fontFamily: 'monospace'
                          }
                        }}
                      />
                      <Typography variant="caption" color="text.secondary" sx={{ mt: 1, display: 'block' }}>
                        {new Date(message.timestamp).toLocaleTimeString()}
                      </Typography>
                    </Box>
                  </Box>
                </MessageBubble>
              </MessageContainer>
            ))
          )}
          <div ref={messagesEndRef} />
        </Box>

        {/* Input Area */}
        <InputContainer>
          <Box sx={{ display: 'flex', gap: 1, alignItems: 'flex-end' }}>
            <TextField
              ref={inputRef}
              fullWidth
              multiline
              maxRows={4}
              value={inputMessage}
              onChange={(e) => setInputMessage(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Type your message..."
              disabled={!currentSession || isLoading}
              variant="outlined"
              size="small"
            />
            <IconButton
              onClick={handleSendMessage}
              disabled={!inputMessage.trim() || !currentSession || isLoading}
              color="primary"
              sx={{ 
                backgroundColor: 'primary.main',
                color: 'primary.contrastText',
                '&:hover': {
                  backgroundColor: 'primary.dark',
                },
                '&:disabled': {
                  backgroundColor: 'grey.300',
                  color: 'grey.500',
                }
              }}
            >
              <SendIcon />
            </IconButton>
          </Box>
        </InputContainer>
      </Box>

      {/* New Chat Dialog */}
      <Dialog open={showNewChatDialog} onClose={() => setShowNewChatDialog(false)}>
        <DialogTitle>Start New Chat</DialogTitle>
        <DialogContent>
          <TextField
            autoFocus
            margin="dense"
            label="Chat Title"
            fullWidth
            value={newChatTitle}
            onChange={(e) => setNewChatTitle(e.target.value)}
            placeholder="Enter chat title..."
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setShowNewChatDialog(false)}>Cancel</Button>
          <Button onClick={createNewSession} variant="contained">
            Create
          </Button>
        </DialogActions>
      </Dialog>

      {/* Session Menu */}
      <Menu
        anchorEl={anchorEl}
        open={Boolean(anchorEl)}
        onClose={() => setAnchorEl(null)}
      >
        <MenuItem onClick={() => {
          // Handle edit title
          setAnchorEl(null);
        }}>
          <ListItemIcon>
            <EditIcon fontSize="small" />
          </ListItemIcon>
          Edit Title
        </MenuItem>
        <MenuItem onClick={() => {
          deleteSession(currentSession?.session_id);
          setAnchorEl(null);
        }}>
          <ListItemIcon>
            <DeleteIcon fontSize="small" />
          </ListItemIcon>
          Delete
        </MenuItem>
      </Menu>

      {/* Snackbar */}
      <Snackbar
        open={snackbar.open}
        autoHideDuration={6000}
        onClose={() => setSnackbar({ ...snackbar, open: false })}
      >
        <Alert 
          onClose={() => setSnackbar({ ...snackbar, open: false })} 
          severity={snackbar.severity}
        >
          {snackbar.message}
        </Alert>
      </Snackbar>
    </ChatContainer>
  );
};

export default ChatGPTStyleChat;
