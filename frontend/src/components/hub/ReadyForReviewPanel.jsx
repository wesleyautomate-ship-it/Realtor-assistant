import React, { useState, useEffect } from 'react';
import {
  Box,
  Card,
  CardContent,
  CardHeader,
  Typography,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  Chip,
  IconButton,
  Tooltip,
  CircularProgress,
  Alert,
  Stack,
  Divider,
  Button,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
} from '@mui/material';
import {
  Assignment as AssignmentIcon,
  CheckCircle as CheckCircleIcon,
  Visibility as VisibilityIcon,
  Edit as EditIcon,
  Approve as ApproveIcon,
  Reject as RejectIcon,
  Refresh as RefreshIcon,
  Description as DescriptionIcon,
  Assessment as AssessmentIcon,
  TrendingUp as TrendingUpIcon,
} from '@mui/icons-material';
import { useAuth } from '../../context/AuthContext';
import { apiClient } from '../../utils/apiClient';

const ReadyForReviewPanel = () => {
  const { user } = useAuth();
  const [reviewItems, setReviewItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [selectedItem, setSelectedItem] = useState(null);
  const [previewOpen, setPreviewOpen] = useState(false);

  useEffect(() => {
    fetchReviewItems();
  }, []);

  const fetchReviewItems = async () => {
    try {
      setLoading(true);
      setError(null);
      
      // Try to fetch from backend first
      try {
        const response = await apiClient.get('/ml/automated-reports/ready-for-review');
        setReviewItems(response.data || []);
      } catch (apiError) {
        console.log('Using mock review data');
        // Fallback to mock data
        setReviewItems(generateMockReviewItems());
      }
    } catch (error) {
      console.error('Error fetching review items:', error);
      setError('Failed to load review items');
      setReviewItems(generateMockReviewItems());
    } finally {
      setLoading(false);
    }
  };

  const generateMockReviewItems = () => [
    {
      id: 1,
      title: 'Market Analysis Report - Downtown Dubai',
      type: 'market_report',
      status: 'pending_review',
      priority: 'high',
      generatedAt: '2024-01-15T10:30:00Z',
      description: 'Comprehensive market analysis for Downtown Dubai properties',
      content: 'This report analyzes recent sales trends, price movements, and market dynamics in Downtown Dubai...',
      generatedBy: 'AI Market Intelligence',
      estimatedReviewTime: '15 min'
    },
    {
      id: 2,
      title: 'Property Valuation - Marina Views Tower',
      type: 'valuation',
      status: 'pending_review',
      priority: 'medium',
      generatedAt: '2024-01-15T09:15:00Z',
      description: 'AI-generated property valuation with market comparisons',
      content: 'Based on recent sales data and market trends, this property is valued at AED 2.8M...',
      generatedBy: 'AI Valuation Engine',
      estimatedReviewTime: '10 min'
    },
    {
      id: 3,
      title: 'Lead Nurturing Campaign - Palm Jumeirah',
      type: 'campaign',
      status: 'pending_review',
      priority: 'low',
      generatedAt: '2024-01-15T08:45:00Z',
      description: 'Automated lead nurturing sequence for Palm Jumeirah prospects',
      content: 'This campaign targets high-value prospects with personalized content...',
      generatedBy: 'AI Lead Nurturing',
      estimatedReviewTime: '8 min'
    },
    {
      id: 4,
      title: 'Performance Analytics - Q4 2024',
      type: 'analytics',
      status: 'pending_review',
      priority: 'high',
      generatedAt: '2024-01-15T07:30:00Z',
      description: 'Quarterly performance analysis and insights',
      content: 'Q4 2024 shows strong growth in property viewings and client engagement...',
      generatedBy: 'AI Analytics Engine',
      estimatedReviewTime: '20 min'
    }
  ];

  const getTypeIcon = (type) => {
    switch (type) {
      case 'market_report':
        return <AssessmentIcon color="primary" />;
      case 'valuation':
        return <TrendingUpIcon color="success" />;
      case 'campaign':
        return <DescriptionIcon color="info" />;
      case 'analytics':
        return <AssessmentIcon color="secondary" />;
      default:
        return <DescriptionIcon color="action" />;
    }
  };

  const getTypeColor = (type) => {
    switch (type) {
      case 'market_report':
        return 'primary';
      case 'valuation':
        return 'success';
      case 'campaign':
        return 'info';
      case 'analytics':
        return 'secondary';
      default:
        return 'default';
    }
  };

  const getPriorityColor = (priority) => {
    switch (priority) {
      case 'high':
        return 'error';
      case 'medium':
        return 'warning';
      case 'low':
        return 'default';
      default:
        return 'default';
    }
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleString('en-US', {
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  const handlePreview = (item) => {
    setSelectedItem(item);
    setPreviewOpen(true);
  };

  const handleApprove = (itemId) => {
    // TODO: Implement approve functionality
    console.log('Approve item:', itemId);
    setReviewItems(prev => prev.filter(item => item.id !== itemId));
  };

  const handleReject = (itemId) => {
    // TODO: Implement reject functionality
    console.log('Reject item:', itemId);
    setReviewItems(prev => prev.filter(item => item.id !== itemId));
  };

  const handleEdit = (itemId) => {
    // TODO: Implement edit functionality
    console.log('Edit item:', itemId);
  };

  const handleRefresh = () => {
    fetchReviewItems();
  };

  if (loading) {
    return (
      <Card>
        <CardContent>
          <Box sx={{ display: 'flex', justifyContent: 'center', py: 3 }}>
            <CircularProgress />
          </Box>
        </CardContent>
      </Card>
    );
  }

  return (
    <>
      <Card sx={{ height: '100%' }}>
        <CardHeader
          title={
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
              <AssignmentIcon color="primary" />
              <Typography variant="h6">Ready for Review</Typography>
            </Box>
          }
          action={
            <Tooltip title="Refresh">
              <IconButton size="small" onClick={handleRefresh}>
                <RefreshIcon />
              </IconButton>
            </Tooltip>
          }
          subheader={`${reviewItems.length} items awaiting review`}
        />
        <CardContent sx={{ pt: 0 }}>
          {error && (
            <Alert severity="error" sx={{ mb: 2 }}>
              {error}
            </Alert>
          )}

          {reviewItems.length === 0 ? (
            <Box sx={{ textAlign: 'center', py: 3 }}>
              <CheckCircleIcon sx={{ fontSize: 48, color: 'success.main', mb: 1 }} />
              <Typography variant="body2" color="text.secondary">
                All caught up! No items pending review.
              </Typography>
            </Box>
          ) : (
            <List sx={{ p: 0 }}>
              {reviewItems.map((item, index) => (
                <React.Fragment key={item.id}>
                  <ListItem sx={{ px: 0, py: 1 }}>
                    <ListItemIcon sx={{ minWidth: 40 }}>
                      {getTypeIcon(item.type)}
                    </ListItemIcon>
                    <ListItemText
                      primary={
                        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 0.5 }}>
                          <Typography variant="subtitle2" sx={{ fontWeight: 600 }}>
                            {item.title}
                          </Typography>
                          <Chip
                            label={item.estimatedReviewTime}
                            size="small"
                            variant="outlined"
                            sx={{ fontSize: '0.7rem' }}
                          />
                        </Box>
                      }
                      secondary={
                        <Stack direction="row" spacing={1} alignItems="center" sx={{ mb: 1 }}>
                          <Chip
                            label={item.type.replace('_', ' ')}
                            size="small"
                            color={getTypeColor(item.type)}
                            sx={{ textTransform: 'capitalize', fontSize: '0.7rem' }}
                          />
                          <Chip
                            label={item.priority}
                            size="small"
                            color={getPriorityColor(item.priority)}
                            sx={{ textTransform: 'capitalize', fontSize: '0.7rem' }}
                          />
                          <Typography variant="caption" color="text.secondary">
                            {formatDate(item.generatedAt)} • {item.generatedBy}
                          </Typography>
                        </Stack>
                      }
                    />
                    <Box sx={{ display: 'flex', gap: 0.5 }}>
                      <Tooltip title="Preview">
                        <IconButton size="small" onClick={() => handlePreview(item)}>
                          <VisibilityIcon />
                        </IconButton>
                      </Tooltip>
                      <Tooltip title="Edit">
                        <IconButton size="small" onClick={() => handleEdit(item.id)}>
                          <EditIcon />
                        </IconButton>
                      </Tooltip>
                      <Tooltip title="Approve">
                        <IconButton 
                          size="small" 
                          color="success"
                          onClick={() => handleApprove(item.id)}
                        >
                          <ApproveIcon />
                        </IconButton>
                      </Tooltip>
                      <Tooltip title="Reject">
                        <IconButton 
                          size="small" 
                          color="error"
                          onClick={() => handleReject(item.id)}
                        >
                          <RejectIcon />
                        </IconButton>
                      </Tooltip>
                    </Box>
                  </ListItem>
                  {index < reviewItems.length - 1 && <Divider />}
                </React.Fragment>
              ))}
            </List>
          )}
        </CardContent>
      </Card>

      {/* Preview Dialog */}
      <Dialog 
        open={previewOpen} 
        onClose={() => setPreviewOpen(false)}
        maxWidth="md"
        fullWidth
      >
        <DialogTitle>
          {selectedItem?.title}
        </DialogTitle>
        <DialogContent>
          <Stack spacing={2}>
            <Box>
              <Typography variant="subtitle2" color="text.secondary" gutterBottom>
                Description
              </Typography>
              <Typography variant="body2">
                {selectedItem?.description}
              </Typography>
            </Box>
            <Box>
              <Typography variant="subtitle2" color="text.secondary" gutterBottom>
                Content Preview
              </Typography>
              <Typography variant="body2">
                {selectedItem?.content}
              </Typography>
            </Box>
            <Box>
              <Typography variant="subtitle2" color="text.secondary" gutterBottom>
                Generated By
              </Typography>
              <Typography variant="body2">
                {selectedItem?.generatedBy} on {selectedItem?.generatedAt ? formatDate(selectedItem.generatedAt) : 'N/A'}
              </Typography>
            </Box>
          </Stack>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setPreviewOpen(false)}>Close</Button>
          <Button 
            onClick={() => selectedItem && handleEdit(selectedItem.id)}
            startIcon={<EditIcon />}
          >
            Edit
          </Button>
          <Button 
            onClick={() => selectedItem && handleApprove(selectedItem.id)}
            color="success"
            startIcon={<ApproveIcon />}
          >
            Approve
          </Button>
          <Button 
            onClick={() => selectedItem && handleReject(selectedItem.id)}
            color="error"
            startIcon={<RejectIcon />}
          >
            Reject
          </Button>
        </DialogActions>
      </Dialog>
    </>
  );
};

export default ReadyForReviewPanel;
