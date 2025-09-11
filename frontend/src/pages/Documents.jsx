import React, { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Card,
  CardContent,
  TextField,
  InputAdornment,
  Chip,
  Stack,
  Grid,
  Button,
  IconButton,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  useTheme,
  useMediaQuery,
  Paper,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  ListItemSecondaryAction,
  Divider,
  LinearProgress,
} from '@mui/material';
import {
  Search as SearchIcon,
  Add as AddIcon,
  Upload as UploadIcon,
  Description as DescriptionIcon,
  PictureAsPdf as PdfIcon,
  Image as ImageIcon,
  InsertDriveFile as FileIcon,
  CloudUpload as CloudUploadIcon,
  FilterList as FilterIcon,
  MoreVert as MoreVertIcon,
  Download as DownloadIcon,
  Share as ShareIcon,
  Delete as DeleteIcon,
  Visibility as ViewIcon,
} from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';
import { useAppContext } from '../context/AppContext';

const Documents = () => {
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('md'));
  const navigate = useNavigate();
  const { currentUser } = useAppContext();
  
  const [searchTerm, setSearchTerm] = useState('');
  const [filter, setFilter] = useState('all');
  const [uploadDialogOpen, setUploadDialogOpen] = useState(false);
  const [uploading, setUploading] = useState(false);
  const [uploadProgress, setUploadProgress] = useState(0);
  
  // Mock data - in real app, this would come from your backend
  const [documents, setDocuments] = useState([
    {
      id: 1,
      name: 'Property Contract - Palm Jumeirah Villa.pdf',
      type: 'pdf',
      size: '2.4 MB',
      category: 'contracts',
      uploadDate: '2024-01-15',
      status: 'processed',
      tags: ['contract', 'palm-jumeirah', 'villa'],
    },
    {
      id: 2,
      name: 'Market Analysis Report Q4 2023.docx',
      type: 'docx',
      size: '1.8 MB',
      category: 'reports',
      uploadDate: '2024-01-14',
      status: 'processed',
      tags: ['market-analysis', 'q4-2023', 'report'],
    },
    {
      id: 3,
      name: 'Property Photos - Dubai Marina Apartment.jpg',
      type: 'jpg',
      size: '4.2 MB',
      category: 'images',
      uploadDate: '2024-01-13',
      status: 'processed',
      tags: ['photos', 'dubai-marina', 'apartment'],
    },
    {
      id: 4,
      name: 'RERA Compliance Checklist.xlsx',
      type: 'xlsx',
      size: '856 KB',
      category: 'compliance',
      uploadDate: '2024-01-12',
      status: 'processing',
      tags: ['rera', 'compliance', 'checklist'],
    },
  ]);

  const filters = [
    { id: 'all', label: 'All Documents', count: documents.length },
    { id: 'contracts', label: 'Contracts', count: documents.filter(d => d.category === 'contracts').length },
    { id: 'reports', label: 'Reports', count: documents.filter(d => d.category === 'reports').length },
    { id: 'images', label: 'Images', count: documents.filter(d => d.category === 'images').length },
    { id: 'compliance', label: 'Compliance', count: documents.filter(d => d.category === 'compliance').length },
  ];

  const getFileIcon = (type) => {
    switch (type) {
      case 'pdf': return <PdfIcon sx={{ color: 'error.main' }} />;
      case 'docx': return <DescriptionIcon sx={{ color: 'primary.main' }} />;
      case 'jpg':
      case 'jpeg':
      case 'png': return <ImageIcon sx={{ color: 'success.main' }} />;
      case 'xlsx': return <FileIcon sx={{ color: 'info.main' }} />;
      default: return <FileIcon sx={{ color: 'text.secondary' }} />;
    }
  };

  const getCategoryColor = (category) => {
    switch (category) {
      case 'contracts': return 'primary';
      case 'reports': return 'secondary';
      case 'images': return 'success';
      case 'compliance': return 'warning';
      default: return 'default';
    }
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'processed': return 'success';
      case 'processing': return 'warning';
      case 'error': return 'error';
      default: return 'default';
    }
  };

  const filteredDocuments = documents.filter(doc => {
    const matchesSearch = doc.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         doc.tags.some(tag => tag.toLowerCase().includes(searchTerm.toLowerCase()));
    
    const matchesFilter = filter === 'all' || doc.category === filter;
    
    return matchesSearch && matchesFilter;
  });

  const handleUpload = async (file) => {
    setUploading(true);
    setUploadProgress(0);
    
    // Simulate upload progress
    const interval = setInterval(() => {
      setUploadProgress(prev => {
        if (prev >= 100) {
          clearInterval(interval);
          setUploading(false);
          setUploadDialogOpen(false);
          // Add new document to list
          const newDoc = {
            id: Date.now(),
            name: file.name,
            type: file.name.split('.').pop(),
            size: `${(file.size / 1024 / 1024).toFixed(1)} MB`,
            category: 'documents',
            uploadDate: new Date().toISOString().split('T')[0],
            status: 'processed',
            tags: [],
          };
          setDocuments(prev => [newDoc, ...prev]);
          return 100;
        }
        return prev + 10;
      });
    }, 200);
  };

  const handleFileUpload = (event) => {
    const file = event.target.files[0];
    if (file) {
      handleUpload(file);
    }
  };

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
            Documents
          </Typography>
          <Button
            variant="contained"
            startIcon={<UploadIcon />}
            onClick={() => setUploadDialogOpen(true)}
            sx={{
              bgcolor: 'rgba(255,255,255,0.2)',
              color: 'white',
              '&:hover': {
                bgcolor: 'rgba(255,255,255,0.3)',
              },
              borderRadius: 2,
            }}
          >
            Upload
          </Button>
        </Box>
        
        <Typography variant="body1" sx={{ opacity: 0.9 }}>
          Manage your property documents and reports
        </Typography>
      </Box>

      {/* Search and Filters */}
      <Box sx={{ p: 2 }}>
        <TextField
          fullWidth
          placeholder="Search documents..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          sx={{
            mb: 2,
            '& .MuiOutlinedInput-root': {
              borderRadius: 3,
            },
          }}
          InputProps={{
            startAdornment: (
              <InputAdornment position="start">
                <SearchIcon />
              </InputAdornment>
            ),
          }}
        />

        {/* Filter Chips */}
        <Stack 
          direction="row" 
          spacing={1} 
          sx={{ 
            mb: 3, 
            flexWrap: 'wrap', 
            gap: 1,
            justifyContent: isMobile ? 'center' : 'flex-start'
          }}
        >
          {filters.map((filterOption) => (
            <Chip
              key={filterOption.id}
              label={`${filterOption.label} (${filterOption.count})`}
              onClick={() => setFilter(filterOption.id)}
              variant={filter === filterOption.id ? 'filled' : 'outlined'}
              color={filter === filterOption.id ? 'primary' : 'default'}
              size="small"
            />
          ))}
        </Stack>

        {/* Documents List */}
        <Paper sx={{ borderRadius: 3, overflow: 'hidden' }}>
          <List>
            {filteredDocuments.map((doc, index) => (
              <React.Fragment key={doc.id}>
                <ListItem>
                  <ListItemIcon>
                    {getFileIcon(doc.type)}
                  </ListItemIcon>
                  <ListItemText
                    primary={
                      <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 0.5 }}>
                        <Typography variant="subtitle1" sx={{ fontWeight: 600 }}>
                          {doc.name}
                        </Typography>
                        <Chip
                          label={doc.category}
                          size="small"
                          color={getCategoryColor(doc.category)}
                          variant="outlined"
                        />
                        <Chip
                          label={doc.status}
                          size="small"
                          color={getStatusColor(doc.status)}
                          variant="filled"
                        />
                      </Box>
                    }
                    secondary={
                      <Box>
                        <Typography variant="body2" color="text.secondary">
                          {doc.size} • Uploaded {doc.uploadDate}
                        </Typography>
                        {doc.tags.length > 0 && (
                          <Box sx={{ mt: 0.5 }}>
                            {doc.tags.map((tag, tagIndex) => (
                              <Chip
                                key={tagIndex}
                                label={tag}
                                size="small"
                                variant="outlined"
                                sx={{ mr: 0.5, mb: 0.5, fontSize: '0.7rem' }}
                              />
                            ))}
                          </Box>
                        )}
                      </Box>
                    }
                  />
                  <ListItemSecondaryAction>
                    <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                      <IconButton size="small" title="View">
                        <ViewIcon />
                      </IconButton>
                      <IconButton size="small" title="Download">
                        <DownloadIcon />
                      </IconButton>
                      <IconButton size="small" title="Share">
                        <ShareIcon />
                      </IconButton>
                      <IconButton size="small" title="More">
                        <MoreVertIcon />
                      </IconButton>
                    </Box>
                  </ListItemSecondaryAction>
                </ListItem>
                {index < filteredDocuments.length - 1 && <Divider />}
              </React.Fragment>
            ))}
          </List>
        </Paper>

        {filteredDocuments.length === 0 && (
          <Paper
            sx={{
              textAlign: 'center',
              py: 6,
              px: 3,
              borderRadius: 3,
              border: `2px dashed ${theme.palette.divider}`,
              bgcolor: 'background.paper'
            }}
          >
            <CloudUploadIcon sx={{ fontSize: 64, color: 'text.secondary', mb: 2 }} />
            <Typography variant="h6" sx={{ mb: 1, color: 'text.secondary' }}>
              No documents found
            </Typography>
            <Typography variant="body2" sx={{ color: 'text.secondary', mb: 3 }}>
              {searchTerm ? 'Try adjusting your search terms' : 'Upload your first document to get started'}
            </Typography>
            <Button
              variant="contained"
              startIcon={<UploadIcon />}
              onClick={() => setUploadDialogOpen(true)}
              sx={{ borderRadius: 2 }}
            >
              Upload Document
            </Button>
          </Paper>
        )}
      </Box>

      {/* Upload Dialog */}
      <Dialog
        open={uploadDialogOpen}
        onClose={() => setUploadDialogOpen(false)}
        maxWidth="sm"
        fullWidth
      >
        <DialogTitle>Upload Document</DialogTitle>
        <DialogContent>
          <Box sx={{ textAlign: 'center', py: 3 }}>
            <CloudUploadIcon sx={{ fontSize: 64, color: 'primary.main', mb: 2 }} />
            <Typography variant="h6" sx={{ mb: 1 }}>
              Drag and drop files here
            </Typography>
            <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
              or click to browse files
            </Typography>
            <input
              type="file"
              onChange={handleFileUpload}
              style={{ display: 'none' }}
              id="file-upload"
              accept=".pdf,.docx,.xlsx,.jpg,.jpeg,.png"
            />
            <label htmlFor="file-upload">
              <Button
                variant="outlined"
                component="span"
                startIcon={<UploadIcon />}
                sx={{ borderRadius: 2 }}
              >
                Choose File
              </Button>
            </label>
          </Box>
          
          {uploading && (
            <Box sx={{ mt: 2 }}>
              <Typography variant="body2" sx={{ mb: 1 }}>
                Uploading... {uploadProgress}%
              </Typography>
              <LinearProgress variant="determinate" value={uploadProgress} />
            </Box>
          )}
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setUploadDialogOpen(false)}>Cancel</Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default Documents;
