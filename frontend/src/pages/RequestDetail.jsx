import React, { useState, useEffect, useRef } from 'react';
import {
  Box,
  Container,
  Typography,
  Card,
  CardContent,
  Chip,
  Button,
  LinearProgress,
  Stepper,
  Step,
  StepLabel,
  StepContent,
  Alert,
  IconButton,
  Tooltip,
  useTheme,
  useMediaQuery,
  Stack,
  Divider,
  Paper,
  Avatar,
  AvatarGroup,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField
} from '@mui/material';
import {
  ArrowBack as ArrowBackIcon,
  Download as DownloadIcon,
  Check as ApproveIcon,
  Edit as EditIcon,
  Refresh as RefreshIcon,
  Schedule as ScheduleIcon,
  Person as PersonIcon,
  GetApp as GetAppIcon,
  Visibility as PreviewIcon,
  Send as SendIcon
} from '@mui/icons-material';
import { useParams, useNavigate } from 'react-router-dom';
import { useAppContext } from '../context/AppContext';
import useRequestStore from '../store/requests';
import { formatDistanceToNow } from 'date-fns';

const RequestDetail = () => {
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('md'));
  const { id } = useParams();
  const navigate = useNavigate();
  const { currentUser } = useAppContext();
  
  const [revisionDialog, setRevisionDialog] = useState(false);
  const [revisionText, setRevisionText] = useState('');
  const [processing, setProcessing] = useState(false);
  const eventSourceRef = useRef(null);
  
  const { 
    currentRequest: request, 
    loading, 
    error, 
    fetchRequest, 
    approveRequest, 
    requestRevision,
    subscribeToRequest,
    clearError 
  } = useRequestStore();

  const steps = [
    { id: 'queued', label: 'Request Received', description: 'Your request has been received and queued for processing' },
    { id: 'planning', label: 'Planning', description: 'AI is analyzing your request and creating a plan' },
    { id: 'generating', label: 'Generating', description: 'AI is creating your content based on the plan' },
    { id: 'validating', label: 'Validating', description: 'Content is being validated for quality and compliance' },
    { id: 'draft_ready', label: 'Draft Ready', description: 'Your content is ready for review' },
    { id: 'approved', label: 'Approved', description: 'Content has been approved and is ready for use' },
    { id: 'delivered', label: 'Delivered', description: 'Content has been delivered to you' }
  ];

  useEffect(() => {
    loadRequest();
    setupEventStream();
    
    return () => {
      if (eventSourceRef.current) {
        eventSourceRef.current.close();
      }
    };
  }, [id]);

  const loadRequest = async () => {
    try {
      await fetchRequest(id);
    } catch (error) {
      console.error('Error loading request:', error);
    }
  };

  const setupEventStream = () => {
    // Mock event stream - replace with actual SSE connection
    // const eventSource = new EventSource(`/api/requests/${id}/stream`);
    // eventSourceRef.current = eventSource;
    
    // eventSource.onmessage = (event) => {
    //   const data = JSON.parse(event.data);
    //   handleStreamUpdate(data);
    // };
    
    // eventSource.onerror = (error) => {
    //   console.error('Event stream error:', error);
    // };
  };

  const handleStreamUpdate = (data) => {
    // Update the request in the store
    // Note: This would need to be implemented in the store if real-time updates are needed
    console.log('Stream update received:', data);
  };

  const handleApprove = async () => {
    try {
      setProcessing(true);
      await approveRequest(id);
    } catch (error) {
      console.error('Failed to approve request:', error);
    } finally {
      setProcessing(false);
    }
  };

  const handleRequestRevision = async () => {
    if (!revisionText.trim()) return;
    
    try {
      setProcessing(true);
      await requestRevision(id, revisionText);
      setRevisionDialog(false);
      setRevisionText('');
    } catch (error) {
      console.error('Failed to request revision:', error);
    } finally {
      setProcessing(false);
    }
  };

  const handleDownload = (deliverable) => {
    // Mock download - replace with actual download logic
    console.log('Downloading:', deliverable.name);
  };

  const getStatusColor = (status) => {
    const colors = {
      queued: 'default',
      planning: 'info',
      generating: 'primary',
      validating: 'warning',
      draft_ready: 'success',
      needs_info: 'warning',
      approved: 'success',
      delivered: 'success',
      failed: 'error'
    };
    return colors[status] || 'default';
  };

  const getTeamColor = (team) => {
    const colors = {
      marketing: '#E91E63',
      analytics: '#9C27B0',
      social: '#FF9800',
      strategy: '#4CAF50',
      packages: '#2E7D32',
      transactions: '#673AB7'
    };
    return colors[team] || theme.palette.primary.main;
  };

  const formatETA = (eta) => {
    if (!eta) return 'TBD';
    const now = new Date();
    const etaDate = new Date(eta);
    const diff = etaDate - now;
    
    if (diff < 0) return 'Overdue';
    if (diff < 60000) return 'Any moment';
    if (diff < 3600000) return `${Math.ceil(diff / 60000)}m`;
    if (diff < 86400000) return `${Math.ceil(diff / 3600000)}h`;
    return `${Math.ceil(diff / 86400000)}d`;
  };

  const getCurrentStepIndex = () => {
    if (!request) return 0;
    return steps.findIndex(step => step.id === request.status);
  };

  if (loading) {
    return (
      <Box sx={{ minHeight: '100vh', backgroundColor: 'background.default', p: 3 }}>
        <Container maxWidth="lg">
          <Typography variant="h4" sx={{ mb: 3 }}>Loading request...</Typography>
        </Container>
      </Box>
    );
  }

  if (error || !request) {
    return (
      <Box sx={{ minHeight: '100vh', backgroundColor: 'background.default', p: 3 }}>
        <Container maxWidth="lg">
          <Alert severity="error" sx={{ mb: 3 }}>
            {error || 'Request not found'}
          </Alert>
          <Button onClick={() => navigate('/hub')} startIcon={<ArrowBackIcon />}>
            Back to Hub
          </Button>
        </Container>
      </Box>
    );
  }

  return (
    <Box sx={{ minHeight: '100vh', backgroundColor: 'background.default' }}>
      <Container maxWidth="lg" sx={{ py: 3 }}>
        {/* Header */}
        <Box sx={{ display: 'flex', alignItems: 'center', mb: 3 }}>
          <IconButton onClick={() => navigate('/hub')} sx={{ mr: 2 }}>
            <ArrowBackIcon />
          </IconButton>
          <Box sx={{ flex: 1 }}>
            <Typography variant="h4" sx={{ fontWeight: 600, mb: 1 }}>
              {request.title}
            </Typography>
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, flexWrap: 'wrap' }}>
              <Chip
                label={request.team?.toUpperCase() || 'GENERAL'}
                sx={{
                  backgroundColor: getTeamColor(request.team),
                  color: 'white',
                  fontWeight: 600
                }}
              />
              <Chip
                label={request.status?.replace('_', ' ').toUpperCase()}
                color={getStatusColor(request.status)}
                variant="outlined"
              />
              <Chip
                label={`ETA: ${formatETA(request.eta)}`}
                icon={<ScheduleIcon />}
                variant="outlined"
                size="small"
              />
            </Box>
          </Box>
          <IconButton onClick={loadRequest} disabled={loading}>
            <RefreshIcon />
          </IconButton>
        </Box>

        <Box sx={{ display: 'grid', gridTemplateColumns: { xs: '1fr', lg: '2fr 1fr' }, gap: 3 }}>
          {/* Main Content */}
          <Box>
            {/* Description */}
            <Card sx={{ mb: 3 }}>
              <CardContent>
                <Typography variant="h6" sx={{ fontWeight: 600, mb: 2 }}>
                  Request Description
                </Typography>
                <Typography variant="body1" sx={{ lineHeight: 1.6 }}>
                  {request.description}
                </Typography>
              </CardContent>
            </Card>

            {/* Progress Timeline */}
            <Card sx={{ mb: 3 }}>
              <CardContent>
                <Typography variant="h6" sx={{ fontWeight: 600, mb: 3 }}>
                  Progress Timeline
                </Typography>
                <Stepper activeStep={getCurrentStepIndex()} orientation="vertical">
                  {steps.map((step, index) => {
                    const stepData = request.steps?.find(s => s.step === step.id);
                    const isCompleted = stepData?.status === 'completed';
                    const isCurrent = stepData?.status === 'current';
                    
                    return (
                      <Step key={step.id} completed={isCompleted} active={isCurrent}>
                        <StepLabel>
                          <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                            <Typography variant="subtitle1" sx={{ fontWeight: 600 }}>
                              {step.label}
                            </Typography>
                            {isCurrent && (
                              <LinearProgress 
                                sx={{ width: 100, height: 4, borderRadius: 2 }} 
                                variant="indeterminate" 
                              />
                            )}
                          </Box>
                        </StepLabel>
                        <StepContent>
                          <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                            {step.description}
                          </Typography>
                          {stepData && (
                            <Box sx={{ display: 'flex', gap: 2, flexWrap: 'wrap' }}>
                              {stepData.started_at && (
                                <Chip
                                  label={`Started: ${formatDistanceToNow(new Date(stepData.started_at), { addSuffix: true })}`}
                                  size="small"
                                  variant="outlined"
                                />
                              )}
                              {stepData.finished_at && (
                                <Chip
                                  label={`Completed: ${formatDistanceToNow(new Date(stepData.finished_at), { addSuffix: true })}`}
                                  size="small"
                                  variant="outlined"
                                  color="success"
                                />
                              )}
                            </Box>
                          )}
                        </StepContent>
                      </Step>
                    );
                  })}
                </Stepper>
              </CardContent>
            </Card>

            {/* Deliverables */}
            {request.deliverables && request.deliverables.length > 0 && (
              <Card>
                <CardContent>
                  <Typography variant="h6" sx={{ fontWeight: 600, mb: 3 }}>
                    Deliverables
                  </Typography>
                  <Stack spacing={2}>
                    {request.deliverables.map((deliverable) => (
                      <Paper
                        key={deliverable.id}
                        sx={{
                          p: 2,
                          display: 'flex',
                          alignItems: 'center',
                          justifyContent: 'space-between',
                          border: `1px solid ${theme.palette.divider}`,
                          borderRadius: 2
                        }}
                      >
                        <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                          <Avatar sx={{ bgcolor: 'primary.main' }}>
                            <GetAppIcon />
                          </Avatar>
                          <Box>
                            <Typography variant="subtitle1" sx={{ fontWeight: 600 }}>
                              {deliverable.name}
                            </Typography>
                            <Typography variant="body2" color="text.secondary">
                              {deliverable.size} • {deliverable.type.toUpperCase()}
                            </Typography>
                          </Box>
                        </Box>
                        <Box sx={{ display: 'flex', gap: 1 }}>
                          <Tooltip title="Preview">
                            <IconButton size="small">
                              <PreviewIcon />
                            </IconButton>
                          </Tooltip>
                          <Tooltip title="Download">
                            <IconButton 
                              size="small" 
                              onClick={() => handleDownload(deliverable)}
                            >
                              <DownloadIcon />
                            </IconButton>
                          </Tooltip>
                        </Box>
                      </Paper>
                    ))}
                  </Stack>
                </CardContent>
              </Card>
            )}
          </Box>

          {/* Sidebar */}
          <Box>
            {/* Team Members */}
            <Card sx={{ mb: 3 }}>
              <CardContent>
                <Typography variant="h6" sx={{ fontWeight: 600, mb: 2 }}>
                  Team Members
                </Typography>
                <AvatarGroup max={4}>
                  {request.assignees?.map((assignee) => (
                    <Avatar
                      key={assignee.id}
                      sx={{ bgcolor: getTeamColor(request.team) }}
                    >
                      {assignee.name?.split(' ').map(n => n[0]).join('') || 'U'}
                    </Avatar>
                  ))}
                </AvatarGroup>
                <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
                  {request.assignees?.map(a => a.name).join(', ')}
                </Typography>
              </CardContent>
            </Card>

            {/* Actions */}
            {request.status === 'draft_ready' && (
              <Card sx={{ mb: 3 }}>
                <CardContent>
                  <Typography variant="h6" sx={{ fontWeight: 600, mb: 2 }}>
                    Actions
                  </Typography>
                  <Stack spacing={2}>
                    <Button
                      variant="contained"
                      startIcon={<ApproveIcon />}
                      onClick={handleApprove}
                      disabled={processing}
                      fullWidth
                      sx={{ py: 1.5 }}
                    >
                      Approve & Deliver
                    </Button>
                    <Button
                      variant="outlined"
                      startIcon={<EditIcon />}
                      onClick={() => setRevisionDialog(true)}
                      disabled={processing}
                      fullWidth
                      sx={{ py: 1.5 }}
                    >
                      Request Revision
                    </Button>
                  </Stack>
                </CardContent>
              </Card>
            )}

            {/* Request Info */}
            <Card>
              <CardContent>
                <Typography variant="h6" sx={{ fontWeight: 600, mb: 2 }}>
                  Request Info
                </Typography>
                <Stack spacing={1}>
                  <Box sx={{ display: 'flex', justifyContent: 'space-between' }}>
                    <Typography variant="body2" color="text.secondary">
                      Created:
                    </Typography>
                    <Typography variant="body2">
                      {formatDistanceToNow(new Date(request.created_at), { addSuffix: true })}
                    </Typography>
                  </Box>
                  <Box sx={{ display: 'flex', justifyContent: 'space-between' }}>
                    <Typography variant="body2" color="text.secondary">
                      Updated:
                    </Typography>
                    <Typography variant="body2">
                      {formatDistanceToNow(new Date(request.updated_at), { addSuffix: true })}
                    </Typography>
                  </Box>
                  <Box sx={{ display: 'flex', justifyContent: 'space-between' }}>
                    <Typography variant="body2" color="text.secondary">
                      Priority:
                    </Typography>
                    <Typography variant="body2">
                      {request.priority || 'Normal'}
                    </Typography>
                  </Box>
                </Stack>
              </CardContent>
            </Card>
          </Box>
        </Box>

        {/* Revision Dialog */}
        <Dialog
          open={revisionDialog}
          onClose={() => setRevisionDialog(false)}
          maxWidth="sm"
          fullWidth
        >
          <DialogTitle>Request Revision</DialogTitle>
          <DialogContent>
            <TextField
              fullWidth
              multiline
              rows={4}
              placeholder="Describe what changes you'd like to make..."
              value={revisionText}
              onChange={(e) => setRevisionText(e.target.value)}
              sx={{ mt: 1 }}
            />
          </DialogContent>
          <DialogActions>
            <Button onClick={() => setRevisionDialog(false)}>
              Cancel
            </Button>
            <Button
              variant="contained"
              onClick={handleRequestRevision}
              disabled={!revisionText.trim() || processing}
              startIcon={<SendIcon />}
            >
              Send Revision Request
            </Button>
          </DialogActions>
        </Dialog>
      </Container>
    </Box>
  );
};

export default RequestDetail;
