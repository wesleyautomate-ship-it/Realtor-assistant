import React, { useState, useEffect, useRef, useCallback } from 'react';
import {
  Box,
  Typography,
  TextField,
  Button,
  IconButton,
  Avatar,
  CircularProgress,
  Alert,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Input,
  Snackbar,
  useMediaQuery,
  useTheme,
  Stack,
  Fade,
  Divider,
  Paper,
  Chip,
  Tooltip,
  Drawer,
  List,
  ListItem,
  ListItemButton,
  ListItemText,
  ListItemIcon,
  Badge,
} from '@mui/material';
import {
  Send as SendIcon,
  AttachFile as AttachFileIcon,
  Person as PersonIcon,
  SmartToy as BotIcon,
  Close as CloseIcon,
  Help as HelpIcon,
  Info as InfoIcon,
  Mic as MicIcon,
  MicOff as MicOffIcon,
  MoreVert as MoreVertIcon,
  Refresh as RefreshIcon,
  Menu as MenuIcon,
  Chat as ChatIcon,
  Add as AddIcon,
  History as HistoryIcon,
} from '@mui/icons-material';
import ReactMarkdown from 'react-markdown';
import { useParams, useNavigate, useLocation } from 'react-router-dom';
import { useAppContext } from '../context/AppContext';
import { api } from '../utils/apiClient';

