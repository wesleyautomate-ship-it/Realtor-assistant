import React, { useState, useEffect } from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  Grid,
  Chip,
  Stepper,
  Step,
  StepLabel,
  Button,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  LinearProgress,
  Stack,
  IconButton,
  Tooltip,
  Avatar,
} from '@mui/material';
import {
  AccountTree as WorkflowIcon,
  Assignment as TaskIcon,
  Schedule as ScheduleIcon,
  CheckCircle as CheckIcon,
  Pending as PendingIcon,
  Refresh as RefreshIcon,
  AutoAwesome as AIIcon,
  Person as PersonIcon,
  Home as HomeIcon,
} from '@mui/icons-material';

const WorkflowPanel = () => {
  const [workflowData, setWorkflowData] = useState(null);
  const [isLoading, setIsLoading] = useState(true);

  // Mock data for development - will be replaced with real API calls
  useEffect(() => {
    const loadWorkflowData = async () => {
      setIsLoading(true);
      
      // Simulate API call
      setTimeout(() => {
        setWorkflowData({
          activeTransactions: [
            {
              id: 1,
              client: 'Ali Khan',
              property: 'Villa 12, Emirates Hills',
              value: '2.5M AED',
              status: 'negotiation',
              progress: 65,
              steps: [
                { label: 'Initial Contact', completed: true },
                { label: 'Property Viewing', completed: true },
                { label: 'Offer Submitted', completed: true },
                { label: 'Negotiation', completed: false },
                { label: 'Contract Signing', completed: false },
                { label: 'Completion', completed: false },
              ],
              nextAction: 'Schedule negotiation meeting',
              dueDate: '2024-12-10'
            },
            {
              id: 2,
              client: 'Sarah Johnson',
              property: 'Apartment 45, Dubai Marina',
              value: '1.8M AED',
              status: 'viewing',
              progress: 35,
              steps: [
                { label: 'Initial Contact', completed: true },
                { label: 'Property Viewing', completed: false },
                { label: 'Offer Submitted', completed: false },
                { label: 'Negotiation', completed: false },
                { label: 'Contract Signing', completed: false },
                { label: 'Completion', completed: false },
              ],
              nextAction: 'Conduct property viewing',
              dueDate: '2024-12-08'
            }
          ],
          pendingApprovals: [
            { id: 1, type: 'CMA Report', client: 'Ahmed Al-Rashid', property: 'Villa 8, Palm Jumeirah', status: 'pending' },
            { id: 2, type: 'Contract Review', client: 'Maria Santos', property: 'Apartment 23, Downtown', status: 'in_review' },
          ],
          workflowMetrics: [
            { label: 'Active Transactions', value: 8, color: 'primary' },
            { label: 'Completion Rate', value: 78, color: 'success' },
            { label: 'Avg. Processing Time', value: 12, color: 'info', unit: 'days' },
            { label: 'Pending Approvals', value: 3, color: 'warning' },
          ],
          aiInsights: [
            "2 transactions are approaching critical deadlines",
            "Consider following up with Ali Khan for negotiation meeting",
            "Average completion time improved by 15% this month"
          ]
        });
        setIsLoading(false);
      }, 1000);
    };

    loadWorkflowData();
  }, []);

  const handleRefresh = () => {
    // TODO: Implement refresh functionality
    console.log('Refreshing workflow data...');
  };

  const handleActionClick = (transaction, action) => {
    console.log('Action clicked:', action, transaction);
    // TODO: Implement workflow actions
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'completed': return 'success';
      case 'negotiation': return 'warning';
      case 'viewing': return 'info';
      case 'pending': return 'error';
      default: return 'default';
    }
  };

  const getStatusIcon = (status) => {
    switch (status) {
      case 'completed': return <CheckIcon />;
      case 'negotiation': return <PendingIcon />;
      case 'viewing': return <ScheduleIcon />;
      case 'pending': return <TaskIcon />;
      default: return <TaskIcon />;
    }
  };

  if (isLoading) {
    return (
      <Card sx={{ borderRadius: 3, boxShadow: 3 }}>
        <CardContent>
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 2 }}>
            <WorkflowIcon color="primary" />
            <Typography variant="h6" sx={{ fontWeight: 600 }}>
              Workflow Status
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
            <WorkflowIcon color="primary" />
            <Typography variant="h6" sx={{ fontWeight: 600 }}>
              Transaction Workflow
            </Typography>
          </Box>
          <Tooltip title="Refresh Data">
            <IconButton onClick={handleRefresh} size="small">
              <RefreshIcon />
            </IconButton>
          </Tooltip>
        </Box>

        {/* Workflow Metrics */}
        <Grid container spacing={2} sx={{ mb: 3 }}>
          {workflowData.workflowMetrics.map((metric, index) => (
            <Grid item xs={6} sm={3} key={index}>
              <Box sx={{ textAlign: 'center', p: 2, borderRadius: 2, backgroundColor: 'action.hover' }}>
                <Typography variant="h4" sx={{ fontWeight: 700, color: `${metric.color}.main` }}>
                  {metric.value}{metric.unit ? ` ${metric.unit}` : ''}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  {metric.label}
                </Typography>
              </Box>
            </Grid>
          ))}
        </Grid>

        {/* Active Transactions */}
        <Box sx={{ mb: 3 }}>
          <Typography variant="subtitle1" sx={{ fontWeight: 600, mb: 2 }}>
            Active Transactions
          </Typography>
          <Stack spacing={3}>
            {workflowData.activeTransactions.map((transaction) => (
              <Box
                key={transaction.id}
                sx={{
                  p: 3,
                  borderRadius: 3,
                  border: '1px solid',
                  borderColor: 'divider',
                  backgroundColor: 'background.paper',
                }}
              >
                {/* Transaction Header */}
                <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', mb: 2 }}>
                  <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                    <Avatar sx={{ bgcolor: 'primary.main' }}>
                      <PersonIcon />
                    </Avatar>
                    <Box>
                      <Typography variant="subtitle1" sx={{ fontWeight: 600 }}>
                        {transaction.client}
                      </Typography>
                      <Typography variant="body2" color="text.secondary">
                        {transaction.property}
                      </Typography>
                    </Box>
                  </Box>
                  <Box sx={{ textAlign: 'right' }}>
                    <Typography variant="h6" sx={{ fontWeight: 600, color: 'primary.main' }}>
                      {transaction.value}
                    </Typography>
                    <Chip
                      icon={getStatusIcon(transaction.status)}
                      label={transaction.status}
                      size="small"
                      color={getStatusColor(transaction.status)}
                      sx={{ textTransform: 'capitalize' }}
                    />
                  </Box>
                </Box>

                {/* Progress Bar */}
                <Box sx={{ mb: 2 }}>
                  <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', mb: 1 }}>
                    <Typography variant="body2" color="text.secondary">
                      Progress
                    </Typography>
                    <Typography variant="body2" sx={{ fontWeight: 600 }}>
                      {transaction.progress}%
                    </Typography>
                  </Box>
                  <LinearProgress
                    variant="determinate"
                    value={transaction.progress}
                    color="primary"
                    sx={{ height: 8, borderRadius: 4 }}
                  />
                </Box>

                {/* Workflow Steps */}
                <Stepper activeStep={transaction.steps.filter(step => step.completed).length} orientation="vertical" sx={{ mb: 2 }}>
                  {transaction.steps.map((step, index) => (
                    <Step key={index}>
                      <StepLabel
                        StepIconComponent={({ active, completed }) => (
                          <Box
                            sx={{
                              width: 24,
                              height: 24,
                              borderRadius: '50%',
                              backgroundColor: completed ? 'success.main' : active ? 'primary.main' : 'action.disabled',
                              display: 'flex',
                              alignItems: 'center',
                              justifyContent: 'center',
                              color: 'white',
                              fontSize: 12,
                              fontWeight: 600,
                            }}
                          >
                            {completed ? <CheckIcon sx={{ fontSize: 16 }} /> : index + 1}
                          </Box>
                        )}
                      >
                        {step.label}
                      </StepLabel>
                    </Step>
                  ))}
                </Stepper>

                {/* Next Action */}
                <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', mt: 2 }}>
                  <Box>
                    <Typography variant="body2" color="text.secondary">
                      Next Action: {transaction.nextAction}
                    </Typography>
                    <Typography variant="caption" color="text.secondary">
                      Due: {transaction.dueDate}
                    </Typography>
                  </Box>
                  <Button
                    variant="contained"
                    size="small"
                    onClick={() => handleActionClick(transaction, 'next_action')}
                    sx={{ borderRadius: 2, textTransform: 'none' }}
                  >
                    Take Action
                  </Button>
                </Box>
              </Box>
            ))}
          </Stack>
        </Box>

        {/* Pending Approvals */}
        <Box sx={{ mb: 3 }}>
          <Typography variant="subtitle1" sx={{ fontWeight: 600, mb: 2 }}>
            Pending Approvals
          </Typography>
          <List>
            {workflowData.pendingApprovals.map((approval) => (
              <ListItem
                key={approval.id}
                sx={{
                  borderRadius: 2,
                  mb: 1,
                  border: '1px solid',
                  borderColor: 'divider',
                }}
              >
                <ListItemIcon>
                  <HomeIcon color="action" />
                </ListItemIcon>
                <ListItemText
                  primary={
                    <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                      <Typography variant="subtitle2" sx={{ fontWeight: 600 }}>
                        {approval.type}
                      </Typography>
                      <Chip
                        label={approval.status.replace('_', ' ')}
                        size="small"
                        color={getStatusColor(approval.status)}
                        sx={{ textTransform: 'capitalize' }}
                      />
                    </Box>
                  }
                  secondary={
                    <Box>
                      <Typography variant="body2" color="text.secondary">
                        {approval.client} • {approval.property}
                      </Typography>
                    </Box>
                  }
                />
                <Button
                  variant="outlined"
                  size="small"
                  onClick={() => handleActionClick(approval, 'review')}
                  sx={{ borderRadius: 2, textTransform: 'none' }}
                >
                  Review
                </Button>
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
              AI Workflow Insights
            </Typography>
          </Box>
          <List dense>
            {workflowData.aiInsights.map((insight, index) => (
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

export default WorkflowPanel;
