import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './PropertyManagement.css';

const API_BASE_URL = 'http://localhost:8001';

const PropertyManagement = () => {
  const [properties, setProperties] = useState([]);
  const [selectedProperty, setSelectedProperty] = useState(null);
  const [loading, setLoading] = useState(false);
  const [propertyTypes, setPropertyTypes] = useState([]);
  const [locations, setLocations] = useState([]);
  
  // Search filters
  const [filters, setFilters] = useState({
    min_price: '',
    max_price: '',
    bedrooms: '',
    bathrooms: '',
    property_type: '',
    location: '',
    min_square_feet: '',
    max_square_feet: ''
  });

  // Load property types and locations on component mount
  useEffect(() => {
    loadPropertyTypes();
    loadLocations();
    searchProperties(); // Load initial properties
  }, []);

  const loadPropertyTypes = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/properties/types/list`);
      setPropertyTypes(response.data.property_types || []);
    } catch (error) {
      console.error('Error loading property types:', error);
    }
  };

  const loadLocations = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/properties/locations/list`);
      setLocations(response.data.locations || []);
    } catch (error) {
      console.error('Error loading locations:', error);
    }
  };

  const searchProperties = async () => {
    setLoading(true);
    try {
      // Build query parameters
      const params = {};
      Object.keys(filters).forEach(key => {
        if (filters[key] !== '') {
          params[key] = filters[key];
        }
      });

      const response = await axios.get(`${API_BASE_URL}/properties/search`, { params });
      setProperties(response.data);
    } catch (error) {
      console.error('Error searching properties:', error);
    } finally {
      setLoading(false);
    }
  };

  const getPropertyDetails = async (propertyId) => {
    try {
      const response = await axios.get(`${API_BASE_URL}/properties/${propertyId}`);
      setSelectedProperty(response.data);
    } catch (error) {
      console.error('Error getting property details:', error);
    }
  };

  const handleFilterChange = (field, value) => {
    setFilters(prev => ({
      ...prev,
      [field]: value
    }));
  };

  const handleSearch = (e) => {
    e.preventDefault();
    searchProperties();
  };

  const clearFilters = () => {
    setFilters({
      min_price: '',
      max_price: '',
      bedrooms: '',
      bathrooms: '',
      property_type: '',
      location: '',
      min_square_feet: '',
      max_square_feet: ''
    });
  };

  const formatPrice = (price) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      minimumFractionDigits: 0,
      maximumFractionDigits: 0,
    }).format(price);
  };

  return (
    <div className="property-management">
      <div className="property-header">
        <h2>🏠 Property Management</h2>
        <p>Search and manage properties with advanced filtering</p>
      </div>

      <div className="property-container">
        {/* Search and Filters Section */}
        <div className="search-section">
          <form onSubmit={handleSearch} className="search-form">
            <div className="filter-grid">
              {/* Price Range */}
              <div className="filter-group">
                <label>Price Range</label>
                <div className="price-inputs">
                  <input
                    type="number"
                    placeholder="Min Price"
                    value={filters.min_price}
                    onChange={(e) => handleFilterChange('min_price', e.target.value)}
                  />
                  <span>-</span>
                  <input
                    type="number"
                    placeholder="Max Price"
                    value={filters.max_price}
                    onChange={(e) => handleFilterChange('max_price', e.target.value)}
                  />
                </div>
              </div>

              {/* Bedrooms & Bathrooms */}
              <div className="filter-group">
                <label>Bedrooms</label>
                <select
                  value={filters.bedrooms}
                  onChange={(e) => handleFilterChange('bedrooms', e.target.value)}
                >
                  <option value="">Any</option>
                  <option value="1">1</option>
                  <option value="2">2</option>
                  <option value="3">3</option>
                  <option value="4">4</option>
                  <option value="5">5+</option>
                </select>
              </div>

              <div className="filter-group">
                <label>Bathrooms</label>
                <select
                  value={filters.bathrooms}
                  onChange={(e) => handleFilterChange('bathrooms', e.target.value)}
                >
                  <option value="">Any</option>
                  <option value="1">1</option>
                  <option value="2">2</option>
                  <option value="3">3</option>
                  <option value="4">4+</option>
                </select>
              </div>

              {/* Property Type */}
              <div className="filter-group">
                <label>Property Type</label>
                <select
                  value={filters.property_type}
                  onChange={(e) => handleFilterChange('property_type', e.target.value)}
                >
                  <option value="">Any Type</option>
                  {propertyTypes.map(type => (
                    <option key={type} value={type}>{type}</option>
                  ))}
                </select>
              </div>

              {/* Location */}
              <div className="filter-group">
                <label>Location</label>
                <select
                  value={filters.location}
                  onChange={(e) => handleFilterChange('location', e.target.value)}
                >
                  <option value="">Any Location</option>
                  {locations.map(location => (
                    <option key={location} value={location}>{location}</option>
                  ))}
                </select>
              </div>

              {/* Square Feet */}
              <div className="filter-group">
                <label>Square Feet</label>
                <div className="sqft-inputs">
                  <input
                    type="number"
                    placeholder="Min Sq Ft"
                    value={filters.min_square_feet}
                    onChange={(e) => handleFilterChange('min_square_feet', e.target.value)}
                  />
                  <span>-</span>
                  <input
                    type="number"
                    placeholder="Max Sq Ft"
                    value={filters.max_square_feet}
                    onChange={(e) => handleFilterChange('max_square_feet', e.target.value)}
                  />
                </div>
              </div>
            </div>

            <div className="search-actions">
              <button type="submit" className="search-btn" disabled={loading}>
                {loading ? '🔍 Searching...' : '🔍 Search Properties'}
              </button>
              <button type="button" className="clear-btn" onClick={clearFilters}>
                🗑️ Clear Filters
              </button>
            </div>
          </form>
        </div>

        {/* Results Section */}
        <div className="results-section">
          <div className="results-header">
            <h3>Properties ({properties.length} found)</h3>
          </div>

          {loading ? (
            <div className="loading">⏳ Loading properties...</div>
          ) : properties.length === 0 ? (
            <div className="no-results">📭 No properties found matching your criteria</div>
          ) : (
            <div className="properties-grid">
              {properties.map((property, index) => (
                <div
                  key={index}
                  className="property-card"
                  onClick={() => getPropertyDetails(index + 1)}
                >
                  <div className="property-image">
                    <div className="image-placeholder">🏠</div>
                  </div>
                  <div className="property-info">
                    <h4 className="property-address">{property.address}</h4>
                    <div className="property-price">{formatPrice(property.price)}</div>
                    <div className="property-details">
                      <span>🛏️ {property.bedrooms} beds</span>
                      <span>🚿 {property.bathrooms} baths</span>
                      {property.square_feet && (
                        <span>📏 {property.square_feet.toLocaleString()} sq ft</span>
                      )}
                    </div>
                    <div className="property-type">{property.property_type}</div>
                    <p className="property-description">
                      {property.description.length > 100
                        ? `${property.description.substring(0, 100)}...`
                        : property.description}
                    </p>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Property Details Modal */}
        {selectedProperty && (
          <div className="property-modal-overlay" onClick={() => setSelectedProperty(null)}>
            <div className="property-modal" onClick={(e) => e.stopPropagation()}>
              <div className="modal-header">
                <h3>Property Details</h3>
                <button className="close-btn" onClick={() => setSelectedProperty(null)}>
                  ✕
                </button>
              </div>

              <div className="modal-content">
                {/* Main Property Info */}
                <div className="property-detail-main">
                  <div className="detail-image">
                    <div className="image-placeholder-large">🏠</div>
                  </div>
                  <div className="detail-info">
                    <h2>{selectedProperty.property.address}</h2>
                    <div className="detail-price">{formatPrice(selectedProperty.property.price)}</div>
                    <div className="detail-stats">
                      <span>🛏️ {selectedProperty.property.bedrooms} Bedrooms</span>
                      <span>🚿 {selectedProperty.property.bathrooms} Bathrooms</span>
                      {selectedProperty.property.square_feet && (
                        <span>📏 {selectedProperty.property.square_feet.toLocaleString()} sq ft</span>
                      )}
                    </div>
                    <div className="detail-type">{selectedProperty.property.property_type}</div>
                    <p className="detail-description">{selectedProperty.property.description}</p>
                  </div>
                </div>

                {/* Market Analysis */}
                <div className="market-analysis">
                  <h4>📊 Market Analysis</h4>
                  <div className="analysis-grid">
                    <div className="analysis-item">
                      <span className="label">Price per sq ft:</span>
                      <span className="value">${selectedProperty.market_analysis.price_per_sqft.toFixed(2)}</span>
                    </div>
                    <div className="analysis-item">
                      <span className="label">Market Trend:</span>
                      <span className="value">{selectedProperty.market_analysis.market_trend}</span>
                    </div>
                    <div className="analysis-item">
                      <span className="label">Days on Market:</span>
                      <span className="value">{selectedProperty.market_analysis.days_on_market}</span>
                    </div>
                    <div className="analysis-item">
                      <span className="label">Investment Potential:</span>
                      <span className="value">{selectedProperty.market_analysis.investment_potential}</span>
                    </div>
                  </div>
                </div>

                {/* Neighborhood Info */}
                <div className="neighborhood-info">
                  <h4>🏘️ Neighborhood: {selectedProperty.neighborhood_info.name}</h4>
                  <div className="neighborhood-grid">
                    <div className="neighborhood-item">
                      <span className="label">Average Price:</span>
                      <span className="value">{formatPrice(selectedProperty.neighborhood_info.average_price)}</span>
                    </div>
                    <div className="neighborhood-item">
                      <span className="label">Walkability Score:</span>
                      <span className="value">{selectedProperty.neighborhood_info.walkability_score}/100</span>
                    </div>
                    <div className="neighborhood-item">
                      <span className="label">Crime Rate:</span>
                      <span className="value">{selectedProperty.neighborhood_info.crime_rate}</span>
                    </div>
                  </div>
                  
                  <div className="neighborhood-amenities">
                    <h5>🏫 Schools</h5>
                    <ul>
                      {selectedProperty.neighborhood_info.schools.map((school, index) => (
                        <li key={index}>{school}</li>
                      ))}
                    </ul>
                    
                    <h5>🏪 Amenities</h5>
                    <ul>
                      {selectedProperty.neighborhood_info.amenities.map((amenity, index) => (
                        <li key={index}>{amenity}</li>
                      ))}
                    </ul>
                  </div>
                </div>

                {/* Similar Properties */}
                {selectedProperty.similar_properties.length > 0 && (
                  <div className="similar-properties">
                    <h4>🏠 Similar Properties</h4>
                    <div className="similar-grid">
                      {selectedProperty.similar_properties.map((property, index) => (
                        <div key={index} className="similar-card">
                          <h5>{property.address}</h5>
                          <div className="similar-price">{formatPrice(property.price)}</div>
                          <div className="similar-details">
                            <span>{property.bedrooms} beds</span>
                            <span>{property.bathrooms} baths</span>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default PropertyManagement;
