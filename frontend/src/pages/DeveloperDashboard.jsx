import React, { useState, useEffect } from 'react';
import {
  Box,
  Container,
  Typography,
  Card,
  CardContent,
  Grid,
  Chip,
  CircularProgress,
  Alert,
  Tabs,
  Tab,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  Button,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  IconButton,
  Tooltip,
  LinearProgress,
  Divider
} from '@mui/material';
import {
  Monitor,
  Speed,
  People,
  Warning,
  CheckCircle,
  Error,
  Info,
  Settings,
  Refresh,
  Visibility,
  TrendingUp,
  TrendingDown,
  TrendingFlat,
  Memory,
  Storage,
  NetworkCheck,
  BugReport
} from '@mui/icons-material';
import { useAppContext } from '../context/AppContext';
import { api } from '../utils/apiClient';

const DeveloperDashboard = () => {
  const { currentUser } = useAppContext();
  const [activeTab, setActiveTab] = useState(0);
  const [systemHealth, setSystemHealth] = useState(null);
  const [performanceAnalytics, setPerformanceAnalytics] = useState(null);
  const [userActivity, setUserActivity] = useState(null);
  const [multiBrokerageAnalytics, setMultiBrokerageAnalytics] = useState(null);
  const [systemAlerts, setSystemAlerts] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [alertDialog, setAlertDialog] = useState(false);
  const [newAlert, setNewAlert] = useState({
    alert_type: 'info',
    alert_category: 'system',
    alert_title: '',
    alert_message: '',
    severity: 'medium'
  });

  useEffect(() => {
    loadSystemHealth();
    loadPerformanceAnalytics();
    loadUserActivity();
    loadMultiBrokerageAnalytics();
    loadSystemAlerts();
  }, []);

  const loadSystemHealth = async () => {
    try {
      const response = await api('/api/phase3/developer/system-health');
      setSystemHealth(response);
    } catch (err) {
      console.error('Failed to load system health:', err);
    }
  };

  const loadPerformanceAnalytics = async () => {
    try {
      const response = await api('/api/phase3/developer/performance-analytics');
      setPerformanceAnalytics(response);
    } catch (err) {
      console.error('Failed to load performance analytics:', err);
    }
  };

  const loadUserActivity = async () => {
    try {
      const response = await api('/api/phase3/developer/user-activity-analytics');
      setUserActivity(response);
    } catch (err) {
      console.error('Failed to load user activity:', err);
    }
  };

  const loadMultiBrokerageAnalytics = async () => {
    try {
      const response = await api('/api/phase3/developer/multi-brokerage-analytics');
      setMultiBrokerageAnalytics(response);
    } catch (err) {
      console.error('Failed to load multi-brokerage analytics:', err);
    }
  };

  const loadSystemAlerts = async () => {
    try {
      const response = await api('/api/phase3/developer/system-alerts');
      setSystemAlerts(response);
    } catch (err) {
      console.error('Failed to load system alerts:', err);
    }
  };

  const handleCreateAlert = async () => {
    try {
      await api('/api/phase3/developer/system-alerts', {
        method: 'POST',
        body: JSON.stringify(newAlert)
      });
      setAlertDialog(false);
      setNewAlert({
        alert_type: 'info',
        alert_category: 'system',
        alert_title: '',
        alert_message: '',
        severity: 'medium'
      });
      loadSystemAlerts();
    } catch (err) {
      setError('Failed to create system alert');
    }
  };

  const handleResolveAlert = async (alertId) => {
    try {
      await api(`/api/phase3/developer/system-alerts/${alertId}/resolve`, {
        method: 'POST',
        body: JSON.stringify({ resolution_notes: 'Resolved by developer' })
      });
      loadSystemAlerts();
    } catch (err) {
      setError('Failed to resolve alert');
    }
  };

  const getHealthIcon = (status) => {
    switch (status) {
      case 'healthy':
        return <CheckCircle color="success" />;
      case 'warning':
        return <Warning color="warning" />;
      case 'critical':
        return <Error color="error" />;
      default:
        return <Info color="info" />;
    }
  };

  const getHealthColor = (status) => {
    switch (status) {
      case 'healthy':
        return 'success';
      case 'warning':
        return 'warning';
      case 'critical':
        return 'error';
      default:
        return 'info';
    }
  };

  const getTrendIcon = (trend) => {
    switch (trend) {
      case 'increasing':
        return <TrendingUp color="error" />;
      case 'decreasing':
        return <TrendingDown color="success" />;
      case 'stable':
        return <TrendingFlat color="info" />;
      default:
        return <TrendingFlat color="disabled" />;
    }
  };

  const getSeverityColor = (severity) => {
    switch (severity) {
      case 'critical':
        return 'error';
      case 'high':
        return 'warning';
      case 'medium':
        return 'info';
      case 'low':
        return 'default';
      default:
        return 'default';
    }
  };

  const formatBytes = (bytes) => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };

  return (
    <Container maxWidth="xl" sx={{ mt: 4, mb: 4 }}>
      <Box sx={{ mb: 4 }}>
        <Typography variant="h4" component="h1" gutterBottom>
          Developer Dashboard
        </Typography>
        <Typography variant="subtitle1" color="text.secondary">
          System monitoring, analytics, and control panel
        </Typography>
      </Box>

      {error && (
        <Alert severity="error" sx={{ mb: 2 }} onClose={() => setError(null)}>
          {error}
        </Alert>
      )}

      <Card sx={{ mb: 4 }}>
        <Box sx={{ borderBottom: 1, borderColor: 'divider' }}>
          <Tabs value={activeTab} onChange={(e, newValue) => setActiveTab(newValue)}>
            <Tab label="System Health" icon={<Monitor />} />
            <Tab label="Performance" icon={<Speed />} />
            <Tab label="User Activity" icon={<People />} />
            <Tab label="Multi-Brokerage" icon={<NetworkCheck />} />
            <Tab label="System Alerts" icon={<Warning />} />
          </Tabs>
        </Box>

        <CardContent>
          {activeTab === 0 && (
            <Box>
              <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
                <Typography variant="h6">System Health Overview</Typography>
                <Button
                  startIcon={<Refresh />}
                  onClick={loadSystemHealth}
                  disabled={loading}
                >
                  Refresh
                </Button>
              </Box>

              {systemHealth ? (
                <Grid container spacing={3}>
                  <Grid item xs={12} md={3}>
                    <Card>
                      <CardContent>
                        <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                          {getHealthIcon(systemHealth.overall_health)}
                          <Typography variant="h6" sx={{ ml: 1 }}>
                            Overall Health
                          </Typography>
                        </Box>
                        <Chip
                          label={systemHealth.overall_health.toUpperCase()}
                          color={getHealthColor(systemHealth.overall_health)}
                          size="small"
                        />
                        <Typography variant="h4" sx={{ mt: 1 }}>
                          {systemHealth.health_score}%
                        </Typography>
                      </CardContent>
                    </Card>
                  </Grid>

                  <Grid item xs={12} md={3}>
                    <Card>
                      <CardContent>
                        <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                          <Memory color="primary" />
                          <Typography variant="h6" sx={{ ml: 1 }}>
                            CPU Usage
                          </Typography>
                        </Box>
                        <LinearProgress
                          variant="determinate"
                          value={systemHealth.system_resources.cpu_usage_percent}
                          sx={{ mb: 1 }}
                        />
                        <Typography variant="h6">
                          {systemHealth.system_resources.cpu_usage_percent.toFixed(1)}%
                        </Typography>
                      </CardContent>
                    </Card>
                  </Grid>

                  <Grid item xs={12} md={3}>
                    <Card>
                      <CardContent>
                        <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                          <Storage color="primary" />
                          <Typography variant="h6" sx={{ ml: 1 }}>
                            Memory Usage
                          </Typography>
                        </Box>
                        <LinearProgress
                          variant="determinate"
                          value={systemHealth.system_resources.memory_usage_percent}
                          sx={{ mb: 1 }}
                        />
                        <Typography variant="h6">
                          {systemHealth.system_resources.memory_usage_percent.toFixed(1)}%
                        </Typography>
                        <Typography variant="body2" color="text.secondary">
                          {systemHealth.system_resources.available_memory_gb}GB available
                        </Typography>
                      </CardContent>
                    </Card>
                  </Grid>

                  <Grid item xs={12} md={3}>
                    <Card>
                      <CardContent>
                        <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                          <BugReport color="primary" />
                          <Typography variant="h6" sx={{ ml: 1 }}>
                            Recent Errors
                          </Typography>
                        </Box>
                        <Typography variant="h4" color={systemHealth.recent_errors_24h > 0 ? 'error' : 'success'}>
                          {systemHealth.recent_errors_24h}
                        </Typography>
                        <Typography variant="body2" color="text.secondary">
                          Last 24 hours
                        </Typography>
                      </CardContent>
                    </Card>
                  </Grid>

                  <Grid item xs={12}>
                    <Card>
                      <CardContent>
                        <Typography variant="h6" gutterBottom>
                          Service Health
                        </Typography>
                        <Grid container spacing={2}>
                          {Object.entries(systemHealth.service_health).map(([service, health]) => (
                            <Grid item xs={12} sm={4} key={service}>
                              <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                                {getHealthIcon(health.status)}
                                <Typography variant="subtitle1" sx={{ ml: 1, textTransform: 'capitalize' }}>
                                  {service}
                                </Typography>
                              </Box>
                              {health.response_time_ms && (
                                <Typography variant="body2" color="text.secondary">
                                  Response: {health.response_time_ms}ms
                                </Typography>
                              )}
                              {health.average_processing_time_ms && (
                                <Typography variant="body2" color="text.secondary">
                                  Processing: {health.average_processing_time_ms}ms
                                </Typography>
                              )}
                            </Grid>
                          ))}
                        </Grid>
                      </CardContent>
                    </Card>
                  </Grid>
                </Grid>
              ) : (
                <Box sx={{ display: 'flex', justifyContent: 'center', p: 4 }}>
                  <CircularProgress />
                </Box>
              )}
            </Box>
          )}

          {activeTab === 1 && (
            <Box>
              <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
                <Typography variant="h6">Performance Analytics</Typography>
                <Button
                  startIcon={<Refresh />}
                  onClick={loadPerformanceAnalytics}
                  disabled={loading}
                >
                  Refresh
                </Button>
              </Box>

              {performanceAnalytics ? (
                <Grid container spacing={3}>
                  {Object.entries(performanceAnalytics.analytics).map(([category, data]) => (
                    <Grid item xs={12} md={6} key={category}>
                      <Card>
                        <CardContent>
                          <Typography variant="h6" gutterBottom sx={{ textTransform: 'capitalize' }}>
                            {category.replace('_', ' ')}
                          </Typography>
                          {data.total_measurements > 0 ? (
                            <Box>
                              <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                                <Typography variant="h4">
                                  {data.average_value.toFixed(2)}
                                </Typography>
                                {getTrendIcon(data.trend)}
                              </Box>
                              <Typography variant="body2" color="text.secondary">
                                Latest: {data.latest_value.toFixed(2)} | 
                                Min: {data.min_value.toFixed(2)} | 
                                Max: {data.max_value.toFixed(2)}
                              </Typography>
                              <Typography variant="body2" color="text.secondary">
                                {data.total_measurements} measurements
                              </Typography>
                            </Box>
                          ) : (
                            <Typography variant="body2" color="text.secondary">
                              {data.message}
                            </Typography>
                          )}
                        </CardContent>
                      </Card>
                    </Grid>
                  ))}
                </Grid>
              ) : (
                <Box sx={{ display: 'flex', justifyContent: 'center', p: 4 }}>
                  <CircularProgress />
                </Box>
              )}
            </Box>
          )}

          {activeTab === 2 && (
            <Box>
              <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
                <Typography variant="h6">User Activity Analytics</Typography>
                <Button
                  startIcon={<Refresh />}
                  onClick={loadUserActivity}
                  disabled={loading}
                >
                  Refresh
                </Button>
              </Box>

              {userActivity ? (
                <Grid container spacing={3}>
                  <Grid item xs={12} md={3}>
                    <Card>
                      <CardContent>
                        <Typography variant="h6" gutterBottom>
                          Total Activities
                        </Typography>
                        <Typography variant="h4">
                          {userActivity.total_activities}
                        </Typography>
                        <Typography variant="body2" color="text.secondary">
                          {userActivity.period_days} days
                        </Typography>
                      </CardContent>
                    </Card>
                  </Grid>

                  <Grid item xs={12} md={3}>
                    <Card>
                      <CardContent>
                        <Typography variant="h6" gutterBottom>
                          Unique Users
                        </Typography>
                        <Typography variant="h4">
                          {userActivity.unique_users}
                        </Typography>
                        <Typography variant="body2" color="text.secondary">
                          Active users
                        </Typography>
                      </CardContent>
                    </Card>
                  </Grid>

                  <Grid item xs={12} md={3}>
                    <Card>
                      <CardContent>
                        <Typography variant="h6" gutterBottom>
                          Avg Activities/User
                        </Typography>
                        <Typography variant="h4">
                          {userActivity.average_activities_per_user.toFixed(1)}
                        </Typography>
                        <Typography variant="body2" color="text.secondary">
                          Per user
                        </Typography>
                      </CardContent>
                    </Card>
                  </Grid>

                  <Grid item xs={12} md={3}>
                    <Card>
                      <CardContent>
                        <Typography variant="h6" gutterBottom>
                          Device Types
                        </Typography>
                        {Object.entries(userActivity.device_breakdown).map(([device, count]) => (
                          <Box key={device} sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                            <Typography variant="body2" sx={{ textTransform: 'capitalize' }}>
                              {device}
                            </Typography>
                            <Typography variant="body2" color="text.secondary">
                              {count}
                            </Typography>
                          </Box>
                        ))}
                      </CardContent>
                    </Card>
                  </Grid>
                </Grid>
              ) : (
                <Box sx={{ display: 'flex', justifyContent: 'center', p: 4 }}>
                  <CircularProgress />
                </Box>
              )}
            </Box>
          )}

          {activeTab === 3 && (
            <Box>
              <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
                <Typography variant="h6">Multi-Brokerage Analytics</Typography>
                <Button
                  startIcon={<Refresh />}
                  onClick={loadMultiBrokerageAnalytics}
                  disabled={loading}
                >
                  Refresh
                </Button>
              </Box>

              {multiBrokerageAnalytics ? (
                <Grid container spacing={3}>
                  <Grid item xs={12} md={6}>
                    <Card>
                      <CardContent>
                        <Typography variant="h6" gutterBottom>
                          System Overview
                        </Typography>
                        <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                          <Typography variant="body2">Total Brokerages:</Typography>
                          <Typography variant="body2" color="text.secondary">
                            {multiBrokerageAnalytics.system_overview.total_brokerages}
                          </Typography>
                        </Box>
                        <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                          <Typography variant="body2">Total Users:</Typography>
                          <Typography variant="body2" color="text.secondary">
                            {multiBrokerageAnalytics.system_overview.total_users}
                          </Typography>
                        </Box>
                        <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                          <Typography variant="body2">Active Experts:</Typography>
                          <Typography variant="body2" color="text.secondary">
                            {multiBrokerageAnalytics.system_overview.active_experts}
                          </Typography>
                        </Box>
                        <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                          <Typography variant="body2">AI Requests:</Typography>
                          <Typography variant="body2" color="text.secondary">
                            {multiBrokerageAnalytics.system_overview.total_ai_requests}
                          </Typography>
                        </Box>
                        <Box sx={{ display: 'flex', justifyContent: 'space-between' }}>
                          <Typography variant="body2">Voice Requests:</Typography>
                          <Typography variant="body2" color="text.secondary">
                            {multiBrokerageAnalytics.system_overview.total_voice_requests}
                          </Typography>
                        </Box>
                      </CardContent>
                    </Card>
                  </Grid>

                  <Grid item xs={12} md={6}>
                    <Card>
                      <CardContent>
                        <Typography variant="h6" gutterBottom>
                          Feature Adoption
                        </Typography>
                        <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                          <Typography variant="body2">AI Requests/Brokerage:</Typography>
                          <Typography variant="body2" color="text.secondary">
                            {multiBrokerageAnalytics.feature_adoption.ai_requests_per_brokerage.toFixed(1)}
                          </Typography>
                        </Box>
                        <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                          <Typography variant="body2">Voice Requests/Brokerage:</Typography>
                          <Typography variant="body2" color="text.secondary">
                            {multiBrokerageAnalytics.feature_adoption.voice_requests_per_brokerage.toFixed(1)}
                          </Typography>
                        </Box>
                        <Box sx={{ display: 'flex', justifyContent: 'space-between' }}>
                          <Typography variant="body2">Experts/Brokerage:</Typography>
                          <Typography variant="body2" color="text.secondary">
                            {multiBrokerageAnalytics.feature_adoption.experts_per_brokerage.toFixed(1)}
                          </Typography>
                        </Box>
                      </CardContent>
                    </Card>
                  </Grid>
                </Grid>
              ) : (
                <Box sx={{ display: 'flex', justifyContent: 'center', p: 4 }}>
                  <CircularProgress />
                </Box>
              )}
            </Box>
          )}

          {activeTab === 4 && (
            <Box>
              <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
                <Typography variant="h6">System Alerts</Typography>
                <Box>
                  <Button
                    startIcon={<BugReport />}
                    onClick={() => setAlertDialog(true)}
                    sx={{ mr: 1 }}
                  >
                    Create Alert
                  </Button>
                  <Button
                    startIcon={<Refresh />}
                    onClick={loadSystemAlerts}
                    disabled={loading}
                  >
                    Refresh
                  </Button>
                </Box>
              </Box>

              {systemAlerts ? (
                <TableContainer component={Paper}>
                  <Table>
                    <TableHead>
                      <TableRow>
                        <TableCell>Type</TableCell>
                        <TableCell>Title</TableCell>
                        <TableCell>Severity</TableCell>
                        <TableCell>Status</TableCell>
                        <TableCell>Created</TableCell>
                        <TableCell>Actions</TableCell>
                      </TableRow>
                    </TableHead>
                    <TableBody>
                      {systemAlerts.alerts.map((alert) => (
                        <TableRow key={alert.id}>
                          <TableCell>
                            <Chip
                              label={alert.alert_type}
                              size="small"
                              color="primary"
                              variant="outlined"
                            />
                          </TableCell>
                          <TableCell>{alert.alert_title}</TableCell>
                          <TableCell>
                            <Chip
                              label={alert.severity}
                              size="small"
                              color={getSeverityColor(alert.severity)}
                            />
                          </TableCell>
                          <TableCell>
                            <Chip
                              label={alert.is_resolved ? 'Resolved' : 'Active'}
                              size="small"
                              color={alert.is_resolved ? 'success' : 'warning'}
                            />
                          </TableCell>
                          <TableCell>
                            {new Date(alert.created_at).toLocaleString()}
                          </TableCell>
                          <TableCell>
                            {!alert.is_resolved && (
                              <Tooltip title="Resolve Alert">
                                <IconButton
                                  size="small"
                                  onClick={() => handleResolveAlert(alert.id)}
                                >
                                  <CheckCircle />
                                </IconButton>
                              </Tooltip>
                            )}
                          </TableCell>
                        </TableRow>
                      ))}
                    </TableBody>
                  </Table>
                </TableContainer>
              ) : (
                <Box sx={{ display: 'flex', justifyContent: 'center', p: 4 }}>
                  <CircularProgress />
                </Box>
              )}
            </Box>
          )}
        </CardContent>
      </Card>

      {/* Create Alert Dialog */}
      <Dialog open={alertDialog} onClose={() => setAlertDialog(false)} maxWidth="md" fullWidth>
        <DialogTitle>Create System Alert</DialogTitle>
        <DialogContent>
          <Grid container spacing={2} sx={{ mt: 1 }}>
            <Grid item xs={12} sm={6}>
              <FormControl fullWidth>
                <InputLabel>Alert Type</InputLabel>
                <Select
                  value={newAlert.alert_type}
                  label="Alert Type"
                  onChange={(e) => setNewAlert({ ...newAlert, alert_type: e.target.value })}
                >
                  <MenuItem value="error">Error</MenuItem>
                  <MenuItem value="warning">Warning</MenuItem>
                  <MenuItem value="info">Info</MenuItem>
                  <MenuItem value="performance">Performance</MenuItem>
                </Select>
              </FormControl>
            </Grid>
            <Grid item xs={12} sm={6}>
              <FormControl fullWidth>
                <InputLabel>Severity</InputLabel>
                <Select
                  value={newAlert.severity}
                  label="Severity"
                  onChange={(e) => setNewAlert({ ...newAlert, severity: e.target.value })}
                >
                  <MenuItem value="low">Low</MenuItem>
                  <MenuItem value="medium">Medium</MenuItem>
                  <MenuItem value="high">High</MenuItem>
                  <MenuItem value="critical">Critical</MenuItem>
                </Select>
              </FormControl>
            </Grid>
            <Grid item xs={12}>
              <TextField
                fullWidth
                label="Alert Title"
                value={newAlert.alert_title}
                onChange={(e) => setNewAlert({ ...newAlert, alert_title: e.target.value })}
              />
            </Grid>
            <Grid item xs={12}>
              <TextField
                fullWidth
                multiline
                rows={4}
                label="Alert Message"
                value={newAlert.alert_message}
                onChange={(e) => setNewAlert({ ...newAlert, alert_message: e.target.value })}
              />
            </Grid>
          </Grid>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setAlertDialog(false)}>Cancel</Button>
          <Button onClick={handleCreateAlert} variant="contained">
            Create Alert
          </Button>
        </DialogActions>
      </Dialog>
    </Container>
  );
};

export default DeveloperDashboard;
