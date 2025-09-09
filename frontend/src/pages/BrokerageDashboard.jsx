import React, { useState, useEffect } from 'react';
import {
  Box,
  Grid,
  Card,
  CardContent,
  Typography,
  Button,
  Chip,
  LinearProgress,
  Avatar,
  List,
  ListItem,
  ListItemText,
  ListItemAvatar,
  IconButton,
  Paper,
  Divider,
  Alert,
  CircularProgress
} from '@mui/material';
import {
  Business as BusinessIcon,
  People as PeopleIcon,
  TrendingUp as TrendingUpIcon,
  Assessment as AssessmentIcon,
  Add as AddIcon,
  MoreVert as MoreVertIcon,
  CheckCircle as CheckCircleIcon,
  Warning as WarningIcon,
  Error as ErrorIcon
} from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';

const BrokerageDashboard = () => {
  const navigate = useNavigate();
  const [dashboardData, setDashboardData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    try {
      setLoading(true);
      // This would be replaced with actual API call
      // const response = await fetch('/api/brokerage/dashboard');
      // const data = await response.json();
      
      // Mock data for now
      const mockData = {
        brokerage: {
          id: 1,
          name: "Dubai Elite Properties",
          license_number: "RERA-001",
          total_agents: 12,
          active_agents: 10,
          total_properties: 156,
          active_listings: 89
        },
        team_overview: {
          total_members: 12,
          active_agents: 10,
          average_consistency_score: 87.5
        },
        performance_summary: {
          average_consistency_score: 87.5,
          performance_metrics_count: 45,
          agent_consistency_scores: [85, 90, 88, 92, 87, 89, 91, 86, 88, 90]
        },
        analytics: {
          team_size: 12,
          knowledge_base_items: 24,
          active_workflows: 8,
          nurturing_sequences: 5,
          compliance_rules: 12
        },
        recent_activity: [
          {
            id: 1,
            type: 'agent_joined',
            message: 'Sarah Ahmed joined the team',
            timestamp: '2024-12-15T10:30:00Z',
            icon: 'person_add'
          },
          {
            id: 2,
            type: 'property_listed',
            message: 'New property listed in Downtown Dubai',
            timestamp: '2024-12-15T09:15:00Z',
            icon: 'home'
          },
          {
            id: 3,
            type: 'compliance_check',
            message: 'Monthly compliance check completed',
            timestamp: '2024-12-15T08:45:00Z',
            icon: 'verified'
          }
        ],
        alerts: [
          {
            id: 1,
            type: 'warning',
            message: '3 agents have pending compliance training',
            severity: 'medium'
          },
          {
            id: 2,
            type: 'info',
            message: 'New RERA regulations available for review',
            severity: 'low'
          }
        ]
      };
      
      setDashboardData(mockData);
    } catch (err) {
      setError('Failed to load dashboard data');
      console.error('Error fetching dashboard data:', err);
    } finally {
      setLoading(false);
    }
  };

  const getAlertIcon = (type) => {
    switch (type) {
      case 'warning':
        return <WarningIcon color="warning" />;
      case 'error':
        return <ErrorIcon color="error" />;
      default:
        return <CheckCircleIcon color="success" />;
    }
  };

  const getAlertColor = (severity) => {
    switch (severity) {
      case 'high':
        return 'error';
      case 'medium':
        return 'warning';
      default:
        return 'info';
    }
  };

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="400px">
        <CircularProgress />
      </Box>
    );
  }

  if (error) {
    return (
      <Box p={3}>
        <Alert severity="error">{error}</Alert>
      </Box>
    );
  }

  if (!dashboardData) {
    return (
      <Box p={3}>
        <Alert severity="info">No dashboard data available</Alert>
      </Box>
    );
  }

  return (
    <Box p={3}>
      {/* Header */}
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
        <Box>
          <Typography variant="h4" component="h1" gutterBottom>
            Brokerage Dashboard
          </Typography>
          <Typography variant="subtitle1" color="text.secondary">
            {dashboardData.brokerage.name} - {dashboardData.brokerage.license_number}
          </Typography>
        </Box>
        <Button
          variant="contained"
          startIcon={<AddIcon />}
          onClick={() => navigate('/team/management')}
        >
          Manage Team
        </Button>
      </Box>

      {/* Alerts */}
      {dashboardData.alerts && dashboardData.alerts.length > 0 && (
        <Box mb={3}>
          {dashboardData.alerts.map((alert) => (
            <Alert
              key={alert.id}
              severity={getAlertColor(alert.severity)}
              sx={{ mb: 1 }}
            >
              {alert.message}
            </Alert>
          ))}
        </Box>
      )}

      {/* Key Metrics */}
      <Grid container spacing={3} mb={3}>
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Box display="flex" alignItems="center" mb={2}>
                <Avatar sx={{ bgcolor: 'primary.main', mr: 2 }}>
                  <PeopleIcon />
                </Avatar>
                <Box>
                  <Typography variant="h6">
                    {dashboardData.team_overview.total_members}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    Team Members
                  </Typography>
                </Box>
              </Box>
              <Typography variant="body2" color="text.secondary">
                {dashboardData.team_overview.active_agents} active agents
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Box display="flex" alignItems="center" mb={2}>
                <Avatar sx={{ bgcolor: 'success.main', mr: 2 }}>
                  <TrendingUpIcon />
                </Avatar>
                <Box>
                  <Typography variant="h6">
                    {dashboardData.team_overview.average_consistency_score}%
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    Consistency Score
                  </Typography>
                </Box>
              </Box>
              <LinearProgress
                variant="determinate"
                value={dashboardData.team_overview.average_consistency_score}
                sx={{ mt: 1 }}
              />
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Box display="flex" alignItems="center" mb={2}>
                <Avatar sx={{ bgcolor: 'info.main', mr: 2 }}>
                  <BusinessIcon />
                </Avatar>
                <Box>
                  <Typography variant="h6">
                    {dashboardData.analytics.active_workflows}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    Active Workflows
                  </Typography>
                </Box>
              </Box>
              <Typography variant="body2" color="text.secondary">
                {dashboardData.analytics.nurturing_sequences} nurturing sequences
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Box display="flex" alignItems="center" mb={2}>
                <Avatar sx={{ bgcolor: 'warning.main', mr: 2 }}>
                  <AssessmentIcon />
                </Avatar>
                <Box>
                  <Typography variant="h6">
                    {dashboardData.analytics.compliance_rules}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    Compliance Rules
                  </Typography>
                </Box>
              </Box>
              <Typography variant="body2" color="text.secondary">
                {dashboardData.analytics.knowledge_base_items} knowledge items
              </Typography>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Main Content */}
      <Grid container spacing={3}>
        {/* Team Performance */}
        <Grid item xs={12} md={8}>
          <Card>
            <CardContent>
              <Box display="flex" justifyContent="space-between" alignItems="center" mb={2}>
                <Typography variant="h6">Team Performance</Typography>
                <IconButton>
                  <MoreVertIcon />
                </IconButton>
              </Box>
              
              <Box mb={3}>
                <Typography variant="body2" color="text.secondary" gutterBottom>
                  Average Consistency Score
                </Typography>
                <Box display="flex" alignItems="center">
                  <LinearProgress
                    variant="determinate"
                    value={dashboardData.performance_summary.average_consistency_score}
                    sx={{ flexGrow: 1, mr: 2 }}
                  />
                  <Typography variant="h6">
                    {dashboardData.performance_summary.average_consistency_score}%
                  </Typography>
                </Box>
              </Box>

              <Divider sx={{ my: 2 }} />

              <Typography variant="body2" color="text.secondary" gutterBottom>
                Individual Agent Scores
              </Typography>
              <Grid container spacing={2}>
                {dashboardData.performance_summary.agent_consistency_scores.map((score, index) => (
                  <Grid item xs={6} sm={4} md={3} key={index}>
                    <Paper sx={{ p: 2, textAlign: 'center' }}>
                      <Typography variant="h6">{score}%</Typography>
                      <Typography variant="caption" color="text.secondary">
                        Agent {index + 1}
                      </Typography>
                    </Paper>
                  </Grid>
                ))}
              </Grid>
            </CardContent>
          </Card>
        </Grid>

        {/* Recent Activity */}
        <Grid item xs={12} md={4}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Recent Activity
              </Typography>
              <List>
                {dashboardData.recent_activity.map((activity) => (
                  <ListItem key={activity.id} divider>
                    <ListItemAvatar>
                      <Avatar sx={{ bgcolor: 'primary.light' }}>
                        {activity.icon === 'person_add' && <PeopleIcon />}
                        {activity.icon === 'home' && <BusinessIcon />}
                        {activity.icon === 'verified' && <CheckCircleIcon />}
                      </Avatar>
                    </ListItemAvatar>
                    <ListItemText
                      primary={activity.message}
                      secondary={new Date(activity.timestamp).toLocaleDateString()}
                    />
                  </ListItem>
                ))}
              </List>
            </CardContent>
          </Card>
        </Grid>

        {/* Quick Actions */}
        <Grid item xs={12}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Quick Actions
              </Typography>
              <Grid container spacing={2}>
                <Grid item xs={12} sm={6} md={3}>
                  <Button
                    variant="outlined"
                    fullWidth
                    startIcon={<PeopleIcon />}
                    onClick={() => navigate('/team/management')}
                  >
                    Manage Team
                  </Button>
                </Grid>
                <Grid item xs={12} sm={6} md={3}>
                  <Button
                    variant="outlined"
                    fullWidth
                    startIcon={<AssessmentIcon />}
                    onClick={() => navigate('/compliance/monitoring')}
                  >
                    Compliance Check
                  </Button>
                </Grid>
                <Grid item xs={12} sm={6} md={3}>
                  <Button
                    variant="outlined"
                    fullWidth
                    startIcon={<BusinessIcon />}
                    onClick={() => navigate('/workflow/automation')}
                  >
                    Workflow Setup
                  </Button>
                </Grid>
                <Grid item xs={12} sm={6} md={3}>
                  <Button
                    variant="outlined"
                    fullWidth
                    startIcon={<TrendingUpIcon />}
                    onClick={() => navigate('/analytics/team')}
                  >
                    View Analytics
                  </Button>
                </Grid>
              </Grid>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  );
};

export default BrokerageDashboard;
