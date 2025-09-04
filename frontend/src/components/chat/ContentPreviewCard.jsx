import React from 'react';
import {
  Card,
  CardContent,
  CardActions,
  Typography,
  Box,
  Chip,
  Button,
  IconButton,
  Avatar,
  Divider,
  LinearProgress
} from '@mui/material';
import {
  Description as DocumentIcon,
  Assessment as ReportIcon,
  PictureAsPdf as PdfIcon,
  Image as ImageIcon,
  VideoFile as VideoIcon,
  AudioFile as AudioIcon,
  TableChart as SpreadsheetIcon,
  Visibility as ViewIcon,
  Download as DownloadIcon,
  Share as ShareIcon,
  OpenInNew as OpenIcon,
  Schedule as TimeIcon,
  Person as PersonIcon
} from '@mui/icons-material';

const ContentPreviewCard = ({ content, type = 'document', onView, onDownload, onShare, compact = false }) => {
  const getContentIcon = (contentType) => {
    switch (contentType?.toLowerCase()) {
      case 'pdf':
        return <PdfIcon />;
      case 'report':
      case 'analysis':
        return <ReportIcon />;
      case 'image':
      case 'photo':
        return <ImageIcon />;
      case 'video':
        return <VideoIcon />;
      case 'audio':
        return <AudioIcon />;
      case 'spreadsheet':
      case 'excel':
        return <SpreadsheetIcon />;
      default:
        return <DocumentIcon />;
    }
  };

  const getContentColor = (contentType) => {
    switch (contentType?.toLowerCase()) {
      case 'pdf':
        return '#f44336';
      case 'report':
      case 'analysis':
        return '#2196f3';
      case 'image':
      case 'photo':
        return '#4caf50';
      case 'video':
        return '#ff9800';
      case 'audio':
        return '#9c27b0';
      case 'spreadsheet':
      case 'excel':
        return '#4caf50';
      default:
        return '#757575';
    }
  };

  const formatFileSize = (bytes) => {
    if (!bytes) return 'Unknown size';
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(1024));
    return Math.round(bytes / Math.pow(1024, i) * 100) / 100 + ' ' + sizes[i];
  };

  const formatDate = (dateString) => {
    if (!dateString) return 'Unknown date';
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric'
    });
  };

  const getPreviewText = (text, maxLength = 120) => {
    if (!text) return 'No preview available';
    return text.length > maxLength ? `${text.substring(0, maxLength)}...` : text;
  };

  if (compact) {
    return (
      <Card 
        sx={{ 
          maxWidth: 300, 
          cursor: 'pointer',
          '&:hover': { boxShadow: 4 },
          transition: 'box-shadow 0.3s ease-in-out'
        }}
        onClick={onView}
      >
        <CardContent sx={{ p: 2 }}>
          <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
            <Avatar 
              sx={{ 
                bgcolor: getContentColor(type), 
                width: 32, 
                height: 32,
                mr: 1
              }}
            >
              {getContentIcon(type)}
            </Avatar>
            <Box sx={{ flexGrow: 1 }}>
              <Typography variant="subtitle2" component="div" sx={{ fontWeight: 'bold' }}>
                {content.title || content.filename || 'Untitled Document'}
              </Typography>
              <Typography variant="caption" color="text.secondary">
                {content.file_type || type} • {formatFileSize(content.file_size)}
              </Typography>
            </Box>
          </Box>
          
          {content.preview_text && (
            <Typography variant="body2" color="text.secondary" sx={{ mb: 1 }}>
              {getPreviewText(content.preview_text, 80)}
            </Typography>
          )}
          
          <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
            <Typography variant="caption" color="text.secondary">
              {formatDate(content.created_at || content.upload_date)}
            </Typography>
            <Chip 
              label={content.status || 'Available'} 
              size="small" 
              color={content.status === 'Processing' ? 'warning' : 'default'}
            />
          </Box>
        </CardContent>
      </Card>
    );
  }

  return (
    <Card sx={{ maxWidth: 400, mb: 2 }}>
      <CardContent>
        <Box sx={{ display: 'flex', alignItems: 'flex-start', mb: 2 }}>
          <Avatar 
            sx={{ 
              bgcolor: getContentColor(type), 
              width: 48, 
              height: 48,
              mr: 2
            }}
          >
            {getContentIcon(type)}
          </Avatar>
          
          <Box sx={{ flexGrow: 1 }}>
            <Typography variant="h6" component="div" sx={{ fontWeight: 'bold', mb: 0.5 }}>
              {content.title || content.filename || 'Untitled Document'}
            </Typography>
            
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 1 }}>
              <Chip 
                label={content.file_type || type} 
                size="small" 
                variant="outlined"
              />
              <Typography variant="body2" color="text.secondary">
                {formatFileSize(content.file_size)}
              </Typography>
            </Box>
            
            {content.status === 'Processing' && (
              <Box sx={{ mb: 1 }}>
                <LinearProgress 
                  variant="determinate" 
                  value={content.progress || 0} 
                  size="small"
                />
                <Typography variant="caption" color="text.secondary">
                  Processing... {content.progress || 0}%
                </Typography>
              </Box>
            )}
          </Box>
        </Box>

        <Divider sx={{ my: 2 }} />

        {content.preview_text && (
          <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
            {getPreviewText(content.preview_text)}
          </Typography>
        )}

        {content.description && (
          <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
            {content.description}
          </Typography>
        )}

        <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, mb: 2 }}>
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 0.5 }}>
            <TimeIcon fontSize="small" color="action" />
            <Typography variant="body2" color="text.secondary">
              {formatDate(content.created_at || content.upload_date)}
            </Typography>
          </Box>
          
          {content.author && (
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 0.5 }}>
              <PersonIcon fontSize="small" color="action" />
              <Typography variant="body2" color="text.secondary">
                {content.author}
              </Typography>
            </Box>
          )}
        </Box>

        {content.tags && content.tags.length > 0 && (
          <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5, mb: 2 }}>
            {content.tags.slice(0, 3).map((tag, index) => (
              <Chip 
                key={index} 
                label={tag} 
                size="small" 
                variant="outlined"
              />
            ))}
            {content.tags.length > 3 && (
              <Chip 
                label={`+${content.tags.length - 3} more`} 
                size="small" 
                variant="outlined"
              />
            )}
          </Box>
        )}

        {content.metadata && (
          <Box sx={{ mb: 2 }}>
            {Object.entries(content.metadata).slice(0, 3).map(([key, value]) => (
              <Typography key={key} variant="caption" color="text.secondary" sx={{ display: 'block' }}>
                <strong>{key}:</strong> {value}
              </Typography>
            ))}
          </Box>
        )}
      </CardContent>

      <CardActions sx={{ justifyContent: 'space-between', px: 2, pb: 2 }}>
        <Box sx={{ display: 'flex', gap: 1 }}>
          <Button
            variant="contained"
            size="small"
            startIcon={<ViewIcon />}
            onClick={onView}
            disabled={content.status === 'Processing'}
          >
            {content.status === 'Processing' ? 'Processing...' : 'View'}
          </Button>
          
          {content.download_url && (
            <Button
              variant="outlined"
              size="small"
              startIcon={<DownloadIcon />}
              onClick={onDownload}
              disabled={content.status === 'Processing'}
            >
              Download
            </Button>
          )}
        </Box>
        
        <Box sx={{ display: 'flex', gap: 0.5 }}>
          <IconButton 
            size="small" 
            onClick={onShare}
            disabled={content.status === 'Processing'}
          >
            <ShareIcon fontSize="small" />
          </IconButton>
          
          {content.external_url && (
            <IconButton 
              size="small" 
              onClick={() => window.open(content.external_url, '_blank')}
              disabled={content.status === 'Processing'}
            >
              <OpenIcon fontSize="small" />
            </IconButton>
          )}
        </Box>
      </CardActions>
    </Card>
  );
};

export default ContentPreviewCard;
