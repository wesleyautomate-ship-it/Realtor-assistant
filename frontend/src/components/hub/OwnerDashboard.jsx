import React, { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  useTheme,
  Container,
  Stack,
  Card,
  CardContent,
  Grid,
  LinearProgress,
  Chip,
  List,
  ListItem,
  ListItemText,
  ListItemAvatar,
  Avatar,
  Fade,
  Grow,
} from '@mui/material';
import {
  TrendingUp as TrendingUpIcon,
  People as PeopleIcon,
  Assessment as AssessmentIcon,
  Security as SecurityIcon,
  Star as StarIcon,
  Warning as WarningIcon,
} from '@mui/icons-material';
import { useAppContext } from '../../context/AppContext';
import { api } from '../../utils/apiClient';
import CommandBar from './CommandBar';
import MarketSnapshot from './MarketSnapshot';
import CompliancePanel from './CompliancePanel';

const OwnerDashboard = () => {
  const theme = useTheme();
  const { currentUser } = useAppContext();
  const [kpis, setKpis] = useState({});
  const [agentLeaderboard, setAgentLeaderboard] = useState([]);
  const [complianceAlerts, setComplianceAlerts] = useState([]);
  const [isLoading, setIsLoading] = useState(true);

  // Mock data for development - will be replaced with real API calls
  useEffect(() => {
    const loadDashboardData = async () => {
      setIsLoading(true);
      
      // Simulate API call
      setTimeout(() => {
        setKpis({
          agentConsistency: 87,
          leadRetention: 92,
          complianceScore: 95,
          workflowEfficiency: 78
        });

        setAgentLeaderboard([
          { name: 'Sarah Johnson', performance: 94, deals: 12, revenue: '2.4M AED' },
          { name: 'Ahmed Al-Rashid', performance: 89, deals: 8, revenue: '1.8M AED' },
          { name: 'Maria Santos', performance: 85, deals: 10, revenue: '1.6M AED' },
          { name: 'David Chen', performance: 82, deals: 6, revenue: '1.2M AED' },
        ]);

        setComplianceAlerts([
          { type: 'warning', message: '3 agents need compliance training renewal', priority: 'medium' },
          { type: 'info', message: 'Brand guidelines updated - review required', priority: 'low' },
          { type: 'success', message: 'All documentation up to date', priority: 'low' },
        ]);

        setIsLoading(false);
      }, 1000);
    };

    loadDashboardData();
  }, []);

  const handleSendMessage = (message) => {
    console.log('Sending message:', message);
    // TODO: Implement message sending to AI assistant
  };

  const getKpiColor = (value) => {
    if (value >= 90) return 'success';
    if (value >= 80) return 'warning';
    return 'error';
  };

  const getAlertColor = (type) => {
    switch (type) {
      case 'warning': return 'warning';
      case 'error': return 'error';
      case 'success': return 'success';
      default: return 'info';
    }
  };

  const commandSuggestions = [
    "Show team performance report",
    "Check compliance status",
    "Generate revenue analytics",
    "Review agent training needs"
  ];

  return (
    <Container maxWidth="xl" sx={{ py: 4 }}>
      <Fade in={true} timeout={500}>
        <Box>
          {/* Welcome Header */}
          <Box sx={{ textAlign: 'center', mb: 4 }}>
            <Typography variant="h4" sx={{ fontWeight: 700, mb: 1, color: 'text.primary' }}>
              Welcome back, {currentUser?.first_name || 'Owner'}!
            </Typography>
            <Typography variant="h6" color="text.secondary" sx={{ fontWeight: 400 }}>
              Your executive command center for team performance
            </Typography>
          </Box>

          {/* AI Command Center */}
          <Grow in={true} timeout={700}>
            <Box sx={{ mb: 4 }}>
              <CommandBar
                onSendMessage={handleSendMessage}
                suggestions={commandSuggestions}
                placeholder="What would you like to review today?"
              />
            </Box>
          </Grow>

          {/* Main Dashboard Grid */}
          <Grid container spacing={3}>
            {/* Left Column - KPIs & Team Performance */}
            <Grid item xs={12} lg={6}>
              <Stack spacing={3}>
                {/* Team Performance KPIs */}
                <Grow in={true} timeout={900}>
                  <Card sx={{ borderRadius: 3, boxShadow: 3 }}>
                    <CardContent>
                      <Typography variant="h6" sx={{ fontWeight: 600, mb: 3, display: 'flex', alignItems: 'center', gap: 1 }}>
                        <AssessmentIcon color="primary" />
                        Team Performance KPIs
                      </Typography>
                      
                      <Grid container spacing={3}>
                        <Grid item xs={12} sm={6}>
                          <Box>
                            <Typography variant="subtitle2" color="text.secondary" gutterBottom>
                              Agent Consistency Score
                            </Typography>
                            <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                              <LinearProgress
                                variant="determinate"
                                value={kpis.agentConsistency}
                                color={getKpiColor(kpis.agentConsistency)}
                                sx={{ flex: 1, height: 8, borderRadius: 4 }}
                              />
                              <Typography variant="h6" sx={{ fontWeight: 600 }}>
                                {kpis.agentConsistency}%
                              </Typography>
                            </Box>
                          </Box>
                        </Grid>
                        
                        <Grid item xs={12} sm={6}>
                          <Box>
                            <Typography variant="subtitle2" color="text.secondary" gutterBottom>
                              Lead Retention Rate
                            </Typography>
                            <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                              <LinearProgress
                                variant="determinate"
                                value={kpis.leadRetention}
                                color={getKpiColor(kpis.leadRetention)}
                                sx={{ flex: 1, height: 8, borderRadius: 4 }}
                              />
                              <Typography variant="h6" sx={{ fontWeight: 600 }}>
                                {kpis.leadRetention}%
                              </Typography>
                            </Box>
                          </Box>
                        </Grid>
                        
                        <Grid item xs={12} sm={6}>
                          <Box>
                            <Typography variant="subtitle2" color="text.secondary" gutterBottom>
                              Compliance Score
                            </Typography>
                            <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                              <LinearProgress
                                variant="determinate"
                                value={kpis.complianceScore}
                                color={getKpiColor(kpis.complianceScore)}
                                sx={{ flex: 1, height: 8, borderRadius: 4 }}
                              />
                              <Typography variant="h6" sx={{ fontWeight: 600 }}>
                                {kpis.complianceScore}%
                              </Typography>
                            </Box>
                          </Box>
                        </Grid>
                        
                        <Grid item xs={12} sm={6}>
                          <Box>
                            <Typography variant="subtitle2" color="text.secondary" gutterBottom>
                              Workflow Efficiency
                            </Typography>
                            <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                              <LinearProgress
                                variant="determinate"
                                value={kpis.workflowEfficiency}
                                color={getKpiColor(kpis.workflowEfficiency)}
                                sx={{ flex: 1, height: 8, borderRadius: 4 }}
                              />
                              <Typography variant="h6" sx={{ fontWeight: 600 }}>
                                {kpis.workflowEfficiency}%
                              </Typography>
                            </Box>
                          </Box>
                        </Grid>
                      </Grid>
                    </CardContent>
                  </Card>
                </Grow>

                {/* Agent Leaderboard */}
                <Grow in={true} timeout={1100}>
                  <Card sx={{ borderRadius: 3, boxShadow: 3 }}>
                    <CardContent>
                      <Typography variant="h6" sx={{ fontWeight: 600, mb: 3, display: 'flex', alignItems: 'center', gap: 1 }}>
                        <PeopleIcon color="primary" />
                        Agent Leaderboard
                      </Typography>
                      
                      <List>
                        {agentLeaderboard.map((agent, index) => (
                          <ListItem key={index} sx={{ px: 0 }}>
                            <ListItemAvatar>
                              <Avatar sx={{ bgcolor: 'primary.main' }}>
                                {agent.name.split(' ').map(n => n[0]).join('')}
                              </Avatar>
                            </ListItemAvatar>
                            <ListItemText
                              primary={
                                <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                                  <Typography variant="subtitle1" sx={{ fontWeight: 600 }}>
                                    {agent.name}
                                  </Typography>
                                  {index < 3 && <StarIcon sx={{ color: 'warning.main', fontSize: 16 }} />}
                                </Box>
                              }
                              secondary={
                                <Box sx={{ display: 'flex', gap: 2, mt: 0.5 }}>
                                  <Chip label={`${agent.performance}% Performance`} size="small" color="primary" />
                                  <Chip label={`${agent.deals} Deals`} size="small" variant="outlined" />
                                  <Chip label={agent.revenue} size="small" variant="outlined" />
                                </Box>
                              }
                            />
                          </ListItem>
                        ))}
                      </List>
                    </CardContent>
                  </Card>
                </Grow>
              </Stack>
            </Grid>

            {/* Right Column - Market Intelligence & Compliance */}
            <Grid item xs={12} lg={6}>
              <Stack spacing={3}>
                {/* Market Intelligence */}
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

export default OwnerDashboard;
