import React, { useState, useEffect } from 'react';
import {
  Paper,
  Box,
  Typography,
  List,
  ListItem,
  ListItemText,
  ListItemAvatar,
  Chip,
  Avatar,
  Divider,
  Skeleton,
  IconButton,
  Collapse,
  Alert,
  Button,
  CircularProgress
} from '@mui/material';
import {
  Close as CloseIcon,
  ExpandMore as ExpandMoreIcon,
  ExpandLess as ExpandLessIcon,
  Home as PropertyIcon,
  Person as ClientIcon,
  LocationOn as LocationIcon,
  Business as CompanyIcon,
  Assessment as ReportIcon,
  Refresh as RefreshIcon,
  Info as InfoIcon,
  Warning as WarningIcon
} from '@mui/icons-material';
import PropertyCard from './PropertyCard';
import ContentPreviewCard from './ContentPreviewCard';

const ContextualSidePanel = ({ 
  entities = [], 
  conversationId, 
  onEntityClick, 
  isVisible = true,
  onClose,
  onRefresh 
}) => {
  const [contextData, setContextData] = useState({});
  const [loadingStates, setLoadingStates] = useState({});
  const [errorStates, setErrorStates] = useState({});
  const [expandedSections, setExpandedSections] = useState({});
  const [overallLoading, setOverallLoading] = useState(false);

  // Group entities by type
  const groupedEntities = entities.reduce((acc, entity) => {
    if (!acc[entity.type]) {
      acc[entity.type] = [];
    }
    acc[entity.type].push(entity);
    return acc;
  }, {});

  const getEntityIcon = (entityType) => {
    switch (entityType?.toLowerCase()) {
      case 'property':
        return <PropertyIcon />;
      case 'client':
      case 'lead':
        return <ClientIcon />;
      case 'location':
      case 'neighborhood':
        return <LocationIcon />;
      case 'company':
        return <CompanyIcon />;
      case 'report':
      case 'document':
        return <ReportIcon />;
      default:
        return <InfoIcon />;
    }
  };

  const getEntityColor = (entityType) => {
    switch (entityType?.toLowerCase()) {
      case 'property':
        return 'primary';
      case 'client':
      case 'lead':
        return 'secondary';
      case 'location':
      case 'neighborhood':
        return 'success';
      case 'company':
        return 'info';
      case 'report':
      case 'document':
        return 'warning';
      default:
        return 'default';
    }
  };

  const formatEntityName = (entity) => {
    if (entity.name) return entity.name;
    if (entity.address) return entity.address;
    if (entity.title) return entity.title;
    return entity.id || 'Unknown';
  };

  const handleSectionToggle = (sectionType) => {
    setExpandedSections(prev => ({
      ...prev,
      [sectionType]: !prev[sectionType]
    }));
  };

  const handleEntityClick = (entity) => {
    if (onEntityClick) {
      onEntityClick(entity);
    }
  };

  const handleRefresh = () => {
    if (onRefresh) {
      onRefresh();
    }
  };

  const renderEntityItem = (entity, index) => {
    const isLoading = loadingStates[entity.id];
    const hasError = errorStates[entity.id];
    const context = contextData[entity.id];

    return (
      <ListItem 
        key={`${entity.id}-${index}`}
        sx={{ 
          flexDirection: 'column', 
          alignItems: 'stretch',
          p: 0,
          mb: 1
        }}
      >
        <Box sx={{ 
          display: 'flex', 
          alignItems: 'center', 
          p: 1,
          cursor: 'pointer',
          '&:hover': { bgcolor: 'action.hover' },
          borderRadius: 1
        }}
        onClick={() => handleEntityClick(entity)}
        >
          <ListItemAvatar>
            <Avatar sx={{ bgcolor: `${getEntityColor(entity.type)}.main` }}>
              {getEntityIcon(entity.type)}
            </Avatar>
          </ListItemAvatar>
          
          <ListItemText
            primary={
              <Typography variant="subtitle2" sx={{ fontWeight: 'medium' }}>
                {formatEntityName(entity)}
              </Typography>
            }
            secondary={
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mt: 0.5 }}>
                <Chip 
                  label={entity.type} 
                  size="small" 
                  color={getEntityColor(entity.type)}
                  variant="outlined"
                />
                {entity.confidence && (
                  <Typography variant="caption" color="text.secondary">
                    {Math.round(entity.confidence * 100)}% confidence
                  </Typography>
                )}
              </Box>
            }
          />
          
          {isLoading && <CircularProgress size={20} />}
          {hasError && <WarningIcon color="error" fontSize="small" />}
        </Box>

        {/* Context Data Display */}
        {context && !isLoading && !hasError && (
          <Box sx={{ ml: 4, mb: 1 }}>
            {entity.type === 'property' && context.property && (
              <PropertyCard 
                property={context.property} 
                compact={true}
                onView={() => handleEntityClick(entity)}
              />
            )}
            
            {entity.type === 'document' && context.document && (
              <ContentPreviewCard 
                content={context.document} 
                type="document"
                compact={true}
                onView={() => handleEntityClick(entity)}
              />
            )}
            
            {entity.type === 'client' && context.client && (
              <Paper sx={{ p: 1, bgcolor: 'grey.50' }}>
                <Typography variant="body2" sx={{ fontWeight: 'medium' }}>
                  {context.client.name}
                </Typography>
                <Typography variant="caption" color="text.secondary">
                  {context.client.email} • {context.client.phone}
                </Typography>
                {context.client.budget_min && context.client.budget_max && (
                  <Typography variant="caption" color="text.secondary" sx={{ display: 'block' }}>
                    Budget: ${context.client.budget_min.toLocaleString()} - ${context.client.budget_max.toLocaleString()}
                  </Typography>
                )}
              </Paper>
            )}
            
            {entity.type === 'location' && context.location && (
              <Paper sx={{ p: 1, bgcolor: 'grey.50' }}>
                <Typography variant="body2" sx={{ fontWeight: 'medium' }}>
                  {context.location.name}
                </Typography>
                <Typography variant="caption" color="text.secondary">
                  {context.location.properties_count} properties • ${context.location.avg_price?.toLocaleString()} avg price
                </Typography>
              </Paper>
            )}
          </Box>
        )}

        {hasError && (
          <Alert severity="error" sx={{ ml: 4, mb: 1 }}>
            Failed to load context data
          </Alert>
        )}
      </ListItem>
    );
  };

  const renderSection = (entityType, entities) => {
    const isExpanded = expandedSections[entityType];
    const entityCount = entities.length;

    return (
      <Box key={entityType} sx={{ mb: 2 }}>
        <Box 
          sx={{ 
            display: 'flex', 
            alignItems: 'center', 
            justifyContent: 'space-between',
            p: 1,
            cursor: 'pointer',
            '&:hover': { bgcolor: 'action.hover' },
            borderRadius: 1
          }}
          onClick={() => handleSectionToggle(entityType)}
        >
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
            <Avatar sx={{ bgcolor: `${getEntityColor(entityType)}.main`, width: 24, height: 24 }}>
              {getEntityIcon(entityType)}
            </Avatar>
            <Typography variant="subtitle1" sx={{ fontWeight: 'medium', textTransform: 'capitalize' }}>
              {entityType}s
            </Typography>
            <Chip label={entityCount} size="small" color={getEntityColor(entityType)} />
          </Box>
          {isExpanded ? <ExpandLessIcon /> : <ExpandMoreIcon />}
        </Box>

        <Collapse in={isExpanded}>
          <List sx={{ pl: 2 }}>
            {entities.map((entity, index) => renderEntityItem(entity, index))}
          </List>
        </Collapse>
      </Box>
    );
  };

  if (!isVisible) {
    return null;
  }

  return (
    <Paper 
      sx={{ 
        width: 350, 
        height: '100%', 
        display: 'flex', 
        flexDirection: 'column',
        borderLeft: 1,
        borderColor: 'divider'
      }}
      elevation={0}
    >
      {/* Header */}
      <Box sx={{ 
        p: 2, 
        borderBottom: 1, 
        borderColor: 'divider',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between'
      }}>
        <Typography variant="h6" sx={{ fontWeight: 'bold' }}>
          Context Panel
        </Typography>
        
        <Box sx={{ display: 'flex', gap: 1 }}>
          <IconButton size="small" onClick={handleRefresh} disabled={overallLoading}>
            <RefreshIcon />
          </IconButton>
          {onClose && (
            <IconButton size="small" onClick={onClose}>
              <CloseIcon />
            </IconButton>
          )}
        </Box>
      </Box>

      {/* Content */}
      <Box sx={{ flexGrow: 1, overflow: 'auto', p: 2 }}>
        {overallLoading ? (
          <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
            {[1, 2, 3].map((i) => (
              <Box key={i}>
                <Skeleton variant="rectangular" height={40} sx={{ mb: 1 }} />
                <Skeleton variant="text" width="60%" />
              </Box>
            ))}
          </Box>
        ) : entities.length === 0 ? (
          <Box sx={{ 
            display: 'flex', 
            flexDirection: 'column', 
            alignItems: 'center', 
            justifyContent: 'center',
            height: '100%',
            textAlign: 'center'
          }}>
            <InfoIcon sx={{ fontSize: 48, color: 'text.secondary', mb: 2 }} />
            <Typography variant="body1" color="text.secondary" sx={{ mb: 1 }}>
              No entities detected
            </Typography>
            <Typography variant="body2" color="text.secondary">
              Entities will appear here as the AI detects them in the conversation
            </Typography>
          </Box>
        ) : (
          <Box>
            {Object.entries(groupedEntities).map(([entityType, typeEntities]) => 
              renderSection(entityType, typeEntities)
            )}
          </Box>
        )}
      </Box>

      {/* Footer */}
      {entities.length > 0 && (
        <Box sx={{ 
          p: 2, 
          borderTop: 1, 
          borderColor: 'divider',
          bgcolor: 'grey.50'
        }}>
          <Typography variant="caption" color="text.secondary">
            {entities.length} entity{entities.length !== 1 ? 's' : ''} detected in this conversation
          </Typography>
        </Box>
      )}
    </Paper>
  );
};

export default ContextualSidePanel;
