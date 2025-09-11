import React, { useState, useRef, useEffect } from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  Tabs,
  Tab,
  TextField,
  Button,
  IconButton,
  Chip,
  LinearProgress,
  Alert,
  useTheme,
  useMediaQuery,
  Stack,
  Fade,
  Grow,
  Paper
} from '@mui/material';
import {
  Mic as MicIcon,
  MicOff as MicOffIcon,
  Send as SendIcon,
  Stop as StopIcon,
  Delete as DeleteIcon,
  PlayArrow as PlayIcon,
  Pause as PauseIcon,
  GraphicEq as WaveformIcon
} from '@mui/icons-material';
import { useNavigate, useSearchParams } from 'react-router-dom';
import useRequestStore from '../store/requests';

const RequestComposer = () => {
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('md'));
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  
  const [activeTab, setActiveTab] = useState(0);
  const [textContent, setTextContent] = useState('');
  const [selectedTeam, setSelectedTeam] = useState(searchParams.get('team') || 'marketing');
  const [selectedTemplate, setSelectedTemplate] = useState(null);
  const [isRecording, setIsRecording] = useState(false);
  const [isProcessing, setIsProcessing] = useState(false);
  const [recordingTime, setRecordingTime] = useState(0);
  const [audioBlob, setAudioBlob] = useState(null);
  const [transcript, setTranscript] = useState('');
  const [error, setError] = useState(null);
  const [isPlaying, setIsPlaying] = useState(false);
  
  const mediaRecorderRef = useRef(null);
  const audioRef = useRef(null);
  const timerRef = useRef(null);
  
  const { createRequest, createAudioRequest } = useRequestStore();

  const templates = {
    marketing: [
      { id: 'postcard', name: 'Property Postcard', description: 'Create a stunning property postcard' },
      { id: 'email', name: 'Marketing Email', description: 'Professional property email campaign' },
      { id: 'social', name: 'Social Media Post', description: 'Engaging social media content' },
      { id: 'brochure', name: 'Property Brochure', description: 'Comprehensive property brochure' }
    ],
    analytics: [
      { id: 'cma', name: 'Comparative Market Analysis', description: 'Detailed CMA report' },
      { id: 'market_report', name: 'Market Report', description: 'Comprehensive market analysis' },
      { id: 'valuation', name: 'Property Valuation', description: 'Professional property valuation' },
      { id: 'trends', name: 'Market Trends', description: 'Current market trends analysis' }
    ],
    social: [
      { id: 'instagram', name: 'Instagram Post', description: 'Eye-catching Instagram content' },
      { id: 'facebook', name: 'Facebook Post', description: 'Engaging Facebook post' },
      { id: 'linkedin', name: 'LinkedIn Post', description: 'Professional LinkedIn content' },
      { id: 'story', name: 'Social Story', description: 'Quick social media story' }
    ],
    strategy: [
      { id: 'business_plan', name: 'Business Plan', description: 'Strategic business planning' },
      { id: 'marketing_strategy', name: 'Marketing Strategy', description: 'Comprehensive marketing plan' },
      { id: 'client_strategy', name: 'Client Strategy', description: 'Client acquisition strategy' },
      { id: 'growth_plan', name: 'Growth Plan', description: 'Business growth planning' }
    ],
    packages: [
      { id: 'premium', name: 'Premium Package', description: 'Complete premium service package' },
      { id: 'standard', name: 'Standard Package', description: 'Standard service package' },
      { id: 'basic', name: 'Basic Package', description: 'Essential service package' },
      { id: 'custom', name: 'Custom Package', description: 'Tailored service package' }
    ],
    transactions: [
      { id: 'contract', name: 'Contract Review', description: 'Legal contract analysis' },
      { id: 'negotiation', name: 'Negotiation Strategy', description: 'Deal negotiation planning' },
      { id: 'closing', name: 'Closing Process', description: 'Transaction closing management' },
      { id: 'compliance', name: 'Compliance Check', description: 'Regulatory compliance review' }
    ]
  };

  const teams = [
    { id: 'marketing', name: 'Marketing', color: '#E91E63' },
    { id: 'analytics', name: 'Data & Analytics', color: '#9C27B0' },
    { id: 'social', name: 'Social Media', color: '#FF9800' },
    { id: 'strategy', name: 'Strategy', color: '#4CAF50' },
    { id: 'packages', name: 'Packages', color: '#2E7D32' },
    { id: 'transactions', name: 'Transactions', color: '#673AB7' }
  ];

  useEffect(() => {
    return () => {
      if (timerRef.current) {
        clearInterval(timerRef.current);
      }
    };
  }, []);

  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      mediaRecorderRef.current = new MediaRecorder(stream);
      const chunks = [];

      mediaRecorderRef.current.ondataavailable = (event) => {
        chunks.push(event.data);
      };

      mediaRecorderRef.current.onstop = () => {
        const blob = new Blob(chunks, { type: 'audio/webm' });
        setAudioBlob(blob);
        stream.getTracks().forEach(track => track.stop());
      };

      mediaRecorderRef.current.start();
      setIsRecording(true);
      setRecordingTime(0);
      
      timerRef.current = setInterval(() => {
        setRecordingTime(prev => prev + 1);
      }, 1000);
    } catch (error) {
      setError('Microphone access denied. Please allow microphone access and try again.');
    }
  };

  const stopRecording = () => {
    if (mediaRecorderRef.current && isRecording) {
      mediaRecorderRef.current.stop();
      setIsRecording(false);
      if (timerRef.current) {
        clearInterval(timerRef.current);
      }
    }
  };

  const deleteRecording = () => {
    setAudioBlob(null);
    setRecordingTime(0);
    setTranscript('');
  };

  const playRecording = () => {
    if (audioBlob && audioRef.current) {
      if (isPlaying) {
        audioRef.current.pause();
        setIsPlaying(false);
      } else {
        audioRef.current.play();
        setIsPlaying(true);
      }
    }
  };

  const formatTime = (seconds) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  const handleSubmit = async () => {
    if (!textContent.trim() && !transcript.trim()) {
      setError('Please provide either text content or record audio instructions.');
      return;
    }

    setIsProcessing(true);
    setError(null);

    try {
      if (activeTab === 0 && audioBlob) {
        // Handle audio upload
        const response = await createAudioRequest(audioBlob, selectedTeam, selectedTemplate);
        navigate(`/requests/${response.id}`);
      } else {
        // Handle text request
        const payload = {
          team: selectedTeam,
          content: textContent || transcript,
          template_id: selectedTemplate
        };
        
        const response = await createRequest(payload);
        navigate(`/requests/${response.id}`);
      }
    } catch (error) {
      setError(error.message || 'Failed to create request. Please try again.');
    } finally {
      setIsProcessing(false);
    }
  };

  const handleTabChange = (event, newValue) => {
    setActiveTab(newValue);
    setError(null);
  };

  return (
    <Box sx={{ maxWidth: 800, mx: 'auto', p: 2 }}>
      <Fade in timeout={500}>
        <Card sx={{ boxShadow: theme.shadows[4] }}>
          <CardContent sx={{ p: 3 }}>
            {/* Header */}
            <Typography variant="h5" sx={{ fontWeight: 600, mb: 3, textAlign: 'center' }}>
              Create AI Request
            </Typography>

            {/* Team Selection */}
            <Box sx={{ mb: 3 }}>
              <Typography variant="subtitle1" sx={{ fontWeight: 600, mb: 2 }}>
                Select AI Team
              </Typography>
              <Stack direction="row" spacing={1} sx={{ flexWrap: 'wrap', gap: 1 }}>
                {teams.map((team) => (
                  <Chip
                    key={team.id}
                    label={team.name}
                    onClick={() => setSelectedTeam(team.id)}
                    variant={selectedTeam === team.id ? 'filled' : 'outlined'}
                    sx={{
                      backgroundColor: selectedTeam === team.id ? team.color : 'transparent',
                      color: selectedTeam === team.id ? 'white' : team.color,
                      borderColor: team.color,
                      '&:hover': {
                        backgroundColor: selectedTeam === team.id ? team.color : `${team.color}20`,
                      }
                    }}
                  />
                ))}
              </Stack>
            </Box>

            {/* Template Selection */}
            <Box sx={{ mb: 3 }}>
              <Typography variant="subtitle1" sx={{ fontWeight: 600, mb: 2 }}>
                Choose Template (Optional)
              </Typography>
              <Stack direction="row" spacing={1} sx={{ flexWrap: 'wrap', gap: 1 }}>
                {templates[selectedTeam]?.map((template) => (
                  <Chip
                    key={template.id}
                    label={template.name}
                    onClick={() => setSelectedTemplate(selectedTemplate === template.id ? null : template.id)}
                    variant={selectedTemplate === template.id ? 'filled' : 'outlined'}
                    color={selectedTemplate === template.id ? 'primary' : 'default'}
                    size="small"
                  />
                ))}
              </Stack>
            </Box>

            {/* Tabs */}
            <Box sx={{ borderBottom: 1, borderColor: 'divider', mb: 3 }}>
              <Tabs value={activeTab} onChange={handleTabChange}>
                <Tab 
                  label="Audio" 
                  icon={<MicIcon />} 
                  iconPosition="start"
                  sx={{ minHeight: 48 }}
                />
                <Tab 
                  label="Text" 
                  icon={<SendIcon />} 
                  iconPosition="start"
                  sx={{ minHeight: 48 }}
                />
              </Tabs>
            </Box>

            {/* Audio Tab */}
            {activeTab === 0 && (
              <Grow in timeout={300}>
                <Box>
                  <Typography variant="h6" sx={{ mb: 2, textAlign: 'center' }}>
                    Record Your Instructions
                  </Typography>
                  
                  {/* Waveform Placeholder */}
                  <Paper
                    sx={{
                      p: 3,
                      mb: 3,
                      textAlign: 'center',
                      backgroundColor: 'grey.50',
                      border: '2px dashed',
                      borderColor: 'grey.300',
                      minHeight: 120,
                      display: 'flex',
                      flexDirection: 'column',
                      alignItems: 'center',
                      justifyContent: 'center'
                    }}
                  >
                    <WaveformIcon sx={{ fontSize: 48, color: 'grey.400', mb: 2 }} />
                    <Typography variant="body2" color="text.secondary">
                      {isRecording ? 'Recording...' : 'Click record to start'}
                    </Typography>
                    {recordingTime > 0 && (
                      <Typography variant="h4" sx={{ fontWeight: 600, color: 'primary.main', mt: 1 }}>
                        {formatTime(recordingTime)}
                      </Typography>
                    )}
                  </Paper>

                  {/* Audio Controls */}
                  <Box sx={{ display: 'flex', justifyContent: 'center', gap: 2, mb: 3 }}>
                    {!isRecording && !audioBlob && (
                      <Button
                        variant="contained"
                        size="large"
                        startIcon={<MicIcon />}
                        onClick={startRecording}
                        sx={{
                          backgroundColor: '#E91E63',
                          '&:hover': { backgroundColor: '#C2185B' },
                          px: 4,
                          py: 1.5
                        }}
                      >
                        Start Recording
                      </Button>
                    )}

                    {isRecording && (
                      <Button
                        variant="contained"
                        size="large"
                        startIcon={<StopIcon />}
                        onClick={stopRecording}
                        color="error"
                        sx={{ px: 4, py: 1.5 }}
                      >
                        Stop Recording
                      </Button>
                    )}

                    {audioBlob && (
                      <>
                        <Button
                          variant="outlined"
                          startIcon={isPlaying ? <PauseIcon /> : <PlayIcon />}
                          onClick={playRecording}
                        >
                          {isPlaying ? 'Pause' : 'Play'}
                        </Button>
                        <Button
                          variant="outlined"
                          startIcon={<DeleteIcon />}
                          onClick={deleteRecording}
                          color="error"
                        >
                          Delete
                        </Button>
                      </>
                    )}
                  </Box>

                  {/* Transcript */}
                  {transcript && (
                    <Box sx={{ mb: 3 }}>
                      <Typography variant="subtitle2" sx={{ mb: 1 }}>
                        Transcript:
                      </Typography>
                      <Paper sx={{ p: 2, backgroundColor: 'grey.50' }}>
                        <Typography variant="body2">{transcript}</Typography>
                      </Paper>
                    </Box>
                  )}

                  <audio ref={audioRef} onEnded={() => setIsPlaying(false)} />
                </Box>
              </Grow>
            )}

            {/* Text Tab */}
            {activeTab === 1 && (
              <Grow in timeout={300}>
                <Box>
                  <Typography variant="h6" sx={{ mb: 2 }}>
                    Describe Your Request
                  </Typography>
                  <TextField
                    fullWidth
                    multiline
                    rows={6}
                    placeholder="Describe what you need from the AI team. Be as specific as possible for better results..."
                    value={textContent}
                    onChange={(e) => setTextContent(e.target.value)}
                    sx={{
                      '& .MuiOutlinedInput-root': {
                        fontSize: '1rem',
                        lineHeight: 1.5
                      }
                    }}
                  />
                </Box>
              </Grow>
            )}

            {/* Error Alert */}
            {error && (
              <Alert severity="error" sx={{ mb: 3 }}>
                {error}
              </Alert>
            )}

            {/* Processing Indicator */}
            {isProcessing && (
              <Box sx={{ mb: 3 }}>
                <LinearProgress />
                <Typography variant="body2" sx={{ mt: 1, textAlign: 'center' }}>
                  Creating your request...
                </Typography>
              </Box>
            )}

            {/* Submit Button */}
            <Box sx={{ display: 'flex', justifyContent: 'center', gap: 2 }}>
              <Button
                variant="outlined"
                onClick={() => navigate('/hub')}
                disabled={isProcessing}
                sx={{ px: 4 }}
              >
                Cancel
              </Button>
              <Button
                variant="contained"
                onClick={handleSubmit}
                disabled={isProcessing || (!textContent.trim() && !transcript.trim())}
                startIcon={<SendIcon />}
                sx={{ px: 4 }}
              >
                {isProcessing ? 'Creating...' : 'Create Request'}
              </Button>
            </Box>
          </CardContent>
        </Card>
      </Fade>
    </Box>
  );
};

export default RequestComposer;
