import React, { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Alert,
  Button,
  Chip,
  LinearProgress,
  Card,
  CardContent,
  Grid,
  IconButton,
  Collapse,
  useTheme,
  Fade,
  Grow,
  Tabs,
  Tab,
  List,
  ListItem,
  ListItemText,
  ListItemIcon,
  Divider,
  Badge,
  Tooltip,
} from '@mui/material';
import {
  TrendingUp as TrendingUpIcon,
  TrendingDown as TrendingDownIcon,
  Notifications as NotificationsIcon,
  ExpandMore as ExpandMoreIcon,
  ExpandLess as ExpandLessIcon,
  Refresh as RefreshIcon,
  Lightbulb as LightbulbIcon,
  Assessment as AssessmentIcon,
  Person as PersonIcon,
  Home as HomeIcon,
  Report as ReportIcon,
  Analytics as AnalyticsIcon,
  AutoAwesome as AutoAwesomeIcon,
  Schedule as ScheduleIcon,
  PriorityHigh as PriorityHighIcon,
  CheckCircle as CheckCircleIcon,
  Warning as WarningIcon,
  Info as InfoIcon,
  Psychology as PsychologyIcon,
} from '@mui/icons-material';

// Phase 4B API integration
import { useAuth } from '../../context/AuthContext';
import { apiClient } from '../../utils/apiClient';
import AdvancedMLPanel from './AdvancedMLPanel';

