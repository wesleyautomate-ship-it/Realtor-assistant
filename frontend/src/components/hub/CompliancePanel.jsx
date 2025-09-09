import React, { useState, useEffect } from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  Grid,
  Chip,
  useTheme,
  Alert,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  Button,
  LinearProgress,
  Stack,
  IconButton,
  Tooltip,
} from '@mui/material';
import {
  Security as SecurityIcon,
  Warning as WarningIcon,
  CheckCircle as CheckIcon,
  Error as ErrorIcon,
  Assignment as DocumentIcon,
  Schedule as ScheduleIcon,
  Refresh as RefreshIcon,
  AutoAwesome as AIIcon,
  TrendingUp as TrendingUpIcon,
} from '@mui/icons-material';

const CompliancePanel = () => {
  const theme = useTheme();
  const [complianceData, setComplianceData] = useState(null);
  const [isLoading, setIsLoading] = useState(true);

  // Mock data for development - will be replaced with real API calls
  useEffect(() => {
    const loadComplianceData = async () => {
      setIsLoading(true);
      
      // Simulate API call
      setTimeout(() => {
        setComplianceData({
          overallScore: 95,
          scoreChange: 2.5,
          alerts: [
            {
              id: 1,
              type: 'warning',
              title: '3 agents need compliance training renewal',
              description: 'Training certificates expire within 30 days',
              priority: 'medium',
              action: 'Schedule Training',
              dueDate: '2024-12-15'
            },
            {
              id: 2,
              type: 'info',
              title: 'Brand guidelines updated',
              description: 'New RERA branding requirements implemented',
              priority: 'low',
              action: 'Review Guidelines',
              dueDate: '2024-12-20'
            },
            {
              id: 3,
              type: 'success',
              title: 'All documentation up to date',
              description: 'Property listings comply with current regulations',
              priority: 'low',
              action: 'View Details',
              dueDate: null
            }
          ],
          pendingDocuments: [
            { name: 'Property Registration - Villa 12', status: 'pending', daysLeft: 5 },
            { name: 'RERA License Renewal', status: 'in_review', daysLeft: 12 },
            { name: 'Client Agreement - Ali Khan', status: 'pending', daysLeft: 2 },
          ],
          complianceMetrics: [
            { label: 'Document Compliance', value: 98, color: 'success' },
            { label: 'Training Completion', value: 87, color: 'warning' },
            { label: 'License Status', value: 100, color: 'success' },
            { label: 'Brand Compliance', value: 92, color: 'primary' },
          ],
          aiInsights: [
            "Compliance score improved by 2.5% this month",
            "All critical documents are up to date",
            "Consider scheduling training sessions for Q1 2025"
          ]
        });
        setIsLoading(false);
      }, 1000);
    };

    loadComplianceData();
  }, []);

  const handleRefresh = () => {
    // TODO: Implement refresh functionality
    console.log('Refreshing compliance data...');
  };

  const handleAlertAction = (alert) => {
    console.log('Alert action:', alert.action, alert);
    // TODO: Implement alert actions
  };

  const getAlertIcon = (type) => {
    switch (type) {
      case 'error': return <ErrorIcon color="error" />;
      case 'warning': return <WarningIcon color="warning" />;
      case 'success': return <CheckIcon color="success" />;
      default: return <SecurityIcon color="info" />;
    }
  };

  const getAlertSeverity = (type) => {
    switch (type) {
      case 'error': return 'error';
      case 'warning': return 'warning';
      case 'success': return 'success';
      default: return 'info';
    }
  };

  const getDocumentStatusColor = (status) => {
    switch (status) {
      case 'pending': return 'error';
      case 'in_review': return 'warning';
      case 'approved': return 'success';
      default: return 'default';
    }
  };

  if (isLoading) {
    return (
      <Card sx={{ borderRadius: 3, boxShadow: 3 }}>
        <CardContent>
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 2 }}>
            <SecurityIcon color="primary" />
            <Typography variant="h6" sx={{ fontWeight: 600 }}>
              Compliance Monitor
            </Typography>
          </Box>
          <LinearProgress />
        </CardContent>
      </Card>
    );
  }

  return (
    <Card sx={{ borderRadius: 3, boxShadow: 3 }}>
      <CardContent>
        <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', mb: 3 }}>
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
            <SecurityIcon color="primary" />
            <Typography variant="h6" sx={{ fontWeight: 600 }}>
              RERA Compliance Monitor
            </Typography>
          </Box>
          <Tooltip title="Refresh Data">
            <IconButton onClick={handleRefresh} size="small">
              <RefreshIcon />
            </IconButton>
          </Tooltip>
        </Box>

        {/* Overall Score */}
        <Box sx={{ mb: 3 }}>
          <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', mb: 2 }}>
            <Typography variant="subtitle1" sx={{ fontWeight: 600 }}>
              Overall Compliance Score
            </Typography>
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 0.5 }}>
              <TrendingUpIcon sx={{ color: 'success.main', fontSize: 16 }} />
              <Typography variant="body2" sx={{ color: 'success.main', fontWeight: 600 }}>
                +{complianceData.scoreChange}%
              </Typography>
            </Box>
          </Box>
          <Box sx={{ position: 'relative', display: 'inline-flex', width: '100%' }}>
            <LinearProgress
              variant="determinate"
              value={complianceData.overallScore}
              color="success"
              sx={{ height: 12, borderRadius: 6, width: '100%' }}
            />
            <Box
              sx={{
                top: 0,
                left: 0,
                bottom: 0,
                right: 0,
                position: 'absolute',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
              }}
            >
              <Typography variant="h6" sx={{ fontWeight: 700, color: 'white' }}>
                {complianceData.overallScore}%
              </Typography>
            </Box>
          </Box>
        </Box>

        {/* Compliance Metrics */}
        <Grid container spacing={2} sx={{ mb: 3 }}>
          {complianceData.complianceMetrics.map((metric, index) => (
            <Grid item xs={6} sm={3} key={index}>
              <Box sx={{ textAlign: 'center' }}>
                <Typography variant="body2" color="text.secondary" sx={{ mb: 1 }}>
                  {metric.label}
                </Typography>
                <LinearProgress
                  variant="determinate"
                  value={metric.value}
                  color={metric.color}
                  sx={{ height: 6, borderRadius: 3, mb: 1 }}
                />
                <Typography variant="h6" sx={{ fontWeight: 600 }}>
                  {metric.value}%
                </Typography>
              </Box>
            </Grid>
          ))}
        </Grid>

        {/* Alerts */}
        <Box sx={{ mb: 3 }}>
          <Typography variant="subtitle1" sx={{ fontWeight: 600, mb: 2 }}>
            Compliance Alerts
          </Typography>
          <Stack spacing={2}>
            {complianceData.alerts.map((alert) => (
              <Alert
                key={alert.id}
                severity={getAlertSeverity(alert.type)}
                icon={getAlertIcon(alert.type)}
                action={
                  <Button
                    color="inherit"
                    size="small"
                    onClick={() => handleAlertAction(alert)}
                    sx={{ textTransform: 'none' }}
                  >
                    {alert.action}
                  </Button>
                }
                sx={{ borderRadius: 2 }}
              >
                <Box>
                  <Typography variant="subtitle2" sx={{ fontWeight: 600, mb: 0.5 }}>
                    {alert.title}
                  </Typography>
                  <Typography variant="body2">
                    {alert.description}
                  </Typography>
                  {alert.dueDate && (
                    <Typography variant="caption" color="text.secondary" sx={{ mt: 0.5, display: 'block' }}>
                      Due: {alert.dueDate}
                    </Typography>
                  )}
                </Box>
              </Alert>
            ))}
          </Stack>
        </Box>

        {/* Pending Documents */}
        <Box sx={{ mb: 3 }}>
          <Typography variant="subtitle1" sx={{ fontWeight: 600, mb: 2, display: 'flex', alignItems: 'center', gap: 1 }}>
            <DocumentIcon color="primary" />
            Pending Documents
          </Typography>
          <List>
            {complianceData.pendingDocuments.map((doc, index) => (
              <ListItem
                key={index}
                sx={{
                  borderRadius: 2,
                  mb: 1,
                  border: '1px solid',
                  borderColor: 'divider',
                }}
              >
                <ListItemIcon>
                  <ScheduleIcon color="action" />
                </ListItemIcon>
                <ListItemText
                  primary={doc.name}
                  secondary={
                    <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mt: 0.5 }}>
                      <Chip
                        label={doc.status.replace('_', ' ')}
                        size="small"
                        color={getDocumentStatusColor(doc.status)}
                        sx={{ textTransform: 'capitalize' }}
                      />
                      <Typography variant="caption" color="text.secondary">
                        {doc.daysLeft} days left
                      </Typography>
                    </Box>
                  }
                />
              </ListItem>
            ))}
          </List>
        </Box>

        {/* AI Insights */}
        <Box
          sx={{
            p: 2,
            borderRadius: 2,
            backgroundColor: 'primary.light',
            border: '1px solid',
            borderColor: 'primary.main',
          }}
        >
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 1 }}>
            <AIIcon sx={{ color: 'primary.main' }} />
            <Typography variant="subtitle2" sx={{ fontWeight: 600, color: 'primary.main' }}>
              AI Compliance Insights
            </Typography>
          </Box>
          <List dense>
            {complianceData.aiInsights.map((insight, index) => (
              <ListItem key={index} sx={{ py: 0.5 }}>
                <ListItemText
                  primary={
                    <Typography variant="body2" color="text.secondary">
                      • {insight}
                    </Typography>
                  }
                />
              </ListItem>
            ))}
          </List>
        </Box>
      </CardContent>
    </Card>
  );
};

export default CompliancePanel;
