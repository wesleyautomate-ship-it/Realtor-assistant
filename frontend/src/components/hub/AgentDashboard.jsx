import React, { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  useTheme,
  Container,
  Stack,
  Fade,
  Grow,
  Grid,
} from '@mui/material';
import { useAppContext } from '../../context/AppContext';
import { api } from '../../utils/apiClient';
import CommandBar from './CommandBar';
import MissionPanel from './MissionPanel';
import MarketSnapshot from './MarketSnapshot';
import CompliancePanel from './CompliancePanel';
import WorkflowPanel from './WorkflowPanel';

const AgentDashboard = () => {
  const theme = useTheme();
  const { currentUser } = useAppContext();
  const [tasks, setTasks] = useState([]);
  const [suggestions, setSuggestions] = useState([]);
  const [isLoading, setIsLoading] = useState(true);

  // Load dashboard data from API
  useEffect(() => {
    const loadDashboardData = async () => {
      setIsLoading(true);
      
      try {
        // Get AI suggestions from backend
        const suggestionsResponse = await api.get('/chat/suggestions');
        const aiData = suggestionsResponse.data;
        
        // Transform API data to component format
        const transformedTasks = aiData.tasks.map((task, index) => ({
          id: index + 1,
          title: task,
          description: `Task: ${task}`,
          type: 'follow_up',
          priority: 'medium',
          scheduled_time: null,
          status: 'pending'
        }));

        const transformedSuggestions = aiData.suggestions.map(suggestion => ({
          title: suggestion.title,
          description: suggestion.description
        }));

        setTasks(transformedTasks);
        setSuggestions(transformedSuggestions);
        
      } catch (error) {
        console.error('Error loading dashboard data:', error);
        // Fallback to mock data if API fails
        setTasks([
          {
            id: 1,
            title: 'Follow up with Ali Khan',
            description: 'Client interested in 3-bed villa in Dubai Marina',
            type: 'follow_up',
            priority: 'high',
            scheduled_time: '10:00 AM',
            status: 'pending'
          }
        ]);
        setSuggestions([
          {
            title: 'Send new CMA for Palm Jumeirah villa',
            description: 'Based on recent market activity, create updated analysis'
          }
        ]);
      } finally {
        setIsLoading(false);
      }
    };

    loadDashboardData();
  }, []);

  const handleSendMessage = (message) => {
    console.log('Sending message:', message);
    // TODO: Implement message sending to AI assistant
  };

  const handleTaskClick = (task) => {
    console.log('Task clicked:', task);
    // TODO: Navigate to task details or mark as completed
  };

  const handleSuggestionClick = (suggestion) => {
    console.log('Suggestion clicked:', suggestion);
    // TODO: Implement suggestion action
  };

  const handleActionClick = (action) => {
    console.log('Action clicked:', action);
    // TODO: Navigate to appropriate action page
  };

  const handleAddTask = () => {
    console.log('Add new task');
    // TODO: Open task creation modal
  };

  const commandSuggestions = [
    "Create a CMA for Dubai Marina",
    "Find properties under 2M AED",
    "Schedule a client meeting",
    "Generate market report"
  ];

  return (
    <Container maxWidth="xl" sx={{ py: 4 }}>
      <Fade in={true} timeout={500}>
        <Box>
          {/* Welcome Header */}
          <Box sx={{ textAlign: 'center', mb: 4 }}>
            <Typography variant="h4" sx={{ fontWeight: 700, mb: 1, color: 'text.primary' }}>
              Welcome back, {currentUser?.first_name || 'Agent'}!
            </Typography>
            <Typography variant="h6" color="text.secondary" sx={{ fontWeight: 400 }}>
              Your intelligent real estate command center
            </Typography>
          </Box>

          {/* AI Command Center */}
          <Grow in={true} timeout={700}>
            <Box sx={{ mb: 4 }}>
              <CommandBar
                onSendMessage={handleSendMessage}
                suggestions={commandSuggestions}
                placeholder="Ask me to generate a CMA, compare properties, or analyze compliance..."
              />
            </Box>
          </Grow>

          {/* Main Dashboard Grid */}
          <Grid container spacing={3}>
            {/* Left Column - Mission & Workflow */}
            <Grid item xs={12} lg={6}>
              <Stack spacing={3}>
                {/* Today's Mission */}
                <Grow in={true} timeout={900}>
                  <Box>
                    <MissionPanel
                      tasks={tasks}
                      suggestions={suggestions}
                      onTaskClick={handleTaskClick}
                      onSuggestionClick={handleSuggestionClick}
                      onAddTask={handleAddTask}
                    />
                  </Box>
                </Grow>

                {/* Workflow Status */}
                <Grow in={true} timeout={1100}>
                  <Box>
                    <WorkflowPanel />
                  </Box>
                </Grow>
              </Stack>
            </Grid>

            {/* Right Column - Market & Compliance */}
            <Grid item xs={12} lg={6}>
              <Stack spacing={3}>
                {/* Market Snapshot */}
                <Grow in={true} timeout={1000}>
                  <Box>
                    <MarketSnapshot />
                  </Box>
                </Grow>

                {/* Compliance Monitor */}
                <Grow in={true} timeout={1200}>
                  <Box>
                    <CompliancePanel />
                  </Box>
                </Grow>
              </Stack>
            </Grid>
          </Grid>
        </Box>
      </Fade>
    </Container>
  );
};

export default AgentDashboard;
