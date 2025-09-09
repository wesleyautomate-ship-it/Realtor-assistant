import React from 'react';
import {
  Card,
  CardContent,
  Typography,
  Box,
  Chip,
  Grid,
  IconButton,
  Tooltip,
  LinearProgress,
  Alert,
  Divider,
  List,
  ListItem,
  ListItemIcon,
  ListItemText
} from '@mui/material';
import {
  Description as DocumentIcon,
  CheckCircle as CheckIcon,
  Warning as WarningIcon,
  Info as InfoIcon,
  Home as HomeIcon,
  LocationOn as LocationIcon,
  Bed as BedIcon,
  Bathtub as BathIcon,
  SquareFoot as SizeIcon,
  AttachMoney as PriceIcon,
  Upload as UploadIcon,
  Visibility as ViewIcon
} from '@mui/icons-material';

const DocumentProcessingCard = ({ 
  processingResult, 
  onViewDocument,
  onUseInChat,
  showActions = true 
}) => {
  if (!processingResult) return null;

  const {
    document_type,
    extracted_property,
    processing_timestamp,
    content_length,
    confidence_score,
    processing_status,
    error
  } = processingResult;

  const {
    building_name,
    unit_number,
    community,
    property_type,
    bedrooms,
    bathrooms,
    size_sqft,
    price,
    address,
    extracted_entities = []
  } = extracted_property || {};

  const getStatusColor = (status) => {
    switch (status) {
      case 'success': return 'success';
      case 'error': return 'error';
      case 'processing': return 'warning';
      default: return 'info';
    }
  };

  const getStatusIcon = (status) => {
    switch (status) {
      case 'success': return <CheckIcon />;
      case 'error': return <WarningIcon />;
      case 'processing': return <UploadIcon />;
      default: return <InfoIcon />;
    }
  };

  const formatFileSize = (bytes) => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };

  const formatTimestamp = (timestamp) => {
    return new Date(timestamp).toLocaleString();
  };

  return (
    <Card sx={{ 
      mb: 2, 
      border: 1, 
      borderColor: getStatusColor(processing_status) + '.main',
      bgcolor: getStatusColor(processing_status) + '.50'
    }}>
      <CardContent>
        <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
          <DocumentIcon sx={{ mr: 1, color: getStatusColor(processing_status) + '.main' }} />
          <Typography variant="h6" sx={{ fontWeight: 600 }}>
            Document Processing Results
          </Typography>
          <Box sx={{ ml: 'auto', display: 'flex', alignItems: 'center', gap: 1 }}>
            <Chip
              label={processing_status}
              color={getStatusColor(processing_status)}
              size="small"
              icon={getStatusIcon(processing_status)}
            />
            {confidence_score !== undefined && (
              <LinearProgress
                variant="determinate"
                value={confidence_score * 100}
                color={getStatusColor(processing_status)}
                sx={{ width: 60, height: 6, borderRadius: 3 }}
              />
            )}
          </Box>
        </Box>

        {/* Document Information */}
        <Grid container spacing={2} sx={{ mb: 2 }}>
          <Grid item xs={12} sm={6}>
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
              <DocumentIcon fontSize="small" color="primary" />
              <Box>
                <Typography variant="caption" color="text.secondary">
                  Document Type
                </Typography>
                <Typography variant="body2" sx={{ fontWeight: 500, textTransform: 'capitalize' }}>
                  {document_type?.replace('_', ' ') || 'Unknown'}
                </Typography>
              </Box>
            </Box>
          </Grid>

          <Grid item xs={12} sm={6}>
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
              <InfoIcon fontSize="small" color="primary" />
              <Box>
                <Typography variant="caption" color="text.secondary">
                  File Size
                </Typography>
                <Typography variant="body2" sx={{ fontWeight: 500 }}>
                  {formatFileSize(content_length || 0)}
                </Typography>
              </Box>
            </Box>
          </Grid>

          <Grid item xs={12}>
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
              <InfoIcon fontSize="small" color="primary" />
              <Box>
                <Typography variant="caption" color="text.secondary">
                  Processed At
                </Typography>
                <Typography variant="body2" sx={{ fontWeight: 500 }}>
                  {formatTimestamp(processing_timestamp)}
                </Typography>
              </Box>
            </Box>
          </Grid>
        </Grid>

        {/* Error Display */}
        {processing_status === 'error' && error && (
          <Alert severity="error" sx={{ mb: 2 }}>
            <Typography variant="body2">
              Processing failed: {error}
            </Typography>
          </Alert>
        )}

        {/* Extracted Property Information */}
        {processing_status === 'success' && extracted_property && (
          <>
            <Divider sx={{ my: 2 }} />
            <Typography variant="subtitle1" sx={{ mb: 2, fontWeight: 600 }}>
              Extracted Property Information:
            </Typography>

            <Grid container spacing={2} sx={{ mb: 2 }}>
              {building_name && (
                <Grid item xs={12} sm={6}>
                  <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                    <HomeIcon fontSize="small" color="primary" />
                    <Box>
                      <Typography variant="caption" color="text.secondary">
                        Building
                      </Typography>
                      <Typography variant="body2" sx={{ fontWeight: 500 }}>
                        {building_name}
                      </Typography>
                    </Box>
                  </Box>
                </Grid>
              )}

              {unit_number && (
                <Grid item xs={12} sm={6}>
                  <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                    <InfoIcon fontSize="small" color="primary" />
                    <Box>
                      <Typography variant="caption" color="text.secondary">
                        Unit
                      </Typography>
                      <Typography variant="body2" sx={{ fontWeight: 500 }}>
                        {unit_number}
                      </Typography>
                    </Box>
                  </Box>
                </Grid>
              )}

              {community && (
                <Grid item xs={12} sm={6}>
                  <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                    <LocationIcon fontSize="small" color="primary" />
                    <Box>
                      <Typography variant="caption" color="text.secondary">
                        Community
                      </Typography>
                      <Typography variant="body2" sx={{ fontWeight: 500 }}>
                        {community}
                      </Typography>
                    </Box>
                  </Box>
                </Grid>
              )}

              {property_type && (
                <Grid item xs={12} sm={6}>
                  <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                    <HomeIcon fontSize="small" color="primary" />
                    <Box>
                      <Typography variant="caption" color="text.secondary">
                        Type
                      </Typography>
                      <Typography variant="body2" sx={{ fontWeight: 500, textTransform: 'capitalize' }}>
                        {property_type}
                      </Typography>
                    </Box>
                  </Box>
                </Grid>
              )}

              {bedrooms && (
                <Grid item xs={12} sm={6}>
                  <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                    <BedIcon fontSize="small" color="primary" />
                    <Box>
                      <Typography variant="caption" color="text.secondary">
                        Bedrooms
                      </Typography>
                      <Typography variant="body2" sx={{ fontWeight: 500 }}>
                        {bedrooms}
                      </Typography>
                    </Box>
                  </Box>
                </Grid>
              )}

              {bathrooms && (
                <Grid item xs={12} sm={6}>
                  <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                    <BathIcon fontSize="small" color="primary" />
                    <Box>
                      <Typography variant="caption" color="text.secondary">
                        Bathrooms
                      </Typography>
                      <Typography variant="body2" sx={{ fontWeight: 500 }}>
                        {bathrooms}
                      </Typography>
                    </Box>
                  </Box>
                </Grid>
              )}

              {size_sqft && (
                <Grid item xs={12} sm={6}>
                  <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                    <SizeIcon fontSize="small" color="primary" />
                    <Box>
                      <Typography variant="caption" color="text.secondary">
                        Size
                      </Typography>
                      <Typography variant="body2" sx={{ fontWeight: 500 }}>
                        {size_sqft.toLocaleString()} sqft
                      </Typography>
                    </Box>
                  </Box>
                </Grid>
              )}

              {price && (
                <Grid item xs={12} sm={6}>
                  <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                    <PriceIcon fontSize="small" color="primary" />
                    <Box>
                      <Typography variant="caption" color="text.secondary">
                        Price
                      </Typography>
                      <Typography variant="body2" sx={{ fontWeight: 500 }}>
                        AED {price.toLocaleString()}
                      </Typography>
                    </Box>
                  </Box>
                </Grid>
              )}
            </Grid>

            {/* Extracted Entities */}
            {extracted_entities.length > 0 && (
              <Box sx={{ mb: 2 }}>
                <Typography variant="subtitle2" sx={{ mb: 1, fontWeight: 600 }}>
                  Detected Information:
                </Typography>
                <Box sx={{ display: 'flex', gap: 1, flexWrap: 'wrap' }}>
                  {extracted_entities.map((entity, index) => (
                    <Chip
                      key={index}
                      label={entity}
                      size="small"
                      variant="outlined"
                      color="primary"
                    />
                  ))}
                </Box>
              </Box>
            )}

            {/* Confidence Warning */}
            {confidence_score < 0.6 && (
              <Alert severity="warning" sx={{ mb: 2 }}>
                <Typography variant="body2">
                  Low confidence extraction. Please verify the property information.
                </Typography>
              </Alert>
            )}
          </>
        )}

        {/* Actions */}
        {showActions && processing_status === 'success' && (
          <>
            <Divider sx={{ my: 2 }} />
            <Box sx={{ display: 'flex', gap: 1, justifyContent: 'flex-end' }}>
              <Tooltip title="View Document">
                <IconButton
                  size="small"
                  onClick={() => onViewDocument && onViewDocument(processingResult)}
                  color="primary"
                >
                  <ViewIcon />
                </IconButton>
              </Tooltip>
              <Tooltip title="Use Property in Chat">
                <IconButton
                  size="small"
                  onClick={() => onUseInChat && onUseInChat(extracted_property)}
                  color="primary"
                >
                  <CheckIcon />
                </IconButton>
              </Tooltip>
            </Box>
          </>
        )}
      </CardContent>
    </Card>
  );
};

export default DocumentProcessingCard;
