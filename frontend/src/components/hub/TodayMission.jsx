import React from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  Chip,
  IconButton,
  useTheme,
  Stack,
  Divider,
} from '@mui/material';
import {
  Assignment as TaskIcon,
  Lightbulb as SuggestionIcon,
  Add as AddIcon,
  CheckCircle as CheckIcon,
  Schedule as ScheduleIcon,
  TrendingUp as TrendingIcon,
} from '@mui/icons-material';

const TodayMission = ({ 
  tasks = [], 
  suggestions = [], 
  onTaskClick, 
  onSuggestionClick,
  onAddTask 
}) => {
  const theme = useTheme();

  const getTaskIcon = (type) => {
    switch (type) {
      case 'follow_up': return <ScheduleIcon />;
      case 'viewing': return <CheckIcon />;
      case 'cma': return <TrendingIcon />;
      default: return <TaskIcon />;
    }
  };

  const getTaskColor = (priority) => {
    switch (priority) {
      case 'high': return 'error';
      case 'medium': return 'warning';
      case 'low': return 'success';
      default: return 'default';
    }
  };

  return (
    <Box sx={{ width: '100%' }}>
      {/* Today's Tasks */}
      <Card sx={{ mb: 3, borderRadius: 2, boxShadow: 2 }}>
        <CardContent>
          <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', mb: 2 }}>
            <Typography variant="h6" sx={{ fontWeight: 600, display: 'flex', alignItems: 'center', gap: 1 }}>
              <TaskIcon color="primary" />
              Today's Tasks
            </Typography>
            <IconButton onClick={onAddTask} size="small" color="primary">
              <AddIcon />
            </IconButton>
          </Box>

          {tasks.length === 0 ? (
            <Box sx={{ textAlign: 'center', py: 3 }}>
              <CheckIcon sx={{ fontSize: 48, color: 'success.main', mb: 1 }} />
              <Typography variant="body1" color="text.secondary">
                All caught up! No tasks for today.
              </Typography>
              <Typography variant="body2" color="text.secondary" sx={{ mt: 0.5 }}>
                Ready to tackle new challenges?
              </Typography>
            </Box>
          ) : (
            <List dense>
              {tasks.map((task, index) => (
                <ListItem
                  key={index}
                  button
                  onClick={() => onTaskClick?.(task)}
                  sx={{
                    borderRadius: 1,
                    mb: 0.5,
                    '&:hover': {
                      backgroundColor: 'action.hover',
                    },
                  }}
                >
                  <ListItemIcon sx={{ minWidth: 40 }}>
                    {getTaskIcon(task.type)}
                  </ListItemIcon>
                  <ListItemText
                    primary={
                      <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                        <Typography variant="body1" sx={{ fontWeight: 500 }}>
                          {task.title}
                        </Typography>
                        <Chip
                          label={task.priority}
                          size="small"
                          color={getTaskColor(task.priority)}
                          sx={{ textTransform: 'capitalize' }}
                        />
                      </Box>
                    }
                    secondary={
                      <Box>
                        <Typography variant="body2" color="text.secondary">
                          {task.description}
                        </Typography>
                        {task.scheduled_time && (
                          <Typography variant="caption" color="text.secondary">
                            Scheduled: {task.scheduled_time}
                          </Typography>
                        )}
                      </Box>
                    }
                  />
                </ListItem>
              ))}
            </List>
          )}
        </CardContent>
      </Card>

      {/* AI Suggestions */}
      <Card sx={{ borderRadius: 2, boxShadow: 2 }}>
        <CardContent>
          <Typography variant="h6" sx={{ fontWeight: 600, display: 'flex', alignItems: 'center', gap: 1, mb: 2 }}>
            <SuggestionIcon color="primary" />
            AI Suggestions
          </Typography>

          {suggestions.length === 0 ? (
            <Box sx={{ textAlign: 'center', py: 2 }}>
              <SuggestionIcon sx={{ fontSize: 32, color: 'text.secondary', mb: 1 }} />
              <Typography variant="body2" color="text.secondary">
                No suggestions at the moment. Start a conversation to get personalized recommendations!
              </Typography>
            </Box>
          ) : (
            <List dense>
              {suggestions.map((suggestion, index) => (
                <React.Fragment key={index}>
                  <ListItem
                    button
                    onClick={() => onSuggestionClick?.(suggestion)}
                    sx={{
                      borderRadius: 1,
                      mb: 0.5,
                      '&:hover': {
                        backgroundColor: 'primary.light',
                        color: 'primary.contrastText',
                      },
                    }}
                  >
                    <ListItemIcon sx={{ minWidth: 40 }}>
                      <SuggestionIcon />
                    </ListItemIcon>
                    <ListItemText
                      primary={
                        <Typography variant="body1" sx={{ fontWeight: 500 }}>
                          {suggestion.title}
                        </Typography>
                      }
                      secondary={
                        <Typography variant="body2" color="text.secondary">
                          {suggestion.description}
                        </Typography>
                      }
                    />
                  </ListItem>
                  {index < suggestions.length - 1 && <Divider />}
                </React.Fragment>
              ))}
            </List>
          )}
        </CardContent>
      </Card>
    </Box>
  );
};

export default TodayMission;
