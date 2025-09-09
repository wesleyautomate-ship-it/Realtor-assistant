import React, { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Card,
  CardContent,
  Grid,
  Button,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  Chip,
  IconButton,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  CircularProgress,
  LinearProgress,
  Snackbar,
  Alert,
  Accordion,
  AccordionSummary,
  AccordionDetails,
  useMediaQuery,
  useTheme,
  Stack,
  Skeleton,
  Fade,
  Grow,
  Divider
} from '@mui/material';
import {
  CloudUpload as CloudUploadIcon,
  Upload as UploadIcon,
  Folder as FolderIcon,
  Assessment as AssessmentIcon,
  Delete as DeleteIcon,
  Download as DownloadIcon,
  Visibility as VisibilityIcon,
  ExpandMore as ExpandMoreIcon,
  CheckCircle as CheckCircleIcon,
  Error as ErrorIcon,
  Schedule as ScheduleIcon,
  PlayArrow as PlayArrowIcon
} from '@mui/icons-material';
import { api } from '../utils/apiClient';

const AdminFilesNew = () => {
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('md'));
  const isSmallScreen = useMediaQuery(theme.breakpoints.down('sm'));
  
  const [files, setFiles] = useState([]);
  const [loading, setLoading] = useState(true);
  const [uploadDialogOpen, setUploadDialogOpen] = useState(false);
  const [uploading, setUploading] = useState(false);
  const [snackbar, setSnackbar] = useState({ open: false, message: '', severity: 'info' });
  const [processingTasks, setProcessingTasks] = useState({});
  const [taskPollingIntervals, setTaskPollingIntervals] = useState({});
  
  // Updated upload form to include instructions instead of category
  const [uploadForm, setUploadForm] = useState({
    file: null,
    instructions: '',
    description: '',
    tags: ''
  });

  useEffect(() => {
    fetchFiles();
  }, []);

  const fetchFiles = async () => {
    try {
      setLoading(true);
      const response = await api.getAdminFiles();
      setFiles(response.files || []);
    } catch (error) {
      console.error('Error fetching files:', error);
      setSnackbar({
        open: true,
        message: 'Failed to fetch files',
        severity: 'error'
      });
    } finally {
      setLoading(false);
    }
  };

  const handleFileUpload = async () => {
    if (!uploadForm.file) return;

    try {
      setUploading(true);

      // Use the new async API function
      const result = await api.uploadFileAsync(
        uploadForm.file,
        uploadForm.instructions
      );
      
      if (result.task_id) {
        // Start polling for task status
        startTaskPolling(result.task_id);
        
        // Add task to processing tasks
        setProcessingTasks(prev => ({
          ...prev,
          [result.task_id]: {
            filename: uploadForm.file.name,
            status: 'processing',
            progress: 0,
            created_at: new Date().toISOString()
          }
        }));

        setSnackbar({
          open: true,
          message: `File processing started. Task ID: ${result.task_id}`,
          severity: 'success'
        });
      }

      setUploadDialogOpen(false);
      setUploadForm({ file: null, instructions: '', description: '', tags: '' });
      
    } catch (error) {
      console.error('Error uploading file:', error);
      const errorMessage = error.message || 'Failed to upload file';
      setSnackbar({
        open: true,
        message: `Failed to upload file: ${errorMessage}`,
        severity: 'error'
      });
    } finally {
      setUploading(false);
    }
  };

  const startTaskPolling = (taskId) => {
    const interval = setInterval(async () => {
      try {
        const taskStatus = await api.getProcessingStatus(taskId);
        
        setProcessingTasks(prev => ({
          ...prev,
          [taskId]: {
            ...prev[taskId],
            ...taskStatus
          }
        }));

        // If task is completed or failed, stop polling
        if (taskStatus.status === 'completed' || taskStatus.status === 'failed') {
          clearInterval(interval);
          setTaskPollingIntervals(prev => {
            const newIntervals = { ...prev };
            delete newIntervals[taskId];
            return newIntervals;
          });

          // Refresh files list if task completed successfully
          if (taskStatus.status === 'completed') {
            fetchFiles();
          }
        }
      } catch (error) {
        console.error('Error polling task status:', error);
      }
    }, 2000); // Poll every 2 seconds

    setTaskPollingIntervals(prev => ({
      ...prev,
      [taskId]: interval
    }));
  };

  const handleCloseSnackbar = () => {
    setSnackbar({ ...snackbar, open: false });
  };

  const formatFileSize = (bytes) => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };

  // Skeleton loader for files
  const FileSkeleton = () => (
    <Box sx={{ p: theme.spacing(2) }}>
      <Stack spacing={2}>
        {[1, 2, 3].map((item) => (
          <Card key={item} variant="outlined">
            <CardContent>
              <Stack spacing={1}>
                <Skeleton variant="text" width="60%" height={24} />
                <Skeleton variant="text" width="40%" height={16} />
                <Stack direction="row" spacing={1}>
                  <Skeleton variant="rectangular" width={60} height={24} />
                  <Skeleton variant="rectangular" width={80} height={24} />
                </Stack>
              </Stack>
            </CardContent>
          </Card>
        ))}
      </Stack>
    </Box>
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
      <FolderIcon 
        sx={{ 
          fontSize: 64, 
          color: 'text.secondary',
          mb: theme.spacing(2)
        }} 
      />
      <Typography variant="h6" color="text.secondary" gutterBottom>
        No files uploaded yet
      </Typography>
      <Typography variant="body2" color="text.secondary" sx={{ mb: theme.spacing(3) }}>
        Get started by uploading your first document for intelligent processing and analysis.
      </Typography>
      <Button
        variant="contained"
        startIcon={<UploadIcon />}
        onClick={() => setUploadDialogOpen(true)}
      >
        Upload First File
      </Button>
    </Box>
  );

  // Mobile file card component
  const MobileFileCard = ({ file }) => (
    <Grow in={true} timeout={300}>
      <Card 
        variant="outlined" 
        sx={{ 
          mb: theme.spacing(2),
          '&:hover': {
            boxShadow: theme.shadows[2],
            transition: theme.transitions.create(['box-shadow'], {
              duration: theme.transitions.duration.shortest,
            }),
          }
        }}
      >
        <CardContent>
          <Stack spacing={1.5}>
            <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
              <Box sx={{ flex: 1, minWidth: 0 }}>
                <Typography variant="subtitle1" sx={{ fontWeight: 600, mb: 0.5 }}>
                  {file.name}
                </Typography>
                <Typography variant="body2" color="text.secondary" sx={{ mb: 1 }}>
                  {file.description || 'No description'}
                </Typography>
              </Box>
              <Stack direction="row" spacing={0.5}>
                <IconButton 
                  size="small" 
                  color="primary"
                  sx={{ 
                    p: theme.spacing(1),
                    '&:hover': { backgroundColor: 'primary.light' }
                  }}
                >
                  <VisibilityIcon fontSize="small" />
                </IconButton>
                <IconButton 
                  size="small" 
                  color="primary"
                  sx={{ 
                    p: theme.spacing(1),
                    '&:hover': { backgroundColor: 'primary.light' }
                  }}
                >
                  <DownloadIcon fontSize="small" />
                </IconButton>
                <IconButton 
                  size="small" 
                  color="error"
                  sx={{ 
                    p: theme.spacing(1),
                    '&:hover': { backgroundColor: 'error.light' }
                  }}
                >
                  <DeleteIcon fontSize="small" />
                </IconButton>
              </Stack>
            </Box>
            
            <Stack direction="row" spacing={1} flexWrap="wrap" useFlexGap>
              <Chip 
                label={file.category} 
                size="small" 
                color="primary"
                variant="outlined"
              />
              <Chip 
                label={formatFileSize(file.size)} 
                size="small" 
                variant="outlined"
              />
            </Stack>
            
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
              {getStatusIcon(file.status)}
              <Typography variant="body2" color="text.secondary">
                {file.status}
              </Typography>
            </Box>
            
            <Typography variant="caption" color="text.secondary">
              Uploaded: {new Date(file.upload_date).toLocaleDateString()}
            </Typography>
          </Stack>
        </CardContent>
      </Card>
    </Grow>
  );

  const getStatusIcon = (status) => {
    switch (status) {
      case 'completed':
        return <CheckCircleIcon color="success" />;
      case 'processing':
        return <PlayArrowIcon color="primary" />;
      case 'failed':
        return <ErrorIcon color="error" />;
      default:
        return <ScheduleIcon color="action" />;
    }
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'completed':
        return 'success';
      case 'processing':
        return 'primary';
      case 'failed':
        return 'error';
      default:
        return 'default';
    }
  };

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h4" sx={{ mb: 3, fontWeight: 'bold' }}>
        File Hub - Advanced AI Data Router
      </Typography>
      
      <Typography variant="body1" color="text.secondary" sx={{ mb: 4 }}>
        Upload documents with natural language instructions for intelligent processing and analysis.
      </Typography>

      {/* Processing Tasks Section */}
      {Object.keys(processingTasks).length > 0 && (
        <Card sx={{ mb: 3 }}>
          <CardContent>
            <Typography variant="h6" sx={{ mb: 2 }}>
              Processing Tasks
            </Typography>
            {Object.entries(processingTasks).map(([taskId, task]) => (
              <Accordion key={taskId} sx={{ mb: 1 }}>
                <AccordionSummary expandIcon={<ExpandMoreIcon />}>
                  <Box sx={{ display: 'flex', alignItems: 'center', width: '100%' }}>
                    {getStatusIcon(task.status)}
                    <Typography sx={{ ml: 1, flexGrow: 1 }}>
                      {task.filename}
                    </Typography>
                    <Chip 
                      label={task.status} 
                      color={getStatusColor(task.status)}
                      size="small"
                      sx={{ mr: 1 }}
                    />
                    {task.status === 'processing' && (
                      <Typography variant="body2" color="text.secondary">
                        {Math.round(task.progress * 100)}%
                      </Typography>
                    )}
                  </Box>
                </AccordionSummary>
                <AccordionDetails>
                  {task.status === 'processing' && (
                    <Box sx={{ mb: 2 }}>
                      <LinearProgress 
                        variant="determinate" 
                        value={task.progress * 100} 
                        sx={{ mb: 1 }}
                      />
                      <Typography variant="body2" color="text.secondary">
                        Processing in progress...
                      </Typography>
                    </Box>
                  )}
                  
                  {task.status === 'completed' && task.result && (
                    <Box>
                      <Typography variant="subtitle2" sx={{ mb: 1 }}>
                        Processing Report
                      </Typography>
                      
                      {task.result.execution_plan && (
                        <Box sx={{ mb: 2 }}>
                          <Typography variant="body2" fontWeight="bold">
                            AI Execution Plan:
                          </Typography>
                          <Typography variant="body2" color="text.secondary">
                            Category: {task.result.execution_plan.category} 
                            (Confidence: {Math.round(task.result.execution_plan.confidence * 100)}%)
                          </Typography>
                        </Box>
                      )}
                      
                      {task.result.storage_summary && (
                        <Box sx={{ mb: 2 }}>
                          <Typography variant="body2" fontWeight="bold">
                            Storage Summary:
                          </Typography>
                          <Typography variant="body2" color="text.secondary">
                            Total records stored: {task.result.storage_summary.total_records_stored || 0}
                          </Typography>
                        </Box>
                      )}
                      
                      {task.result.performance_metrics && (
                        <Box>
                          <Typography variant="body2" fontWeight="bold">
                            Performance:
                          </Typography>
                          <Typography variant="body2" color="text.secondary">
                            Processing time: {task.result.performance_metrics.total_processing_time_seconds?.toFixed(2)}s
                          </Typography>
                        </Box>
                      )}
                    </Box>
                  )}
                  
                  {task.status === 'failed' && (
                    <Typography variant="body2" color="error">
                      Error: {task.error_message || 'Unknown error occurred'}
                    </Typography>
                  )}
                </AccordionDetails>
              </Accordion>
            ))}
          </CardContent>
        </Card>
      )}

      <Grid container spacing={3}>
        {/* File Upload Section */}
        <Grid item xs={12} lg={4} md={5}>
          <Stack spacing={3}>
            <Card>
              <CardContent>
                <Box sx={{ display: 'flex', alignItems: 'center', mb: theme.spacing(3) }}>
                  <CloudUploadIcon color="primary" sx={{ mr: theme.spacing(1) }} />
                  <Typography variant="h6">Upload New File</Typography>
                </Box>
                
                <Button
                  fullWidth
                  variant="contained"
                  startIcon={<UploadIcon />}
                  onClick={() => setUploadDialogOpen(true)}
                  sx={{ 
                    mb: theme.spacing(2),
                    py: theme.spacing(1.5),
                    borderRadius: 2
                  }}
                >
                  Upload Document
                </Button>
                
                <Typography variant="body2" color="text.secondary">
                  Upload documents with natural language instructions for intelligent processing and analysis.
                </Typography>
              </CardContent>
            </Card>

            {/* Categories */}
            <Card>
              <CardContent>
                <Typography variant="h6" sx={{ mb: theme.spacing(2) }}>
                  Categories
                </Typography>
                <List dense>
                  {mockStats.categories.map((category) => (
                    <ListItem key={category.name}>
                      <ListItemIcon>
                        <FolderIcon color="primary" />
                      </ListItemIcon>
                      <ListItemText
                        primary={category.name}
                        secondary={`${category.count} files • ${category.size}`}
                      />
                    </ListItem>
                  ))}
                </List>
              </CardContent>
            </Card>
          </Stack>
        </Grid>

        {/* Files Section */}
        <Grid item xs={12} lg={8} md={7}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: theme.spacing(3) }}>
                <AssessmentIcon color="primary" sx={{ mr: theme.spacing(1) }} />
                <Typography variant="h6">Recent Files</Typography>
              </Box>

              {loading ? (
                <FileSkeleton />
              ) : files.length === 0 ? (
                <EmptyState />
              ) : isMobile ? (
                // Mobile: Card list view
                <Stack spacing={2}>
                  {files.map((file) => (
                    <MobileFileCard key={file.id} file={file} />
                  ))}
                </Stack>
              ) : (
                // Desktop: Table view
                <Fade in={true} timeout={500}>
                  <TableContainer component={Paper} variant="outlined">
                    <Table>
                      <TableHead>
                        <TableRow>
                          <TableCell>File</TableCell>
                          <TableCell>Category</TableCell>
                          <TableCell>Size</TableCell>
                          <TableCell>Status</TableCell>
                          <TableCell>Upload Date</TableCell>
                          <TableCell>Actions</TableCell>
                        </TableRow>
                      </TableHead>
                      <TableBody>
                        {files.map((file) => (
                          <TableRow key={file.id} hover>
                            <TableCell>
                              <Box>
                                <Typography variant="body2" sx={{ fontWeight: 500 }}>
                                  {file.name}
                                </Typography>
                                <Typography variant="caption" color="text.secondary">
                                  {file.description}
                                </Typography>
                              </Box>
                            </TableCell>
                            <TableCell>
                              <Chip label={file.category} size="small" />
                            </TableCell>
                            <TableCell>
                              <Typography variant="body2">
                                {formatFileSize(file.size)}
                              </Typography>
                            </TableCell>
                            <TableCell>
                              <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                                {getStatusIcon(file.status)}
                                <Typography variant="body2">
                                  {file.status}
                                </Typography>
                              </Box>
                            </TableCell>
                            <TableCell>
                              <Typography variant="body2">
                                {new Date(file.upload_date).toLocaleDateString()}
                              </Typography>
                            </TableCell>
                            <TableCell>
                              <Stack direction="row" spacing={0.5}>
                                <IconButton 
                                  size="small" 
                                  color="primary"
                                  sx={{ 
                                    p: theme.spacing(1),
                                    '&:hover': { backgroundColor: 'primary.light' }
                                  }}
                                >
                                  <VisibilityIcon />
                                </IconButton>
                                <IconButton 
                                  size="small" 
                                  color="primary"
                                  sx={{ 
                                    p: theme.spacing(1),
                                    '&:hover': { backgroundColor: 'primary.light' }
                                  }}
                                >
                                  <DownloadIcon />
                                </IconButton>
                                <IconButton 
                                  size="small" 
                                  color="error"
                                  sx={{ 
                                    p: theme.spacing(1),
                                    '&:hover': { backgroundColor: 'error.light' }
                                  }}
                                >
                                  <DeleteIcon />
                                </IconButton>
                              </Stack>
                            </TableCell>
                          </TableRow>
                        ))}
                      </TableBody>
                    </Table>
                  </TableContainer>
                </Fade>
              )}
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Upload Dialog */}
      <Dialog 
        open={uploadDialogOpen} 
        onClose={() => setUploadDialogOpen(false)}
        maxWidth="sm"
        fullWidth
      >
        <DialogTitle>Upload Document with AI Processing</DialogTitle>
        <DialogContent>
          <Box sx={{ mb: 3 }}>
            <input
              type="file"
              onChange={(e) => setUploadForm(prev => ({ ...prev, file: e.target.files[0] }))}
              accept=".pdf,.docx,.xlsx,.txt,.csv"
              style={{ width: '100%', padding: '10px', border: '1px solid #ccc', borderRadius: '4px' }}
            />
          </Box>

          {/* Instructions Text Area - Replaces Category Dropdown */}
          <TextField
            fullWidth
            label="Processing Instructions (Optional)"
            value={uploadForm.instructions}
            onChange={(e) => setUploadForm(prev => ({ ...prev, instructions: e.target.value }))}
            multiline
            rows={3}
            placeholder="Provide specific instructions for how you want this document processed. For example: 'Focus on extracting property prices and transaction dates' or 'Classify this as a market report and extract key trends'"
            sx={{ mb: 2 }}
          />

          <TextField
            fullWidth
            label="Description"
            value={uploadForm.description}
            onChange={(e) => setUploadForm(prev => ({ ...prev, description: e.target.value }))}
            multiline
            rows={2}
            sx={{ mb: 2 }}
          />

          <TextField
            fullWidth
            label="Tags (comma-separated)"
            value={uploadForm.tags}
            onChange={(e) => setUploadForm(prev => ({ ...prev, tags: e.target.value }))}
            placeholder="market-analysis, dubai, 2024"
            sx={{ mb: 2 }}
          />

          {uploading && (
            <Box sx={{ mt: 2 }}>
              <LinearProgress />
              <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
                Uploading and initiating processing...
              </Typography>
            </Box>
          )}
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setUploadDialogOpen(false)}>Cancel</Button>
          <Button
            onClick={handleFileUpload}
            variant="contained"
            disabled={!uploadForm.file || uploading}
          >
            Upload & Process
          </Button>
        </DialogActions>
      </Dialog>

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

export default AdminFilesNew;
