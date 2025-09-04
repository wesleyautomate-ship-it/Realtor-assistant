import React, { useState, useEffect } from 'react';
import {
  Box,
  Card,
  CardContent,
  CardHeader,
  Typography,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  Chip,
  IconButton,
  Tooltip,
  CircularProgress,
  Alert,
  Stack,
  Divider,
} from '@mui/material';
import {
  Schedule as ScheduleIcon,
  CheckCircle as CheckCircleIcon,
  Pending as PendingIcon,
  PriorityHigh as PriorityHighIcon,
  ExpandMore as PriorityLowIcon,
  Refresh as RefreshIcon,
  Add as AddIcon,
} from '@mui/icons-material';
import { useAuth } from '../../context/AuthContext';
import { apiClient } from '../../utils/apiClient';

const TodaysAgendaPanel = () => {
  const { user } = useAuth();
  const [agenda, setAgenda] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchTodaysAgenda();
  }, []);

  const fetchTodaysAgenda = async () => {
    try {
      setLoading(true);
      setError(null);
      
      // Try to fetch from backend first
      try {
        const response = await apiClient.get('/users/me/agenda');
        setAgenda(response.data || []);
      } catch (apiError) {
        console.log('Using mock agenda data');
        // Fallback to mock data
        setAgenda(generateMockAgenda());
      }
    } catch (error) {
      console.error('Error fetching agenda:', error);
      setError('Failed to load today\'s agenda');
      setAgenda(generateMockAgenda());
    } finally {
      setLoading(false);
    }
  };

  const generateMockAgenda = () => [
    {
      id: 1,
      title: 'Client Meeting - Downtown Property',
      time: '09:00 AM',
      type: 'meeting',
      priority: 'high',
      status: 'pending',
      description: 'Discuss offer details for Downtown property with client'
    },
    {
      id: 2,
      title: 'Property Viewing - Marina Views',
      time: '11:30 AM',
      type: 'viewing',
      priority: 'medium',
      status: 'pending',
      description: 'Show Marina Views property to potential buyers'
    },
    {
      id: 3,
      title: 'Market Research - Palm Jumeirah',
      time: '02:00 PM',
      type: 'research',
      priority: 'low',
      status: 'pending',
      description: 'Research recent sales and market trends in Palm Jumeirah'
    },
    {
      id: 4,
      title: 'Document Preparation - Sheikh Zayed Road',
      time: '04:30 PM',
      type: 'admin',
      priority: 'high',
      status: 'pending',
      description: 'Prepare contracts and documents for Sheikh Zayed Road property'
    }
  ];

  const getPriorityIcon = (priority) => {
    switch (priority) {
      case 'high':
        return <PriorityHighIcon color="error" />;
      case 'medium':
        return <PriorityHighIcon color="warning" />;
      case 'low':
        return <PriorityLowIcon color="action" />;
      default:
        return <PriorityLowIcon color="action" />;
    }
  };

  const getPriorityColor = (priority) => {
    switch (priority) {
      case 'high':
        return 'error';
      case 'medium':
        return 'warning';
      case 'low':
        return 'default';
      default:
        return 'default';
    }
  };

  const getTypeColor = (type) => {
    switch (type) {
      case 'meeting':
        return 'primary';
      case 'viewing':
        return 'success';
      case 'research':
        return 'info';
      case 'admin':
        return 'secondary';
      default:
        return 'default';
    }
  };

  const handleRefresh = () => {
    fetchTodaysAgenda();
  };

  const handleAddTask = () => {
    // TODO: Implement add task functionality
    console.log('Add task clicked');
  };

  if (loading) {
    return (
      <Card>
        <CardContent>
          <Box sx={{ display: 'flex', justifyContent: 'center', py: 3 }}>
            <CircularProgress />
          </Box>
        </CardContent>
      </Card>
    );
  }

  return (
    <Card sx={{ height: '100%' }}>
      <CardHeader
        title={
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
            <ScheduleIcon color="primary" />
            <Typography variant="h6">Today's Agenda</Typography>
          </Box>
        }
        action={
          <Box sx={{ display: 'flex', gap: 1 }}>
            <Tooltip title="Add Task">
              <IconButton size="small" onClick={handleAddTask}>
                <AddIcon />
              </IconButton>
            </Tooltip>
            <Tooltip title="Refresh">
              <IconButton size="small" onClick={handleRefresh}>
                <RefreshIcon />
              </IconButton>
            </Tooltip>
          </Box>
        }
        subheader={`${new Date().toLocaleDateString('en-US', { 
          weekday: 'long', 
          year: 'numeric', 
          month: 'long', 
          day: 'numeric' 
        })}`}
      />
      <CardContent sx={{ pt: 0 }}>
        {error && (
          <Alert severity="error" sx={{ mb: 2 }}>
            {error}
          </Alert>
        )}

        {agenda.length === 0 ? (
          <Box sx={{ textAlign: 'center', py: 3 }}>
            <Typography variant="body2" color="text.secondary">
              No agenda items for today
            </Typography>
          </Box>
        ) : (
          <List sx={{ p: 0 }}>
            {agenda.map((item, index) => (
              <React.Fragment key={item.id}>
                <ListItem sx={{ px: 0, py: 1 }}>
                  <ListItemIcon sx={{ minWidth: 40 }}>
                    {getPriorityIcon(item.priority)}
                  </ListItemIcon>
                  <ListItemText
                    primary={
                      <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 0.5 }}>
                        <Typography variant="subtitle2" sx={{ fontWeight: 600 }}>
                          {item.title}
                        </Typography>
                        <Chip
                          label={item.time}
                          size="small"
                          variant="outlined"
                          sx={{ fontSize: '0.7rem' }}
                        />
                      </Box>
                    }
                    secondary={
                      <Stack direction="row" spacing={1} alignItems="center">
                        <Chip
                          label={item.type}
                          size="small"
                          color={getTypeColor(item.type)}
                          sx={{ textTransform: 'capitalize', fontSize: '0.7rem' }}
                        />
                        <Chip
                          label={item.priority}
                          size="small"
                          color={getPriorityColor(item.priority)}
                          sx={{ textTransform: 'capitalize', fontSize: '0.7rem' }}
                        />
                        <Typography variant="caption" color="text.secondary">
                          {item.description}
                        </Typography>
                      </Stack>
                    }
                  />
                </ListItem>
                {index < agenda.length - 1 && <Divider />}
              </React.Fragment>
            ))}
          </List>
        )}
      </CardContent>
    </Card>
  );
};

export default TodaysAgendaPanel;
