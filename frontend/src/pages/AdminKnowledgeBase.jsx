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
  Tabs,
  Tab,
  Accordion,
  AccordionSummary,
  AccordionDetails,
  Divider,
  Badge,
  Avatar,
  ListItemAvatar
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
  ExpandMore as ExpandMoreIcon,
  Image as ImageIcon,
  Description as DescriptionIcon,
  TableChart as TableChartIcon,
  TextFields as TextFieldsIcon,
  DragIndicator as DragIndicatorIcon,
  Add as AddIcon,
  Close as CloseIcon,
  Search as SearchIcon,
  Refresh as RefreshIcon,
  DataObject as DataObjectIcon,
  Schema as SchemaIcon,
  Analytics as AnalyticsIcon,
  Database as DatabaseIcon
} from '@mui/icons-material';
import { useAppContext } from '../context/AppContext';
import { api } from '../utils/apiClient';

const AdminKnowledgeBase = () => {
  const { currentUser } = useAppContext();
  const [activeTab, setActiveTab] = useState(0);
  const [uploadDialogOpen, setUploadDialogOpen] = useState(false);
  const [uploading, setUploading] = useState(false);
  const [uploadProgress, setUploadProgress] = useState(0);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [snackbar, setSnackbar] = useState({ open: false, message: '', severity: 'info' });
  
  // Knowledge base state
  const [stats, setStats] = useState({
    totalDocuments: 0,
    documentsByType: {},
    recentUploads: [],
    processingStats: {}
  });
  
  const [structuredData, setStructuredData] = useState({});
  const [searchResults, setSearchResults] = useState([]);
  const [schemas, setSchemas] = useState({});
  
  // Upload form state
  const [uploadForm, setUploadForm] = useState({
    files: [],
    documentCategory: '',
    priority: 'normal',
    description: '',
    tags: ''
  });

  // Document type categories for knowledge base
  const documentCategories = [
    { value: 'transaction_data', label: 'Transaction Data', icon: <TableChartIcon />, color: 'primary' },
    { value: 'legal_document', label: 'Legal Documents', icon: <SecurityIcon />, color: 'secondary' },
    { value: 'market_report', label: 'Market Reports', icon: <AssessmentIcon />, color: 'success' },
    { value: 'property_listing', label: 'Property Listings', icon: <DescriptionIcon />, color: 'info' },
    { value: 'guideline_document', label: 'Guidelines', icon: <TextFieldsIcon />, color: 'warning' }
  ];

  useEffect(() => {
    fetchKnowledgeBaseStats();
    fetchDocumentSchemas();
  }, []);

  const fetchKnowledgeBaseStats = async () => {
    try {
      setLoading(true);
      const response = await api.get('/admin/knowledge/stats');
      setStats(response);
    } catch (error) {
      console.error('Error fetching knowledge base stats:', error);
      setError('Failed to load knowledge base statistics');
    } finally {
      setLoading(false);
    }
  };

  const fetchDocumentSchemas = async () => {
    try {
      const response = await api.get('/admin/knowledge/schemas');
      setSchemas(response.schemas);
    } catch (error) {
      console.error('Error fetching document schemas:', error);
    }
  };

  const fetchStructuredData = async (documentType) => {
    try {
      const response = await api.get(`/admin/knowledge/data/${documentType}`);
      setStructuredData(prev => ({
        ...prev,
        [documentType]: response.data
      }));
    } catch (error) {
      console.error(`Error fetching ${documentType} data:`, error);
    }
  };

  const searchKnowledgeBase = async (query, documentType = null) => {
    try {
      const params = new URLSearchParams({ query });
      if (documentType) params.append('document_type', documentType);
      
      const response = await api.get(`/admin/knowledge/search?${params.toString()}`);
      setSearchResults(response.results);
    } catch (error) {
      console.error('Error searching knowledge base:', error);
      setSnackbar({
        open: true,
        message: 'Search failed',
        severity: 'error'
      });
    }
  };

  const handleFileUpload = async () => {
    if (!uploadForm.files.length) return;

    try {
      setUploading(true);
      setUploadProgress(0);

      const totalFiles = uploadForm.files.length;
      let uploadedCount = 0;

      for (const file of uploadForm.files) {
        const formData = new FormData();
        formData.append('file', file);
        formData.append('document_category', uploadForm.documentCategory || '');
        formData.append('priority', uploadForm.priority);
        formData.append('description', uploadForm.description || '');
        formData.append('tags', uploadForm.tags || '');

        const response = await api.upload('/admin/knowledge/upload', formData, (progressEvent) => {
          const progress = Math.round((progressEvent.loaded * 100) / progressEvent.total);
          setUploadProgress(progress);
        });

        uploadedCount++;
        setUploadProgress((uploadedCount / totalFiles) * 100);
      }

      // Reset form and close dialog
      setUploadForm({
        files: [],
        documentCategory: '',
        priority: 'normal',
        description: '',
        tags: ''
      });
      setUploadDialogOpen(false);

      // Refresh stats
      await fetchKnowledgeBaseStats();
      
      setSnackbar({
        open: true,
        message: `Successfully uploaded and processed ${uploadedCount} file(s)`,
        severity: 'success'
      });

    } catch (error) {
      console.error('Upload error:', error);
      setSnackbar({
        open: true,
        message: `Upload failed: ${error.message}`,
        severity: 'error'
      });
    } finally {
      setUploading(false);
      setUploadProgress(0);
    }
  };

  const handleFileSelect = useCallback((acceptedFiles) => {
    setUploadForm(prev => ({
      ...prev,
      files: [...prev.files, ...acceptedFiles]
    }));
  }, []);

  const handleFileRemove = (index) => {
    setUploadForm(prev => ({
      ...prev,
      files: prev.files.filter((_, i) => i !== index)
    }));
  };

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
        Knowledge Base Management
      </Typography>
      <Typography variant="body1" color="text.secondary" sx={{ mb: 3 }}>
        Upload and manage documents with intelligent data sorting and schema conversion
      </Typography>

      {/* Stats Cards */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Box display="flex" alignItems="center">
                <DatabaseIcon color="primary" sx={{ mr: 2 }} />
                <Box>
                  <Typography variant="h6">{stats.totalDocuments}</Typography>
                  <Typography variant="body2" color="text.secondary">Total Documents</Typography>
                </Box>
              </Box>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Box display="flex" alignItems="center">
                <SchemaIcon color="success" sx={{ mr: 2 }} />
                <Box>
                  <Typography variant="h6">{Object.keys(schemas).length}</Typography>
                  <Typography variant="body2" color="text.secondary">Data Schemas</Typography>
                </Box>
              </Box>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Box display="flex" alignItems="center">
                <AnalyticsIcon color="info" sx={{ mr: 2 }} />
                <Box>
                  <Typography variant="h6">{stats.processingStats?.successful_uploads || 0}</Typography>
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
                  <Typography variant="h6">{stats.processingStats?.failed_uploads || 0}</Typography>
                  <Typography variant="body2" color="text.secondary">Failed</Typography>
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
          Upload to Knowledge Base
        </Button>
        <Button
          variant="outlined"
          startIcon={<RefreshIcon />}
          onClick={fetchKnowledgeBaseStats}
        >
          Refresh Stats
        </Button>
      </Box>

      {/* Error Display */}
      {error && (
        <Alert severity="error" sx={{ mb: 3 }}>
          {error}
        </Alert>
      )}

      {/* Main Content Tabs */}
      <Card>
        <Box sx={{ borderBottom: 1, borderColor: 'divider' }}>
          <Tabs value={activeTab} onChange={(e, newValue) => setActiveTab(newValue)}>
            <Tab label="Document Types" />
            <Tab label="Structured Data" />
            <Tab label="Search & Analytics" />
            <Tab label="Recent Uploads" />
          </Tabs>
        </Box>

        <CardContent>
          {/* Document Types Tab */}
          {activeTab === 0 && (
            <Box>
              <Typography variant="h6" gutterBottom>
                Document Types & Schemas
              </Typography>
              <Grid container spacing={3}>
                {documentCategories.map((category) => (
                  <Grid item xs={12} sm={6} md={4} key={category.value}>
                    <Card variant="outlined">
                      <CardContent>
                        <Box display="flex" alignItems="center" sx={{ mb: 2 }}>
                          <Avatar sx={{ bgcolor: `${category.color}.main`, mr: 2 }}>
                            {category.icon}
                          </Avatar>
                          <Box>
                            <Typography variant="subtitle1">{category.label}</Typography>
                            <Typography variant="body2" color="text.secondary">
                              {stats.documentsByType?.[category.value] || 0} documents
                            </Typography>
                          </Box>
                        </Box>
                        <Button
                          size="small"
                          variant="outlined"
                          onClick={() => fetchStructuredData(category.value)}
                          startIcon={<DataObjectIcon />}
                        >
                          View Data
                        </Button>
                      </CardContent>
                    </Card>
                  </Grid>
                ))}
              </Grid>
            </Box>
          )}

          {/* Structured Data Tab */}
          {activeTab === 1 && (
            <Box>
              <Typography variant="h6" gutterBottom>
                Structured Data by Type
              </Typography>
              {Object.keys(structuredData).length === 0 ? (
                <Alert severity="info">
                  No structured data loaded. Click "View Data" on document types to load data.
                </Alert>
              ) : (
                Object.entries(structuredData).map(([type, data]) => (
                  <Accordion key={type} sx={{ mb: 2 }}>
                    <AccordionSummary expandIcon={<ExpandMoreIcon />}>
                      <Box display="flex" alignItems="center">
                        <Typography variant="h6" sx={{ mr: 2 }}>
                          {documentCategories.find(c => c.value === type)?.label || type}
                        </Typography>
                        <Badge badgeContent={data.length} color="primary">
                          <Chip label={`${data.length} records`} size="small" />
                        </Badge>
                      </Box>
                    </AccordionSummary>
                    <AccordionDetails>
                      <TableContainer component={Paper} variant="outlined">
                        <Table size="small">
                          <TableHead>
                            <TableRow>
                              {data.length > 0 && Object.keys(data[0]).map((key) => (
                                <TableCell key={key}>{key}</TableCell>
                              ))}
                            </TableRow>
                          </TableHead>
                          <TableBody>
                            {data.slice(0, 10).map((row, index) => (
                              <TableRow key={index}>
                                {Object.values(row).map((value, cellIndex) => (
                                  <TableCell key={cellIndex}>
                                    {typeof value === 'object' ? JSON.stringify(value) : String(value)}
                                  </TableCell>
                                ))}
                              </TableRow>
                            ))}
                          </TableBody>
                        </Table>
                      </TableContainer>
                      {data.length > 10 && (
                        <Typography variant="caption" color="text.secondary" sx={{ mt: 1 }}>
                          Showing first 10 of {data.length} records
                        </Typography>
                      )}
                    </AccordionDetails>
                  </Accordion>
                ))
              )}
            </Box>
          )}

          {/* Search & Analytics Tab */}
          {activeTab === 2 && (
            <Box>
              <Typography variant="h6" gutterBottom>
                Search Knowledge Base
              </Typography>
              <Box sx={{ mb: 3, display: 'flex', gap: 2 }}>
                <TextField
                  fullWidth
                  placeholder="Search structured data..."
                  onKeyPress={(e) => {
                    if (e.key === 'Enter') {
                      searchKnowledgeBase(e.target.value);
                    }
                  }}
                />
                <Button
                  variant="contained"
                  startIcon={<SearchIcon />}
                  onClick={() => {
                    const input = document.querySelector('input[placeholder="Search structured data..."]');
                    if (input) searchKnowledgeBase(input.value);
                  }}
                >
                  Search
                </Button>
              </Box>
              
              {searchResults.length > 0 && (
                <Box>
                  <Typography variant="subtitle1" gutterBottom>
                    Search Results ({searchResults.length})
                  </Typography>
                  <TableContainer component={Paper} variant="outlined">
                    <Table size="small">
                      <TableHead>
                        <TableRow>
                          {searchResults.length > 0 && Object.keys(searchResults[0]).map((key) => (
                            <TableCell key={key}>{key}</TableCell>
                          ))}
                        </TableRow>
                      </TableHead>
                      <TableBody>
                        {searchResults.map((row, index) => (
                          <TableRow key={index}>
                            {Object.values(row).map((value, cellIndex) => (
                              <TableCell key={cellIndex}>
                                {typeof value === 'object' ? JSON.stringify(value) : String(value)}
                              </TableCell>
                            ))}
                          </TableRow>
                        ))}
                      </TableBody>
                    </Table>
                  </TableContainer>
                </Box>
              )}
            </Box>
          )}

          {/* Recent Uploads Tab */}
          {activeTab === 3 && (
            <Box>
              <Typography variant="h6" gutterBottom>
                Recent Uploads
              </Typography>
              {stats.recentUploads.length === 0 ? (
                <Alert severity="info">No recent uploads found.</Alert>
              ) : (
                <List>
                  {stats.recentUploads.map((upload, index) => (
                    <ListItem key={index}>
                      <ListItemAvatar>
                        <Avatar>
                          {documentCategories.find(c => c.value === upload.document_type)?.icon || <DescriptionIcon />}
                        </Avatar>
                      </ListItemAvatar>
                      <ListItemText
                        primary={documentCategories.find(c => c.value === upload.document_type)?.label || upload.document_type}
                        secondary={`Uploaded ${formatDate(upload.created_at)}`}
                      />
                      <Chip label={`ID: ${upload.id}`} size="small" />
                    </ListItem>
                  ))}
                </List>
              )}
            </Box>
          )}
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
            <Typography variant="h6">Upload to Knowledge Base</Typography>
            <IconButton onClick={() => setUploadDialogOpen(false)}>
              <CloseIcon />
            </IconButton>
          </Box>
        </DialogTitle>
        <DialogContent>
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
            onClick={() => document.getElementById('knowledge-file-input').click()}
          >
            <DragIndicatorIcon sx={{ fontSize: 48, color: 'primary.main', mb: 2 }} />
            <Typography variant="h6" gutterBottom>
              Drag & Drop Documents Here
            </Typography>
            <Typography variant="body2" color="text.secondary">
              or click to browse files
            </Typography>
            <Typography variant="caption" display="block" sx={{ mt: 1 }}>
              Supports: PDF, DOCX, XLSX, TXT, CSV
            </Typography>
            <Input
              id="knowledge-file-input"
              type="file"
              inputProps={{
                multiple: true,
                accept: '.pdf,.docx,.xlsx,.txt,.csv',
              }}
              onChange={(e) => handleFileSelect(Array.from(e.target.files || []))}
              sx={{ display: 'none' }}
            />
          </Box>

          {/* Selected Files List */}
          {uploadForm.files.length > 0 && (
            <Box sx={{ mb: 3 }}>
              <Typography variant="h6" gutterBottom>
                Selected Files ({uploadForm.files.length})
              </Typography>
              <List>
                {uploadForm.files.map((file, index) => (
                  <ListItem key={index}>
                    <ListItemAvatar>
                      <Avatar>
                        <DescriptionIcon />
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

          {/* Upload Options */}
          <Grid container spacing={3}>
            <Grid item xs={12} sm={6}>
              <FormControl fullWidth>
                <InputLabel>Document Category</InputLabel>
                <Select
                  value={uploadForm.documentCategory}
                  onChange={(e) => setUploadForm(prev => ({ ...prev, documentCategory: e.target.value }))}
                  label="Document Category"
                >
                  {documentCategories.map((category) => (
                    <MenuItem key={category.value} value={category.value}>
                      <Box display="flex" alignItems="center">
                        {category.icon}
                        <Typography sx={{ ml: 1 }}>{category.label}</Typography>
                      </Box>
                    </MenuItem>
                  ))}
                </Select>
              </FormControl>
            </Grid>
            <Grid item xs={12} sm={6}>
              <FormControl fullWidth>
                <InputLabel>Priority</InputLabel>
                <Select
                  value={uploadForm.priority}
                  onChange={(e) => setUploadForm(prev => ({ ...prev, priority: e.target.value }))}
                  label="Priority"
                >
                  <MenuItem value="low">Low</MenuItem>
                  <MenuItem value="normal">Normal</MenuItem>
                  <MenuItem value="high">High</MenuItem>
                </Select>
              </FormControl>
            </Grid>
            <Grid item xs={12}>
              <TextField
                fullWidth
                label="Description"
                value={uploadForm.description}
                onChange={(e) => setUploadForm(prev => ({ ...prev, description: e.target.value }))}
                multiline
                rows={2}
                placeholder="Optional description of the documents"
              />
            </Grid>
            <Grid item xs={12}>
              <TextField
                fullWidth
                label="Tags (comma-separated)"
                value={uploadForm.tags}
                onChange={(e) => setUploadForm(prev => ({ ...prev, tags: e.target.value }))}
                placeholder="market-analysis, dubai, 2024, investment"
              />
            </Grid>
          </Grid>

          {uploading && (
            <Box sx={{ mt: 2 }}>
              <LinearProgress variant="determinate" value={uploadProgress} />
              <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
                Uploading and processing... {Math.round(uploadProgress)}%
              </Typography>
            </Box>
          )}
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setUploadDialogOpen(false)}>Cancel</Button>
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

export default AdminKnowledgeBase;
