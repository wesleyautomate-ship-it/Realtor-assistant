import React, { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Card,
  CardContent,
  CardActions,
  Button,
  Chip,
  List,
  ListItem,
  ListItemText,
  ListItemIcon,
  IconButton,
  LinearProgress,
  useTheme,
  Fade,
  Grow,
  Alert,
  Skeleton,
  Tooltip,
} from '@mui/material';
import {
  PlayArrow as PlayIcon,
  Pause as PauseIcon,
  Stop as StopIcon,
  Schedule as ScheduleIcon,
  TrendingUp as TrendingUpIcon,
  Person as PersonIcon,
  Home as HomeIcon,
  Assessment as AssessmentIcon,
  PriorityHigh as PriorityHighIcon,
  ExpandMore as PriorityLowIcon,
  MoreVert as MoreVertIcon,
  CheckCircle as CheckCircleIcon,
} from '@mui/icons-material';

const TaskQueue = () => {
  const theme = useTheme();
  const [tasks, setTasks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [expanded, setExpanded] = useState(true);

  // Mock data for development - will be replaced with real API calls
  const mockTasks = [
    {
      id: 1,
      title: 'Follow up with Ali Khan',
      description: 'Client viewed similar properties yesterday',
      type: 'client_followup',
      priority: 'high',
      estimatedDuration: '15 minutes',
      dueDate: 'Today',
      status: 'pending',
      aiScore: 95,
      category: 'Lead Nurturing',
      icon: PersonIcon,
      tags: ['Client', 'Follow-up', 'High Value'],
    },
    {
      id: 2,
      title: 'Generate CMA for Villa 12',
      description: 'Comparative Market Analysis for Emirates Hills property',
      type: 'cma_generation',
      priority: 'high',
      estimatedDuration: '45 minutes',
      dueDate: 'Tomorrow',
      status: 'pending',
      aiScore: 92,
      category: 'Property Analysis',
      icon: AssessmentIcon,
      tags: ['CMA', 'Villa', 'Emirates Hills'],
    },
    {
      id: 3,
      title: 'Market Trend Analysis',
      description: 'Weekly market report for Dubai Marina area',
      type: 'market_analysis',
      priority: 'medium',
      estimatedDuration: '30 minutes',
      dueDate: 'This Week',
      status: 'pending',
      aiScore: 87,
      category: 'Market Intelligence',
      icon: TrendingUpIcon,
      tags: ['Market', 'Analysis', 'Weekly'],
    },
    {
      id: 4,
      title: 'Client Satisfaction Survey',
      description: 'Follow-up with 3 clients for feedback',
      type: 'client_retention',
      priority: 'low',
      estimatedDuration: '20 minutes',
      dueDate: 'This Week',
      status: 'pending',
      aiScore: 78,
      category: 'Client Relations',
      icon: PersonIcon,
      tags: ['Survey', 'Feedback', 'Retention'],
    },
    {
      id: 5,
      title: 'Property Photo Update',
      description: 'Update photos for Downtown Apartment listing',
      type: 'property_management',
      priority: 'medium',
      estimatedDuration: '25 minutes',
      dueDate: 'Tomorrow',
      status: 'pending',
      aiScore: 82,
      category: 'Property Management',
      icon: HomeIcon,
      tags: ['Photos', 'Listing', 'Update'],
    },
  ];

  useEffect(() => {
    // Simulate API call delay
    const timer = setTimeout(() => {
      setTasks(mockTasks);
      setLoading(false);
    }, 100);
    
    return () => clearTimeout(timer);
  }, []);

  const handleStartTask = (taskId) => {
    console.log('Starting task:', taskId);
    // TODO: Implement task start functionality
    setTasks(prev => prev.map(task => 
      task.id === taskId 
        ? { ...task, status: 'in_progress' }
        : task
    ));
  };

  const handlePauseTask = (taskId) => {
    console.log('Pausing task:', taskId);
    // TODO: Implement task pause functionality
    setTasks(prev => prev.map(task => 
      task.id === taskId 
        ? { ...task, status: 'paused' }
        : task
    ));
  };

  const handleStopTask = (taskId) => {
    console.log('Stopping task:', taskId);
    // TODO: Implement task stop functionality
    setTasks(prev => prev.map(task => 
      task.id === taskId 
        ? { ...task, status: 'stopped' }
        : task
    ));
  };

  const handleRescheduleTask = (taskId) => {
    console.log('Rescheduling task:', taskId);
    // TODO: Implement task rescheduling
  };

  const getPriorityColor = (priority) => {
    switch (priority) {
      case 'high':
        return 'error';
      case 'medium':
        return 'warning';
      case 'low':
        return 'success';
      default:
        return 'default';
    }
  };

  const getPriorityIcon = (priority) => {
    switch (priority) {
      case 'high':
        return <PriorityHighIcon />;
      case 'medium':
        return <ScheduleIcon />;
      case 'low':
        return <PriorityLowIcon />;
      default:
        return <ScheduleIcon />;
    }
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'in_progress':
        return 'primary';
      case 'paused':
        return 'warning';
      case 'stopped':
        return 'error';
      case 'completed':
        return 'success';
      default:
        return 'default';
    }
  };

  const getStatusIcon = (status) => {
    switch (status) {
      case 'in_progress':
        return <PlayIcon />;
      case 'paused':
        return <PauseIcon />;
      case 'stopped':
        return <StopIcon />;
      case 'completed':
        return <CheckCircleIcon />;
      default:
        return <ScheduleIcon />;
    }
  };

  const getAIScoreColor = (score) => {
    if (score >= 90) return 'success.main';
    if (score >= 80) return 'warning.main';
    if (score >= 70) return 'info.main';
    return 'error.main';
  };

  const renderTaskItem = (task, index) => {
    // Safety check to prevent rendering with undefined task properties
    if (!task || !task.priority || !task.icon) {
      return null;
    }
    
    return (
      <ListItem
        key={task.id}
        sx={{
          bgcolor: 'background.paper',
          borderRadius: 2,
          mb: 2,
          border: `1px solid ${theme.palette.divider}`,
          '&:hover': {
            boxShadow: theme.shadows[4],
            transform: 'translateY(-1px)',
          },
          transition: 'all 0.2s ease',
        }}
      >
        <ListItemIcon>
          <Box
            sx={{
              width: 40,
              height: 40,
              borderRadius: '50%',
              bgcolor: 'primary.light',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              color: 'primary.contrastText',
            }}
          >
            {React.createElement(task.icon)}
          </Box>
        </ListItemIcon>

        <ListItemText
          primary={
            <Box>
              <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', mb: 1 }}>
                <Typography variant="subtitle1" sx={{ fontWeight: 600 }}>
                  {task.title}
                </Typography>
                <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                  <Chip
                    label={`AI: ${task.aiScore}%`}
                    size="small"
                    sx={{
                      bgcolor: getAIScoreColor(task.aiScore),
                      color: 'white',
                      fontWeight: 600,
                    }}
                  />
                  <Chip
                    icon={getPriorityIcon(task.priority)}
                    label={task.priority}
                    size="small"
                    color={getPriorityColor(task.priority)}
                    variant="outlined"
                  />
                </Box>
              </Box>
              
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
                <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                  <Typography variant="caption" sx={{ color: 'text.secondary' }}>
                    ⏱️ {task.estimatedDuration}
                  </Typography>
                  <Typography variant="caption" sx={{ color: 'text.secondary' }}>
                    📅 {task.dueDate}
                  </Typography>
                  <Typography variant="caption" sx={{ color: 'text.secondary' }}>
                    📁 {task.category}
                  </Typography>
                </Box>
              </Box>
            </Box>
          }
        />

        <Box sx={{ display: 'flex', flexDirection: 'column', gap: 1 }}>
          {task.status === 'pending' && (
            <Button
              variant="contained"
              size="small"
              startIcon={<PlayIcon />}
              onClick={() => handleStartTask(task.id)}
              sx={{ minWidth: 'auto' }}
            >
              Start
            </Button>
          )}
          
          {task.status === 'in_progress' && (
            <>
              <Button
                variant="outlined"
                size="small"
                startIcon={<PauseIcon />}
                onClick={() => handlePauseTask(task.id)}
                sx={{ minWidth: 'auto' }}
              >
                Pause
              </Button>
              <Button
                variant="outlined"
                size="small"
                startIcon={<StopIcon />}
                onClick={() => handleStopTask(task.id)}
                color="error"
                sx={{ minWidth: 'auto' }}
              >
                Stop
              </Button>
            </>
          )}

          {task.status === 'paused' && (
            <Button
              variant="contained"
              size="small"
              startIcon={<PlayIcon />}
              onClick={() => handleStartTask(task.id)}
              sx={{ minWidth: 'auto' }}
            >
              Resume
            </Button>
          )}

          <Tooltip title="More options">
            <IconButton size="small">
              <MoreVertIcon />
            </IconButton>
          </Tooltip>
        </Box>
      </ListItem>
    );
  };

  // Render loading state
  if (loading) {
    return (
      <Box>
        {/* Header */}
        <Box
          sx={{
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
            cursor: 'pointer',
            p: 2,
            bgcolor: 'background.paper',
            borderBottom: `1px solid ${theme.palette.divider}`,
          }}
        >
          <Typography variant="h6" sx={{ fontWeight: 700, color: 'primary.main' }}>
            📋 Smart Task Queue
          </Typography>
        </Box>
        
        {/* Loading skeletons */}
        <Box sx={{ p: 2 }}>
          <Skeleton variant="rectangular" height={60} sx={{ mb: 2 }} />
          <Skeleton variant="rectangular" height={200} sx={{ mb: 2 }} />
          <Skeleton variant="rectangular" height={200} />
        </Box>
      </Box>
    );
  }

  // Render main content when not loading
  return (
    <Box>
      {/* Header */}
      <Box
        sx={{
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          cursor: 'pointer',
          p: 2,
          bgcolor: 'background.paper',
          borderBottom: `1px solid ${theme.palette.divider}`,
        }}
        onClick={() => setExpanded(!expanded)}
      >
        <Typography variant="h6" sx={{ fontWeight: 700, color: 'primary.main' }}>
          📋 Smart Task Queue
        </Typography>
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
          <Typography variant="caption" sx={{ color: 'text.secondary' }}>
            {tasks.filter(t => t.status === 'pending').length} pending
          </Typography>
        </Box>
      </Box>

      {/* Content */}
      <Box sx={{ p: 2 }}>
        {tasks.length === 0 ? (
          <Alert severity="info">
            No tasks in queue. AI will suggest tasks based on your priorities.
          </Alert>
        ) : (
          <List>
            {tasks
              .filter(task => task && task.priority && task.icon)
              .sort((a, b) => b.aiScore - a.aiScore)
              .map((task, index) => (
                <Grow in timeout={200 + index * 100} key={task.id}>
                  {renderTaskItem(task, index)}
                </Grow>
              ))}
          </List>
        )}
      </Box>
    </Box>
  );
};

export default TaskQueue;
