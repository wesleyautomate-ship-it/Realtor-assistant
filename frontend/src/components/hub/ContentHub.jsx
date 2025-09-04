import React, { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Card,
  CardContent,
  CardActions,
  Button,
  Chip,
  LinearProgress,
  IconButton,
  List,
  ListItem,
  ListItemText,
  ListItemIcon,
  Divider,
  useTheme,
  Fade,
  Grow,
  Alert,
  Skeleton,
} from '@mui/material';
import {
  PlayArrow as PlayIcon,
  Stop as StopIcon,
  CheckCircle as CheckCircleIcon,
  Error as ErrorIcon,
  Download as DownloadIcon,
  Share as ShareIcon,
  Visibility as VisibilityIcon,
  Schedule as ScheduleIcon,
  TrendingUp as TrendingUpIcon,
  Assessment as AssessmentIcon,
  Description as DescriptionIcon,
  Image as ImageIcon,
} from '@mui/icons-material';

const ContentHub = () => {
  const theme = useTheme();
  const [activeTasks, setActiveTasks] = useState([]);
  const [completedTasks, setCompletedTasks] = useState([]);
  const [loading, setLoading] = useState(false);

  // Mock data for development - will be replaced with real API calls
  const mockActiveTasks = [
    {
      id: 1,
      type: 'cma_generation',
      title: 'Generating CMA for Villa 12',
      description: 'Comparative Market Analysis for Emirates Hills property',
      progress: 75,
      estimatedTime: '2 minutes remaining',
      status: 'processing',
      icon: AssessmentIcon,
    },
    {
      id: 2,
      type: 'market_analysis',
      title: 'Analyzing Market Trends',
      description: 'Processing Dubai Marina market data',
      progress: 45,
      estimatedTime: '5 minutes remaining',
      status: 'processing',
      icon: TrendingUpIcon,
    },
  ];

  const mockCompletedTasks = [
    {
      id: 1,
      type: 'cma_report',
      title: 'CMA Report - Villa 12',
      description: '3-bed villa, 2,500 sq ft, Emirates Hills',
      status: 'completed',
      resultUrl: 'https://example.com/cma-report-1',
      fileSize: '2.4 MB',
      completedAt: '5 minutes ago',
      icon: AssessmentIcon,
      tags: ['CMA', 'Villa', 'Emirates Hills'],
    },
    {
      id: 2,
      type: 'client_template',
      title: 'Client Follow-up Template',
      description: 'Personalized message template for Ali Khan',
      status: 'completed',
      resultUrl: 'https://example.com/template-1',
      fileSize: '15 KB',
      completedAt: '15 minutes ago',
      icon: DescriptionIcon,
      tags: ['Template', 'Client', 'Follow-up'],
    },
    {
      id: 3,
      type: 'property_analysis',
      title: 'Property Comparison Analysis',
      description: '5 similar properties found in Dubai Marina',
      status: 'completed',
      resultUrl: 'https://example.com/analysis-1',
      fileSize: '1.8 MB',
      completedAt: '1 hour ago',
      icon: TrendingUpIcon,
      tags: ['Analysis', 'Comparison', 'Dubai Marina'],
    },
  ];

  useEffect(() => {
    // Load mock data
    setActiveTasks(mockActiveTasks);
    setCompletedTasks(mockCompletedTasks);
  }, []);

  const handleCancelTask = (taskId) => {
    console.log('Cancelling task:', taskId);
    // TODO: Implement task cancellation
    setActiveTasks(prev => prev.filter(task => task.id !== taskId));
  };

  const handleViewResult = (task) => {
    console.log('Viewing result:', task.title);
    // TODO: Implement result viewing
    window.open(task.resultUrl, '_blank');
  };

  const handleDownload = (task) => {
    console.log('Downloading:', task.title);
    // TODO: Implement download functionality
  };

  const handleShare = (task) => {
    console.log('Sharing:', task.title);
    // TODO: Implement share functionality
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'processing':
        return 'primary';
      case 'completed':
        return 'success';
      case 'error':
        return 'error';
      case 'pending':
        return 'warning';
      default:
        return 'default';
    }
  };

  const getStatusIcon = (status) => {
    switch (status) {
      case 'processing':
        return <PlayIcon />;
      case 'completed':
        return <CheckCircleIcon />;
      case 'error':
        return <ErrorIcon />;
      case 'pending':
        return <ScheduleIcon />;
      default:
        return <ScheduleIcon />;
    }
  };

  const getTypeIcon = (type) => {
    switch (type) {
      case 'cma_generation':
      case 'cma_report':
        return AssessmentIcon;
      case 'market_analysis':
      case 'property_analysis':
        return TrendingUpIcon;
      case 'client_template':
        return DescriptionIcon;
      case 'image_processing':
        return ImageIcon;
      default:
        return DescriptionIcon;
    }
  };

  const renderActiveTasks = () => (
    <Box sx={{ mb: 3 }}>
      <Typography variant="h6" sx={{ fontWeight: 600, mb: 2, display: 'flex', alignItems: 'center' }}>
        <PlayIcon sx={{ mr: 1, color: 'primary.main' }} />
        In Progress ({activeTasks.length})
      </Typography>

      {activeTasks.length === 0 ? (
        <Alert severity="info" sx={{ mb: 2 }}>
          No active tasks. Start a new task to see progress here.
        </Alert>
      ) : (
        <List dense>
          {activeTasks.map((task, index) => (
            <ListItem
              key={task.id}
              sx={{
                bgcolor: 'background.paper',
                borderRadius: 1,
                mb: 1,
                border: `1px solid ${theme.palette.divider}`,
              }}
            >
              <ListItemIcon>
                {React.createElement(task.icon, { sx: { color: 'primary.main' } })}
              </ListItemIcon>
              <ListItemText
                primary={
                  <Box>
                    <Typography variant="subtitle2" sx={{ fontWeight: 600, mb: 0.5 }}>
                      {task.title}
                    </Typography>
                    <Typography variant="body2" sx={{ color: 'text.secondary', mb: 1 }}>
                      {task.description}
                    </Typography>
                    <Box sx={{ mb: 1 }}>
                      <LinearProgress
                        variant="determinate"
                        value={task.progress}
                        sx={{ height: 6, borderRadius: 3 }}
                      />
                    </Box>
                    <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                      <Typography variant="caption" sx={{ color: 'text.secondary' }}>
                        {task.progress}% complete
                      </Typography>
                      <Typography variant="caption" sx={{ color: 'text.secondary' }}>
                        {task.estimatedTime}
                      </Typography>
                    </Box>
                  </Box>
                }
              />
              <IconButton
                size="small"
                onClick={() => handleCancelTask(task.id)}
                sx={{ color: 'error.main' }}
              >
                <StopIcon />
              </IconButton>
            </ListItem>
          ))}
        </List>
      )}
    </Box>
  );

  const renderCompletedTasks = () => (
    <Box>
      <Typography variant="h6" sx={{ fontWeight: 600, mb: 2, display: 'flex', alignItems: 'center' }}>
        <CheckCircleIcon sx={{ mr: 1, color: 'success.main' }} />
        Ready for Review ({completedTasks.length})
      </Typography>

      {completedTasks.length === 0 ? (
        <Alert severity="info">
          No completed tasks yet. Results will appear here when ready.
        </Alert>
      ) : (
        <List dense>
          {completedTasks.map((task, index) => (
            <ListItem
              key={task.id}
              sx={{
                bgcolor: 'background.paper',
                borderRadius: 1,
                mb: 1,
                border: `1px solid ${theme.palette.divider}`,
              }}
            >
              <ListItemIcon>
                {React.createElement(task.icon, { sx: { color: 'success.main' } })}
              </ListItemIcon>
              <ListItemText
                primary={
                  <Box>
                    <Typography variant="subtitle2" sx={{ fontWeight: 600, mb: 0.5 }}>
                      {task.title}
                    </Typography>
                    <Typography variant="body2" sx={{ color: 'text.secondary', mb: 1 }}>
                      {task.description}
                    </Typography>
                    <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 1 }}>
                      {task.tags.map((tag, tagIndex) => (
                        <Chip
                          key={tagIndex}
                          label={tag}
                          size="small"
                          variant="outlined"
                          sx={{ fontSize: '0.7rem' }}
                        />
                      ))}
                    </Box>
                    <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                      <Typography variant="caption" sx={{ color: 'text.secondary' }}>
                        {task.fileSize} • {task.completedAt}
                      </Typography>
                    </Box>
                  </Box>
                }
              />
              <Box sx={{ display: 'flex', flexDirection: 'column', gap: 0.5 }}>
                <IconButton
                  size="small"
                  onClick={() => handleViewResult(task)}
                  sx={{ color: 'primary.main' }}
                  title="View Result"
                >
                  <VisibilityIcon />
                </IconButton>
                <IconButton
                  size="small"
                  onClick={() => handleDownload(task)}
                  sx={{ color: 'success.main' }}
                  title="Download"
                >
                  <DownloadIcon />
                </IconButton>
                <IconButton
                  size="small"
                  onClick={() => handleShare(task)}
                  sx={{ color: 'info.main' }}
                  title="Share"
                >
                  <ShareIcon />
                </IconButton>
              </Box>
            </ListItem>
          ))}
        </List>
      )}
    </Box>
  );

  if (loading) {
    return (
      <Box>
        <Skeleton variant="rectangular" height={60} sx={{ mb: 2 }} />
        <Skeleton variant="rectangular" height={200} sx={{ mb: 2 }} />
        <Skeleton variant="rectangular" height={300} />
      </Box>
    );
  }

  return (
    <Box>
      {renderActiveTasks()}
      <Divider sx={{ my: 2 }} />
      {renderCompletedTasks()}
    </Box>
  );
};

export default ContentHub;
