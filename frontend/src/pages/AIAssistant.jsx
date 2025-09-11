import React, { useState, useEffect } from 'react';
import {
  Box,
  Container,
  Typography,
  Card,
  CardContent,
  TextField,
  Button,
  Grid,
  Chip,
  CircularProgress,
  Alert,
  Tabs,
  Tab,
  List,
  ListItem,
  ListItemText,
  ListItemSecondaryAction,
  IconButton,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Paper,
  Divider
} from '@mui/material';
import {
  Mic,
  MicOff,
  Send,
  Download,
  Visibility,
  Refresh,
  History,
  VoiceChat,
  SmartToy,
  Person
} from '@mui/icons-material';
import { useAppContext } from '../context/AppContext';
import { api } from '../utils/apiClient';

const AIAssistant = () => {
  const { currentUser } = useAppContext();
  const [activeTab, setActiveTab] = useState(0);
  const [requestText, setRequestText] = useState('');
  const [requestType, setRequestType] = useState('general');
  const [priority, setPriority] = useState('normal');
  const [isRecording, setIsRecording] = useState(false);
  const [isProcessing, setIsProcessing] = useState(false);
  const [requests, setRequests] = useState([]);
  const [voiceRequests, setVoiceRequests] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(null);
  const [selectedRequest, setSelectedRequest] = useState(null);
  const [contentDialog, setContentDialog] = useState(false);
  const [deliverableContent, setDeliverableContent] = useState(null);

  const requestTypes = [
    { value: 'cma', label: 'Comparative Market Analysis (AI Generated)' },
    { value: 'presentation', label: 'Listing Presentation (AI Generated)' },
    { value: 'marketing', label: 'Marketing Materials (AI Generated)' },
    { value: 'compliance', label: 'Compliance Documents (Human Review Required)' },
    { value: 'follow_up', label: 'Client Follow-up (AI Generated)' },
    { value: 'general', label: 'General Request (AI Generated)' }
  ];

  const priorities = [
    { value: 'low', label: 'Low' },
    { value: 'normal', label: 'Normal' },
    { value: 'high', label: 'High' },
    { value: 'urgent', label: 'Urgent' }
  ];

  const statusColors = {
    pending: 'default',
    processing: 'primary',
    ai_complete: 'info',
    human_review: 'warning', // Only for contract-related requests
    completed: 'success',
    failed: 'error'
  };

  const getStatusDescription = (status) => {
    const descriptions = {
      pending: 'Request received',
      processing: 'AI is generating content',
      ai_complete: 'AI content ready for human review (contracts only)',
      human_review: 'Under human expert review',
      completed: 'Content ready for use',
      failed: 'Generation failed'
    };
    return descriptions[status] || status;
  };

  useEffect(() => {
    loadRequests();
    loadVoiceRequests();
  }, []);

  const loadRequests = async () => {
    try {
      setLoading(true);
      const response = await api('/api/ai-assistant/requests');
      setRequests(response.requests || []);
    } catch (err) {
      setError('Failed to load AI requests');
    } finally {
      setLoading(false);
    }
  };

  const loadVoiceRequests = async () => {
    try {
      const response = await api('/api/ai-assistant/voice-requests');
      setVoiceRequests(response.voice_requests || []);
    } catch (err) {
      console.error('Failed to load voice requests:', err);
    }
  };

  const handleSubmitRequest = async () => {
    if (!requestText.trim()) {
      setError('Please enter a request');
      return;
    }

    try {
      setIsProcessing(true);
      setError(null);
      
      const response = await api('/api/ai-assistant/requests', {
        method: 'POST',
        body: JSON.stringify({
          request_type: requestType,
          request_content: requestText,
          priority: priority,
          output_format: 'text'
        })
      });

      setSuccess('AI is generating your content! Most requests will be ready instantly.');
      setRequestText('');
      loadRequests();
    } catch (err) {
      setError('Failed to submit request');
    } finally {
      setIsProcessing(false);
    }
  };

  const handleVoiceRequest = async () => {
    try {
      setIsRecording(true);
      
      // In a real implementation, this would use the Web Audio API
      // For now, we'll simulate the voice request
      const mockAudioFile = new File(['mock audio data'], 'voice_request.wav', {
        type: 'audio/wav'
      });

      const formData = new FormData();
      formData.append('audio_file', mockAudioFile);

      const response = await api('/api/ai-assistant/voice-requests', {
        method: 'POST',
        body: formData,
        headers: {
          // Don't set Content-Type, let the browser set it for FormData
        }
      });

      setSuccess('Voice request submitted successfully!');
      loadVoiceRequests();
    } catch (err) {
      setError('Failed to submit voice request');
    } finally {
      setIsRecording(false);
    }
  };

  const handleViewContent = async (requestId) => {
    try {
      const response = await api(`/api/ai-assistant/requests/${requestId}/content`);
      setDeliverableContent(response);
      setContentDialog(true);
    } catch (err) {
      setError('Failed to load content');
    }
  };

  const handleDownloadContent = async (requestId) => {
    try {
      const response = await api(`/api/ai-assistant/requests/${requestId}/content`);
      
      // Create and download file
      const blob = new Blob([response.content_data], { type: response.mime_type });
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `ai_request_${requestId}.txt`;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);
    } catch (err) {
      setError('Failed to download content');
    }
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleString();
  };

  const getStatusIcon = (status) => {
    switch (status) {
      case 'completed':
        return <SmartToy color="success" />;
      case 'human_review':
        return <Person color="warning" />;
      case 'processing':
        return <CircularProgress size={20} />;
      default:
        return <SmartToy />;
    }
  };

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Box sx={{ mb: 4 }}>
        <Typography variant="h4" component="h1" gutterBottom>
          AI Assistant
        </Typography>
        <Typography variant="subtitle1" color="text.secondary">
          Get professional real estate assistance with AI-powered content generation
        </Typography>
      </Box>

      {error && (
        <Alert severity="error" sx={{ mb: 2 }} onClose={() => setError(null)}>
          {error}
        </Alert>
      )}

      {success && (
        <Alert severity="success" sx={{ mb: 2 }} onClose={() => setSuccess(null)}>
          {success}
        </Alert>
      )}

      <Card sx={{ mb: 4 }}>
        <CardContent>
          <Typography variant="h6" gutterBottom>
            Create New Request
          </Typography>
          
          <Grid container spacing={2} sx={{ mb: 2 }}>
            <Grid item xs={12} md={6}>
              <FormControl fullWidth>
                <InputLabel>Request Type</InputLabel>
                <Select
                  value={requestType}
                  label="Request Type"
                  onChange={(e) => setRequestType(e.target.value)}
                >
                  {requestTypes.map((type) => (
                    <MenuItem key={type.value} value={type.value}>
                      {type.label}
                    </MenuItem>
                  ))}
                </Select>
              </FormControl>
            </Grid>
            
            <Grid item xs={12} md={6}>
              <FormControl fullWidth>
                <InputLabel>Priority</InputLabel>
                <Select
                  value={priority}
                  label="Priority"
                  onChange={(e) => setPriority(e.target.value)}
                >
                  {priorities.map((p) => (
                    <MenuItem key={p.value} value={p.value}>
                      {p.label}
                    </MenuItem>
                  ))}
                </Select>
              </FormControl>
            </Grid>
          </Grid>

          <TextField
            fullWidth
            multiline
            rows={4}
            label="Describe your request"
            placeholder="e.g., Generate a CMA for 123 Sheikh Zayed Road, Dubai Marina (AI will create this instantly)"
            value={requestText}
            onChange={(e) => setRequestText(e.target.value)}
            sx={{ mb: 2 }}
          />

          <Box sx={{ display: 'flex', gap: 2, justifyContent: 'flex-end' }}>
            <Button
              variant="outlined"
              startIcon={isRecording ? <MicOff /> : <Mic />}
              onClick={handleVoiceRequest}
              disabled={isRecording}
              color="secondary"
            >
              {isRecording ? 'Recording...' : 'Voice Request'}
            </Button>
            
            <Button
              variant="contained"
              startIcon={<Send />}
              onClick={handleSubmitRequest}
              disabled={isProcessing || !requestText.trim()}
            >
              {isProcessing ? 'Submitting...' : 'Submit Request'}
            </Button>
          </Box>
        </CardContent>
      </Card>

      <Card>
        <Box sx={{ borderBottom: 1, borderColor: 'divider' }}>
          <Tabs value={activeTab} onChange={(e, newValue) => setActiveTab(newValue)}>
            <Tab label="AI Requests" />
            <Tab label="Voice Requests" />
          </Tabs>
        </Box>

        <CardContent>
          {activeTab === 0 && (
            <Box>
              <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
                <Typography variant="h6">Your AI Requests</Typography>
                <Button
                  startIcon={<Refresh />}
                  onClick={loadRequests}
                  disabled={loading}
                >
                  Refresh
                </Button>
              </Box>

              {loading ? (
                <Box sx={{ display: 'flex', justifyContent: 'center', p: 4 }}>
                  <CircularProgress />
                </Box>
              ) : requests.length === 0 ? (
                <Paper sx={{ p: 4, textAlign: 'center' }}>
                  <Typography variant="body1" color="text.secondary">
                    No AI requests yet. Create your first request above!
                  </Typography>
                </Paper>
              ) : (
                <List>
                  {requests.map((request) => (
                    <React.Fragment key={request.request_id}>
                      <ListItem>
                        <Box sx={{ display: 'flex', alignItems: 'center', mr: 2 }}>
                          {getStatusIcon(request.status)}
                        </Box>
                        
                        <ListItemText
                          primary={
                            <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                              <Typography variant="subtitle1">
                                {requestTypes.find(t => t.value === request.request_type)?.label || request.request_type}
                              </Typography>
                              <Chip
                                label={request.status}
                                color={statusColors[request.status]}
                                size="small"
                              />
                              <Chip
                                label={priorities.find(p => p.value === request.priority)?.label || request.priority}
                                variant="outlined"
                                size="small"
                              />
                            </Box>
                          }
                          secondary={
                            <Box>
                              <Typography variant="body2" color="text.secondary">
                                Created: {formatDate(request.created_at)}
                              </Typography>
                              {request.estimated_completion && (
                                <Typography variant="body2" color="text.secondary">
                                  Estimated completion: {formatDate(request.estimated_completion)}
                                </Typography>
                              )}
                              {request.ai_confidence && (
                                <Typography variant="body2" color="text.secondary">
                                  AI Confidence: {(request.ai_confidence * 100).toFixed(1)}%
                                </Typography>
                              )}
                            </Box>
                          }
                        />
                        
                        <ListItemSecondaryAction>
                          <Box sx={{ display: 'flex', gap: 1 }}>
                            {request.status === 'completed' && request.has_deliverable && (
                              <>
                                <IconButton
                                  onClick={() => handleViewContent(request.request_id)}
                                  color="primary"
                                >
                                  <Visibility />
                                </IconButton>
                                <IconButton
                                  onClick={() => handleDownloadContent(request.request_id)}
                                  color="primary"
                                >
                                  <Download />
                                </IconButton>
                              </>
                            )}
                          </Box>
                        </ListItemSecondaryAction>
                      </ListItem>
                      <Divider />
                    </React.Fragment>
                  ))}
                </List>
              )}
            </Box>
          )}

          {activeTab === 1 && (
            <Box>
              <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
                <Typography variant="h6">Voice Requests</Typography>
                <Button
                  startIcon={<Refresh />}
                  onClick={loadVoiceRequests}
                  disabled={loading}
                >
                  Refresh
                </Button>
              </Box>

              {voiceRequests.length === 0 ? (
                <Paper sx={{ p: 4, textAlign: 'center' }}>
                  <VoiceChat sx={{ fontSize: 48, color: 'text.secondary', mb: 2 }} />
                  <Typography variant="body1" color="text.secondary">
                    No voice requests yet. Try the voice request feature above!
                  </Typography>
                </Paper>
              ) : (
                <List>
                  {voiceRequests.map((voiceRequest) => (
                    <React.Fragment key={voiceRequest.voice_request_id}>
                      <ListItem>
                        <Box sx={{ display: 'flex', alignItems: 'center', mr: 2 }}>
                          <VoiceChat color="primary" />
                        </Box>
                        
                        <ListItemText
                          primary={
                            <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                              <Typography variant="subtitle1">Voice Request</Typography>
                              <Chip
                                label={voiceRequest.processing_status}
                                color={statusColors[voiceRequest.processing_status]}
                                size="small"
                              />
                            </Box>
                          }
                          secondary={
                            <Box>
                              <Typography variant="body2" color="text.secondary">
                                Created: {formatDate(voiceRequest.created_at)}
                              </Typography>
                              {voiceRequest.transcription && (
                                <Typography variant="body2" sx={{ mt: 1 }}>
                                  Transcription: {voiceRequest.transcription}
                                </Typography>
                              )}
                              {voiceRequest.transcription_confidence && (
                                <Typography variant="body2" color="text.secondary">
                                  Confidence: {(voiceRequest.transcription_confidence * 100).toFixed(1)}%
                                </Typography>
                              )}
                              {voiceRequest.error_message && (
                                <Typography variant="body2" color="error">
                                  Error: {voiceRequest.error_message}
                                </Typography>
                              )}
                            </Box>
                          }
                        />
                      </ListItem>
                      <Divider />
                    </React.Fragment>
                  ))}
                </List>
              )}
            </Box>
          )}
        </CardContent>
      </Card>

      {/* Content Dialog */}
      <Dialog
        open={contentDialog}
        onClose={() => setContentDialog(false)}
        maxWidth="md"
        fullWidth
      >
        <DialogTitle>Deliverable Content</DialogTitle>
        <DialogContent>
          {deliverableContent && (
            <Box>
              <Typography variant="body2" color="text.secondary" gutterBottom>
                Content Type: {deliverableContent.content_type}
              </Typography>
              <Typography variant="body2" color="text.secondary" gutterBottom>
                Quality Score: {deliverableContent.quality_score ? (deliverableContent.quality_score * 100).toFixed(1) + '%' : 'N/A'}
              </Typography>
              <Divider sx={{ my: 2 }} />
              <Typography variant="body1" sx={{ whiteSpace: 'pre-wrap' }}>
                {deliverableContent.content_data}
              </Typography>
            </Box>
          )}
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setContentDialog(false)}>Close</Button>
          {deliverableContent && (
            <Button
              variant="contained"
              startIcon={<Download />}
              onClick={() => {
                const blob = new Blob([deliverableContent.content_data], { type: deliverableContent.mime_type });
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = `ai_deliverable_${Date.now()}.txt`;
                document.body.appendChild(a);
                a.click();
                window.URL.revokeObjectURL(url);
                document.body.removeChild(a);
              }}
            >
              Download
            </Button>
          )}
        </DialogActions>
      </Dialog>
    </Container>
  );
};

export default AIAssistant;
