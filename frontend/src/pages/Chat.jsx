import React, { useState, useEffect, useRef } from 'react';
import {
  Box,
  Typography,
  Paper,
  TextField,
  Button,
  Card,
  CardContent,
  IconButton,
  Avatar,
  Chip,
  CircularProgress,
  Alert,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Input,
  Tooltip,
  Snackbar,
  Grid,
  useMediaQuery,
  useTheme,
  Stack,
  Skeleton,
  Fade,
  Grow,
  Divider,
} from '@mui/material';
import {
  Send as SendIcon,
  AttachFile as AttachFileIcon,
  Person as PersonIcon,
  SmartToy as BotIcon,
  Close as CloseIcon,
  Visibility as ViewIcon,
  Help as HelpIcon,
} from '@mui/icons-material';
import ReactMarkdown from 'react-markdown';
import { useParams, useNavigate } from 'react-router-dom';
import { useAppContext } from '../context/AppContext';
import { apiUtils, handleApiError } from '../utils/api';

const Chat = () => {
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('md'));
  const isSmallScreen = useMediaQuery(theme.breakpoints.down('sm'));
  
  const { sessionId } = useParams();
  const navigate = useNavigate();
  const { currentUser, setCurrentSessionId } = useAppContext();
  const [messages, setMessages] = useState([]);
  const [inputMessage, setInputMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [uploadDialogOpen, setUploadDialogOpen] = useState(false);
  const [uploadedFile, setUploadedFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [snackbar, setSnackbar] = useState({ open: false, message: '', severity: 'info' });
  const messagesEndRef = useRef(null);
  const [isNearBottom, setIsNearBottom] = useState(true);

  

  // Contextual help examples
  const helpExamples = [
    {
      title: "Property Search",
      examples: [
        "Show me 2-bedroom apartments in Dubai Marina under 3M AED",
        "Find villas in Palm Jumeirah with 4+ bedrooms",
        "What properties are available in Downtown Dubai?",
      ]
    },
    {
      title: "Market Analysis",
      examples: [
        "What's the current market trend in Palm Jumeirah?",
        "Show me price trends for apartments in Dubai Marina",
        "What are the hot areas in Dubai right now?",
      ]
    },
    {
      title: "Investment Advice",
      examples: [
        "Calculate ROI for a 2M AED apartment in Dubai Marina",
        "What's the best investment strategy for Dubai real estate?",
        "Compare rental yields across different areas",
      ]
    },
    {
      title: "Document Analysis",
      examples: [
        "Analyze this property document for key details",
        "Extract important information from this contract",
        "Summarize the main points from this market report",
      ]
    }
  ];

  useEffect(() => {
    if (sessionId && sessionId !== 'undefined') {
      setCurrentSessionId(sessionId);
      fetchConversationHistory();
    } else if (!sessionId) {
      // If no session ID, create a new conversation
      createNewSession();
    }
  }, [sessionId, setCurrentSessionId]);

  // Separate effect to handle session creation
  useEffect(() => {
    if (!sessionId && currentUser) {
      // Only create new session if we have a current user and no session ID
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
    const threshold = 100; // pixels from bottom
    const isNearBottomNow = scrollHeight - scrollTop - clientHeight < threshold;
    setIsNearBottom(isNearBottomNow);
  };

  const createNewSession = async () => {
    // Prevent multiple simultaneous session creation attempts
    if (isLoading) {
      console.log('Already loading, skipping session creation');
      return;
    }

    try {
      setIsLoading(true);
      const newSession = await apiUtils.createSession();
      console.log('Created new session:', newSession);
      navigate(`/chat/${newSession.session_id}`);
    } catch (error) {
      console.error('Error creating new session:', error);
      const errorMessage = handleApiError(error);
      setError(errorMessage);
      setSnackbar({
        open: true,
        message: errorMessage,
        severity: 'error',
      });
    } finally {
      setIsLoading(false);
    }
  };

  const fetchConversationHistory = async () => {
    // Prevent fetching with undefined sessionId
    if (!sessionId || sessionId === 'undefined') {
      console.log('No valid session ID available, skipping conversation history fetch');
      return;
    }

    try {
      setIsLoading(true);
      const response = await apiUtils.getConversationHistory(sessionId);
      
      // Convert API response format to frontend format and ensure proper ordering
      const convertedMessages = (response.messages || []).map(msg => ({
        id: msg.id,
        type: msg.role === 'user' ? 'user' : 'ai', // Convert 'role' to 'type'
        content: msg.content || '', // Ensure content is never undefined
        timestamp: msg.timestamp,
        interactive: msg.interactive || false,
        suggestions: msg.suggestions || [],
        context_used: msg.context_used || [],
      }));
      
      // Sort messages by timestamp to ensure proper order
      const sortedMessages = convertedMessages.sort((a, b) => 
        new Date(a.timestamp) - new Date(b.timestamp)
      );
      
      setMessages(sortedMessages);
    } catch (error) {
      console.log('Using mock conversation data');
      setMessages([]);
    } finally {
      setIsLoading(false);
    }
  };

  const sendMessage = async () => {
    if (!inputMessage.trim()) return;
    
    console.log('sendMessage called with sessionId:', sessionId);
    console.log('sessionId type:', typeof sessionId);
    console.log('sessionId === undefined:', sessionId === undefined);
    console.log('sessionId === "undefined":', sessionId === 'undefined');
    
    if (!sessionId || sessionId === 'undefined') {
      console.log('Session validation failed - showing warning');
      setSnackbar({
        open: true,
        message: 'No active chat session. Please wait for session to be created.',
        severity: 'warning',
      });
      return;
    }

    const currentTime = new Date();
    const userMessage = {
      id: Date.now(),
      type: 'user',
      content: inputMessage,
      timestamp: currentTime,
    };

    setMessages(prev => [...prev, userMessage]);
    setInputMessage('');
    setIsLoading(true);

    try {
      const response = await apiUtils.sendMessage(sessionId, inputMessage, uploadedFile);
      console.log('Chat response:', response);

      const aiMessage = {
        id: Date.now() + 1,
        type: 'ai',
        content: response.response || 'I apologize, but I encountered an error processing your request.',
        timestamp: new Date(currentTime.getTime() + 1000), // Ensure AI message comes after user message
        interactive: response.interactive || false,
        suggestions: response.suggestions || [],
        context_used: response.context_used || [],
      };

      setMessages(prev => [...prev, aiMessage]);
      setUploadedFile(null); // Clear uploaded file after sending
    } catch (error) {
      console.error('Error sending message:', error);
  setSnackbar({
    open: true,
    message: 'Failed to send message. Please try again.',
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
      const response = await apiUtils.uploadFile(file, sessionId, currentUser?.role || 'agent');

      setUploadedFile({
        id: response.file_id,
        name: file.name,
        size: file.size,
        type: file.type,
      });

      setUploadDialogOpen(false);
      setSnackbar({
        open: true,
        message: 'File uploaded successfully!',
        severity: 'success',
      });
    } catch (error) {
      console.error('Error uploading file:', error);
      const errorMessage = handleApiError(error);
      setError(errorMessage);
      setSnackbar({
        open: true,
        message: `Failed to upload file: ${errorMessage}`,
        severity: 'error',
      });
    } finally {
      setUploading(false);
    }
  };

  const handleInteractiveAction = async (action) => {
    try {
      setSnackbar({
        open: true,
        message: `Executing ${action}...`,
        severity: 'info',
      });

      const result = await apiUtils.executeAction(action, {
        session_id: sessionId,
        user_id: currentUser?.id,
      });

      setSnackbar({
        open: true,
        message: `${action} completed successfully!`,
        severity: 'success',
      });

      console.log(`Interactive action result:`, result);
    } catch (error) {
      const errorMessage = handleApiError(error);
      setSnackbar({
        open: true,
        message: `Failed to execute ${action}: ${errorMessage}`,
        severity: 'error',
      });
    }
  };

  const handleCloseSnackbar = () => {
    setSnackbar({ ...snackbar, open: false });
  };

  const MessageBubble = ({ message }) => {
    const isUser = message.type === 'user';
    
    return (
      <Box
        sx={{
          display: 'flex',
          justifyContent: isUser ? 'flex-end' : 'flex-start',
          mb: 2,
        }}
      >
        <Box
          sx={{
            maxWidth: '70%',
            display: 'flex',
            flexDirection: isUser ? 'row-reverse' : 'row',
            alignItems: 'flex-start',
            gap: 1,
          }}
        >
          <Avatar
            sx={{
              bgcolor: isUser ? 'primary.main' : 'secondary.main',
              width: 32,
              height: 32,
            }}
          >
            {isUser ? <PersonIcon /> : <BotIcon />}
          </Avatar>
          
          <Card
            sx={{
              bgcolor: isUser ? 'primary.main' : 'background.paper',
              color: isUser ? 'primary.contrastText' : 'text.primary',
              border: isUser ? 'none' : 1,
              borderColor: 'divider',
            }}
          >
            <CardContent sx={{ py: 2, px: 2, '&:last-child': { pb: 2 } }}>
              {isUser ? (
                <Typography variant="body1">{message.content}</Typography>
              ) : (
                <Box>
                  <ReactMarkdown
                    components={{
                      h1: ({ children }) => (
                        <Typography variant="h5" sx={{ fontWeight: 700, mb: 1.5, color: 'primary.main', borderBottom: '2px solid', borderColor: 'primary.main', pb: 0.5 }}>
                          {children}
                        </Typography>
                      ),
                      h2: ({ children }) => (
                        <Typography variant="h6" sx={{ fontWeight: 600, mb: 1, color: 'primary.main', mt: 2 }}>
                          {children}
                        </Typography>
                      ),
                      h3: ({ children }) => (
                        <Typography variant="subtitle1" sx={{ fontWeight: 600, mb: 1, color: 'primary.main', mt: 1.5 }}>
                          {children}
                        </Typography>
                      ),
                      h4: ({ children }) => (
                        <Typography variant="subtitle2" sx={{ fontWeight: 600, mb: 0.5, color: 'primary.main', mt: 1 }}>
                          {children}
                        </Typography>
                      ),
                      p: ({ children }) => (
                        <Typography variant="body1" sx={{ mb: theme.spacing(1), lineHeight: 1.6 }}>
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
                        <Box component="span" sx={{ fontWeight: 700, color: 'primary.main', backgroundColor: 'primary.50', px: 0.5, borderRadius: 0.5 }}>
                          {children}
                        </Box>
                      ),
                      em: ({ children }) => (
                        <Box component="span" sx={{ fontStyle: 'italic', color: 'text.secondary' }}>
                          {children}
                        </Box>
                      ),
                      code: ({ children }) => (
                        <Box
                          component="code"
                          sx={{
                            bgcolor: 'grey.100',
                            px: 1,
                            py: 0.5,
                            borderRadius: 1,
                            fontFamily: 'monospace',
                            fontSize: '0.875rem',
                            border: '1px solid',
                            borderColor: 'grey.300'
                          }}
                        >
                          {children}
                        </Box>
                      ),
                      blockquote: ({ children }) => (
                        <Box
                          sx={{
                            borderLeft: 4,
                            borderColor: 'primary.main',
                            pl: 2,
                            ml: 0,
                            my: 1.5,
                            bgcolor: 'primary.50',
                            py: 1.5,
                            borderRadius: 1,
                            boxShadow: 1
                          }}
                        >
                          {children}
                        </Box>
                      ),
                      table: ({ children }) => (
                        <Box
                          component="table"
                          sx={{
                            width: '100%',
                            borderCollapse: 'collapse',
                            my: 2,
                            border: '1px solid',
                            borderColor: 'grey.300',
                            borderRadius: 1,
                            overflow: 'hidden'
                          }}
                        >
                          {children}
                        </Box>
                      ),
                      th: ({ children }) => (
                        <Box
                          component="th"
                          sx={{
                            bgcolor: 'primary.main',
                            color: 'primary.contrastText',
                            p: 1,
                            textAlign: 'left',
                            fontWeight: 600,
                            border: '1px solid',
                            borderColor: 'grey.300'
                          }}
                        >
                          {children}
                        </Box>
                      ),
                      td: ({ children }) => (
                        <Box
                          component="td"
                          sx={{
                            p: 1,
                            border: '1px solid',
                            borderColor: 'grey.300',
                            bgcolor: 'background.paper'
                          }}
                        >
                          {children}
                        </Box>
                      )
                    }}
                  >
                    {message.content}
                  </ReactMarkdown>

                  {/* Interactive Elements */}
                  {message.interactive && message.suggestions && (
                    <Box sx={{ mt: theme.spacing(2) }}>
                      <Typography variant="subtitle2" sx={{ mb: theme.spacing(1) }}>
                        Quick Actions:
                      </Typography>
                      <Box sx={{ display: 'flex', gap: 1, flexWrap: 'wrap' }}>
                        {message.suggestions.map((suggestion, index) => (
                          <Button
                            key={index}
                            size="small"
                            variant="outlined"
                            onClick={() => handleInteractiveAction(suggestion)}
                            startIcon={<ViewIcon />}
                          >
                            {suggestion}
                          </Button>
                        ))}
                      </Box>
                    </Box>
                  )}

                  {/* Context Used */}
                  {message.context_used && message.context_used.length > 0 && (
                    <Box sx={{ mt: 2, pt: 2, borderTop: 1, borderColor: 'divider' }}>
                      <Typography variant="caption" color="text.secondary">
                        Sources used:
                      </Typography>
                      <Box sx={{ display: 'flex', gap: 0.5, flexWrap: 'wrap', mt: 0.5 }}>
                        {message.context_used.map((source, index) => (
                          <Chip
                            key={index}
                            label={source.source}
                            size="small"
                            variant="outlined"
                          />
                        ))}
                      </Box>
                    </Box>
                  )}
                </Box>
              )}
              
              <Typography variant="caption" color="text.secondary" sx={{ mt: 1, display: 'block' }}>
                {(() => {
                  // Parse the UTC timestamp from the database
                  // The database stores UTC timestamps without timezone info
                  // So we need to explicitly treat them as UTC
                  const timestampStr = message.timestamp;
                  let utcDate;
                  
                  // Handle different timestamp formats with proper type checking
                  if (timestampStr && typeof timestampStr === 'string') {
                    if (timestampStr.includes('T')) {
                      // ISO format with T
                      utcDate = new Date(timestampStr);
                    } else {
                      // PostgreSQL format: "2025-08-31 11:32:22.114730"
                      // Add 'Z' to indicate UTC timezone
                      utcDate = new Date(timestampStr + 'Z');
                    }
                  } else if (timestampStr instanceof Date) {
                    // If it's already a Date object
                    utcDate = timestampStr;
                  } else {
                    // Fallback to current time if timestamp is invalid
                    utcDate = new Date();
                  }
                  
                  return utcDate.toLocaleTimeString();
                })()}
              </Typography>
            </CardContent>
          </Card>
        </Box>
      </Box>
    );
  };

  // Contextual Help Component
  const ContextualHelp = () => (
    <Card sx={{ mb: 3, bgcolor: 'primary.light', color: 'primary.contrastText' }}>
      <CardContent>
        <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
          <HelpIcon sx={{ mr: theme.spacing(1) }} />
          <Typography variant="h6">Need help? Try these examples:</Typography>
        </Box>
        
        <Grid container spacing={2}>
          {helpExamples.map((category, index) => (
            <Grid item xs={12} sm={6} md={3} key={index}>
              <Typography variant="subtitle2" sx={{ mb: 1, fontWeight: 600 }}>
                {category.title}
              </Typography>
              <Box sx={{ display: 'flex', flexDirection: 'column', gap: 0.5 }}>
                {category.examples.map((example, idx) => (
                  <Button
                    key={idx}
                    size="small"
                    variant="outlined"
                    onClick={() => setInputMessage(example)}
                    sx={{ 
                      justifyContent: 'flex-start',
                      textAlign: 'left',
                      color: 'inherit',
                      borderColor: 'rgba(255,255,255,0.3)',
                      '&:hover': {
                        borderColor: 'rgba(255,255,255,0.5)',
                        bgcolor: 'rgba(255,255,255,0.1)',
                      }
                    }}
                  >
                    {example}
                  </Button>
                ))}
              </Box>
            </Grid>
          ))}
        </Grid>
      </CardContent>
    </Card>
  );

  return (
    <Box sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
      {/* Header */}
      <Box sx={{ mb: theme.spacing(3) }}>
        <Typography variant="h4" sx={{ fontWeight: 600, mb: 1 }}>
          Chat
        </Typography>
        <Typography variant="body1" color="text.secondary">
          {sessionId ? `Session: ${sessionId}` : 'New conversation'}
        </Typography>
      </Box>

      {/* Chat Area */}
      <Paper 
        sx={{ 
          flex: 1, 
          display: 'flex', 
          flexDirection: 'column',
          overflow: 'hidden',
          mb: 2
        }}
      >
        {/* Messages Area */}
        <Box sx={{ flex: 1, p: 3, overflow: 'auto' }} onScroll={handleScroll}>
          {isLoading && messages.length === 0 ? (
            <Box display="flex" justifyContent="center" alignItems="center" minHeight="200px">
              <CircularProgress size={60} />
            </Box>
          ) : (
            <>
              {/* Show contextual help when no messages */}
              {messages.length === 0 && <ContextualHelp />}
              
              {messages.map((message) => (
                <MessageBubble key={message.id} message={message} />
              ))}
              
              {isLoading && (
                <Box sx={{ display: 'flex', justifyContent: 'flex-start', mb: 2 }}>
                  <Box sx={{ display: 'flex', alignItems: 'flex-start', gap: 1 }}>
                    <Avatar sx={{ bgcolor: 'secondary.main', width: 32, height: 32 }}>
                      <BotIcon />
                    </Avatar>
                    <Card sx={{ bgcolor: 'background.paper', border: 1, borderColor: 'divider' }}>
                      <CardContent sx={{ py: 2, px: 2 }}>
                        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                          <CircularProgress size={16} />
                          <Typography variant="body2" color="text.secondary">
                            AI is thinking...
                          </Typography>
                        </Box>
                      </CardContent>
                    </Card>
                  </Box>
                </Box>
              )}
              
              <div ref={messagesEndRef} />
            </>
          )}
        </Box>

        {/* Uploaded File Indicator */}
        {uploadedFile && (
          <Box sx={{ px: 3, py: 1, bgcolor: 'primary.light', color: 'primary.contrastText' }}>
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
              <AttachFileIcon fontSize="small" />
              <Typography variant="body2">
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

        {/* Input Area */}
        <Box sx={{ p: 3, borderTop: 1, borderColor: 'divider' }}>
          <Box sx={{ display: 'flex', gap: 2, alignItems: 'flex-end' }}>
            <TextField
              fullWidth
              placeholder="Ask about Dubai real estate..."
              value={inputMessage}
              onChange={(e) => setInputMessage(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && !e.shiftKey && sendMessage()}
              variant="outlined"
              size="small"
              multiline
              maxRows={4}
              disabled={isLoading}
            />
            <Tooltip title="Attach file">
              <IconButton
                onClick={() => setUploadDialogOpen(true)}
                disabled={isLoading}
                color="primary"
              >
                <AttachFileIcon />
              </IconButton>
            </Tooltip>
            <Button
              variant="contained"
              endIcon={<SendIcon />}
              onClick={sendMessage}
              disabled={!inputMessage.trim() || isLoading}
            >
              Send
            </Button>
          </Box>
        </Box>
      </Paper>

      {/* File Upload Dialog */}
      <Dialog open={uploadDialogOpen} onClose={() => setUploadDialogOpen(false)}>
        <DialogTitle>Upload File for Analysis</DialogTitle>
        <DialogContent>
          <Typography variant="body2" color="text.secondary" sx={{ mb: theme.spacing(2) }}>
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
        <Alert severity="error" sx={{ mb: theme.spacing(2) }} onClose={() => setError(null)}>
          {error}
        </Alert>
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
    </Box>
  );
};

export default Chat;
