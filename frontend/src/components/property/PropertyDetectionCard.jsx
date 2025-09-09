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
  Divider
} from '@mui/material';
import {
  LocationOn as LocationIcon,
  Home as HomeIcon,
  Bed as BedIcon,
  Bathtub as BathIcon,
  SquareFoot as SizeIcon,
  AttachMoney as PriceIcon,
  CheckCircle as CheckIcon,
  Warning as WarningIcon,
  Info as InfoIcon
} from '@mui/icons-material';

const PropertyDetectionCard = ({ 
  detectedProperty, 
  onPropertyClick, 
  onViewDetails,
  showActions = true 
}) => {
  if (!detectedProperty) return null;

  const {
    building_name,
    unit_number,
    community,
    property_type,
    bedrooms,
    bathrooms,
    size_sqft,
    price,
    confidence,
    extracted_entities = [],
    address
  } = detectedProperty;

  const getConfidenceColor = (confidence) => {
    if (confidence >= 0.8) return 'success';
    if (confidence >= 0.6) return 'warning';
    return 'error';
  };

  const getConfidenceLabel = (confidence) => {
    if (confidence >= 0.8) return 'High Confidence';
    if (confidence >= 0.6) return 'Medium Confidence';
    return 'Low Confidence';
  };

  return (
    <Card sx={{ 
      mb: 2, 
      border: 1, 
      borderColor: 'primary.main',
      bgcolor: 'primary.50'
    }}>
      <CardContent>
        <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
          <HomeIcon sx={{ mr: 1, color: 'primary.main' }} />
          <Typography variant="h6" sx={{ fontWeight: 600 }}>
            Property Detected
          </Typography>
          <Box sx={{ ml: 'auto', display: 'flex', alignItems: 'center', gap: 1 }}>
            <Chip
              label={getConfidenceLabel(confidence)}
              color={getConfidenceColor(confidence)}
              size="small"
              icon={confidence >= 0.8 ? <CheckIcon /> : <WarningIcon />}
            />
            <LinearProgress
              variant="determinate"
              value={confidence * 100}
              color={getConfidenceColor(confidence)}
              sx={{ width: 60, height: 6, borderRadius: 3 }}
            />
          </Box>
        </Box>

        {/* Property Details Grid */}
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
          <>
            <Divider sx={{ my: 2 }} />
            <Box>
              <Typography variant="subtitle2" sx={{ mb: 1, fontWeight: 600 }}>
                Extracted Information:
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
          </>
        )}

        {/* Actions */}
        {showActions && (
          <>
            <Divider sx={{ my: 2 }} />
            <Box sx={{ display: 'flex', gap: 1, justifyContent: 'flex-end' }}>
              <Tooltip title="View Property Details">
                <IconButton
                  size="small"
                  onClick={() => onViewDetails && onViewDetails(detectedProperty)}
                  color="primary"
                >
                  <InfoIcon />
                </IconButton>
              </Tooltip>
              <Tooltip title="Use in Chat">
                <IconButton
                  size="small"
                  onClick={() => onPropertyClick && onPropertyClick(detectedProperty)}
                  color="primary"
                >
                  <CheckIcon />
                </IconButton>
              </Tooltip>
            </Box>
          </>
        )}

        {/* Low Confidence Warning */}
        {confidence < 0.6 && (
          <Alert severity="warning" sx={{ mt: 2 }}>
            <Typography variant="body2">
              Low confidence detection. Please verify the property information.
            </Typography>
          </Alert>
        )}
      </CardContent>
    </Card>
  );
};

export default PropertyDetectionCard;
