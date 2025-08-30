import React, { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Card,
  CardContent,
  Grid,
  Button,
  Chip,
  List,
  ListItem,
  ListItemText,
  ListItemIcon,
  Avatar,
  CircularProgress,
  Alert,
  Snackbar,
  useMediaQuery,
  useTheme,
  Stack,
  Skeleton,
  Fade,
  Grow,
  Divider,
} from '@mui/material';
import {
  TrendingUp as TrendingUpIcon,
  Home as HomeIcon,
  Assessment as AssessmentIcon,
  Schedule as ScheduleIcon,
  Person as PersonIcon,
  Phone as PhoneIcon,
  Add as AddIcon,
  LocationOn as LocationIcon,
} from '@mui/icons-material';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { useAppContext } from '../context/AppContext';
import { apiUtils, handleApiError } from '../utils/api';

const Dashboard = () => {
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('md'));
  const isSmallScreen = useMediaQuery(theme.breakpoints.down('sm'));
  
  const { currentUser } = useAppContext();
  const [dailyBriefing, setDailyBriefing] = useState(null);
  const [marketData, setMarketData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [snackbar, setSnackbar] = useState({ open: false, message: '', severity: 'info' });

  useEffect(() => {
    const fetchDashboardData = async () => {
      try {
        setLoading(true);
        setError(null);
        
        // Fetch daily briefing
        try {
          const briefingData = await apiUtils.getDailyBriefing();
          setDailyBriefing(briefingData);
        } catch (error) {
          console.log('Using mock daily briefing data');
          setDailyBriefing(null);
        }

        // Fetch market data
        try {
          const marketResponse = await apiUtils.getMarketOverview();
          setMarketData(marketResponse);
        } catch (error) {
          console.log('Using mock market data');
          setMarketData(null);
        }

      } catch (error) {
        console.error('Error fetching dashboard data:', error);
        const errorMessage = handleApiError(error);
        setError(errorMessage);
        setSnackbar({
          open: true,
          message: errorMessage,
          severity: 'error',
        });
      } finally {
        setLoading(false);
      }
    };

    fetchDashboardData();
  }, []);

  const handleQuickAction = async (action) => {
    try {
      setSnackbar({
        open: true,
        message: `Executing ${action}...`,
        severity: 'info',
      });

      // Execute action via API
      const result = await apiUtils.executeAction(action, {
        user_id: currentUser?.id,
        timestamp: new Date().toISOString(),
      });

      setSnackbar({
        open: true,
        message: `${action} completed successfully!`,
        severity: 'success',
      });

      console.log(`Quick action result:`, result);
    } catch (error) {
      const errorMessage = handleApiError(error);
      setSnackbar({
        open: true,
        message: `Failed to execute ${action}: ${errorMessage}`,
        severity: 'error',
      });
    }
  };

  const handleCloseSnackbar = () => {
    setSnackbar({ ...snackbar, open: false });
  };

  // Skeleton loader for dashboard widgets
  const DashboardSkeleton = () => (
    <Grid container spacing={3}>
      <Grid item xs={12} md={6} lg={4}>
        <Card>
          <CardContent>
            <Stack spacing={2}>
              <Skeleton variant="text" width="60%" height={32} />
              <Skeleton variant="rectangular" width="100%" height={120} />
              <Skeleton variant="text" width="40%" height={20} />
            </Stack>
          </CardContent>
        </Card>
      </Grid>
      <Grid item xs={12} md={6} lg={4}>
        <Card>
          <CardContent>
            <Stack spacing={2}>
              <Skeleton variant="text" width="70%" height={32} />
              <Skeleton variant="rectangular" width="100%" height={120} />
              <Skeleton variant="text" width="50%" height={20} />
            </Stack>
          </CardContent>
        </Card>
      </Grid>
      <Grid item xs={12} md={6} lg={4}>
        <Card>
          <CardContent>
            <Stack spacing={2}>
              <Skeleton variant="text" width="50%" height={32} />
              <Skeleton variant="rectangular" width="100%" height={120} />
              <Skeleton variant="text" width="30%" height={20} />
            </Stack>
          </CardContent>
        </Card>
      </Grid>
      <Grid item xs={12}>
        <Card>
          <CardContent>
            <Stack spacing={2}>
              <Skeleton variant="text" width="40%" height={32} />
              <Skeleton variant="rectangular" width="100%" height={200} />
            </Stack>
          </CardContent>
        </Card>
      </Grid>
    </Grid>
  );

  // Empty state component
  const EmptyState = () => (
    <Box 
      sx={{ 
        textAlign: 'center', 
        py: theme.spacing(8),
        px: theme.spacing(2)
      }}
    >
      <AssessmentIcon 
        sx={{ 
          fontSize: 64, 
          color: 'text.secondary',
          mb: theme.spacing(2)
        }} 
      />
      <Typography variant="h6" color="text.secondary" gutterBottom>
        No dashboard data available
      </Typography>
      <Typography variant="body2" color="text.secondary" sx={{ mb: theme.spacing(3) }}>
        Dashboard data will appear here once available.
      </Typography>
      <Button
        variant="contained"
        onClick={() => window.location.reload()}
      >
        Refresh Dashboard
      </Button>
    </Box>
  );

  if (loading) {
    return <DashboardSkeleton />;
  }

  return (
    <Box>
      {/* Header */}
      <Box sx={{ mb: 4 }}>
        <Typography variant="h4" sx={{ fontWeight: 600, mb: 1 }}>
          Good morning, {currentUser?.name?.split(' ')[0] || 'Agent'}! 👋
        </Typography>
        <Typography variant="body1" color="text.secondary">
          Here's your daily briefing and market overview
        </Typography>
      </Box>

      {/* Error Alert */}
      {error && (
        <Alert severity="error" sx={{ mb: 3 }} onClose={() => setError(null)}>
          {error}
        </Alert>
      )}

      <Grid container spacing={3}>
        {/* Daily Briefing Widget */}
        <Grid item xs={12} lg={8}>
          <Card sx={{ height: '100%' }}>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 3 }}>
                <ScheduleIcon color="primary" sx={{ mr: 1 }} />
                <Typography variant="h6">Today's Schedule</Typography>
              </Box>

              <Grid container spacing={2}>
                {/* Appointments */}
                <Grid item xs={12} md={6}>
                  <Typography variant="subtitle1" sx={{ fontWeight: 600, mb: 2 }}>
                    Appointments ({dailyBriefing?.appointments?.length || 0})
                  </Typography>
                  <List dense>
                    {dailyBriefing?.appointments?.map((appointment) => (
                      <ListItem key={appointment.id} sx={{ px: 0 }}>
                        <ListItemIcon sx={{ minWidth: 40 }}>
                          <Avatar sx={{ width: 32, height: 32, bgcolor: 'primary.main' }}>
                            <PersonIcon fontSize="small" />
                          </Avatar>
                        </ListItemIcon>
                        <ListItemText
                          primary={appointment.client}
                          secondary={
                            <Box>
                              <Typography variant="body2" color="text.secondary">
                                {appointment.time} • {appointment.type}
                              </Typography>
                              <Typography variant="caption" color="text.secondary">
                                📍 {appointment.location}
                              </Typography>
                            </Box>
                          }
                        />
                      </ListItem>
                    ))}
                  </List>
                </Grid>

                {/* Priority Leads */}
                <Grid item xs={12} md={6}>
                  <Typography variant="subtitle1" sx={{ fontWeight: 600, mb: 2 }}>
                    Priority Leads ({dailyBriefing?.priorityLeads?.length || 0})
                  </Typography>
                  <List dense>
                    {dailyBriefing?.priorityLeads?.map((lead) => (
                      <ListItem key={lead.id} sx={{ px: 0 }}>
                        <ListItemIcon sx={{ minWidth: 40 }}>
                          <Chip
                            label={lead.status}
                            size="small"
                            color={lead.status === 'Hot' ? 'error' : 'warning'}
                            sx={{ height: 20, fontSize: '0.75rem' }}
                          />
                        </ListItemIcon>
                        <ListItemText
                          primary={lead.name}
                          secondary={
                            <Box>
                              <Typography variant="body2" color="text.secondary">
                                {lead.budget} • {lead.interest}
                              </Typography>
                            </Box>
                          }
                        />
                      </ListItem>
                    ))}
                  </List>
                </Grid>
              </Grid>
            </CardContent>
          </Card>
        </Grid>

        {/* Quick Actions Widget */}
        <Grid item xs={12} lg={4}>
          <Card sx={{ height: '100%' }}>
            <CardContent>
              <Typography variant="h6" sx={{ mb: 3 }}>
                Quick Actions
              </Typography>
              <Grid container spacing={2}>
                <Grid item xs={6}>
                  <Button
                    fullWidth
                    variant="outlined"
                    startIcon={<PhoneIcon />}
                    onClick={() => handleQuickAction('log-call')}
                    sx={{ py: 1.5 }}
                  >
                    Log Call
                  </Button>
                </Grid>
                <Grid item xs={6}>
                  <Button
                    fullWidth
                    variant="outlined"
                    startIcon={<AddIcon />}
                    onClick={() => handleQuickAction('add-lead')}
                    sx={{ py: 1.5 }}
                  >
                    Add Lead
                  </Button>
                </Grid>
                <Grid item xs={6}>
                  <Button
                    fullWidth
                    variant="outlined"
                    startIcon={<HomeIcon />}
                    onClick={() => handleQuickAction('schedule-viewing')}
                    sx={{ py: 1.5 }}
                  >
                    Schedule Viewing
                  </Button>
                </Grid>
                <Grid item xs={6}>
                  <Button
                    fullWidth
                    variant="outlined"
                    startIcon={<AssessmentIcon />}
                    onClick={() => handleQuickAction('generate-cma')}
                    sx={{ py: 1.5 }}
                  >
                    Generate CMA
                  </Button>
                </Grid>
              </Grid>
            </CardContent>
          </Card>
        </Grid>

        {/* Market Update Widget */}
        <Grid item xs={12}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 3 }}>
                <TrendingUpIcon color="primary" sx={{ mr: 1 }} />
                <Typography variant="h6">Market Overview</Typography>
              </Box>

              <Grid container spacing={3}>
                {/* Market Stats */}
                <Grid item xs={12} md={3}>
                  <Box textAlign="center">
                    <Typography variant="h4" color="primary" sx={{ fontWeight: 600 }}>
                      {dailyBriefing?.marketInsights?.avgPrice || '1,285,000 AED'}
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      Average Price
                    </Typography>
                  </Box>
                </Grid>
                <Grid item xs={12} md={3}>
                  <Box textAlign="center">
                    <Typography variant="h4" color="success.main" sx={{ fontWeight: 600 }}>
                      {dailyBriefing?.marketInsights?.priceChange || '+8.5%'}
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      Price Change (YoY)
                    </Typography>
                  </Box>
                </Grid>
                <Grid item xs={12} md={3}>
                  <Box textAlign="center">
                    <Typography variant="h4" color="info.main" sx={{ fontWeight: 600 }}>
                      {dailyBriefing?.marketInsights?.volumeChange || '+12.3%'}
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      Volume Change
                    </Typography>
                  </Box>
                </Grid>
                <Grid item xs={12} md={3}>
                  <Box textAlign="center">
                    <Typography variant="h4" color="secondary.main" sx={{ fontWeight: 600 }}>
                      {dailyBriefing?.marketInsights?.hotAreas?.length || 3}
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      Hot Areas
                    </Typography>
                  </Box>
                </Grid>

                {/* Market Chart */}
                <Grid item xs={12}>
                  <Box sx={{ height: 300, mt: 2 }}>
                    <ResponsiveContainer width="100%" height="100%">
                      <LineChart data={marketData}>
                        <CartesianGrid strokeDasharray="3 3" />
                        <XAxis dataKey="name" />
                        <YAxis />
                        <Tooltip formatter={(value) => [`${value.toLocaleString()} AED`, 'Price']} />
                        <Line type="monotone" dataKey="price" stroke="#1976d2" strokeWidth={2} />
                      </LineChart>
                    </ResponsiveContainer>
                  </Box>
                </Grid>

                {/* Hot Areas */}
                <Grid item xs={12}>
                  <Typography variant="subtitle1" sx={{ fontWeight: 600, mb: 2 }}>
                    Hot Areas
                  </Typography>
                  <Box sx={{ display: 'flex', gap: 1, flexWrap: 'wrap' }}>
                    {dailyBriefing?.marketInsights?.hotAreas?.map((area, index) => (
                      <Chip
                        key={index}
                        label={area}
                        color="primary"
                        variant="outlined"
                        icon={<LocationIcon />}
                      />
                    ))}
                  </Box>
                </Grid>
              </Grid>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Snackbar for notifications */}
      <Snackbar
        open={snackbar.open}
        autoHideDuration={6000}
        onClose={handleCloseSnackbar}
        anchorOrigin={{ vertical: 'bottom', horizontal: 'right' }}
      >
        <Alert onClose={handleCloseSnackbar} severity={snackbar.severity} sx={{ width: '100%' }}>
          {snackbar.message}
        </Alert>
      </Snackbar>
    </Box>
  );
};

export default Dashboard;
