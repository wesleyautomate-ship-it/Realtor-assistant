import React, { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Grid,
  Card,
  CardContent,
  CardMedia,
  Button,
  TextField,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Chip,
  IconButton,
  ToggleButton,
  ToggleButtonGroup,
  Slider,
  CircularProgress,
  Alert,
  Snackbar,
  useMediaQuery,
  useTheme,
  Stack,
  Skeleton,
  Fade,
  Grow,
  Divider,
  Collapse,
} from '@mui/material';
import {
  Search as SearchIcon,
  LocationOn as LocationIcon,
  Hotel as BedroomIcon,
  ViewModule as GridIcon,
  ViewList as ListIcon,
  Map as MapIcon,
  FilterList as FilterIcon,
  Favorite as FavoriteIcon,
  FavoriteBorder as FavoriteBorderIcon,
  Assessment as AssessmentIcon,
  Phone as PhoneIcon,
} from '@mui/icons-material';
import { useAppContext } from '../context/AppContext';
import { apiUtils, handleApiError } from '../utils/api';

const Properties = () => {
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('md'));
  const isSmallScreen = useMediaQuery(theme.breakpoints.down('sm'));
  
  const { currentUser } = useAppContext();
  const [properties, setProperties] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [viewMode, setViewMode] = useState('grid');
  const [showFilters, setShowFilters] = useState(!isMobile);
  const [snackbar, setSnackbar] = useState({ open: false, message: '', severity: 'info' });
  const [filters, setFilters] = useState({
    search: '',
    location: '',
    propertyType: '',
    minPrice: 0,
    maxPrice: 10000000,
    bedrooms: '',
    priceRange: [0, 10000000],
  });

  useEffect(() => {
    fetchProperties();
  }, []);

  const fetchProperties = async (filterParams = {}) => {
    try {
      setLoading(true);
      setError(null);
      
      const response = await apiUtils.getProperties(filterParams);
      setProperties(response.properties || []);
    } catch (error) {
      console.log('No properties data available');
      setProperties([]);
    } finally {
      setLoading(false);
    }
  };

  const handleViewModeChange = (event, newViewMode) => {
    if (newViewMode !== null) {
      setViewMode(newViewMode);
    }
  };

  const handleFilterChange = async (field, value) => {
    const newFilters = {
      ...filters,
      [field]: value,
    };
    
    setFilters(newFilters);

    // Apply filters to API call
    const filterParams = {
      search: newFilters.search,
      location: newFilters.location,
      property_type: newFilters.propertyType,
      min_price: newFilters.priceRange[0],
      max_price: newFilters.priceRange[1],
      bedrooms: newFilters.bedrooms,
    };

    await fetchProperties(filterParams);
  };

  const handlePriceRangeChange = async (event, newValue) => {
    const newFilters = {
      ...filters,
      priceRange: newValue,
    };
    
    setFilters(newFilters);

    // Apply price filter to API call
    const filterParams = {
      search: newFilters.search,
      location: newFilters.location,
      property_type: newFilters.propertyType,
      min_price: newValue[0],
      max_price: newValue[1],
      bedrooms: newFilters.bedrooms,
    };

    await fetchProperties(filterParams);
  };

  const toggleFavorite = async (propertyId) => {
    try {
      // Update local state immediately for better UX
      setProperties(prev => 
        prev.map(property => 
          property.id === propertyId 
            ? { ...property, favorite: !property.favorite }
            : property
        )
      );

      // Call API to update favorite status
      await apiUtils.executeAction('toggle-favorite', {
        property_id: propertyId,
        user_id: currentUser?.id,
      });

      setSnackbar({
        open: true,
        message: 'Favorite status updated successfully!',
        severity: 'success',
      });
    } catch (error) {
      // Revert local state if API call fails
      setProperties(prev => 
        prev.map(property => 
          property.id === propertyId 
            ? { ...property, favorite: !property.favorite }
            : property
        )
      );

      const errorMessage = handleApiError(error);
      setSnackbar({
        open: true,
        message: `Failed to update favorite: ${errorMessage}`,
        severity: 'error',
      });
    }
  };

  const handleQuickAction = async (action, propertyId) => {
    try {
      setSnackbar({
        open: true,
        message: `Executing ${action}...`,
        severity: 'info',
      });

      const result = await apiUtils.executeAction(action, {
        property_id: propertyId,
        user_id: currentUser?.id,
      });

      setSnackbar({
        open: true,
        message: `${action} completed successfully!`,
        severity: 'success',
      });

      console.log(`${action} result:`, result);
    } catch (error) {
      const errorMessage = handleApiError(error);
      setSnackbar({
        open: true,
        message: `Failed to execute ${action}: ${errorMessage}`,
        severity: 'error',
      });
    }
  };

  const formatPrice = (price) => {
    return new Intl.NumberFormat('en-AE', {
      style: 'currency',
      currency: 'AED',
      minimumFractionDigits: 0,
      maximumFractionDigits: 0,
    }).format(price);
  };

  const filteredProperties = properties.filter(property => {
    const searchTerm = filters.search.toLowerCase();
    const title = (property.title || '').toLowerCase();
    const location = (property.location || '').toLowerCase();
    
    const matchesSearch = title.includes(searchTerm) || location.includes(searchTerm);
    const matchesLocation = !filters.location || (property.location || '') === filters.location;
    const matchesType = !filters.propertyType || (property.propertyType || '') === filters.propertyType;
    const matchesBedrooms = !filters.bedrooms || (property.bedrooms || 0) === parseInt(filters.bedrooms);
    const matchesPrice = (property.price || 0) >= filters.priceRange[0] && (property.price || 0) <= filters.priceRange[1];
    
    return matchesSearch && matchesLocation && matchesType && matchesBedrooms && matchesPrice;
  });

  const PropertyCard = ({ property }) => (
    <Card sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
      <Box sx={{ position: 'relative' }}>
        <CardMedia
          component="img"
          height="200"
          image={property.image}
          alt={property.title}
        />
        <IconButton
          sx={{ position: 'absolute', top: 8, right: 8, bgcolor: 'rgba(255,255,255,0.8)' }}
          onClick={() => toggleFavorite(property.id)}
        >
          {property.favorite ? <FavoriteIcon color="error" /> : <FavoriteBorderIcon />}
        </IconButton>
        <Chip
          label={property.status}
          color={property.status === 'Ready' ? 'success' : 'warning'}
          size="small"
          sx={{ position: 'absolute', top: 8, left: 8 }}
        />
      </Box>
      
      <CardContent sx={{ flexGrow: 1, display: 'flex', flexDirection: 'column' }}>
        <Typography variant="h6" sx={{ mb: 1, fontWeight: 600 }}>
          {property.title || 'Untitled Property'}
        </Typography>
        
        <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
          <LocationIcon fontSize="small" color="action" sx={{ mr: 0.5 }} />
          <Typography variant="body2" color="text.secondary">
            {property.location || 'Location not specified'}
          </Typography>
        </Box>

        <Box sx={{ display: 'flex', gap: 1, mb: 2 }}>
          <Chip
            icon={<BedroomIcon />}
            label={`${property.bedrooms || 0} BR`}
            size="small"
            variant="outlined"
          />
          <Chip
            label={`${property.bathrooms || 0} Bath`}
            size="small"
            variant="outlined"
          />
          <Chip
            label={`${property.area || 0} sqft`}
            size="small"
            variant="outlined"
          />
        </Box>

        <Typography variant="h5" color="primary" sx={{ fontWeight: 600, mb: 2 }}>
          {formatPrice(property.price || 0)}
        </Typography>

        <Typography variant="body2" color="text.secondary" sx={{ mb: 2, flexGrow: 1 }}>
          {property.description || 'No description available'}
        </Typography>

        <Box sx={{ display: 'flex', gap: 1, flexWrap: 'wrap', mb: 2 }}>
          {(property.amenities || []).slice(0, 3).map((amenity, index) => (
            <Chip key={index} label={amenity} size="small" />
          ))}
          {(property.amenities || []).length > 3 && (
            <Chip label={`+${(property.amenities || []).length - 3} more`} size="small" variant="outlined" />
          )}
        </Box>

        <Box sx={{ display: 'flex', gap: 1 }}>
          <Button
            size="small"
            variant="outlined"
            startIcon={<AssessmentIcon />}
            onClick={() => handleQuickAction('generate-cma', property.id)}
            sx={{ flex: 1 }}
          >
            Generate CMA
          </Button>
          <Button
            size="small"
            variant="contained"
            startIcon={<PhoneIcon />}
            onClick={() => handleQuickAction('contact-agent', property.id)}
            sx={{ flex: 1 }}
          >
            Contact
          </Button>
        </Box>
      </CardContent>
    </Card>
  );

  const PropertyListItem = ({ property }) => (
    <Card sx={{ mb: 2 }}>
      <Grid container>
        <Grid item xs={12} md={4}>
          <CardMedia
            component="img"
            height="200"
            image={property.image}
            alt={property.title}
          />
        </Grid>
        <Grid item xs={12} md={8}>
          <CardContent>
            <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', mb: 2 }}>
              <Box>
                <Typography variant="h6" sx={{ fontWeight: 600 }}>
                  {property.title || 'Untitled Property'}
                </Typography>
                <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                  <LocationIcon fontSize="small" color="action" sx={{ mr: 0.5 }} />
                  <Typography variant="body2" color="text.secondary">
                    {property.location || 'Location not specified'}
                  </Typography>
                </Box>
              </Box>
              <IconButton onClick={() => toggleFavorite(property.id)}>
                {property.favorite ? <FavoriteIcon color="error" /> : <FavoriteBorderIcon />}
              </IconButton>
            </Box>

            <Box sx={{ display: 'flex', gap: 1, mb: 2 }}>
              <Chip icon={<BedroomIcon />} label={`${property.bedrooms || 0} BR`} size="small" />
              <Chip label={`${property.bathrooms || 0} Bath`} size="small" />
              <Chip label={`${property.area || 0} sqft`} size="small" />
              <Chip label={property.propertyType || 'Unknown'} size="small" color="primary" />
            </Box>

            <Typography variant="h5" color="primary" sx={{ fontWeight: 600, mb: 2 }}>
              {formatPrice(property.price || 0)}
            </Typography>

            <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
              {property.description || 'No description available'}
            </Typography>

            <Box sx={{ display: 'flex', gap: 1 }}>
              <Button
                size="small"
                variant="outlined"
                startIcon={<AssessmentIcon />}
                onClick={() => handleQuickAction('generate-cma', property.id)}
              >
                Generate CMA
              </Button>
              <Button
                size="small"
                variant="contained"
                startIcon={<PhoneIcon />}
                onClick={() => handleQuickAction('contact-agent', property.id)}
              >
                Contact Agent
              </Button>
            </Box>
          </CardContent>
        </Grid>
      </Grid>
    </Card>
  );

  const handleCloseSnackbar = () => {
    setSnackbar({ ...snackbar, open: false });
  };

  // Skeleton loader for properties
  const PropertySkeleton = () => (
    <Grid container spacing={3}>
      {[1, 2, 3, 4, 5, 6].map((item) => (
        <Grid item xs={12} sm={6} md={4} lg={3} key={item}>
          <Card>
            <Skeleton variant="rectangular" width="100%" height={200} />
            <CardContent>
              <Stack spacing={1}>
                <Skeleton variant="text" width="80%" height={24} />
                <Skeleton variant="text" width="60%" height={20} />
                <Skeleton variant="text" width="40%" height={20} />
                <Stack direction="row" spacing={1}>
                  <Skeleton variant="rectangular" width={60} height={24} />
                  <Skeleton variant="rectangular" width={80} height={24} />
                </Stack>
              </Stack>
            </CardContent>
          </Card>
        </Grid>
      ))}
    </Grid>
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
      <HomeIcon 
        sx={{ 
          fontSize: 64, 
          color: 'text.secondary',
          mb: theme.spacing(2)
        }} 
      />
      <Typography variant="h6" color="text.secondary" gutterBottom>
        No properties found
      </Typography>
      <Typography variant="body2" color="text.secondary" sx={{ mb: theme.spacing(3) }}>
        Try adjusting your filters or search criteria to find more properties.
      </Typography>
      <Button
        variant="contained"
        onClick={() => {
          setFilters({
            search: '',
            location: '',
            propertyType: '',
            minPrice: 0,
            maxPrice: 10000000,
            bedrooms: '',
            priceRange: [0, 10000000],
          });
          fetchProperties();
        }}
      >
        Clear Filters
      </Button>
    </Box>
  );

  if (loading) {
    return <PropertySkeleton />;
  }

  return (
    <Box>
      {/* Header */}
      <Box sx={{ mb: 4 }}>
        <Typography variant="h4" sx={{ fontWeight: 600, mb: 1 }}>
          Properties
        </Typography>
        <Typography variant="body1" color="text.secondary">
          Browse {filteredProperties.length} properties in Dubai
        </Typography>
      </Box>

      <Grid container spacing={3}>
        {/* Filter Panel */}
        <Grid item xs={12} md={3}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                <FilterIcon sx={{ mr: 1 }} />
                <Typography variant="h6">Filters</Typography>
              </Box>

              <TextField
                fullWidth
                placeholder="Search properties..."
                value={filters.search}
                onChange={(e) => handleFilterChange('search', e.target.value)}
                InputProps={{
                  startAdornment: <SearchIcon />,
                }}
                sx={{ mb: 2 }}
              />

              <FormControl fullWidth sx={{ mb: 2 }}>
                <InputLabel>Location</InputLabel>
                <Select
                  value={filters.location}
                  label="Location"
                  onChange={(e) => handleFilterChange('location', e.target.value)}
                >
                  <MenuItem value="">All Locations</MenuItem>
                  <MenuItem value="Dubai Marina">Dubai Marina</MenuItem>
                  <MenuItem value="Palm Jumeirah">Palm Jumeirah</MenuItem>
                  <MenuItem value="Downtown Dubai">Downtown Dubai</MenuItem>
                  <MenuItem value="Arabian Ranches">Arabian Ranches</MenuItem>
                  <MenuItem value="JLT">JLT</MenuItem>
                  <MenuItem value="Emirates Hills">Emirates Hills</MenuItem>
                </Select>
              </FormControl>

              <FormControl fullWidth sx={{ mb: 2 }}>
                <InputLabel>Type</InputLabel>
                <Select
                  value={filters.propertyType}
                  label="Type"
                  onChange={(e) => handleFilterChange('propertyType', e.target.value)}
                >
                  <MenuItem value="">All Types</MenuItem>
                  <MenuItem value="Apartment">Apartment</MenuItem>
                  <MenuItem value="Villa">Villa</MenuItem>
                  <MenuItem value="Penthouse">Penthouse</MenuItem>
                  <MenuItem value="Studio">Studio</MenuItem>
                  <MenuItem value="Townhouse">Townhouse</MenuItem>
                </Select>
              </FormControl>

              <Box sx={{ mb: 2 }}>
                <Typography variant="subtitle2" sx={{ mb: 1 }}>
                  Price Range
                </Typography>
                <Slider
                  value={filters.priceRange}
                  onChange={handlePriceRangeChange}
                  valueLabelDisplay="auto"
                  min={0}
                  max={10000000}
                  step={100000}
                  valueLabelFormat={(value) => formatPrice(value)}
                />
                <Box sx={{ display: 'flex', justifyContent: 'space-between', mt: 1 }}>
                  <Typography variant="caption">
                    {formatPrice(filters.priceRange[0])}
                  </Typography>
                  <Typography variant="caption">
                    {formatPrice(filters.priceRange[1])}
                  </Typography>
                </Box>
              </Box>

              <FormControl fullWidth>
                <InputLabel>Bedrooms</InputLabel>
                <Select
                  value={filters.bedrooms}
                  label="Bedrooms"
                  onChange={(e) => handleFilterChange('bedrooms', e.target.value)}
                >
                  <MenuItem value="">Any</MenuItem>
                  <MenuItem value={0}>Studio</MenuItem>
                  <MenuItem value={1}>1 Bedroom</MenuItem>
                  <MenuItem value={2}>2 Bedrooms</MenuItem>
                  <MenuItem value={3}>3 Bedrooms</MenuItem>
                  <MenuItem value={4}>4+ Bedrooms</MenuItem>
                </Select>
              </FormControl>
            </CardContent>
          </Card>
        </Grid>

        {/* Properties List */}
        <Grid item xs={12} md={9}>
          {/* View Toggle and Results */}
          <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
            <Typography variant="body2" color="text.secondary">
              Showing {filteredProperties.length} properties
            </Typography>
            <ToggleButtonGroup
              value={viewMode}
              exclusive
              onChange={handleViewModeChange}
              size="small"
            >
              <ToggleButton value="grid">
                <GridIcon />
              </ToggleButton>
              <ToggleButton value="list">
                <ListIcon />
              </ToggleButton>
              <ToggleButton value="map">
                <MapIcon />
              </ToggleButton>
            </ToggleButtonGroup>
          </Box>

          {/* Properties Grid/List */}
          {viewMode === 'grid' && (
            <Grid container spacing={3}>
              {filteredProperties.map((property) => (
                <Grid item xs={12} sm={6} lg={4} key={property.id}>
                  <PropertyCard property={property} />
                </Grid>
              ))}
            </Grid>
          )}

          {viewMode === 'list' && (
            <Box>
              {filteredProperties.map((property) => (
                <PropertyListItem key={property.id} property={property} />
              ))}
            </Box>
          )}

          {viewMode === 'map' && (
            <Card sx={{ height: 400, display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
              <Typography variant="h6" color="text.secondary">
                Map view will be implemented in Phase 3
              </Typography>
            </Card>
          )}

          {filteredProperties.length === 0 && (
            <Card sx={{ p: 4, textAlign: 'center' }}>
              <Typography variant="h6" color="text.secondary" sx={{ mb: 2 }}>
                No properties found
              </Typography>
              <Typography variant="body2" color="text.secondary">
                Try adjusting your filters to see more results
              </Typography>
            </Card>
          )}
        </Grid>
      </Grid>

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

export default Properties;
