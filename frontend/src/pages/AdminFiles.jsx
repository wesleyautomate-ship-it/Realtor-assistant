import React, { useState, useEffect, useCallback } from 'react';
import {
  Box,
  Typography,
  Card,
  CardContent,
  Grid,
  Button,
  List,
  ListItem,
  ListItemText,
  ListItemIcon,
  Chip,
  CircularProgress,
  Alert,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Input,
  LinearProgress,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  IconButton,
  Tooltip,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  TextField,
  Snackbar,
  // Enhanced upload components
  DropzoneArea,
  ListItemAvatar,
  Avatar,
  Divider,
  Accordion,
  AccordionSummary,
  AccordionDetails,
  Tabs,
  Tab,
} from '@mui/material';
import {
  Upload as UploadIcon,
  Folder as FolderIcon,
  Delete as DeleteIcon,
  Visibility as ViewIcon,
  Download as DownloadIcon,
  CloudUpload as CloudUploadIcon,
  Storage as StorageIcon,
  Assessment as AssessmentIcon,
  Security as SecurityIcon,
  Speed as SpeedIcon,
  CheckCircle as CheckCircleIcon,
  Error as ErrorIcon,
  Info as InfoIcon,
  // Enhanced icons
  ExpandMore as ExpandMoreIcon,
  Image as ImageIcon,
  Description as DescriptionIcon,
  TableChart as TableChartIcon,
  TextFields as TextFieldsIcon,
  DragIndicator as DragIndicatorIcon,
  Add as AddIcon,
  Close as CloseIcon,
} from '@mui/icons-material';
import { useAppContext } from '../context/AppContext';
import { api } from '../utils/apiClient';

