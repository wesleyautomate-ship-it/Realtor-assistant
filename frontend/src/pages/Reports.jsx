import React, { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Card,
  CardContent,
  TextField,
  Button,
  IconButton,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  useTheme,
  useMediaQuery,
  Stack,
  Grid,
  Chip,
  LinearProgress,
  Alert,
  Paper,
  List,
  ListItem,
  ListItemText,
  ListItemIcon,
  ListItemSecondaryAction,
  Divider,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
  CircularProgress,
  Tabs,
  Tab,
} from '@mui/material';
import {
  Assessment as AssessmentIcon,
  TrendingUp as TrendingUpIcon,
  Download as DownloadIcon,
  Refresh as RefreshIcon,
  Add as AddIcon,
  SmartToy as SmartToyIcon,
  Analytics as AnalyticsIcon,
  BarChart as BarChartIcon,
  PieChart as PieChartIcon,
  Timeline as TimelineIcon,
  LocationOn as LocationIcon,
  AttachMoney as MoneyIcon,
  Business as BusinessIcon,
  FilterList as FilterIcon,
} from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';
import { useAppContext } from '../context/AppContext';
import { api } from '../utils/apiClient';

const Reports = () => {
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('md'));
  const navigate = useNavigate();
  const { currentUser } = useAppContext();
  
  const [activeTab, setActiveTab] = useState(0);
  const [loading, setLoading] = useState(false);
  const [generateDialogOpen, setGenerateDialogOpen] = useState(false);
  const [reportType, setReportType] = useState('');
  const [reportParameters, setReportParameters] = useState({});
  const [availableReports, setAvailableReports] = useState([]);
  const [marketData, setMarketData] = useState(null);
  const [mlInsights, setMlInsights] = useState(null);
  const [performanceMetrics, setPerformanceMetrics] = useState(null);

  // Report templates
  const reportTemplates = [
    {
      id: 'market-overview',
      name: 'Market Overview Report',
      description: 'Comprehensive market analysis with trends and predictions',
      icon: <TrendingUpIcon />,
      category: 'market',
      parameters: ['area', 'timeframe', 'property_type']
    },
    {
      id: 'property-valuation',
      name: 'Property Valuation Report',
      description: 'AI-powered property valuation with market comparison',
      icon: <MoneyIcon />,
      category: 'valuation',
      parameters: ['property_data', 'comparison_area']
    },
    {
      id: 'investment-analysis',
      name: 'Investment Opportunity Analysis',
      description: 'ML-driven investment recommendations and ROI projections',
      icon: <BusinessIcon />,
      category: 'investment',
      parameters: ['investment_criteria', 'risk_tolerance', 'budget']
    },
    {
      id: 'performance-analytics',
      name: 'Performance Analytics Report',
      description: 'System performance metrics and usage analytics',
      icon: <AnalyticsIcon />,
      category: 'analytics',
      parameters: ['timeframe', 'metrics']
    },
    {
      id: 'lead-nurturing',
      name: 'Lead Nurturing Report',
      description: 'Lead scoring and nurturing campaign effectiveness',
      icon: <SmartToyIcon />,
      category: 'leads',
      parameters: ['campaign_id', 'timeframe']
    },
    {
      id: 'area-analysis',
      name: 'Area Analysis Report',
      description: 'Detailed area market analysis with growth projections',
      icon: <LocationIcon />,
      category: 'area',
      parameters: ['area_name', 'analysis_depth']
    }
  ];

  useEffect(() => {
    loadInitialData();
  }, []);

  const loadInitialData = async () => {
    setLoading(true);
    try {
      // Load market overview
      const marketOverview = await api.getMarketOverview();
      setMarketData(marketOverview);

      // Load performance metrics
      const metrics = await api.getPerformanceMetrics();
      setPerformanceMetrics(metrics);

      // Load available reports
      const reports = await api.getReportTemplates();
      setAvailableReports(reports);

    } catch (error) {
      console.error('Error loading initial data:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleGenerateReport = async () => {
    if (!reportType) return;

    setLoading(true);
    try {
      const result = await api.generateReport(reportType, reportParameters);
      
      // Show success message and close dialog
      setGenerateDialogOpen(false);
      setReportType('');
      setReportParameters({});
      
      // Refresh reports list
      loadInitialData();
      
    } catch (error) {
      console.error('Error generating report:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleDownloadReport = async (reportId) => {
    try {
      const blob = await api.downloadReport(reportId);
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `report-${reportId}.pdf`;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);
    } catch (error) {
      console.error('Error downloading report:', error);
    }
  };

  const handleTabChange = (event, newValue) => {
    setActiveTab(newValue);
  };

  const getMarketInsights = async (area) => {
    try {
      const insights = await api.getMarketTrends(area);
      setMlInsights(insights);
    } catch (error) {
      console.error('Error loading market insights:', error);
    }
  };

  const renderMarketOverview = () => (
    <Grid container spacing={2}>
      {/* Market Overview Card */}
      <Grid item xs={12} md={6}>
        <Card sx={{ borderRadius: 3, boxShadow: '0 4px 12px rgba(0,0,0,0.1)' }}>
          <CardContent>
            <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
              <TrendingUpIcon sx={{ color: 'primary.main', mr: 1 }} />
              <Typography variant="h6" sx={{ fontWeight: 600 }}>
                Market Overview
              </Typography>
            </Box>
            {marketData ? (
              <Stack spacing={2}>
                <Box>
                  <Typography variant="body2" color="text.secondary">
                    Average Property Price
                  </Typography>
                  <Typography variant="h5" sx={{ fontWeight: 600, color: 'primary.main' }}>
                    AED {marketData.average_price?.toLocaleString() || 'N/A'}
                  </Typography>
                </Box>
                <Box>
                  <Typography variant="body2" color="text.secondary">
                    Market Trend
                  </Typography>
                  <Chip
                    label={marketData.trend || 'Stable'}
                    color={marketData.trend === 'Rising' ? 'success' : marketData.trend === 'Falling' ? 'error' : 'default'}
                    size="small"
                  />
                </Box>
                <Box>
                  <Typography variant="body2" color="text.secondary">
                    Active Listings
                  </Typography>
                  <Typography variant="h6">
                    {marketData.active_listings || 'N/A'}
                  </Typography>
                </Box>
              </Stack>
            ) : (
              <CircularProgress size={24} />
            )}
          </CardContent>
        </Card>
      </Grid>

      {/* ML Insights Card */}
      <Grid item xs={12} md={6}>
        <Card sx={{ borderRadius: 3, boxShadow: '0 4px 12px rgba(0,0,0,0.1)' }}>
          <CardContent>
            <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
              <SmartToyIcon sx={{ color: 'secondary.main', mr: 1 }} />
              <Typography variant="h6" sx={{ fontWeight: 600 }}>
                AI Insights
              </Typography>
            </Box>
            {mlInsights ? (
              <Stack spacing={2}>
                <Box>
                  <Typography variant="body2" color="text.secondary">
                    Price Prediction (6M)
                  </Typography>
                  <Typography variant="h6" sx={{ color: 'secondary.main' }}>
                    {mlInsights.price_prediction || 'N/A'}
                  </Typography>
                </Box>
                <Box>
                  <Typography variant="body2" color="text.secondary">
                    Investment Score
                  </Typography>
                  <Typography variant="h6">
                    {mlInsights.investment_score || 'N/A'}/10
                  </Typography>
                </Box>
                <Box>
                  <Typography variant="body2" color="text.secondary">
                    Risk Level
                  </Typography>
                  <Chip
                    label={mlInsights.risk_level || 'Medium'}
                    color={mlInsights.risk_level === 'Low' ? 'success' : mlInsights.risk_level === 'High' ? 'error' : 'warning'}
                    size="small"
                  />
                </Box>
              </Stack>
            ) : (
              <Button
                variant="outlined"
                onClick={() => getMarketInsights('Dubai')}
                startIcon={<SmartToyIcon />}
                sx={{ borderRadius: 2 }}
              >
                Generate AI Insights
              </Button>
            )}
          </CardContent>
        </Card>
      </Grid>

      {/* Performance Metrics */}
      <Grid item xs={12}>
        <Card sx={{ borderRadius: 3, boxShadow: '0 4px 12px rgba(0,0,0,0.1)' }}>
          <CardContent>
            <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
              <AnalyticsIcon sx={{ color: 'info.main', mr: 1 }} />
              <Typography variant="h6" sx={{ fontWeight: 600 }}>
                System Performance
              </Typography>
            </Box>
            {performanceMetrics ? (
              <Grid container spacing={2}>
                <Grid item xs={6} sm={3}>
                  <Box sx={{ textAlign: 'center' }}>
                    <Typography variant="h4" sx={{ fontWeight: 600, color: 'success.main' }}>
                      {performanceMetrics.uptime || '99.9'}%
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      Uptime
                    </Typography>
                  </Box>
                </Grid>
                <Grid item xs={6} sm={3}>
                  <Box sx={{ textAlign: 'center' }}>
                    <Typography variant="h4" sx={{ fontWeight: 600, color: 'primary.main' }}>
                      {performanceMetrics.response_time || '120'}ms
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      Avg Response
                    </Typography>
                  </Box>
                </Grid>
                <Grid item xs={6} sm={3}>
                  <Box sx={{ textAlign: 'center' }}>
                    <Typography variant="h4" sx={{ fontWeight: 600, color: 'warning.main' }}>
                      {performanceMetrics.active_users || '0'}
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      Active Users
                    </Typography>
                  </Box>
                </Grid>
                <Grid item xs={6} sm={3}>
                  <Box sx={{ textAlign: 'center' }}>
                    <Typography variant="h4" sx={{ fontWeight: 600, color: 'info.main' }}>
                      {performanceMetrics.queries_today || '0'}
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      Queries Today
                    </Typography>
                  </Box>
                </Grid>
              </Grid>
            ) : (
              <CircularProgress size={24} />
            )}
          </CardContent>
        </Card>
      </Grid>
    </Grid>
  );

  const renderReportTemplates = () => (
    <Grid container spacing={2}>
      {reportTemplates.map((template) => (
        <Grid item xs={12} sm={6} md={4} key={template.id}>
          <Card 
            sx={{ 
              borderRadius: 3, 
              boxShadow: '0 4px 12px rgba(0,0,0,0.1)',
              cursor: 'pointer',
              '&:hover': {
                boxShadow: '0 8px 24px rgba(0,0,0,0.15)',
                transform: 'translateY(-2px)',
                transition: 'all 0.2s ease-in-out'
              }
            }}
            onClick={() => {
              setReportType(template.id);
              setGenerateDialogOpen(true);
            }}
          >
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                <Box sx={{ 
                  p: 1, 
                  borderRadius: 2, 
                  bgcolor: 'primary.light', 
                  color: 'primary.contrastText',
                  mr: 2
                }}>
                  {template.icon}
                </Box>
                <Typography variant="h6" sx={{ fontWeight: 600 }}>
                  {template.name}
                </Typography>
              </Box>
              <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                {template.description}
              </Typography>
              <Chip
                label={template.category}
                size="small"
                color="primary"
                variant="outlined"
              />
            </CardContent>
          </Card>
        </Grid>
      ))}
    </Grid>
  );

  const renderGeneratedReports = () => (
    <Paper sx={{ borderRadius: 3, overflow: 'hidden' }}>
      <List>
        {availableReports.length > 0 ? (
          availableReports.map((report, index) => (
            <React.Fragment key={report.id || index}>
              <ListItem>
                <ListItemIcon>
                  <AssessmentIcon sx={{ color: 'primary.main' }} />
                </ListItemIcon>
                <ListItemText
                  primary={
                    <Typography variant="subtitle1" sx={{ fontWeight: 600 }}>
                      {report.name || `Report ${report.id}`}
                    </Typography>
                  }
                  secondary={
                    <Box>
                      <Typography variant="body2" color="text.secondary">
                        Generated: {report.created_at || 'Unknown'}
                      </Typography>
                      <Typography variant="caption" color="text.secondary">
                        Type: {report.type || 'Unknown'} • Status: {report.status || 'Completed'}
                      </Typography>
                    </Box>
                  }
                />
                <ListItemSecondaryAction>
                  <IconButton
                    onClick={() => handleDownloadReport(report.id)}
                    title="Download Report"
                  >
                    <DownloadIcon />
                  </IconButton>
                </ListItemSecondaryAction>
              </ListItem>
              {index < availableReports.length - 1 && <Divider />}
            </React.Fragment>
          ))
        ) : (
          <ListItem>
            <ListItemText
              primary={
                <Typography variant="body1" color="text.secondary" align="center">
                  No reports generated yet
                </Typography>
              }
            />
          </ListItem>
        )}
      </List>
    </Paper>
  );

  return (
    <Box sx={{ 
      minHeight: '100vh', 
      bgcolor: 'background.default',
      pb: isMobile ? 8 : 4
    }}>
      {/* Header */}
      <Box sx={{ 
        p: 3, 
        background: 'linear-gradient(135deg, #1976d2 0%, #42a5f5 100%)',
        color: 'white'
      }}>
        <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', mb: 2 }}>
          <Typography variant="h4" sx={{ fontWeight: 700 }}>
            Reports & Analytics
          </Typography>
          <Button
            variant="contained"
            startIcon={<AddIcon />}
            onClick={() => setGenerateDialogOpen(true)}
            sx={{
              bgcolor: 'rgba(255,255,255,0.2)',
              color: 'white',
              '&:hover': {
                bgcolor: 'rgba(255,255,255,0.3)',
              },
              borderRadius: 2,
            }}
          >
            Generate Report
          </Button>
        </Box>
        
        <Typography variant="body1" sx={{ opacity: 0.9 }}>
          AI-powered market insights and comprehensive analytics
        </Typography>
      </Box>

      {/* Tabs */}
      <Box sx={{ px: 2, pt: 2 }}>
        <Tabs
          value={activeTab}
          onChange={handleTabChange}
          variant={isMobile ? 'scrollable' : 'standard'}
          scrollButtons="auto"
          sx={{
            '& .MuiTab-root': {
              textTransform: 'none',
              fontWeight: 600,
            },
          }}
        >
          <Tab label="Market Overview" icon={<TrendingUpIcon />} />
          <Tab label="Report Templates" icon={<AssessmentIcon />} />
          <Tab label="Generated Reports" icon={<DownloadIcon />} />
        </Tabs>
      </Box>

      {/* Content */}
      <Box sx={{ p: 2 }}>
        {loading && <LinearProgress sx={{ mb: 2 }} />}
        
        {activeTab === 0 && renderMarketOverview()}
        {activeTab === 1 && renderReportTemplates()}
        {activeTab === 2 && renderGeneratedReports()}
      </Box>

      {/* Generate Report Dialog */}
      <Dialog
        open={generateDialogOpen}
        onClose={() => setGenerateDialogOpen(false)}
        maxWidth="sm"
        fullWidth
      >
        <DialogTitle>Generate Report</DialogTitle>
        <DialogContent>
          <Stack spacing={2} sx={{ mt: 1 }}>
            <FormControl fullWidth>
              <InputLabel>Report Type</InputLabel>
              <Select
                value={reportType}
                onChange={(e) => setReportType(e.target.value)}
                label="Report Type"
              >
                {reportTemplates.map((template) => (
                  <MenuItem key={template.id} value={template.id}>
                    <Box sx={{ display: 'flex', alignItems: 'center' }}>
                      {template.icon}
                      <Typography sx={{ ml: 1 }}>{template.name}</Typography>
                    </Box>
                  </MenuItem>
                ))}
              </Select>
            </FormControl>

            {reportType && (
              <Alert severity="info">
                {reportTemplates.find(t => t.id === reportType)?.description}
              </Alert>
            )}

            {/* Dynamic parameters based on report type */}
            {reportType === 'market-overview' && (
              <Stack spacing={2}>
                <TextField
                  label="Area"
                  value={reportParameters.area || ''}
                  onChange={(e) => setReportParameters(prev => ({ ...prev, area: e.target.value }))}
                  placeholder="e.g., Dubai Marina, Palm Jumeirah"
                />
                <TextField
                  label="Timeframe"
                  value={reportParameters.timeframe || ''}
                  onChange={(e) => setReportParameters(prev => ({ ...prev, timeframe: e.target.value }))}
                  placeholder="e.g., 6 months, 1 year"
                />
              </Stack>
            )}

            {reportType === 'investment-analysis' && (
              <Stack spacing={2}>
                <TextField
                  label="Budget Range"
                  value={reportParameters.budget || ''}
                  onChange={(e) => setReportParameters(prev => ({ ...prev, budget: e.target.value }))}
                  placeholder="e.g., AED 2M - 5M"
                />
                <TextField
                  label="Risk Tolerance"
                  value={reportParameters.risk_tolerance || ''}
                  onChange={(e) => setReportParameters(prev => ({ ...prev, risk_tolerance: e.target.value }))}
                  placeholder="Low, Medium, High"
                />
              </Stack>
            )}
          </Stack>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setGenerateDialogOpen(false)}>Cancel</Button>
          <Button
            variant="contained"
            onClick={handleGenerateReport}
            disabled={!reportType || loading}
            startIcon={loading ? <CircularProgress size={16} /> : <SmartToyIcon />}
          >
            {loading ? 'Generating...' : 'Generate Report'}
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default Reports;
