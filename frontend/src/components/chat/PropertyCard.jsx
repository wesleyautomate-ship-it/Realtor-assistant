import React from 'react';
import {
  Card,
  CardContent,
  CardMedia,
  CardActions,
  Typography,
  Box,
  Chip,
  Rating,
  Button,
  IconButton,
  Avatar,
  Divider
} from '@mui/material';
import {
  Home as HomeIcon,
  Bed as BedIcon,
  Bathtub as BathIcon,
  SquareFoot as SqftIcon,
  LocationOn as LocationIcon,
  AttachMoney as PriceIcon,
  Visibility as ViewIcon,
  Favorite as FavoriteIcon,
  Share as ShareIcon
} from '@mui/icons-material';

const PropertyCard = ({ property, compact = false, onClick, onView, onFavorite, onShare }) => {
  const formatPrice = (price) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      minimumFractionDigits: 0,
      maximumFractionDigits: 0,
    }).format(price);
  };

  const formatAddress = (address) => {
    if (!address) return 'Address not available';
    return address.length > 50 ? `${address.substring(0, 50)}...` : address;
  };

  const getStatusColor = (status) => {
    switch (status?.toLowerCase()) {
      case 'active':
      case 'for sale':
        return 'success';
      case 'pending':
      case 'under contract':
        return 'warning';
      case 'sold':
        return 'error';
      case 'off market':
        return 'default';
      default:
        return 'primary';
    }
  };

  const getPropertyTypeIcon = (type) => {
    switch (type?.toLowerCase()) {
      case 'apartment':
        return '🏢';
      case 'house':
      case 'single family':
        return '🏠';
      case 'condo':
        return '🏢';
      case 'townhouse':
        return '🏘️';
      case 'villa':
        return '🏰';
      default:
        return '🏠';
    }
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
        onClick={onClick}
      >
        <CardMedia
          component="img"
          height="140"
          image={property.image_url || '/default-property.jpg'}
          alt={property.address}
          sx={{ objectFit: 'cover' }}
        />
        <CardContent sx={{ p: 2 }}>
          <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
            <Typography variant="h6" component="div" sx={{ flexGrow: 1, fontWeight: 'bold' }}>
              {formatPrice(property.price)}
            </Typography>
            <Chip 
              label={property.listing_status || 'Active'} 
              size="small" 
              color={getStatusColor(property.listing_status)}
            />
          </Box>
          
          <Typography variant="body2" color="text.secondary" sx={{ mb: 1 }}>
            {formatAddress(property.address)}
          </Typography>
          
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 1 }}>
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 0.5 }}>
              <BedIcon fontSize="small" color="action" />
              <Typography variant="body2">{property.bedrooms || 'N/A'}</Typography>
            </Box>
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 0.5 }}>
              <BathIcon fontSize="small" color="action" />
              <Typography variant="body2">{property.bathrooms || 'N/A'}</Typography>
            </Box>
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 0.5 }}>
              <SqftIcon fontSize="small" color="action" />
              <Typography variant="body2">{property.square_feet ? `${property.square_feet} sqft` : 'N/A'}</Typography>
            </Box>
          </Box>
          
          <Typography variant="body2" color="text.secondary">
            {property.property_type || 'Property'}
          </Typography>
        </CardContent>
      </Card>
    );
  }

  return (
    <Card sx={{ maxWidth: 400, mb: 2 }}>
      <CardMedia
        component="img"
        height="200"
        image={property.image_url || '/default-property.jpg'}
        alt={property.address}
        sx={{ objectFit: 'cover' }}
      />
      
      <CardContent>
        <Box sx={{ display: 'flex', alignItems: 'flex-start', justifyContent: 'space-between', mb: 2 }}>
          <Box sx={{ flexGrow: 1 }}>
            <Typography variant="h5" component="div" sx={{ fontWeight: 'bold', color: 'primary.main' }}>
              {formatPrice(property.price)}
            </Typography>
            <Typography variant="body1" color="text.secondary" sx={{ mb: 1 }}>
              {property.address}
            </Typography>
          </Box>
          <Chip 
            label={property.listing_status || 'Active'} 
            color={getStatusColor(property.listing_status)}
            size="small"
          />
        </Box>

        <Divider sx={{ my: 2 }} />

        <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, mb: 2 }}>
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 0.5 }}>
            <BedIcon color="action" />
            <Typography variant="body2">{property.bedrooms || 'N/A'} beds</Typography>
          </Box>
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 0.5 }}>
            <BathIcon color="action" />
            <Typography variant="body2">{property.bathrooms || 'N/A'} baths</Typography>
          </Box>
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 0.5 }}>
            <SqftIcon color="action" />
            <Typography variant="body2">{property.square_feet ? `${property.square_feet} sqft` : 'N/A'}</Typography>
          </Box>
        </Box>

        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 2 }}>
          <Avatar sx={{ bgcolor: 'primary.main', width: 24, height: 24 }}>
            <Typography variant="caption">{getPropertyTypeIcon(property.property_type)}</Typography>
          </Avatar>
          <Typography variant="body2" color="text.secondary">
            {property.property_type || 'Property'}
          </Typography>
        </Box>

        {property.description && (
          <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
            {property.description.length > 150 
              ? `${property.description.substring(0, 150)}...` 
              : property.description
            }
          </Typography>
        )}

        {property.rating && (
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 2 }}>
            <Rating value={property.rating} readOnly size="small" />
            <Typography variant="body2" color="text.secondary">
              ({property.rating_count || 0} reviews)
            </Typography>
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
          >
            View Details
          </Button>
        </Box>
        
        <Box sx={{ display: 'flex', gap: 0.5 }}>
          <IconButton 
            size="small" 
            onClick={onFavorite}
            color={property.is_favorite ? 'error' : 'default'}
          >
            <FavoriteIcon fontSize="small" />
          </IconButton>
          <IconButton size="small" onClick={onShare}>
            <ShareIcon fontSize="small" />
          </IconButton>
        </Box>
      </CardActions>
    </Card>
  );
};

export default PropertyCard;
