import React, { useState } from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  Tabs,
  Tab,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  Button,
  Chip,
  useTheme,
  Stack,
  Divider,
  IconButton,
  Tooltip,
} from '@mui/material';
import {
  Assignment as TaskIcon,
  AutoAwesome as SuggestionIcon,
  CheckCircle as CheckIcon,
  Schedule as ScheduleIcon,
  TrendingUp as TrendingIcon,
  Add as AddIcon,
  Send as SendIcon,
  CalendarToday as CalendarIcon,
  Assessment as ReportIcon,
  Phone as CallIcon,
} from '@mui/icons-material';

const MissionPanel = ({ 
  tasks = [], 
  suggestions = [], 
  onTaskClick, 
  onSuggestionClick,
  onAddTask 
}) => {
  const theme = useTheme();
  const [activeTab, setActiveTab] = useState(0);

  const handleTabChange = (event, newValue) => {
    setActiveTab(newValue);
  };

  const getTaskIcon = (type) => {
    switch (type) {
      case 'follow_up': return <CallIcon />;
      case 'viewing': return <CalendarIcon />;
      case 'cma': return <ReportIcon />;
      case 'meeting': return <ScheduleIcon />;
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

  const getSuggestionAction = (suggestion) => {
    if (suggestion.title.includes('CMA')) return 'Generate';
    if (suggestion.title.includes('follow-up')) return 'Send';
    if (suggestion.title.includes('Schedule')) return 'Schedule';
    if (suggestion.title.includes('Check')) return 'Review';
    return 'View';
  };

  const getSuggestionIcon = (suggestion) => {
    if (suggestion.title.includes('CMA')) return <ReportIcon />;
    if (suggestion.title.includes('follow-up')) return <SendIcon />;
    if (suggestion.title.includes('Schedule')) return <CalendarIcon />;
    if (suggestion.title.includes('Check')) return <TrendingIcon />;
    return <SuggestionIcon />;
  };

  return (
    <Card sx={{ borderRadius: 3, boxShadow: 3, overflow: 'hidden' }}>
      <Box sx={{ borderBottom: 1, borderColor: 'divider' }}>
        <Tabs 
          value={activeTab} 
          onChange={handleTabChange}
          sx={{
            '& .MuiTab-root': {
              textTransform: 'none',
              fontWeight: 600,
              fontSize: '1rem',
            },
          }}
        >
          <Tab 
            icon={<TaskIcon />} 
            label={`Tasks (${tasks.length})`} 
            iconPosition="start"
          />
          <Tab 
            icon={<SuggestionIcon />} 
            label={`AI Suggestions (${suggestions.length})`} 
            iconPosition="start"
          />
        </Tabs>
      </Box>

      <CardContent sx={{ p: 0 }}>
        {/* Tasks Tab */}
        {activeTab === 0 && (
          <Box sx={{ p: 3 }}>
            {tasks.length === 0 ? (
              <Box sx={{ textAlign: 'center', py: 4 }}>
                <CheckIcon sx={{ fontSize: 64, color: 'success.main', mb: 2 }} />
                <Typography variant="h6" color="text.secondary" sx={{ mb: 1 }}>
                  All caught up!
                </Typography>
                <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                  No tasks for today. Ready to tackle new challenges?
                </Typography>
                <Button
                  variant="outlined"
                  startIcon={<AddIcon />}
                  onClick={onAddTask}
                  sx={{ borderRadius: 2 }}
                >
                  Add New Task
                </Button>
              </Box>
            ) : (
              <List>
                {tasks.map((task, index) => (
                  <React.Fragment key={index}>
                    <ListItem
                      sx={{
                        borderRadius: 2,
                        mb: 1,
                        border: '1px solid',
                        borderColor: 'divider',
                        '&:hover': {
                          backgroundColor: 'action.hover',
                          borderColor: 'primary.main',
                        },
                      }}
                    >
                      <ListItemIcon sx={{ minWidth: 48 }}>
                        <Box
                          sx={{
                            p: 1,
                            borderRadius: 2,
                            backgroundColor: 'primary.light',
                            color: 'primary.contrastText',
                          }}
                        >
                          {getTaskIcon(task.type)}
                        </Box>
                      </ListItemIcon>
                      <ListItemText
                        primary={
                          <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 0.5 }}>
                            <Typography variant="subtitle1" sx={{ fontWeight: 600 }}>
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
                            <Typography variant="body2" color="text.secondary" sx={{ mb: 0.5 }}>
                              {task.description}
                            </Typography>
                            {task.scheduled_time && (
                              <Typography variant="caption" color="text.secondary">
                                📅 {task.scheduled_time}
                              </Typography>
                            )}
                          </Box>
                        }
                      />
                      <Button
                        variant="contained"
                        size="small"
                        onClick={() => onTaskClick?.(task)}
                        sx={{ borderRadius: 2, textTransform: 'none' }}
                      >
                        Complete
                      </Button>
                    </ListItem>
                    {index < tasks.length - 1 && <Divider sx={{ my: 1 }} />}
                  </React.Fragment>
                ))}
              </List>
            )}
          </Box>
        )}

        {/* AI Suggestions Tab */}
        {activeTab === 1 && (
          <Box sx={{ p: 3 }}>
            {suggestions.length === 0 ? (
              <Box sx={{ textAlign: 'center', py: 4 }}>
                <SuggestionIcon sx={{ fontSize: 64, color: 'primary.main', mb: 2 }} />
                <Typography variant="h6" color="text.secondary" sx={{ mb: 1 }}>
                  No suggestions yet
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Start a conversation to get personalized AI recommendations!
                </Typography>
              </Box>
            ) : (
              <List>
                {suggestions.map((suggestion, index) => (
                  <React.Fragment key={index}>
                    <ListItem
                      sx={{
                        borderRadius: 2,
                        mb: 1,
                        border: '1px solid',
                        borderColor: 'divider',
                        backgroundColor: 'primary.light',
                        '&:hover': {
                          backgroundColor: 'primary.main',
                          color: 'primary.contrastText',
                          '& .MuiTypography-root': {
                            color: 'primary.contrastText',
                          },
                        },
                      }}
                    >
                      <ListItemIcon sx={{ minWidth: 48 }}>
                        <Box
                          sx={{
                            p: 1,
                            borderRadius: 2,
                            backgroundColor: 'background.paper',
                            color: 'primary.main',
                          }}
                        >
                          {getSuggestionIcon(suggestion)}
                        </Box>
                      </ListItemIcon>
                      <ListItemText
                        primary={
                          <Typography variant="subtitle1" sx={{ fontWeight: 600, mb: 0.5 }}>
                            ✨ {suggestion.title}
                          </Typography>
                        }
                        secondary={
                          <Typography variant="body2" color="text.secondary">
                            {suggestion.description}
                          </Typography>
                        }
                      />
                      <Button
                        variant="contained"
                        size="small"
                        onClick={() => onSuggestionClick?.(suggestion)}
                        sx={{ 
                          borderRadius: 2, 
                          textTransform: 'none',
                          backgroundColor: 'background.paper',
                          color: 'primary.main',
                          '&:hover': {
                            backgroundColor: 'background.paper',
                            opacity: 0.9,
                          },
                        }}
                      >
                        {getSuggestionAction(suggestion)}
                      </Button>
                    </ListItem>
                    {index < suggestions.length - 1 && <Divider sx={{ my: 1 }} />}
                  </React.Fragment>
                ))}
              </List>
            )}
          </Box>
        )}
      </CardContent>
    </Card>
  );
};

export default MissionPanel;
