import React, { useState, useEffect } from 'react';

const ModernPropertyManagement = ({ properties = [] }) => {
  const [filteredProperties, setFilteredProperties] = useState(properties);
  const [filters, setFilters] = useState({
    minPrice: '',
    maxPrice: '',
    bedrooms: 'any',
    bathrooms: 'any',
    propertyType: 'any',
    location: 'any',
    minSqFt: '',
    maxSqFt: ''
  });
  const [searchTerm, setSearchTerm] = useState('');
  const [sortBy, setSortBy] = useState('price');
  const [viewMode, setViewMode] = useState('grid'); // 'grid' or 'list'

  // Sample property types and locations for filters
  const propertyTypes = ['Apartment', 'Villa', 'Townhouse', 'Penthouse', 'Studio', 'Duplex'];
  const locations = ['Downtown Dubai', 'Dubai Marina', 'Palm Jumeirah', 'Business Bay', 'Dubai Hills Estate'];

  useEffect(() => {
    let filtered = [...properties];

    // Apply search filter
    if (searchTerm) {
      filtered = filtered.filter(property =>
        property.address.toLowerCase().includes(searchTerm.toLowerCase()) ||
        property.property_type.toLowerCase().includes(searchTerm.toLowerCase()) ||
        property.area.toLowerCase().includes(searchTerm.toLowerCase())
      );
    }

    // Apply price filters
    if (filters.minPrice) {
      filtered = filtered.filter(property => property.price_aed >= parseInt(filters.minPrice));
    }
    if (filters.maxPrice) {
      filtered = filtered.filter(property => property.price_aed <= parseInt(filters.maxPrice));
    }

    // Apply bedroom filter
    if (filters.bedrooms !== 'any') {
      filtered = filtered.filter(property => property.bedrooms === parseInt(filters.bedrooms));
    }

    // Apply bathroom filter
    if (filters.bathrooms !== 'any') {
      filtered = filtered.filter(property => property.bathrooms === parseInt(filters.bathrooms));
    }

    // Apply property type filter
    if (filters.propertyType !== 'any') {
      filtered = filtered.filter(property => property.property_type === filters.propertyType);
    }

    // Apply location filter
    if (filters.location !== 'any') {
      filtered = filtered.filter(property => property.area === filters.location);
    }

    // Apply square footage filters
    if (filters.minSqFt) {
      filtered = filtered.filter(property => property.square_feet >= parseInt(filters.minSqFt));
    }
    if (filters.maxSqFt) {
      filtered = filtered.filter(property => property.square_feet <= parseInt(filters.maxSqFt));
    }

    // Apply sorting
    filtered.sort((a, b) => {
      switch (sortBy) {
        case 'price':
          return a.price_aed - b.price_aed;
        case 'price-desc':
          return b.price_aed - a.price_aed;
        case 'size':
          return a.square_feet - b.square_feet;
        case 'bedrooms':
          return b.bedrooms - a.bedrooms;
        default:
          return 0;
      }
    });

    setFilteredProperties(filtered);
  }, [properties, filters, searchTerm, sortBy]);

  const handleFilterChange = (key, value) => {
    setFilters(prev => ({ ...prev, [key]: value }));
  };

  const clearFilters = () => {
    setFilters({
      minPrice: '',
      maxPrice: '',
      bedrooms: 'any',
      bathrooms: 'any',
      propertyType: 'any',
      location: 'any',
      minSqFt: '',
      maxSqFt: ''
    });
    setSearchTerm('');
    setSortBy('price');
  };

  const formatPrice = (price) => {
    return new Intl.NumberFormat('en-AE', {
      style: 'currency',
      currency: 'AED',
      minimumFractionDigits: 0,
      maximumFractionDigits: 0,
    }).format(price);
  };

  const getPropertyIcon = (type) => {
    const icons = {
      'Apartment': '🏢',
      'Villa': '🏡',
      'Townhouse': '🏘️',
      'Penthouse': '🏙️',
      'Studio': '🏠',
      'Duplex': '🏛️'
    };
    return icons[type] || '🏠';
  };

  return (
    <div className="property-container">
      {/* Header */}
      <div className="property-header">
        <div className="flex items-center justify-between w-full p-6">
          <div className="flex items-center">
            <div className="w-12 h-12 bg-gradient-to-br from-primary-500 to-primary-300 rounded-full flex items-center justify-center text-2xl font-bold text-secondary-50 mr-4 shadow-lg">
              🏠
            </div>
            <div>
              <h1 className="text-2xl font-bold text-primary-500">Property Management</h1>
              <p className="text-sm text-text-secondary">
                {filteredProperties.length} properties found
              </p>
            </div>
          </div>
          
          <div className="flex items-center gap-4">
            <button
              className={`btn ${viewMode === 'grid' ? 'btn-primary' : 'btn-secondary'} btn-sm`}
              onClick={() => setViewMode('grid')}
            >
              📊 Grid
            </button>
            <button
              className={`btn ${viewMode === 'list' ? 'btn-primary' : 'btn-secondary'} btn-sm`}
              onClick={() => setViewMode('list')}
            >
              📋 List
            </button>
          </div>
        </div>
      </div>

      {/* Filters */}
      <div className="card m-6">
        <div className="card-header">
          <h3 className="text-lg font-semibold text-text-primary">Filters & Search</h3>
        </div>
        <div className="card-body">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            {/* Search */}
            <div className="lg:col-span-2">
              <label className="block text-sm font-medium text-text-secondary mb-2">Search</label>
              <input
                type="text"
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                placeholder="Search by address, type, or area..."
                className="input w-full"
              />
            </div>

            {/* Price Range */}
            <div>
              <label className="block text-sm font-medium text-text-secondary mb-2">Min Price (AED)</label>
              <input
                type="number"
                value={filters.minPrice}
                onChange={(e) => handleFilterChange('minPrice', e.target.value)}
                placeholder="Min price"
                className="input w-full"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-text-secondary mb-2">Max Price (AED)</label>
              <input
                type="number"
                value={filters.maxPrice}
                onChange={(e) => handleFilterChange('maxPrice', e.target.value)}
                placeholder="Max price"
                className="input w-full"
              />
            </div>

            {/* Property Type */}
            <div>
              <label className="block text-sm font-medium text-text-secondary mb-2">Property Type</label>
              <select
                value={filters.propertyType}
                onChange={(e) => handleFilterChange('propertyType', e.target.value)}
                className="input w-full"
              >
                <option value="any">Any Type</option>
                {propertyTypes.map(type => (
                  <option key={type} value={type}>{type}</option>
                ))}
              </select>
            </div>

            {/* Location */}
            <div>
              <label className="block text-sm font-medium text-text-secondary mb-2">Location</label>
              <select
                value={filters.location}
                onChange={(e) => handleFilterChange('location', e.target.value)}
                className="input w-full"
              >
                <option value="any">Any Location</option>
                {locations.map(location => (
                  <option key={location} value={location}>{location}</option>
                ))}
              </select>
            </div>

            {/* Bedrooms */}
            <div>
              <label className="block text-sm font-medium text-text-secondary mb-2">Bedrooms</label>
              <select
                value={filters.bedrooms}
                onChange={(e) => handleFilterChange('bedrooms', e.target.value)}
                className="input w-full"
              >
                <option value="any">Any</option>
                {[1, 2, 3, 4, 5, 6].map(num => (
                  <option key={num} value={num}>{num}+</option>
                ))}
              </select>
            </div>

            {/* Bathrooms */}
            <div>
              <label className="block text-sm font-medium text-text-secondary mb-2">Bathrooms</label>
              <select
                value={filters.bathrooms}
                onChange={(e) => handleFilterChange('bathrooms', e.target.value)}
                className="input w-full"
              >
                <option value="any">Any</option>
                {[1, 2, 3, 4, 5].map(num => (
                  <option key={num} value={num}>{num}+</option>
                ))}
              </select>
            </div>
          </div>

          <div className="flex items-center justify-between mt-6">
            <div className="flex items-center gap-4">
              <label className="text-sm font-medium text-text-secondary">Sort by:</label>
              <select
                value={sortBy}
                onChange={(e) => setSortBy(e.target.value)}
                className="input"
              >
                <option value="price">Price (Low to High)</option>
                <option value="price-desc">Price (High to Low)</option>
                <option value="size">Size</option>
                <option value="bedrooms">Bedrooms</option>
              </select>
            </div>

            <button
              onClick={clearFilters}
              className="btn btn-ghost btn-sm"
            >
              🗑️ Clear Filters
            </button>
          </div>
        </div>
      </div>

      {/* Properties Grid/List */}
      <div className="p-6">
        {filteredProperties.length === 0 ? (
          <div className="flex flex-col items-center justify-center py-12 text-center">
            <div className="w-16 h-16 bg-gradient-to-br from-primary-500 to-primary-300 rounded-full flex items-center justify-center text-3xl mb-4">
              🏠
            </div>
            <h3 className="text-xl font-semibold text-text-primary mb-2">No Properties Found</h3>
            <p className="text-text-secondary max-w-md">
              Try adjusting your filters or search terms to find more properties.
            </p>
          </div>
        ) : (
          <div className={viewMode === 'grid' ? 'property-grid' : 'space-y-4'}>
            {filteredProperties.map((property, index) => (
              <div
                key={index}
                className={`property-card ${viewMode === 'list' ? 'flex items-center' : ''}`}
              >
                <div className={`${viewMode === 'list' ? 'flex-1 flex items-center' : ''}`}>
                  <div className={`${viewMode === 'list' ? 'flex items-center gap-6' : 'p-6'}`}>
                    <div className={`${viewMode === 'list' ? 'w-20 h-20' : 'w-full h-48'} bg-gradient-to-br from-primary-500 to-primary-300 rounded-lg flex items-center justify-center text-4xl shadow-lg`}>
                      {getPropertyIcon(property.property_type)}
                    </div>
                    
                    <div className={`${viewMode === 'list' ? 'flex-1' : 'mt-4'}`}>
                      <div className="flex items-center justify-between mb-2">
                        <h3 className="text-lg font-semibold text-text-primary">
                          {property.property_type}
                        </h3>
                        <span className="text-xl font-bold text-primary-500">
                          {formatPrice(property.price_aed)}
                        </span>
                      </div>
                      
                      <p className="text-text-secondary mb-2">
                        📍 {property.address}
                      </p>
                      
                      <div className="flex items-center gap-4 text-sm text-text-secondary">
                        <span>🛏️ {property.bedrooms} beds</span>
                        <span>🚿 {property.bathrooms} baths</span>
                        <span>📏 {property.square_feet} sq ft</span>
                      </div>
                      
                      <div className="flex items-center gap-2 mt-3">
                        <span className="badge badge-primary">{property.area}</span>
                        <span className="badge badge-success">Available</span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default ModernPropertyManagement;
