import React, { useState, useEffect, useRef, useCallback } from 'react';
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
  Fab,
  Zoom,
} from '@mui/material';
import {
  Send as SendIcon,
  AttachFile as AttachFileIcon,
  Person as PersonIcon,
  SmartToy as BotIcon,
  Close as CloseIcon,
  Visibility as ViewIcon,
  Help as HelpIcon,
  Info as InfoIcon,
  Tune as TuneIcon,
} from '@mui/icons-material';
import ReactMarkdown from 'react-markdown';
import { useParams, useNavigate, useLocation } from 'react-router-dom';
import { useAppContext } from '../context/AppContext';
import { api } from '../utils/apiClient';
import ContextualSidePanel from '../components/chat/ContextualSidePanel';
import PropertyCard from '../components/chat/PropertyCard';
import ContentPreviewCard from '../components/chat/ContentPreviewCard';
import PropertyDetectionCard from '../components/property/PropertyDetectionCard';
import DocumentProcessingCard from '../components/document/DocumentProcessingCard';

const Chat = () => {
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('md'));
  const isSmallScreen = useMediaQuery(theme.breakpoints.down('sm'));
  
  const { sessionId } = useParams();
  const navigate = useNavigate();
  const location = useLocation();
  const { currentUser, setCurrentSessionId } = useAppContext();
  
  // Existing state
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

  // Phase 3B: New state for contextual features
  const [detectedEntities, setDetectedEntities] = useState([]);
  const [contextPanelVisible, setContextPanelVisible] = useState(!isMobile);
  const [entityDetectionLoading, setEntityDetectionLoading] = useState(false);
  const [contextData, setContextData] = useState({});
  const [contextLoadingStates, setContextLoadingStates] = useState({});
  
  // Enhanced property detection state
  const [detectedProperty, setDetectedProperty] = useState(null);
  const [documentProcessingResult, setDocumentProcessingResult] = useState(null);
  const [propertyDetectionLoading, setPropertyDetectionLoading] = useState(false);

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
    },
    {
      title: "Property Detection",
      examples: [
        "Create a CMA for 413 Collective Tower",
        "Generate market report for Business Bay apartments",
        "Analyze property in Dubai Marina building",
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

  // Handle prepopulated prompt from navigation state
  useEffect(() => {
    if (location.state?.prepopulatedPrompt && sessionId) {
      setInputMessage(location.state.prepopulatedPrompt);
      // Clear the state to prevent re-triggering
      navigate(location.pathname, { replace: true, state: {} });
    }
  }, [location.state, sessionId, navigate]);

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

  // Phase 3B: Effect to detect entities when new AI messages arrive
  useEffect(() => {
    const lastMessage = messages[messages.length - 1];
    if (lastMessage && lastMessage.type === 'ai' && lastMessage.content) {
      detectEntitiesInMessage(lastMessage.content);
    }
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const handleScroll = (event) => {
    const { scrollTop, scrollHeight, clientHeight } = event.target;
    const threshold = 100; // pixels from bottom
    const isNearBottomNow = scrollHeight - scrollTop - clientHeight < threshold;
    setIsNearBottom(isNearBottomNow);
  };

  // Phase 3B: Entity detection function
  const detectEntitiesInMessage = useCallback(async (messageContent) => {
    try {
      setEntityDetectionLoading(true);
      const response = await api.detectEntities(messageContent, sessionId);
      
      if (response.entities && response.entities.length > 0) {
        setDetectedEntities(prev => {
          // Merge new entities with existing ones, avoiding duplicates
          const existingIds = new Set(prev.map(e => e.id));
          const newEntities = response.entities.filter(e => !existingIds.has(e.id));
          return [...prev, ...newEntities];
        });
        
        // Fetch context for new entities
        fetchContextForEntities(response.entities);
      }
    } catch (error) {
      console.error('Error detecting entities:', error);
      // Don't show error to user for entity detection failures
    } finally {
      setEntityDetectionLoading(false);
    }
  }, [sessionId]);

  // Phase 3B: Fetch context for entities
  const fetchContextForEntities = useCallback(async (entities) => {
    for (const entity of entities) {
      try {
        setContextLoadingStates(prev => ({ ...prev, [entity.id]: true }));
        
        const context = await api.fetchEntityContext(entity.type, entity.id, sessionId);
        
        setContextData(prev => ({
          ...prev,
          [entity.id]: context
        }));
      } catch (error) {
        console.error(`Error fetching context for entity ${entity.id}:`, error);
        setContextLoadingStates(prev => ({ ...prev, [entity.id]: false }));
      } finally {
        setContextLoadingStates(prev => ({ ...prev, [entity.id]: false }));
      }
    }
  }, [sessionId]);

  // Phase 3B: Handle entity click
  const handleEntityClick = useCallback((entity) => {
    // Add entity information to the chat input
    const entityPrompt = `Tell me more about ${entity.name || entity.id} (${entity.type})`;
    setInputMessage(entityPrompt);
  }, []);

  // Phase 3B: Handle context panel refresh
  const handleContextRefresh = useCallback(() => {
    if (detectedEntities.length > 0) {
      fetchContextForEntities(detectedEntities);
    }
  }, [detectedEntities, fetchContextForEntities]);

  const createNewSession = async () => {
    // Prevent multiple simultaneous session creation attempts
    if (isLoading) {
      console.log('Already loading, skipping session creation');
      return;
    }

    try {
      setIsLoading(true);
      const newSession = await api.createSession();
      console.log('Created new session:', newSession);
      navigate(`/chat/${newSession.session_id}`);
    } catch (error) {
      console.error('Error creating new session:', error);
      const errorMessage = error.message || 'An error occurred';
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
      const response = await api.getConversationHistory(sessionId);
      
      // Convert API response format to frontend format and ensure proper ordering
      const convertedMessages = (response.messages || []).map(msg => ({
        id: msg.id,
        type: msg.role === 'user' ? 'user' : 'ai', // Convert 'role' to 'type'
        content: msg.content || '', // Ensure content is never undefined
        timestamp: msg.timestamp,
        interactive: msg.interactive || false,
        suggestions: msg.suggestions || [],
        context_used: msg.context_used || [],
        // Phase 3B: Add rich content support
        rich_content: msg.rich_content || null,
        entities_detected: msg.entities_detected || [],
      }));
      
      // Sort messages by timestamp to ensure proper order
      const sortedMessages = convertedMessages.sort((a, b) => 
        new Date(a.timestamp) - new Date(b.timestamp)
      );
      
      setMessages(sortedMessages);
      
      // Phase 3B: Extract entities from all messages
      const allEntities = sortedMessages
        .filter(msg => msg.entities_detected && msg.entities_detected.length > 0)
        .flatMap(msg => msg.entities_detected);
      
      if (allEntities.length > 0) {
        setDetectedEntities(allEntities);
        fetchContextForEntities(allEntities);
      }
    } catch (error) {
      console.error('Error fetching conversation history:', error);
      const errorMessage = error.message || 'An error occurred';
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
      // Try to detect property information from the message
      setPropertyDetectionLoading(true);
      try {
        const propertyDetection = await api.detectProperty(inputMessage);
        if (propertyDetection && propertyDetection.confidence > 0.3) {
          setDetectedProperty(propertyDetection);
        }
      } catch (detectionError) {
        console.log('Property detection failed:', detectionError);
        // Don't show error to user, just continue with normal chat
      } finally {
        setPropertyDetectionLoading(false);
      }

      // Send message with enhanced property detection and entity detection
      const response = await api.sendMessageWithPropertyDetection(sessionId, inputMessage, uploadedFile, true);
      
      const aiMessage = {
        id: response.message_id || Date.now().toString(),
        type: 'ai',
        content: response.response || response.content || '',
        timestamp: new Date().toISOString(),
        interactive: response.interactive || false,
        suggestions: response.suggestions || [],
        context_used: response.context_used || [],
        // Phase 3B: Add rich content support
        rich_content: response.rich_content || null,
        entities_detected: response.entities_detected || [],
        // Enhanced property detection
        detected_property: response.detected_property || null,
        building_specific_data: response.building_specific_data || null,
      };

      setMessages(prev => [...prev, aiMessage]);
      setUploadedFile(null);
      setDocumentProcessingResult(null);
    } catch (error) {
      console.error('Error sending message:', error);
      const errorMessage = error.message || 'An error occurred';
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

  const handleFileUpload = async (event) => {
    const file = event.target.files[0];
    if (!file) return;

    setUploading(true);
    try {
      // First upload the file
      const uploadResponse = await api.uploadFile(file, sessionId);
      
      // Then process the document for property information
      const processingResponse = await api.processDocument(file, sessionId);
      
      setUploadedFile({
        id: uploadResponse.file_id,
        name: file.name,
        size: file.size,
      });
      
      // Store document processing results
      setDocumentProcessingResult(processingResponse);
      
      setUploadDialogOpen(false);
      setSnackbar({
        open: true,
        message: 'File uploaded and processed successfully!',
        severity: 'success',
      });
    } catch (error) {
      console.error('Error uploading file:', error);
      const errorMessage = error.message || 'An error occurred';
      setSnackbar({
        open: true,
        message: errorMessage,
        severity: 'error',
      });
    } finally {
      setUploading(false);
    }
  };

  const handleInteractiveAction = (suggestion) => {
    setInputMessage(suggestion);
  };

  const handleCloseSnackbar = () => {
    setSnackbar({ ...snackbar, open: false });
  };

  // Enhanced property detection handlers
  const handlePropertyClick = (property) => {
    const propertyPrompt = `Tell me more about ${property.building_name || property.address} in ${property.community || 'Dubai'}`;
    setInputMessage(propertyPrompt);
  };

  const handlePropertyViewDetails = (property) => {
    // Navigate to property details or show in modal
    console.log('View property details:', property);
    setSnackbar({
      open: true,
      message: 'Property details feature coming soon!',
      severity: 'info',
    });
  };

  const handleDocumentUseInChat = (extractedProperty) => {
    if (extractedProperty && extractedProperty.building_name) {
      const documentPrompt = `Create a CMA for ${extractedProperty.building_name} in ${extractedProperty.community || 'Dubai'}`;
      setInputMessage(documentPrompt);
    }
  };

  const handleDocumentView = (processingResult) => {
    console.log('View document:', processingResult);
    setSnackbar({
      open: true,
      message: 'Document viewer feature coming soon!',
      severity: 'info',
    });
  };

  // Phase 3B: Render rich content components
  const renderRichContent = (richContent) => {
    if (!richContent) return null;

    switch (richContent.type) {
      case 'property':
        return (
          <Box sx={{ mt: 2 }}>
            <PropertyCard 
              property={richContent.data}
              onView={() => handleEntityClick({ type: 'property', id: richContent.data.id, name: richContent.data.address })}
              onFavorite={() => console.log('Favorite property:', richContent.data.id)}
              onShare={() => console.log('Share property:', richContent.data.id)}
            />
          </Box>
        );
      
      case 'document':
      case 'report':
        return (
          <Box sx={{ mt: 2 }}>
            <ContentPreviewCard 
              content={richContent.data}
              type={richContent.type}
              onView={() => handleEntityClick({ type: 'document', id: richContent.data.id, name: richContent.data.title })}
              onDownload={() => console.log('Download document:', richContent.data.id)}
              onShare={() => console.log('Share document:', richContent.data.id)}
            />
          </Box>
        );
      
      default:
        return null;
    }
  };

  // Message Bubble Component
  const MessageBubble = ({ message }) => {
    const isUser = message.type === 'user';

    return (
      <Box sx={{ display: 'flex', justifyContent: isUser ? 'flex-end' : 'flex-start', mb: 2 }}>
        <Box sx={{ display: 'flex', alignItems: 'flex-start', gap: 1, maxWidth: '80%' }}>
          {!isUser && (
            <Avatar sx={{ bgcolor: 'secondary.main', width: 32, height: 32 }}>
              <BotIcon />
            </Avatar>
          )}
          
          <Card sx={{ 
            bgcolor: isUser ? 'primary.main' : 'background.paper', 
            color: isUser ? 'primary.contrastText' : 'text.primary',
            border: 1, 
            borderColor: 'divider',
            maxWidth: '100%'
          }}>
            <CardContent sx={{ py: 2, px: 2 }}>
              {isUser ? (
                <Typography variant="body1">
                  {message.content}
                </Typography>
              ) : (
                <Box>
                  {/* Phase 3B: Render rich content if available */}
                  {message.rich_content && renderRichContent(message.rich_content)}
                  
                  {/* Enhanced property detection display */}
                  {message.detected_property && (
                    <Box sx={{ mt: 2 }}>
                      <PropertyDetectionCard
                        detectedProperty={message.detected_property}
                        onPropertyClick={handlePropertyClick}
                        onViewDetails={handlePropertyViewDetails}
                        showActions={true}
                      />
                    </Box>
                  )}
                  
                  {/* Building-specific data display */}
                  {message.building_specific_data && (
                    <Box sx={{ mt: 2 }}>
                      <Alert severity="info" sx={{ mb: 2 }}>
                        <Typography variant="body2">
                          <strong>Building-Specific Analysis:</strong> This report includes data from {message.building_specific_data.comparable_count || 0} comparable properties in the same building.
                        </Typography>
                      </Alert>
                    </Box>
                  )}
                  
                  {/* Regular markdown content */}
                  <ReactMarkdown
                    components={{
                      h1: ({ children }) => (
                        <Typography variant="h4" sx={{ mb: theme.spacing(1), fontWeight: 600 }}>
                          {children}
                        </Typography>
                      ),
                      h2: ({ children }) => (
                        <Typography variant="h5" sx={{ mb: theme.spacing(1), fontWeight: 600 }}>
                          {children}
                        </Typography>
                      ),
                      h3: ({ children }) => (
                        <Typography variant="h6" sx={{ mb: theme.spacing(1), fontWeight: 600 }}>
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
                        <Typography component="span" sx={{ fontWeight: 700, color: 'primary.main', backgroundColor: 'primary.50', px: 0.5, borderRadius: 0.5 }}>
                          {children}
                        </Typography>
                      ),
                      em: ({ children }) => (
                        <Typography component="span" sx={{ fontStyle: 'italic', color: 'text.secondary' }}>
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
                            border: '1px solid',
                            borderColor: 'grey.300'
                          }}
                        >
                          {children}
                        </Typography>
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
            <Grid item xs={12} sm={6} key={index}>
              <Typography variant="subtitle1" sx={{ mb: 1, fontWeight: 600 }}>
                {category.title}
              </Typography>
              <Stack spacing={1}>
                {category.examples.map((example, exampleIndex) => (
                  <Button
                    key={exampleIndex}
                    variant="outlined"
                    size="small"
                    onClick={() => setInputMessage(example)}
                    sx={{ 
                      justifyContent: 'flex-start', 
                      textAlign: 'left',
                      color: 'inherit',
                      borderColor: 'rgba(255,255,255,0.3)',
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
            </Grid>
          ))}
        </Grid>
      </CardContent>
    </Card>
  );

  return (
    <Box sx={{ height: '100vh', display: 'flex', flexDirection: 'column' }}>
      {/* Header */}
      <Paper sx={{ p: 2, borderBottom: 1, borderColor: 'divider' }}>
        <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
          <Typography variant="h5" sx={{ fontWeight: 'bold' }}>
            Dubai Real Estate AI Assistant
          </Typography>
          
          {/* Phase 3B: Context Panel Toggle */}
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
            {(entityDetectionLoading || propertyDetectionLoading) && (
              <CircularProgress size={20} />
            )}
            <Tooltip title={contextPanelVisible ? "Hide Context Panel" : "Show Context Panel"}>
              <IconButton
                onClick={() => setContextPanelVisible(!contextPanelVisible)}
                color={contextPanelVisible ? "primary" : "default"}
              >
                <InfoIcon />
              </IconButton>
            </Tooltip>
          </Box>
        </Box>
      </Paper>

      {/* Main Content Area - Two Panel Layout */}
      <Box sx={{ flex: 1, display: 'flex', overflow: 'hidden' }}>
        {/* Chat Area */}
        <Paper 
          sx={{ 
            flex: 1, 
            display: 'flex', 
            flexDirection: 'column',
            overflow: 'hidden',
            mr: contextPanelVisible && !isMobile ? 0 : 0
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
                  onClick={() => {
                    setUploadedFile(null);
                    setDocumentProcessingResult(null);
                  }}
                  sx={{ color: 'inherit' }}
                >
                  <CloseIcon fontSize="small" />
                </IconButton>
              </Box>
            </Box>
          )}

          {/* Document Processing Results */}
          {documentProcessingResult && (
            <Box sx={{ px: 3, py: 2 }}>
              <DocumentProcessingCard
                processingResult={documentProcessingResult}
                onViewDocument={handleDocumentView}
                onUseInChat={handleDocumentUseInChat}
                showActions={true}
              />
            </Box>
          )}

          {/* Property Detection Results */}
          {detectedProperty && (
            <Box sx={{ px: 3, py: 2 }}>
              <PropertyDetectionCard
                detectedProperty={detectedProperty}
                onPropertyClick={handlePropertyClick}
                onViewDetails={handlePropertyViewDetails}
                showActions={true}
              />
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

        {/* Phase 3B: Contextual Side Panel */}
        {contextPanelVisible && !isMobile && (
          <ContextualSidePanel
            entities={detectedEntities}
            conversationId={sessionId}
            onEntityClick={handleEntityClick}
            isVisible={contextPanelVisible}
            onClose={() => setContextPanelVisible(false)}
            onRefresh={handleContextRefresh}
          />
        )}
      </Box>

      {/* Mobile Context Panel Toggle */}
      {isMobile && (
        <Zoom in={detectedEntities.length > 0}>
          <Fab
            color="primary"
            aria-label="Context Panel"
            sx={{ position: 'fixed', bottom: 16, right: 16 }}
            onClick={() => setContextPanelVisible(!contextPanelVisible)}
          >
            <InfoIcon />
          </Fab>
        </Zoom>
      )}

      {/* Mobile Context Panel Overlay */}
      {isMobile && contextPanelVisible && (
        <Dialog
          fullScreen
          open={contextPanelVisible}
          onClose={() => setContextPanelVisible(false)}
        >
          <ContextualSidePanel
            entities={detectedEntities}
            conversationId={sessionId}
            onEntityClick={handleEntityClick}
            isVisible={true}
            onClose={() => setContextPanelVisible(false)}
            onRefresh={handleContextRefresh}
          />
        </Dialog>
      )}

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