const AIInsightsPanel = () => {
  const theme = useTheme();
  const { user } = useAuth();
  const [expanded, setExpanded] = useState(true);
  const [loading, setLoading] = useState(false);
  const [activeTab, setActiveTab] = useState(0);
  const [insights, setInsights] = useState([]);
  const [marketAlerts, setMarketAlerts] = useState([]);
  const [opportunities, setOpportunities] = useState([]);
  const [automatedReports, setAutomatedReports] = useState([]);
  const [smartNotifications, setSmartNotifications] = useState([]);
  const [performanceMetrics, setPerformanceMetrics] = useState(null);
  const [lastRefresh, setLastRefresh] = useState(null);

  // Tab configuration for Phase 4B features
  const tabs = [
    { label: 'AI Insights', icon: LightbulbIcon, value: 0 },
    { label: 'Smart Reports', icon: ReportIcon, value: 1 },
    { label: 'Live Alerts', icon: NotificationsIcon, value: 2 },
    { label: 'Performance', icon: AnalyticsIcon, value: 3 },
    { label: 'Advanced ML', icon: PsychologyIcon, value: 4 },
  ];

  useEffect(() => {
    if (user) {
      loadPhase4BData();
    }
  }, [user]);

  const loadPhase4BData = async () => {
    setLoading(true);
    try {
      // Load all Phase 4B data in parallel
      const [
        insightsData,
        reportsData,
        notificationsData,
        metricsData
      ] = await Promise.all([
        loadAIInsights(),
        loadAutomatedReports(),
        loadSmartNotifications(),
        loadPerformanceMetrics()
      ]);

      setInsights(insightsData);
      setAutomatedReports(reportsData);
      setSmartNotifications(notificationsData);
      setPerformanceMetrics(metricsData);
      setLastRefresh(new Date());
    } catch (error) {
      console.error('Failed to load Phase 4B data:', error);
    } finally {
      setLoading(false);
    }
  };

  const loadAIInsights = async () => {
    try {
      // Load market alerts and opportunities
      const [alerts, opps] = await Promise.all([
        apiClient.get('/ml/notifications/market-alerts'),
        apiClient.get('/ml/notifications/opportunities')
      ]);
      
      setMarketAlerts(alerts.data || []);
      setOpportunities(opps.data || []);
      
      // Combine into insights
      return [
        ...(alerts.data || []).map(alert => ({
          id: alert.id,
          type: 'market_alert',
          priority: alert.priority || 'medium',
          icon: TrendingUpIcon,
          title: `Market Alert: ${alert.location}`,
          message: alert.message || `${alert.count} new opportunities`,
          action: 'View Details',
          color: 'info',
          timestamp: formatTimestamp(alert.created_at),
          data: alert
        })),
        ...(opps.data || []).map(opp => ({
          id: opp.id,
          type: 'opportunity',
          priority: opp.priority || 'medium',
          icon: LightbulbIcon,
          title: opp.title,
          message: opp.description,
          action: 'Take Action',
          color: 'success',
          timestamp: formatTimestamp(opp.created_at),
          data: opp
        }))
      ];
    } catch (error) {
      console.error('Failed to load AI insights:', error);
      return [];
    }
  };

  const loadAutomatedReports = async () => {
    try {
      const response = await apiClient.get('/ml/reports/history?limit=10');
      return response.data || [];
    } catch (error) {
      console.error('Failed to load automated reports:', error);
      return [];
    }
  };

  const loadSmartNotifications = async () => {
    try {
      const response = await apiClient.get(`/ml/notifications/user/${user?.id}?status=active&limit=20`);
      return response.data || [];
    } catch (error) {
      console.error('Failed to load smart notifications:', error);
      return [];
    }
  };

  const loadPerformanceMetrics = async () => {
    try {
      const response = await apiClient.get(`/ml/analytics/agent-performance/${user?.id}?period=monthly&include_comparison=true`);
      return response.data;
    } catch (error) {
      console.error('Failed to load performance metrics:', error);
      return null;
    }
  };

  const generateAutomatedReport = async (reportType, location, propertyType) => {
    setLoading(true);
    try {
      const response = await apiClient.post('/ml/reports/generate', {
        report_type: reportType,
        location: location,
        property_type: propertyType,
        include_analysis: true,
        include_recommendations: true
      });
      
      // Refresh reports after generation
      await loadAutomatedReports();
      
      return response.data;
    } catch (error) {
      console.error('Failed to generate report:', error);
      throw error;
    } finally {
      setLoading(false);
    }
  };

  const handleRefresh = async () => {
    await loadPhase4BData();
  };

  const handleActionClick = async (insight) => {
    try {
      switch (insight.type) {
        case 'market_alert':
          // Navigate to market analysis
          console.log('Navigating to market analysis for:', insight.data.location);
          break;
        case 'opportunity':
          // Handle opportunity action
          console.log('Handling opportunity:', insight.title);
          break;
        default:
          console.log('Action clicked:', insight.action, 'for insight:', insight.title);
      }
    } catch (error) {
      console.error('Failed to handle action:', error);
    }
  };

  const formatTimestamp = (timestamp) => {
    if (!timestamp) return 'Unknown';
    const date = new Date(timestamp);
    const now = new Date();
    const diffMs = now - date;
    const diffMins = Math.floor(diffMs / 60000);
    
    if (diffMins < 1) return 'Just now';
    if (diffMins < 60) return `${diffMins} minutes ago`;
    if (diffMins < 1440) return `${Math.floor(diffMins / 60)} hours ago`;
    return `${Math.floor(diffMins / 1440)} days ago`;
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
        return <PriorityHighIcon color="error" />;
      case 'medium':
        return <WarningIcon color="warning" />;
      case 'low':
        return <CheckCircleIcon color="success" />;
      default:
        return <InfoIcon color="info" />;
    }
  };

  const renderAIInsights = () => (
    <Box sx={{ mb: 3 }}>
      <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', mb: 2 }}>
        <Typography variant="h6" sx={{ fontWeight: 600, display: 'flex', alignItems: 'center' }}>
          <LightbulbIcon sx={{ mr: 1, color: 'primary.main' }} />
          AI-Powered Insights
        </Typography>
        <IconButton
          size="small"
          onClick={handleRefresh}
          disabled={loading}
          sx={{ color: 'primary.main' }}
        >
          <RefreshIcon />
        </IconButton>
      </Box>

      {loading && (
        <Box sx={{ mb: 2 }}>
          <LinearProgress />
        </Box>
      )}

      {insights.length === 0 ? (
        <Alert severity="info">
          No AI insights available. Click refresh to load the latest data.
        </Alert>
      ) : (
        <Grid container spacing={2}>
          {insights.map((insight) => (
            <Grid item xs={12} key={insight.id}>
              <Card 
                sx={{ 
                  borderLeft: `4px solid ${theme.palette[insight.color].main}`,
                  '&:hover': { boxShadow: 2 }
                }}
              >
                <CardContent sx={{ py: 2, '&:last-child': { pb: 2 } }}>
                  <Box sx={{ display: 'flex', alignItems: 'flex-start', justifyContent: 'space-between' }}>
                    <Box sx={{ display: 'flex', alignItems: 'flex-start', flex: 1 }}>
                      <Box sx={{ mr: 2, mt: 0.5 }}>
                        {getPriorityIcon(insight.priority)}
                      </Box>
                      <Box sx={{ flex: 1 }}>
                        <Typography variant="subtitle2" sx={{ fontWeight: 600, mb: 0.5 }}>
                          {insight.title}
                        </Typography>
                        <Typography variant="body2" color="text.secondary" sx={{ mb: 1 }}>
                          {insight.message}
                        </Typography>
                        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                          <Chip 
                            label={insight.priority} 
                            size="small" 
                            color={getPriorityColor(insight.priority)}
                            variant="outlined"
                          />
                          <Typography variant="caption" color="text.secondary">
                            {insight.timestamp}
                          </Typography>
                        </Box>
                      </Box>
                    </Box>
                    <Button
                      size="small"
                      variant="outlined"
                      onClick={() => handleActionClick(insight)}
                      sx={{ ml: 2 }}
                    >
                      {insight.action}
                    </Button>
                  </Box>
                </CardContent>
              </Card>
            </Grid>
          ))}
        </Grid>
      )}
    </Box>
  );

  const renderSmartReports = () => (
    <Box sx={{ mb: 3 }}>
      <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', mb: 2 }}>
        <Typography variant="h6" sx={{ fontWeight: 600, display: 'flex', alignItems: 'center' }}>
          <ReportIcon sx={{ mr: 1, color: 'primary.main' }} />
          Automated Reports
        </Typography>
        <Button
          size="small"
          variant="contained"
          startIcon={<AutoAwesomeIcon />}
          onClick={() => generateAutomatedReport('market_analysis', 'Dubai', 'apartments')}
          disabled={loading}
        >
          Generate Report
        </Button>
      </Box>

      {automatedReports.length === 0 ? (
        <Alert severity="info">
          No automated reports available. Generate your first report to get started.
        </Alert>
      ) : (
        <List>
          {automatedReports.map((report, index) => (
            <React.Fragment key={report.id || index}>
              <ListItem sx={{ px: 0 }}>
                <ListItemIcon>
                  <AssessmentIcon color="primary" />
                </ListItemIcon>
                <ListItemText
                  primary={report.title || `${report.report_type} Report`}
                  secondary={
                    <Box>
                      <Typography variant="body2" color="text.secondary">
                        {report.description || 'AI-generated market analysis'}
                      </Typography>
                      <Box sx={{ display: 'flex', gap: 1, mt: 1 }}>
                        <Chip label={report.report_type} size="small" variant="outlined" />
                        <Chip label={formatTimestamp(report.generated_at)} size="small" variant="outlined" />
                      </Box>
                    </Box>
                  }
                />
                <Button size="small" variant="outlined">
                  View
                </Button>
              </ListItem>
              {index < automatedReports.length - 1 && <Divider />}
            </React.Fragment>
          ))}
        </List>
      )}
    </Box>
  );

  const renderLiveAlerts = () => (
    <Box sx={{ mb: 3 }}>
      <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', mb: 2 }}>
        <Typography variant="h6" sx={{ fontWeight: 600, display: 'flex', alignItems: 'center' }}>
          <NotificationsIcon sx={{ mr: 1, color: 'primary.main' }} />
          Live Smart Alerts
                          <Badge badgeContent={smartNotifications.length} color="error" sx={{ ml: 1 }}>
                            <NotificationsIcon />
                          </Badge>
        </Typography>
      </Box>

      {smartNotifications.length === 0 ? (
        <Alert severity="info">
          No active notifications. You're all caught up!
        </Alert>
      ) : (
        <List>
          {smartNotifications.map((notification, index) => (
            <React.Fragment key={notification.id || index}>
              <ListItem sx={{ px: 0 }}>
                <ListItemIcon>
                  {getPriorityIcon(notification.priority)}
                </ListItemIcon>
                <ListItemText
                  primary={notification.title}
                  secondary={
                    <Box>
                      <Typography variant="body2" color="text.secondary">
                        {notification.message}
                      </Typography>
                      <Box sx={{ display: 'flex', gap: 1, mt: 1 }}>
                        <Chip label={notification.notification_type} size="small" variant="outlined" />
                        <Chip label={formatTimestamp(notification.created_at)} size="small" variant="outlined" />
                      </Box>
                    </Box>
                  }
                />
                <Button size="small" variant="outlined">
                  Dismiss
                </Button>
              </ListItem>
              {index < smartNotifications.length - 1 && <Divider />}
            </React.Fragment>
          ))}
        </List>
      )}
    </Box>
  );

  const renderPerformance = () => (
    <Box sx={{ mb: 3 }}>
      <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', mb: 2 }}>
        <Typography variant="h6" sx={{ fontWeight: 600, display: 'flex', alignItems: 'center' }}>
          <AnalyticsIcon sx={{ mr: 1, color: 'primary.main' }} />
          Performance Analytics
        </Typography>
      </Box>

      {!performanceMetrics ? (
        <Alert severity="info">
          Loading performance metrics...
        </Alert>
      ) : (
        <Grid container spacing={2}>
          <Grid item xs={12} md={6}>
            <Card>
              <CardContent>
                <Typography variant="subtitle2" color="text.secondary" gutterBottom>
                  Current Period Performance
                </Typography>
                <Typography variant="h4" sx={{ fontWeight: 600, color: 'primary.main' }}>
                  {performanceMetrics.performance_scores?.overall_score || 'N/A'}%
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Overall performance score
                </Typography>
              </CardContent>
            </Card>
          </Grid>
          <Grid item xs={12} md={6}>
            <Card>
              <CardContent>
                <Typography variant="subtitle2" color="text.secondary" gutterBottom>
                  Goal Progress
                </Typography>
                <Typography variant="h4" sx={{ fontWeight: 600, color: 'success.main' }}>
                  {performanceMetrics.goal_progress?.achievement_rate || 'N/A'}%
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Target achievement rate
                </Typography>
              </CardContent>
            </Card>
          </Grid>
          {performanceMetrics.recommendations && (
            <Grid item xs={12}>
              <Card>
                <CardContent>
                  <Typography variant="subtitle2" color="text.secondary" gutterBottom>
                    AI Recommendations
                  </Typography>
                  <List dense>
                    {performanceMetrics.recommendations.slice(0, 3).map((rec, index) => (
                      <ListItem key={index} sx={{ px: 0 }}>
                        <ListItemIcon>
                          <LightbulbIcon color="primary" fontSize="small" />
                        </ListItemIcon>
                        <ListItemText primary={rec} />
                      </ListItem>
                    ))}
                  </List>
                </CardContent>
              </Card>
            </Grid>
          )}
        </Grid>
      )}
    </Box>
  );

  const renderAdvancedML = () => (
    <Box>
      <AdvancedMLPanel />
    </Box>
  );

  const renderTabContent = () => {
    switch (activeTab) {
      case 0:
        return renderAIInsights();
      case 1:
        return renderSmartReports();
      case 2:
        return renderLiveAlerts();
      case 3:
        return renderPerformance();
      case 4:
        return renderAdvancedML();
      default:
        return renderAIInsights();
    }
  };

  return (
    <Card sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
      <CardContent sx={{ flex: 1, p: 0 }}>
        {/* Header */}
        <Box sx={{ 
          p: 2, 
          borderBottom: `1px solid ${theme.palette.divider}`,
          backgroundColor: theme.palette.background.default
        }}>
          <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
            <Typography variant="h6" sx={{ fontWeight: 600 }}>
              Phase 4B: AI-Powered Insights Hub
            </Typography>
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
              {lastRefresh && (
                <Typography variant="caption" color="text.secondary">
                  Last updated: {formatTimestamp(lastRefresh)}
                </Typography>
              )}
              <IconButton
                size="small"
                onClick={() => setExpanded(!expanded)}
              >
                {expanded ? <ExpandLessIcon /> : <ExpandMoreIcon />}
              </IconButton>
            </Box>
          </Box>
        </Box>

        {/* Content */}
        <Collapse in={expanded}>
          <Box sx={{ p: 2 }}>
            {/* Tabs */}
            <Box sx={{ borderBottom: 1, borderColor: 'divider', mb: 3 }}>
              <Tabs 
                value={activeTab} 
                onChange={(e, newValue) => setActiveTab(newValue)}
                variant="scrollable"
                scrollButtons="auto"
              >
                {tabs.map((tab) => (
                  <Tab
                    key={tab.value}
                    label={tab.label}
                    icon={<tab.icon />}
                    iconPosition="start"
                    sx={{ minHeight: 48 }}
                  />
                ))}
              </Tabs>
            </Box>

            {/* Tab Content */}
            <Fade in={true} timeout={300}>
              {renderTabContent()}
            </Fade>
          </Box>
        </Collapse>
      </CardContent>
    </Card>
  );
};

export default AIInsightsPanel;