const Chat = () => {
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('md'));
  const isSmallScreen = useMediaQuery(theme.breakpoints.down('sm'));
  
  const { sessionId } = useParams();
  const navigate = useNavigate();
  const location = useLocation();
  const { currentUser, setCurrentSessionId, conversations, createNewConversation } = useAppContext();
  
  // State management
  const [messages, setMessages] = useState([]);
  const [inputMessage, setInputMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [uploadDialogOpen, setUploadDialogOpen] = useState(false);
  const [uploadedFile, setUploadedFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [snackbar, setSnackbar] = useState({ open: false, message: '', severity: 'info' });
  const [isRecording, setIsRecording] = useState(false);
  const [showHelp, setShowHelp] = useState(false);
  const [propertyDetectionEnabled, setPropertyDetectionEnabled] = useState(true);
  const [detectedProperties, setDetectedProperties] = useState([]);
  
  // Session panel state
  const [sessionPanelOpen, setSessionPanelOpen] = useState(!isMobile);
  const [isCreatingChat, setIsCreatingChat] = useState(false);
  
  const messagesEndRef = useRef(null);
  const [isNearBottom, setIsNearBottom] = useState(true);

  // Help examples for mobile-first design with property detection
  const helpExamples = [
    "Show me 2-bedroom apartments in Dubai Marina under 3M AED",
    "What's the current market trend in Palm Jumeirah?",
    "Calculate ROI for a 2M AED apartment in Dubai Marina",
    "Find villas in Palm Jumeirah with 4+ bedrooms",
    "What are the hot areas in Dubai right now?",
    "Compare rental yields across different areas",
    "Analyze this property image for market value",
    "Detect property details from this description",
    "Generate market analysis report for Dubai Marina",
    "Create investment opportunity analysis"
  ];

  useEffect(() => {
    if (sessionId && sessionId !== 'undefined') {
      setCurrentSessionId(sessionId);
      fetchConversationHistory();
    } else if (!sessionId) {
      createNewSession();
    }
  }, [sessionId, setCurrentSessionId]);

  useEffect(() => {
    if (location.state?.prepopulatedPrompt && sessionId) {
      setInputMessage(location.state.prepopulatedPrompt);
      navigate(location.pathname, { replace: true, state: {} });
    }
  }, [location.state, sessionId, navigate]);

  useEffect(() => {
    if (!sessionId && currentUser) {
      createNewSession();
    }
  }, [currentUser, sessionId]);

  useEffect(() => {
    if (isNearBottom) {
      scrollToBottom();
    }
  }, [messages, isNearBottom]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const handleScroll = (event) => {
    const { scrollTop, scrollHeight, clientHeight } = event.target;
    const threshold = 100;
    const isNearBottomNow = scrollHeight - scrollTop - clientHeight < threshold;
    setIsNearBottom(isNearBottomNow);
  };

  const createNewSession = async () => {
    if (isLoading || isCreatingChat) return;

    try {
      setIsCreatingChat(true);
      const newConversation = await createNewConversation();
      if (newConversation && newConversation.id) {
        setCurrentSessionId(newConversation.id);
        navigate(`/chat/${newConversation.id}`);
        setMessages([]);
        setError(null);
        if (isMobile) {
          setSessionPanelOpen(false);
        }
      } else {
        throw new Error('Failed to create new conversation');
      }
    } catch (error) {
      console.error('Error creating new session:', error);
      setError('Failed to create new chat session. Please try again.');
      setSnackbar({
        open: true,
        message: 'Failed to create new chat session. Please try again.',
        severity: 'error',
      });
    } finally {
      setIsCreatingChat(false);
    }
  };

  // Handle session selection
  const handleSessionSelect = (selectedSessionId) => {
    if (selectedSessionId !== sessionId) {
      navigate(`/chat/${selectedSessionId}`);
      if (isMobile) {
        setSessionPanelOpen(false);
      }
    }
  };

  // Format conversation title
  const getConversationTitle = (conversation) => {
    if (conversation.title) return conversation.title;
    if (conversation.messages && conversation.messages.length > 0) {
      const firstMessage = conversation.messages[0];
      return firstMessage.content.substring(0, 50) + (firstMessage.content.length > 50 ? '...' : '');
    }
    return `Chat ${conversation.id}`;
  };

  // Format conversation time
  const getConversationTime = (conversation) => {
    if (conversation.updated_at) {
      const date = new Date(conversation.updated_at);
      const now = new Date();
      const diffInHours = (now - date) / (1000 * 60 * 60);
      
      if (diffInHours < 1) {
        return 'Just now';
      } else if (diffInHours < 24) {
        return `${Math.floor(diffInHours)}h ago`;
      } else if (diffInHours < 168) { // 7 days
        return `${Math.floor(diffInHours / 24)}d ago`;
      } else {
        return date.toLocaleDateString();
      }
    }
    return 'Unknown';
  };

  const fetchConversationHistory = async () => {
    if (!sessionId || sessionId === 'undefined') return;

    try {
      setIsLoading(true);
      const response = await api.getConversationHistory(sessionId);
      
      const convertedMessages = (response.messages || []).map(msg => ({
        id: msg.id,
        type: msg.role === 'user' ? 'user' : 'ai',
        content: msg.content || '',
        timestamp: msg.timestamp,
        interactive: msg.interactive || false,
        suggestions: msg.suggestions || [],
        context_used: msg.context_used || [],
      }));
      
      const sortedMessages = convertedMessages.sort((a, b) => 
        new Date(a.timestamp) - new Date(b.timestamp)
      );
      
      setMessages(sortedMessages);
    } catch (error) {
      console.error('Error fetching conversation history:', error);
      setError(error.message || 'An error occurred');
      setSnackbar({
        open: true,
        message: error.message || 'An error occurred',
        severity: 'error',
      });
    } finally {
      setIsLoading(false);
    }
  };

  const sendMessage = async () => {
    if (!inputMessage.trim() || isLoading) return;

    const userMessage = {
      id: Date.now().toString(),
      type: 'user',
      content: inputMessage,
      timestamp: new Date().toISOString(),
    };

    setMessages(prev => [...prev, userMessage]);
    setInputMessage('');
    setIsLoading(true);

    try {
      // First, try property detection if enabled
      let propertyDetectionResult = null;
      if (propertyDetectionEnabled) {
        propertyDetectionResult = await handlePropertyDetection(inputMessage);
      }

      const response = await api.sendMessageWithPropertyDetection(sessionId, inputMessage, uploadedFile, true);
      
      const aiMessage = {
        id: response.message_id || Date.now().toString(),
        type: 'ai',
        content: response.response || response.content || '',
        timestamp: new Date().toISOString(),
        interactive: response.interactive || false,
        suggestions: response.suggestions || [],
        context_used: response.context_used || [],
      };

      setMessages(prev => [...prev, aiMessage]);
      setUploadedFile(null);
    } catch (error) {
      console.error('Error sending message:', error);
      setError(error.message || 'An error occurred');
      setSnackbar({
        open: true,
        message: error.message || 'An error occurred',
        severity: 'error',
      });
    } finally {
      setIsLoading(false);
    }
  };

  const handleFileUpload = async (event) => {
    const file = event.target.files[0];
    if (!file) return;

    setUploading(true);
    try {
      // Check if it's an image file for property detection
      const isImage = file.type.startsWith('image/');
      
      if (isImage && propertyDetectionEnabled) {
        // Use property detection API for images
        const detectionResult = await api.detectPropertyFromImage(file, sessionId);
        
        if (detectionResult.properties && detectionResult.properties.length > 0) {
          setDetectedProperties(detectionResult.properties);
          setSnackbar({
            open: true,
            message: `Detected ${detectionResult.properties.length} property(ies) in image!`,
            severity: 'success',
          });
        }
      }

      const uploadResponse = await api.uploadFile(file, sessionId);
      
      setUploadedFile({
        id: uploadResponse.file_id,
        name: file.name,
        size: file.size,
      });
      
      setUploadDialogOpen(false);
      setSnackbar({
        open: true,
        message: 'File uploaded successfully!',
        severity: 'success',
      });
    } catch (error) {
      console.error('Error uploading file:', error);
      setSnackbar({
        open: true,
        message: error.message || 'An error occurred',
        severity: 'error',
      });
    } finally {
      setUploading(false);
    }
  };

  const handlePropertyDetection = async (message) => {
    if (!propertyDetectionEnabled) return;

    try {
      const detectionResult = await api.detectPropertyFromText(message, sessionId);
      
      if (detectionResult.properties && detectionResult.properties.length > 0) {
        setDetectedProperties(detectionResult.properties);
        return detectionResult;
      }
    } catch (error) {
      console.error('Error detecting properties:', error);
    }
    
    return null;
  };

  const handleInteractiveAction = (suggestion) => {
    setInputMessage(suggestion);
  };

  const handleCloseSnackbar = () => {
    setSnackbar({ ...snackbar, open: false });
  };

  // Modern Message Bubble Component
  const MessageBubble = ({ message }) => {
    const isUser = message.type === 'user';

    return (
      <Fade in={true} timeout={300}>
        <Box sx={{ 
          display: 'flex', 
          justifyContent: isUser ? 'flex-end' : 'flex-start', 
          mb: 2,
          px: isMobile ? 2 : 3
        }}>
          <Box sx={{ 
            display: 'flex', 
            alignItems: 'flex-start', 
            gap: 1, 
            maxWidth: isMobile ? '90%' : '80%',
            flexDirection: isUser ? 'row-reverse' : 'row'
          }}>
            {!isUser && (
              <Avatar sx={{ 
                bgcolor: 'primary.main', 
                width: 32, 
                height: 32,
                boxShadow: '0 2px 8px rgba(0,0,0,0.1)'
              }}>
                <BotIcon fontSize="small" />
              </Avatar>
            )}
            
            <Paper sx={{ 
              bgcolor: isUser ? 'primary.main' : 'background.paper', 
              color: isUser ? 'primary.contrastText' : 'text.primary',
              border: 1, 
              borderColor: isUser ? 'primary.main' : 'divider',
              borderRadius: 3,
              maxWidth: '100%',
              boxShadow: '0 2px 8px rgba(0,0,0,0.08)',
              overflow: 'hidden'
            }}>
              <Box sx={{ p: 2 }}>
                {isUser ? (
                  <Typography variant="body1" sx={{ lineHeight: 1.5 }}>
                    {message.content}
                  </Typography>
                ) : (
                  <Box>
                    <ReactMarkdown
                      components={{
                        h1: ({ children }) => (
                          <Typography variant="h6" sx={{ mb: 1, fontWeight: 600 }}>
                            {children}
                          </Typography>
                        ),
                        h2: ({ children }) => (
                          <Typography variant="subtitle1" sx={{ mb: 1, fontWeight: 600 }}>
                            {children}
                          </Typography>
                        ),
                        h3: ({ children }) => (
                          <Typography variant="subtitle2" sx={{ mb: 1, fontWeight: 600 }}>
                            {children}
                          </Typography>
                        ),
                        p: ({ children }) => (
                          <Typography variant="body1" sx={{ mb: 1, lineHeight: 1.6 }}>
                            {children}
                          </Typography>
                        ),
                        ul: ({ children }) => (
                          <Box component="ul" sx={{ pl: 2, mb: 1 }}>
                            {children}
                          </Box>
                        ),
                        ol: ({ children }) => (
                          <Box component="ol" sx={{ pl: 2, mb: 1 }}>
                            {children}
                          </Box>
                        ),
                        li: ({ children }) => (
                          <Typography component="li" variant="body1" sx={{ mb: 0.5, lineHeight: 1.6 }}>
                            {children}
                          </Typography>
                        ),
                        strong: ({ children }) => (
                          <Typography component="span" sx={{ fontWeight: 700, color: 'primary.main' }}>
                            {children}
                          </Typography>
                        ),
                        code: ({ children }) => (
                          <Typography
                            component="code"
                            sx={{
                              bgcolor: 'grey.100',
                              px: 1,
                              py: 0.5,
                              borderRadius: 1,
                              fontFamily: 'monospace',
                              fontSize: '0.875rem',
                            }}
                          >
                            {children}
                          </Typography>
                        ),
                      }}
                    >
                      {message.content}
                    </ReactMarkdown>

                    {/* Interactive Elements */}
                    {message.interactive && message.suggestions && (
                      <Box sx={{ mt: 2 }}>
                        <Typography variant="caption" color="text.secondary" sx={{ mb: 1, display: 'block' }}>
                          Quick Actions:
                        </Typography>
                        <Stack direction="row" spacing={1} flexWrap="wrap" useFlexGap>
                          {message.suggestions.map((suggestion, index) => (
                            <Chip
                              key={index}
                              label={suggestion}
                              size="small"
                              variant="outlined"
                              onClick={() => handleInteractiveAction(suggestion)}
                              sx={{ 
                                cursor: 'pointer',
                                '&:hover': {
                                  bgcolor: 'primary.light',
                                  color: 'primary.contrastText'
                                }
                              }}
                            />
                          ))}
                        </Stack>
                      </Box>
                    )}

                    {/* Context Used */}
                    {message.context_used && message.context_used.length > 0 && (
                      <Box sx={{ mt: 2, pt: 2, borderTop: 1, borderColor: 'divider' }}>
                        <Typography variant="caption" color="text.secondary" sx={{ mb: 1, display: 'block' }}>
                          Sources:
                        </Typography>
                        <Stack direction="row" spacing={0.5} flexWrap="wrap" useFlexGap>
                          {message.context_used.map((source, index) => (
                            <Chip
                              key={index}
                              label={source.source}
                              size="small"
                              variant="outlined"
                              sx={{ fontSize: '0.7rem' }}
                            />
                          ))}
                        </Stack>
                      </Box>
                    )}
                  </Box>
                )}
                
                <Typography variant="caption" color="text.secondary" sx={{ mt: 1, display: 'block', opacity: 0.7 }}>
                  {(() => {
                    const timestampStr = message.timestamp;
                    let utcDate;
                    
                    if (timestampStr && typeof timestampStr === 'string') {
                      if (timestampStr.includes('T')) {
                        utcDate = new Date(timestampStr);
                      } else {
                        utcDate = new Date(timestampStr + 'Z');
                      }
                    } else if (timestampStr instanceof Date) {
                      utcDate = timestampStr;
                    } else {
                      utcDate = new Date();
                    }
                    
                    return utcDate.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
                  })()}
                </Typography>
              </Box>
            </Paper>
          </Box>
        </Box>
      </Fade>
    );
  };

  // Session Panel Component
  const SessionPanel = () => (
    <Drawer
      variant={isMobile ? "temporary" : "persistent"}
      open={sessionPanelOpen}
      onClose={() => setSessionPanelOpen(false)}
      sx={{
        '& .MuiDrawer-paper': {
          width: 280,
          bgcolor: '#2d2d44',
          borderRight: '1px solid #3a3a5c',
          color: 'white',
        },
      }}
    >
      <Box sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
        {/* Header */}
        <Box sx={{ 
          p: 2, 
          borderBottom: '1px solid #3a3a5c',
          display: 'flex', 
          alignItems: 'center', 
          justifyContent: 'space-between' 
        }}>
          <Typography variant="h6" sx={{ fontWeight: 600, color: 'white' }}>
            Chat History
          </Typography>
          {isMobile && (
            <IconButton onClick={() => setSessionPanelOpen(false)} size="small" sx={{ color: 'white' }}>
              <CloseIcon />
            </IconButton>
          )}
        </Box>

        {/* New Chat Button */}
        <Box sx={{ p: 2 }}>
          <Button
            fullWidth
            variant="contained"
            startIcon={isCreatingChat ? <CircularProgress size={16} /> : <AddIcon />}
            onClick={createNewSession}
            disabled={isCreatingChat}
            sx={{
              bgcolor: '#1976d2',
              color: 'white',
              borderRadius: 2,
              py: 1.5,
              textTransform: 'none',
              fontWeight: 600,
              '&:hover': {
                bgcolor: '#1565c0',
              },
              '&:disabled': {
                bgcolor: '#3a3a5c',
                color: '#b0b0b0',
              },
            }}
          >
            New Chat
          </Button>
        </Box>

        {/* Conversations List */}
        <Box sx={{ flex: 1, overflow: 'auto' }}>
          {conversations.length === 0 ? (
            <Box sx={{ p: 2, textAlign: 'center' }}>
              <HistoryIcon sx={{ fontSize: 48, color: '#b0b0b0', mb: 1 }} />
              <Typography variant="body2" sx={{ color: '#b0b0b0' }}>
                No conversations yet
              </Typography>
            </Box>
          ) : (
            <List sx={{ p: 0 }}>
              {conversations.map((conversation) => (
                <ListItem key={conversation.id} disablePadding>
                  <ListItemButton
                    onClick={() => handleSessionSelect(conversation.id)}
                    selected={conversation.id === sessionId}
                    sx={{
                      px: 2,
                      py: 1.5,
                      '&.Mui-selected': {
                        bgcolor: '#3a3a5c',
                        '&:hover': {
                          bgcolor: '#4a4a6c',
                        },
                      },
                      '&:hover': {
                        bgcolor: '#3a3a5c',
                      },
                    }}
                  >
                    <ListItemIcon sx={{ minWidth: 40 }}>
                      <ChatIcon sx={{ color: conversation.id === sessionId ? '#64b5f6' : '#b0b0b0' }} />
                    </ListItemIcon>
                    <ListItemText
                      primary={
                        <Typography 
                          variant="body2" 
                          sx={{ 
                            color: 'white',
                            fontWeight: conversation.id === sessionId ? 600 : 400,
                            overflow: 'hidden',
                            textOverflow: 'ellipsis',
                            whiteSpace: 'nowrap',
                          }}
                        >
                          {getConversationTitle(conversation)}
                        </Typography>
                      }
                      secondary={
                        <Typography 
                          variant="caption" 
                          sx={{ 
                            color: '#b0b0b0',
                            fontSize: '0.75rem',
                          }}
                        >
                          {getConversationTime(conversation)}
                        </Typography>
                      }
                    />
                  </ListItemButton>
                </ListItem>
              ))}
            </List>
          )}
        </Box>
      </Box>
    </Drawer>
  );

  // Mobile-First Help Component
  const MobileHelp = () => (
    <Paper sx={{ 
      m: 2, 
      p: 2, 
      bgcolor: 'primary.light', 
      color: 'primary.contrastText',
      borderRadius: 3,
      boxShadow: '0 4px 12px rgba(0,0,0,0.1)'
    }}>
      <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
        <HelpIcon sx={{ mr: 1 }} />
        <Typography variant="h6" sx={{ fontWeight: 600 }}>
          Try these examples:
        </Typography>
      </Box>
      <Stack spacing={1}>
        {helpExamples.map((example, index) => (
          <Button
            key={index}
            variant="outlined"
            size="small"
            onClick={() => setInputMessage(example)}
            sx={{ 
              justifyContent: 'flex-start', 
              textAlign: 'left',
              color: 'inherit',
              borderColor: 'rgba(255,255,255,0.3)',
              borderRadius: 2,
              py: 1,
              '&:hover': {
                borderColor: 'rgba(255,255,255,0.5)',
                bgcolor: 'rgba(255,255,255,0.1)'
              }
            }}
          >
            {example}
          </Button>
        ))}
      </Stack>
    </Paper>
  );

  return (
    <Box sx={{ 
      height: '100vh', 
      display: 'flex', 
      flexDirection: 'column',
      bgcolor: 'background.default'
    }}>
      {/* Session Panel */}
      <SessionPanel />
      {/* Modern Header */}
      <Paper sx={{ 
        p: 2, 
        borderBottom: 1, 
        borderColor: 'divider',
        bgcolor: 'background.paper',
        boxShadow: '0 2px 8px rgba(0,0,0,0.05)'
      }}>
        <Box sx={{ 
          display: 'flex', 
          alignItems: 'center', 
          justifyContent: 'space-between',
          maxWidth: '1200px',
          mx: 'auto'
        }}>
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
            <Tooltip title="Chat History">
              <IconButton
                onClick={() => setSessionPanelOpen(!sessionPanelOpen)}
                color="primary"
                size="small"
                sx={{
                  bgcolor: 'background.default',
                  border: 1,
                  borderColor: 'divider',
                  '&:hover': {
                    bgcolor: 'primary.light',
                    color: 'primary.contrastText'
                  }
                }}
              >
                <MenuIcon />
              </IconButton>
            </Tooltip>
            <Avatar sx={{ 
              bgcolor: 'primary.main', 
              width: 40, 
              height: 40,
              boxShadow: '0 2px 8px rgba(0,0,0,0.1)'
            }}>
              <BotIcon />
            </Avatar>
            <Box>
              <Typography variant="h6" sx={{ fontWeight: 600, color: 'text.primary' }}>
                Laura AI Assistant
              </Typography>
              <Typography variant="caption" color="text.secondary">
                Your intelligent property assistant
              </Typography>
            </Box>
          </Box>
          
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
            <Tooltip title="Help">
              <IconButton
                onClick={() => setShowHelp(!showHelp)}
                color={showHelp ? "primary" : "default"}
                size="small"
              >
                <HelpIcon />
              </IconButton>
            </Tooltip>
            <Tooltip title="New Chat">
              <IconButton
                onClick={createNewSession}
                disabled={isLoading}
                size="small"
              >
                <RefreshIcon />
              </IconButton>
            </Tooltip>
          </Box>
        </Box>
      </Paper>

      {/* Main Chat Area */}
      <Box sx={{ 
        flex: 1, 
        display: 'flex', 
        flexDirection: 'column',
        overflow: 'hidden',
        ml: !isMobile && sessionPanelOpen ? '280px' : 0,
        transition: 'margin-left 0.3s ease',
      }}>
        {/* Messages Area */}
        <Box sx={{ 
          flex: 1, 
          overflow: 'auto',
          bgcolor: 'background.default'
        }} onScroll={handleScroll}>
          {isLoading && messages.length === 0 ? (
            <Box display="flex" justifyContent="center" alignItems="center" minHeight="200px">
              <CircularProgress size={60} />
            </Box>
          ) : (
            <>
              {/* Show help when no messages */}
              {messages.length === 0 && <MobileHelp />}
              
              {messages.map((message) => (
                <MessageBubble key={message.id} message={message} />
              ))}
              
              {isLoading && (
                <Box sx={{ display: 'flex', justifyContent: 'flex-start', mb: 2, px: isMobile ? 2 : 3 }}>
                  <Box sx={{ display: 'flex', alignItems: 'flex-start', gap: 1 }}>
                    <Avatar sx={{ 
                      bgcolor: 'primary.main', 
                      width: 32, 
                      height: 32,
                      boxShadow: '0 2px 8px rgba(0,0,0,0.1)'
                    }}>
                      <BotIcon fontSize="small" />
                    </Avatar>
                    <Paper sx={{ 
                      bgcolor: 'background.paper', 
                      border: 1, 
                      borderColor: 'divider',
                      borderRadius: 3,
                      boxShadow: '0 2px 8px rgba(0,0,0,0.08)'
                    }}>
                      <Box sx={{ p: 2, display: 'flex', alignItems: 'center', gap: 1 }}>
                        <CircularProgress size={16} />
                        <Typography variant="body2" color="text.secondary">
                          AI is thinking...
                        </Typography>
                      </Box>
                    </Paper>
                  </Box>
                </Box>
              )}
              
              <div ref={messagesEndRef} />
            </>
          )}
        </Box>

        {/* Uploaded File Indicator */}
        {uploadedFile && (
          <Box sx={{ 
            px: 2, 
            py: 1, 
            bgcolor: 'primary.light', 
            color: 'primary.contrastText',
            borderTop: 1,
            borderColor: 'divider'
          }}>
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
              <AttachFileIcon fontSize="small" />
              <Typography variant="body2" sx={{ flex: 1 }}>
                File attached: {uploadedFile.name}
              </Typography>
              <IconButton
                size="small"
                onClick={() => setUploadedFile(null)}
                sx={{ color: 'inherit' }}
              >
                <CloseIcon fontSize="small" />
              </IconButton>
            </Box>
          </Box>
        )}

        {/* Modern Input Area */}
        <Paper sx={{ 
          p: 2, 
          borderTop: 1, 
          borderColor: 'divider',
          bgcolor: 'background.paper',
          boxShadow: '0 -2px 8px rgba(0,0,0,0.05)'
        }}>
          <Box sx={{ 
            display: 'flex', 
            gap: 1, 
            alignItems: 'flex-end',
            maxWidth: '1200px',
            mx: 'auto'
          }}>
            <TextField
              fullWidth
              placeholder="Ask Laura about Dubai real estate..."
              value={inputMessage}
              onChange={(e) => setInputMessage(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && !e.shiftKey && sendMessage()}
              variant="outlined"
              size="small"
              multiline
              maxRows={4}
              disabled={isLoading}
              sx={{
                '& .MuiOutlinedInput-root': {
                  borderRadius: 3,
                  bgcolor: 'background.default',
                  '&:hover': {
                    '& .MuiOutlinedInput-notchedOutline': {
                      borderColor: 'primary.main',
                    },
                  },
                },
              }}
            />
            <Tooltip title="Attach file">
              <IconButton
                onClick={() => setUploadDialogOpen(true)}
                disabled={isLoading}
                color="primary"
                sx={{
                  bgcolor: 'background.default',
                  border: 1,
                  borderColor: 'divider',
                  '&:hover': {
                    bgcolor: 'primary.light',
                    color: 'primary.contrastText'
                  }
                }}
              >
                <AttachFileIcon />
              </IconButton>
            </Tooltip>
            <Button
              variant="contained"
              endIcon={<SendIcon />}
              onClick={sendMessage}
              disabled={!inputMessage.trim() || isLoading}
              sx={{
                borderRadius: 3,
                px: 3,
                py: 1,
                fontWeight: 600,
                boxShadow: '0 2px 8px rgba(0,0,0,0.1)',
                '&:hover': {
                  boxShadow: '0 4px 12px rgba(0,0,0,0.15)',
                },
              }}
            >
              {isMobile ? '' : 'Send'}
            </Button>
          </Box>
        </Paper>
      </Box>

      {/* File Upload Dialog */}
      <Dialog 
        open={uploadDialogOpen} 
        onClose={() => setUploadDialogOpen(false)}
        maxWidth="sm"
        fullWidth
      >
        <DialogTitle>Upload File for Analysis</DialogTitle>
        <DialogContent>
          <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
            Upload a document to provide context for our conversation. Supported formats: PDF, DOCX, XLSX, TXT
          </Typography>
          <Input
            type="file"
            onChange={handleFileUpload}
            inputProps={{
              accept: '.pdf,.docx,.xlsx,.txt',
            }}
            fullWidth
          />
          {uploading && (
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mt: 2 }}>
              <CircularProgress size={16} />
              <Typography variant="body2">Uploading...</Typography>
            </Box>
          )}
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setUploadDialogOpen(false)}>Cancel</Button>
        </DialogActions>
      </Dialog>

      {/* Error Alert */}
      {error && (
        <Alert 
          severity="error" 
          sx={{ m: 2 }} 
          onClose={() => setError(null)}
        >
          {error}
        </Alert>
      )}

      {/* Snackbar for notifications */}
      <Snackbar
        open={snackbar.open}
        autoHideDuration={6000}
        onClose={handleCloseSnackbar}
        anchorOrigin={{ vertical: 'bottom', horizontal: 'center' }}
      >
        <Alert onClose={handleCloseSnackbar} severity={snackbar.severity} sx={{ width: '100%' }}>
          {snackbar.message}
        </Alert>
      </Snackbar>
    </Box>
  );
};

export default Chat;