const AdminFiles = () => {
  const { currentUser } = useAppContext();
  const [files, setFiles] = useState([]);
  const [uploadDialogOpen, setUploadDialogOpen] = useState(false);
  const [uploading, setUploading] = useState(false);
  const [uploadProgress, setUploadProgress] = useState(0);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [snackbar, setSnackbar] = useState({ open: false, message: '', severity: 'info' });
  const [uploadForm, setUploadForm] = useState({
    files: [],
    category: '',
    description: '',
    tags: '',
    processingInstructions: '',
  });
  const [processingTasks, setProcessingTasks] = useState({});
  const [activeTab, setActiveTab] = useState(0);

  // Enhanced categories based on documentation
  const categories = [
    { value: 'market-reports', label: 'Market Reports', icon: <AssessmentIcon /> },
    { value: 'property-data', label: 'Property Data', icon: <TableChartIcon /> },
    { value: 'legal-documents', label: 'Legal Documents', icon: <SecurityIcon /> },
    { value: 'investment-guides', label: 'Investment Guides', icon: <InfoIcon /> },
    { value: 'property-images', label: 'Property Images', icon: <ImageIcon /> },
    { value: 'contracts', label: 'Contracts', icon: <DescriptionIcon /> },
    { value: 'financial-data', label: 'Financial Data', icon: <TableChartIcon /> },
    { value: 'market-analysis', label: 'Market Analysis', icon: <AssessmentIcon /> },
    { value: 'development-plans', label: 'Development Plans', icon: <InfoIcon /> },
    { value: 'regulatory-docs', label: 'Regulatory Documents', icon: <SecurityIcon /> },
    { value: 'uncategorized', label: 'Uncategorized', icon: <FolderIcon /> },
  ];

  // Real data state
  const [stats, setStats] = useState({
    totalFiles: 0,
    totalSize: '0 B',
    processedFiles: 0,
    processingFiles: 0,
    errorFiles: 0,
    categories: [],
  });

  useEffect(() => {
    fetchFiles();
  }, []);

  const fetchFiles = async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await api.getAdminFiles();
      setFiles(response.files || []);
      
      // Calculate stats from real data
      const totalFiles = response.files?.length || 0;
      const totalSize = response.files?.reduce((sum, file) => sum + (file.size || 0), 0) || 0;
      const processedFiles = response.files?.filter(f => f.status === 'processed').length || 0;
      const processingFiles = response.files?.filter(f => f.status === 'processing').length || 0;
      const errorFiles = response.files?.filter(f => f.status === 'error').length || 0;
      
      // Group by category
      const categoryMap = {};
      response.files?.forEach(file => {
        const category = file.category || 'Uncategorized';
        if (!categoryMap[category]) {
          categoryMap[category] = { count: 0, size: 0 };
        }
        categoryMap[category].count++;
        categoryMap[category].size += file.size || 0;
      });
      
      const categories = Object.entries(categoryMap).map(([name, data]) => ({
        name,
        count: data.count,
        size: formatFileSize(data.size)
      }));
      
      setStats({
        totalFiles,
        totalSize: formatFileSize(totalSize),
        processedFiles,
        processingFiles,
        errorFiles,
        categories
      });
    } catch (error) {
      console.error('Error fetching files:', error);
      setError('Failed to load files');
      setFiles([]);
    } finally {
      setLoading(false);
    }
  };

  // Enhanced file upload with multiple files support
  const handleFileUpload = async () => {
    if (!uploadForm.files.length) return;

    try {
    setUploading(true);
    setUploadProgress(0);

      const totalFiles = uploadForm.files.length;
      let uploadedCount = 0;

      for (const file of uploadForm.files) {
        // Create FormData for each file
        const formData = new FormData();
        formData.append('file', file);
        formData.append('category', uploadForm.category || 'uncategorized');
        formData.append('description', uploadForm.description || '');
        formData.append('tags', uploadForm.tags || '');
        formData.append('processingInstructions', uploadForm.processingInstructions || '');

        // Upload file using the new endpoint
        const response = await fetch(`${process.env.REACT_APP_API_URL || 'http://localhost:8003'}/upload`, {
          method: 'POST',
          body: formData,
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('authToken')}`
          }
        });

        if (!response.ok) {
          throw new Error(`Upload failed for ${file.name}: ${response.statusText}`);
        }

        uploadedCount++;
        setUploadProgress((uploadedCount / totalFiles) * 100);
      }

      // Reset form and close dialog
      setUploadForm({
        files: [],
        category: '',
        description: '',
        tags: '',
        processingInstructions: '',
      });
      setUploadDialogOpen(false);

      // Refresh file list
      await fetchFiles();
      
      setSnackbar({
        open: true,
        message: `Successfully uploaded ${uploadedCount} file(s)`,
        severity: 'success',
      });

    } catch (error) {
      console.error('Upload error:', error);
      setSnackbar({
        open: true,
        message: `Upload failed: ${error.message}`,
        severity: 'error',
      });
    } finally {
      setUploading(false);
      setUploadProgress(0);
    }
  };

  // Handle file selection
  const handleFileSelect = useCallback((acceptedFiles) => {
    setUploadForm(prev => ({
      ...prev,
      files: [...prev.files, ...acceptedFiles]
    }));
  }, []);

  // Handle file removal
  const handleFileRemove = (index) => {
    setUploadForm(prev => ({
      ...prev,
      files: prev.files.filter((_, i) => i !== index)
    }));
  };

  // Handle drag and drop
  const handleDrop = useCallback((acceptedFiles) => {
    handleFileSelect(acceptedFiles);
  }, [handleFileSelect]);

  const formatFileSize = (bytes) => {
    if (bytes === 0) return '0 B';
    const k = 1024;
    const sizes = ['B', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };

  const formatDate = (dateString) => {
    if (!dateString) return 'N/A';
    try {
      return new Date(dateString).toLocaleDateString();
    } catch {
      return 'N/A';
    }
  };

  const handleCloseSnackbar = () => {
    setSnackbar({ ...snackbar, open: false });
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'processed': return 'success';
      case 'processing': return 'warning';
      case 'error': return 'error';
      default: return 'default';
    }
  };

  const getStatusIcon = (status) => {
    switch (status) {
      case 'processed': return <CheckCircleIcon />;
      case 'processing': return <CircularProgress size={16} />;
      case 'error': return <ErrorIcon />;
      default: return <InfoIcon />;
    }
  };

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="400px">
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h4" gutterBottom>
        File Hub
        </Typography>

      {/* Stats Cards */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Box display="flex" alignItems="center">
                <StorageIcon color="primary" sx={{ mr: 2 }} />
                <Box>
                  <Typography variant="h6">{stats.totalFiles}</Typography>
                  <Typography variant="body2" color="text.secondary">Total Files</Typography>
                </Box>
              </Box>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Box display="flex" alignItems="center">
                <CheckCircleIcon color="success" sx={{ mr: 2 }} />
                <Box>
                  <Typography variant="h6">{stats.processedFiles}</Typography>
                  <Typography variant="body2" color="text.secondary">Processed</Typography>
                </Box>
              </Box>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Box display="flex" alignItems="center">
                <SpeedIcon color="warning" sx={{ mr: 2 }} />
                <Box>
                  <Typography variant="h6">{stats.processingFiles}</Typography>
                  <Typography variant="body2" color="text.secondary">Processing</Typography>
                </Box>
              </Box>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Box display="flex" alignItems="center">
                <ErrorIcon color="error" sx={{ mr: 2 }} />
                <Box>
                  <Typography variant="h6">{stats.errorFiles}</Typography>
                  <Typography variant="body2" color="text.secondary">Errors</Typography>
                </Box>
              </Box>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Action Buttons */}
      <Box sx={{ mb: 3, display: 'flex', gap: 2 }}>
              <Button
                variant="contained"
          startIcon={<CloudUploadIcon />}
                onClick={() => setUploadDialogOpen(true)}
        >
          Upload Files
        </Button>
        <Button
          variant="outlined"
          startIcon={<AssessmentIcon />}
          onClick={fetchFiles}
        >
          Refresh
              </Button>
      </Box>

      {/* Error Display */}
      {error && (
        <Alert severity="error" sx={{ mb: 3 }}>
          {error}
        </Alert>
      )}

      {/* Files Table */}
      <Card>
        <CardContent>
          <Typography variant="h6" gutterBottom>
            Document Categories
          </Typography>
          <Grid container spacing={2}>
            {stats.categories.map((category) => (
              <Grid item xs={12} sm={6} md={4} key={category.name}>
                <Card variant="outlined">
                  <CardContent>
                    <Typography variant="subtitle1">{category.name}</Typography>
              <Typography variant="body2" color="text.secondary">
                      {category.count} files • {category.size}
              </Typography>
            </CardContent>
          </Card>
              </Grid>
            ))}
          </Grid>
            </CardContent>
          </Card>

        {/* Files Table */}
      <Card sx={{ mt: 3 }}>
            <CardContent>
          <Typography variant="h6" gutterBottom>
            All Files
          </Typography>
          <TableContainer>
                  <Table>
                    <TableHead>
                      <TableRow>
                  <TableCell>File Name</TableCell>
                        <TableCell>Category</TableCell>
                        <TableCell>Size</TableCell>
                        <TableCell>Status</TableCell>
                        <TableCell>Upload Date</TableCell>
                        <TableCell>Actions</TableCell>
                      </TableRow>
                    </TableHead>
                    <TableBody>
                      {files.map((file) => (
                        <TableRow key={file.id}>
                          <TableCell>
                      <Box display="flex" alignItems="center">
                        <FolderIcon sx={{ mr: 1 }} />
                                {file.name}
                            </Box>
                          </TableCell>
                          <TableCell>
                            <Chip label={file.category} size="small" />
                          </TableCell>
                    <TableCell>{formatFileSize(file.size)}</TableCell>
                          <TableCell>
                              <Chip
                        icon={getStatusIcon(file.status)}
                                label={file.status}
                        color={getStatusColor(file.status)}
                                size="small"
                              />
                          </TableCell>
                    <TableCell>{formatDate(file.upload_date)}</TableCell>
                          <TableCell>
                                <IconButton size="small">
                        <Tooltip title="View">
                                  <ViewIcon />
                        </Tooltip>
                                </IconButton>
                      <IconButton size="small">
                              <Tooltip title="Download">
                                  <DownloadIcon />
                        </Tooltip>
                                </IconButton>
                      <IconButton size="small" color="error">
                              <Tooltip title="Delete">
                                  <DeleteIcon />
                        </Tooltip>
                                </IconButton>
                          </TableCell>
                        </TableRow>
                      ))}
                    </TableBody>
                  </Table>
                </TableContainer>
            </CardContent>
          </Card>

      {/* Enhanced Upload Dialog */}
      <Dialog 
        open={uploadDialogOpen} 
        onClose={() => setUploadDialogOpen(false)}
        maxWidth="md"
        fullWidth
      >
        <DialogTitle>
          <Box display="flex" alignItems="center" justifyContent="space-between">
            <Typography variant="h6">Upload Documents with AI Processing</Typography>
            <IconButton onClick={() => setUploadDialogOpen(false)}>
              <CloseIcon />
            </IconButton>
          </Box>
        </DialogTitle>
        <DialogContent>
          <Tabs value={activeTab} onChange={(e, newValue) => setActiveTab(newValue)} sx={{ mb: 3 }}>
            <Tab label="Upload Files" />
            <Tab label="Processing Options" />
          </Tabs>

          {activeTab === 0 && (
            <Box>
              {/* Drag and Drop Zone */}
              <Box
                sx={{
                  border: '2px dashed',
                  borderColor: 'primary.main',
                  borderRadius: 2,
                  p: 4,
                  textAlign: 'center',
                  mb: 3,
                  backgroundColor: 'action.hover',
                  cursor: 'pointer',
                  '&:hover': {
                    backgroundColor: 'action.selected',
                  },
                }}
                onDrop={(e) => {
                  e.preventDefault();
                  const files = Array.from(e.dataTransfer.files);
                  handleFileSelect(files);
                }}
                onDragOver={(e) => e.preventDefault()}
                onClick={() => document.getElementById('file-input').click()}
              >
                <DragIndicatorIcon sx={{ fontSize: 48, color: 'primary.main', mb: 2 }} />
                <Typography variant="h6" gutterBottom>
                  Drag & Drop Files Here
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  or click to browse files
                </Typography>
                <Typography variant="caption" display="block" sx={{ mt: 1 }}>
                  Supports: PDF, DOCX, XLSX, TXT, CSV, Images (JPG, PNG)
                </Typography>
            <Input
                  id="file-input"
              type="file"
              inputProps={{
                    multiple: true,
                    accept: '.pdf,.docx,.xlsx,.txt,.csv,.jpg,.jpeg,.png',
              }}
                  onChange={(e) => handleFileSelect(Array.from(e.target.files || []))}
                  sx={{ display: 'none' }}
            />
          </Box>

              {/* Selected Files List */}
              {uploadForm.files.length > 0 && (
                <Box>
                  <Typography variant="h6" gutterBottom>
                    Selected Files ({uploadForm.files.length})
                  </Typography>
                  <List>
                    {uploadForm.files.map((file, index) => (
                      <ListItem key={index}>
                        <ListItemAvatar>
                          <Avatar>
                            {file.type.startsWith('image/') ? <ImageIcon /> : <DescriptionIcon />}
                          </Avatar>
                        </ListItemAvatar>
                        <ListItemText
                          primary={file.name}
                          secondary={`${formatFileSize(file.size)} • ${file.type}`}
                        />
                        <IconButton onClick={() => handleFileRemove(index)} color="error">
                          <DeleteIcon />
                        </IconButton>
                      </ListItem>
                    ))}
                  </List>
                </Box>
              )}
            </Box>
          )}

          {activeTab === 1 && (
            <Box>
              {/* Category Selection */}
              <FormControl fullWidth sx={{ mb: 3 }}>
                <InputLabel>Document Category</InputLabel>
            <Select
              value={uploadForm.category}
              onChange={(e) => setUploadForm(prev => ({ ...prev, category: e.target.value }))}
                  label="Document Category"
                >
                  {categories.map((category) => (
                    <MenuItem key={category.value} value={category.value}>
                      <Box display="flex" alignItems="center">
                        {category.icon}
                        <Typography sx={{ ml: 1 }}>{category.label}</Typography>
                      </Box>
                    </MenuItem>
                  ))}
            </Select>
          </FormControl>

              {/* Processing Instructions */}
              <TextField
                fullWidth
                label="AI Processing Instructions (Optional)"
                value={uploadForm.processingInstructions}
                onChange={(e) => setUploadForm(prev => ({ ...prev, processingInstructions: e.target.value }))}
                multiline
                rows={3}
                placeholder="Provide specific instructions for AI processing. For example: 'Focus on extracting property prices and transaction dates' or 'Classify this as a market report and extract key trends'"
                sx={{ mb: 3 }}
              />

              {/* Description */}
          <TextField
            fullWidth
            label="Description"
            value={uploadForm.description}
            onChange={(e) => setUploadForm(prev => ({ ...prev, description: e.target.value }))}
            multiline
                rows={2}
                sx={{ mb: 3 }}
          />

              {/* Tags */}
          <TextField
            fullWidth
            label="Tags (comma-separated)"
            value={uploadForm.tags}
            onChange={(e) => setUploadForm(prev => ({ ...prev, tags: e.target.value }))}
                placeholder="market-analysis, dubai, 2024, investment"
                sx={{ mb: 3 }}
          />
            </Box>
          )}

          {uploading && (
            <Box sx={{ mt: 2 }}>
              <LinearProgress variant="determinate" value={uploadProgress} />
              <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
                Uploading... {Math.round(uploadProgress)}%
              </Typography>
            </Box>
          )}
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setUploadDialogOpen(false)}>Cancel</Button>
          <Button
            onClick={() => setActiveTab(activeTab === 0 ? 1 : 0)}
            disabled={uploadForm.files.length === 0}
          >
            {activeTab === 0 ? 'Next' : 'Back'}
          </Button>
          <Button
            onClick={handleFileUpload}
            variant="contained"
            disabled={!uploadForm.files.length || uploading}
            startIcon={<CloudUploadIcon />}
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

export default AdminFiles;
