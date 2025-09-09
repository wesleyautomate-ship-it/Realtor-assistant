import React, { useState, useEffect, useCallback } from 'react';
import {
  Card,
  CardContent,
  Typography,
  Button,
  Grid,
  Box,
  Chip,
  LinearProgress,
  Alert,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Accordion,
  AccordionSummary,
  AccordionDetails,
  IconButton,
  Tooltip,
  Divider,
  List,
  ListItem,
  ListItemText,
  ListItemIcon,
  Badge
} from '@mui/material';
import {
  Psychology as PsychologyIcon,
  Train as TrainIcon,
  TrendingUp as TrendingUpIcon,
  Assessment as AssessmentIcon,
  Refresh as RefreshIcon,
  PlayArrow as PlayArrowIcon,
  Stop as StopIcon,
  Settings as SettingsIcon,
  ExpandMore as ExpandMoreIcon,
  CheckCircle as CheckCircleIcon,
  Warning as WarningIcon,
  Error as ErrorIcon,
  Info as InfoIcon,
  Timeline as TimelineIcon,
  ShowChart as ShowChartIcon,
  DataUsage as DataUsageIcon,
  Speed as SpeedIcon,
  Memory as MemoryIcon
} from '@mui/icons-material';
import { useAppContext } from '../../context/AppContext';
import { api } from '../../utils/apiClient';

const AdvancedMLPanel = () => {
  const { currentUser: user } = useAppContext();
  const [models, setModels] = useState({});
  const [modelStatus, setModelStatus] = useState({});
  const [performance, setPerformance] = useState({});
  const [insights, setInsights] = useState({});
  const [loading, setLoading] = useState(false);
  const [trainingStatus, setTrainingStatus] = useState({});
  const [predictionDialog, setPredictionDialog] = useState(false);
  const [propertyFeatures, setPropertyFeatures] = useState({
    property_size: 150,
    bedrooms: 2,
    bathrooms: 2,
    floor_number: 5,
    age: 5,
    distance_to_metro: 1.0,
    distance_to_mall: 2.0,
    distance_to_school: 1.5,
    parking_spaces: 1,
    balcony: true,
    garden: false,
    pool: false,
    gym: false,
    security: true,
    maintenance_fee: 500,
    service_charges: 200,
    market_demand_score: 0.7,
    economic_indicator: 1.0,
    seasonality_factor: 1.0
  });
  const [selectedModel, setSelectedModel] = useState('ensemble');
  const [predictionResult, setPredictionResult] = useState(null);

  // Load initial data
  useEffect(() => {
    loadModelsData();
  }, []);

  const loadModelsData = useCallback(async () => {
    try {
      setLoading(true);
      
      // Load models status
      const statusResponse = await api.get('/ml/advanced/models/status');
      setModelStatus(statusResponse.data);
      
      // Load performance metrics
      const performanceResponse = await api.get('/ml/advanced/models/performance');
      setPerformance(performanceResponse.data);
      
      // Load insights
      const insightsResponse = await api.get('/ml/advanced/models/insights');
      setInsights(insightsResponse.data);
      
    } catch (error) {
      console.error('Error loading ML models data:', error);
      console.error('Failed to load ML models data');
    } finally {
      setLoading(false);
    }
  }, []);

  const handleTrainModel = async (modelName) => {
    try {
      setTrainingStatus(prev => ({ ...prev, [modelName]: 'training' }));
      
      const response = await api.post(`/ml/advanced/models/train/${modelName}`);
      
      if (response.data.status === 'success') {
        console.success(`Training started for ${modelName} model`);
        setTrainingStatus(prev => ({ ...prev, [modelName]: 'started' }));
        
        // Poll for completion
        pollTrainingStatus(modelName);
      }
    } catch (error) {
      console.error(`Error training ${modelName}:`, error);
      console.error(`Failed to start training for ${modelName}`);
      setTrainingStatus(prev => ({ ...prev, [modelName]: 'error' }));
    }
  };

  const handleTrainAllModels = async () => {
    try {
      setLoading(true);
      
      const response = await api.post('/ml/advanced/models/train-all');
      
      if (response.data.status === 'success') {
        console.success(`Training started for ${response.data.models.length} models`);
        
        // Update status for all models
        const newStatus = {};
        response.data.models.forEach(modelName => {
          newStatus[modelName] = 'started';
        });
        setTrainingStatus(newStatus);
        
        // Poll for completion
        response.data.models.forEach(modelName => {
          pollTrainingStatus(modelName);
        });
      }
    } catch (error) {
      console.error('Error training all models:', error);
      console.error('Failed to start training for all models');
    } finally {
      setLoading(false);
    }
  };

  const pollTrainingStatus = async (modelName) => {
    const maxAttempts = 30; // 5 minutes max
    let attempts = 0;
    
    const poll = async () => {
      try {
        const response = await api.get('/ml/advanced/models/performance', {
          params: { model_name: modelName }
        });
        
        const modelPerformance = response.data.performance;
        
        if (modelPerformance && modelPerformance.performance && modelPerformance.performance.r2) {
          // Training completed
          setTrainingStatus(prev => ({ ...prev, [modelName]: 'completed' }));
          console.success(`${modelName} model training completed!`);
          
          // Refresh data
          setTimeout(() => {
            loadModelsData();
          }, 1000);
          
          return;
        }
        
        attempts++;
        if (attempts < maxAttempts) {
          setTimeout(poll, 10000); // Poll every 10 seconds
        } else {
          setTrainingStatus(prev => ({ ...prev, [modelName]: 'timeout' }));
          console.warning(`${modelName} model training timed out`);
        }
        
      } catch (error) {
        console.error(`Error polling ${modelName} status:`, error);
        attempts++;
        if (attempts < maxAttempts) {
          setTimeout(poll, 10000);
        } else {
          setTrainingStatus(prev => ({ ...prev, [modelName]: 'error' }));
        }
      }
    };
    
    poll();
  };

  const handleOptimizeModel = async (modelName) => {
    try {
      setTrainingStatus(prev => ({ ...prev, [modelName]: 'optimizing' }));
      
      const response = await api.post(`/ml/advanced/models/optimize/${modelName}`);
      
      if (response.data.status === 'success') {
        console.success(`Hyperparameter optimization started for ${modelName}`);
        setTrainingStatus(prev => ({ ...prev, [modelName]: 'optimizing' }));
        
        // Poll for completion
        pollTrainingStatus(modelName);
      }
    } catch (error) {
      console.error(`Error optimizing ${modelName}:`, error);
      console.error(`Failed to start optimization for ${modelName}`);
      setTrainingStatus(prev => ({ ...prev, [modelName]: 'error' }));
    }
  };

  const handleGenerateTrainingData = async () => {
    try {
      setLoading(true);
      
      const response = await api.post('/ml/advanced/models/generate-training-data', {
        num_samples: 10000
      });
      
      if (response.data.status === 'success') {
        console.success(`Generated ${response.data.samples_count} training samples`);
        loadModelsData(); // Refresh data
      }
    } catch (error) {
      console.error('Error generating training data:', error);
      console.error('Failed to generate training data');
    } finally {
      setLoading(false);
    }
  };

  const handleMakePrediction = async () => {
    try {
      setLoading(true);
      
      const response = await api.post('/ml/advanced/predict/property-price', {
        property_features: propertyFeatures,
        model_name: selectedModel
      });
      
      if (response.data.status === 'success') {
        setPredictionResult(response.data.prediction);
        console.success('Property price prediction completed!');
      }
    } catch (error) {
      console.error('Error making prediction:', error);
      console.error('Failed to make property price prediction');
    } finally {
      setLoading(false);
    }
  };

  const getStatusIcon = (status) => {
    switch (status) {
      case 'trained':
        return <CheckCircleIcon color="success" />;
      case 'untrained':
        return <WarningIcon color="warning" />;
      case 'training':
        return <PlayArrowIcon color="primary" />;
      case 'optimizing':
        return <SettingsIcon color="primary" />;
      case 'error':
        return <ErrorIcon color="error" />;
      default:
        return <InfoIcon color="info" />;
    }
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'trained':
        return 'success';
      case 'untrained':
        return 'warning';
      case 'training':
      case 'optimizing':
        return 'primary';
      case 'error':
        return 'error';
      default:
        return 'default';
    }
  };

  const getTrainingStatusText = (modelName) => {
    const status = trainingStatus[modelName];
    switch (status) {
      case 'training':
        return 'Training...';
      case 'started':
        return 'Started';
      case 'completed':
        return 'Completed';
      case 'optimizing':
        return 'Optimizing...';
      case 'error':
        return 'Error';
      case 'timeout':
        return 'Timeout';
      default:
        return '';
    }
  };

  const renderModelCard = (modelName, modelInfo) => {
    const status = modelStatus.models?.[modelName]?.status || 'unknown';
    const trainingStatusText = getTrainingStatusText(modelName);
    const isTraining = trainingStatus[modelName] === 'training' || trainingStatus[modelName] === 'optimizing';
    
    return (
      <Card key={modelName} sx={{ mb: 2 }}>
        <CardContent>
          <Box display="flex" alignItems="center" justifyContent="space-between" mb={2}>
            <Box display="flex" alignItems="center" gap={1}>
              <PsychologyIcon color="primary" />
              <Typography variant="h6" component="div">
                {modelName.replace('_', ' ').toUpperCase()}
              </Typography>
            </Box>
            <Chip
              icon={getStatusIcon(status)}
              label={status}
              color={getStatusColor(status)}
              size="small"
            />
          </Box>
          
          {trainingStatusText && (
            <Box mb={2}>
              <Typography variant="body2" color="text.secondary" gutterBottom>
                {trainingStatusText}
              </Typography>
              {isTraining && <LinearProgress />}
            </Box>
          )}
          
          <Grid container spacing={2} mb={2}>
            <Grid item xs={6}>
              <Typography variant="body2" color="text.secondary">
                Training Samples
              </Typography>
              <Typography variant="body1">
                {modelInfo.training_samples || 0}
              </Typography>
            </Grid>
            <Grid item xs={6}>
              <Typography variant="body2" color="text.secondary">
                Last Updated
              </Typography>
              <Typography variant="body1">
                {modelInfo.last_updated ? 
                  new Date(modelInfo.last_updated * 1000).toLocaleDateString() : 
                  'Never'
                }
              </Typography>
            </Grid>
          </Grid>
          
          <Box display="flex" gap={1} flexWrap="wrap">
            <Button
              variant="contained"
              size="small"
              startIcon={<TrainIcon />}
              onClick={() => handleTrainModel(modelName)}
              disabled={isTraining}
            >
              Train
            </Button>
            <Button
              variant="outlined"
              size="small"
              startIcon={<SettingsIcon />}
              onClick={() => handleOptimizeModel(modelName)}
              disabled={isTraining || status === 'untrained'}
            >
              Optimize
            </Button>
          </Box>
        </CardContent>
      </Card>
    );
  };

  const renderPerformanceMetrics = () => {
    if (!performance.performance?.models) return null;
    
    return (
      <Accordion>
        <AccordionSummary expandIcon={<ExpandMoreIcon />}>
          <Box display="flex" alignItems="center" gap={1}>
            <AssessmentIcon />
            <Typography variant="h6">Performance Metrics</Typography>
          </Box>
        </AccordionSummary>
        <AccordionDetails>
          <Grid container spacing={2}>
            {Object.entries(performance.performance.models).map(([modelName, modelPerf]) => (
              <Grid item xs={12} md={6} key={modelName}>
                <Card variant="outlined">
                  <CardContent>
                    <Typography variant="h6" gutterBottom>
                      {modelName.replace('_', ' ').toUpperCase()}
                    </Typography>
                    {modelPerf.metrics ? (
                      <Box>
                        <Typography variant="body2">
                          R² Score: <strong>{modelPerf.metrics.r2?.toFixed(4) || 'N/A'}</strong>
                        </Typography>
                        <Typography variant="body2">
                          RMSE: <strong>{modelPerf.metrics.rmse?.toFixed(2) || 'N/A'}</strong>
                        </Typography>
                        <Typography variant="body2">
                          CV R²: <strong>{modelPerf.metrics.cv_r2_mean?.toFixed(4) || 'N/A'}</strong>
                        </Typography>
                      </Box>
                    ) : (
                      <Typography variant="body2" color="text.secondary">
                        No performance data available
                      </Typography>
                    )}
                  </CardContent>
                </Card>
              </Grid>
            ))}
          </Grid>
        </AccordionDetails>
      </Accordion>
    );
  };

  const renderPredictionDialog = () => (
    <Dialog open={predictionDialog} onClose={() => setPredictionDialog(false)} maxWidth="md" fullWidth>
      <DialogTitle>
        <Box display="flex" alignItems="center" gap={1}>
          <TrendingUpIcon />
          Property Price Prediction
        </Box>
      </DialogTitle>
      <DialogContent>
        <Grid container spacing={2} sx={{ mt: 1 }}>
          <Grid item xs={12} md={6}>
            <FormControl fullWidth>
              <InputLabel>ML Model</InputLabel>
              <Select
                value={selectedModel}
                onChange={(e) => setSelectedModel(e.target.value)}
                label="ML Model"
              >
                <MenuItem value="ensemble">Ensemble (All Models)</MenuItem>
                <MenuItem value="random_forest">Random Forest</MenuItem>
                <MenuItem value="xgboost">XGBoost</MenuItem>
                <MenuItem value="lightgbm">LightGBM</MenuItem>
                <MenuItem value="catboost">CatBoost</MenuItem>
              </Select>
            </FormControl>
          </Grid>
          
          <Grid item xs={12} md={6}>
            <TextField
              fullWidth
              label="Property Size (sqm)"
              type="number"
              value={propertyFeatures.property_size}
              onChange={(e) => setPropertyFeatures(prev => ({ ...prev, property_size: parseFloat(e.target.value) }))}
            />
          </Grid>
          
          <Grid item xs={12} md={6}>
            <TextField
              fullWidth
              label="Bedrooms"
              type="number"
              value={propertyFeatures.bedrooms}
              onChange={(e) => setPropertyFeatures(prev => ({ ...prev, bedrooms: parseInt(e.target.value) }))}
            />
          </Grid>
          
          <Grid item xs={12} md={6}>
            <TextField
              fullWidth
              label="Bathrooms"
              type="number"
              value={propertyFeatures.bathrooms}
              onChange={(e) => setPropertyFeatures(prev => ({ ...prev, bathrooms: parseInt(e.target.value) }))}
            />
          </Grid>
          
          <Grid item xs={12} md={6}>
            <TextField
              fullWidth
              label="Floor Number"
              type="number"
              value={propertyFeatures.floor_number}
              onChange={(e) => setPropertyFeatures(prev => ({ ...prev, floor_number: parseInt(e.target.value) }))}
            />
          </Grid>
          
          <Grid item xs={12} md={6}>
            <TextField
              fullWidth
              label="Age (years)"
              type="number"
              value={propertyFeatures.age}
              onChange={(e) => setPropertyFeatures(prev => ({ ...prev, age: parseInt(e.target.value) }))}
            />
          </Grid>
          
          <Grid item xs={12} md={6}>
            <TextField
              fullWidth
              label="Distance to Metro (km)"
              type="number"
              step="0.1"
              value={propertyFeatures.distance_to_metro}
              onChange={(e) => setPropertyFeatures(prev => ({ ...prev, distance_to_metro: parseFloat(e.target.value) }))}
            />
          </Grid>
          
          <Grid item xs={12} md={6}>
            <TextField
              fullWidth
              label="Distance to Mall (km)"
              type="number"
              step="0.1"
              value={propertyFeatures.distance_to_mall}
              onChange={(e) => setPropertyFeatures(prev => ({ ...prev, distance_to_mall: parseFloat(e.target.value) }))}
            />
          </Grid>
        </Grid>
        
        {predictionResult && (
          <Box mt={3} p={2} bgcolor="grey.50" borderRadius={1}>
            <Typography variant="h6" gutterBottom>
              Prediction Result
            </Typography>
            <Typography variant="h4" color="primary" gutterBottom>
              AED {predictionResult.predicted_price_per_sqm?.toFixed(2)} / sqm
            </Typography>
            <Typography variant="body2" color="text.secondary" gutterBottom>
              Confidence: {(predictionResult.confidence_score * 100).toFixed(1)}%
            </Typography>
            <Typography variant="body2" color="text.secondary">
              Model: {predictionResult.model_used}
            </Typography>
            {predictionResult.explanation && (
              <Typography variant="body2" sx={{ mt: 1 }}>
                {predictionResult.explanation}
              </Typography>
            )}
          </Box>
        )}
      </DialogContent>
      <DialogActions>
        <Button onClick={() => setPredictionDialog(false)}>Close</Button>
        <Button 
          onClick={handleMakePrediction} 
          variant="contained" 
          disabled={loading}
        >
          {loading ? 'Predicting...' : 'Make Prediction'}
        </Button>
      </DialogActions>
    </Dialog>
  );

  return (
    <Box>
      <Card sx={{ mb: 3 }}>
        <CardContent>
          <Box display="flex" alignItems="center" justifyContent="space-between" mb={2}>
            <Box display="flex" alignItems="center" gap={1}>
              <PsychologyIcon color="primary" />
              <Typography variant="h5" component="h2">
                Advanced ML Models
              </Typography>
            </Box>
            <Box display="flex" gap={1}>
              <Button
                variant="contained"
                startIcon={<TrendingUpIcon />}
                onClick={() => setPredictionDialog(true)}
              >
                Make Prediction
              </Button>
              <Button
                variant="outlined"
                startIcon={<RefreshIcon />}
                onClick={loadModelsData}
                disabled={loading}
              >
                Refresh
              </Button>
            </Box>
          </Box>
          
          <Typography variant="body1" color="text.secondary" paragraph>
            Train, optimize, and manage machine learning models for property price predictions and market insights.
          </Typography>
          
          <Box display="flex" gap={2} flexWrap="wrap" mb={3}>
            <Button
              variant="contained"
              startIcon={<TrainIcon />}
              onClick={handleTrainAllModels}
              disabled={loading}
            >
              Train All Models
            </Button>
            <Button
              variant="outlined"
              startIcon={<DataUsageIcon />}
              onClick={handleGenerateTrainingData}
              disabled={loading}
            >
              Generate Training Data
            </Button>
          </Box>
        </CardContent>
      </Card>

      {/* Models Overview */}
      <Card sx={{ mb: 3 }}>
        <CardContent>
          <Typography variant="h6" gutterBottom>
            Models Overview
          </Typography>
          <Grid container spacing={2}>
            <Grid item xs={12} md={3}>
              <Box textAlign="center" p={2}>
                <Typography variant="h4" color="primary">
                  {modelStatus.total_models || 0}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Total Models
                </Typography>
              </Box>
            </Grid>
            <Grid item xs={12} md={3}>
              <Box textAlign="center" p={2}>
                <Typography variant="h4" color="success.main">
                  {modelStatus.models ? 
                    Object.values(modelStatus.models).filter(m => m.status === 'trained').length : 0
                  }
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Trained Models
                </Typography>
              </Box>
            </Grid>
            <Grid item xs={12} md={3}>
              <Box textAlign="center" p={2}>
                <Typography variant="h4" color="warning.main">
                  {modelStatus.models ? 
                    Object.values(modelStatus.models).filter(m => m.status === 'untrained').length : 0
                  }
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Untrained Models
                </Typography>
              </Box>
            </Grid>
            <Grid item xs={12} md={3}>
              <Box textAlign="center" p={2}>
                <Typography variant="h4" color="info.main">
                  {Object.values(trainingStatus).filter(s => s === 'training' || s === 'optimizing').length}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Active Tasks
                </Typography>
              </Box>
            </Grid>
          </Grid>
        </CardContent>
      </Card>

      {/* Individual Models */}
      <Card sx={{ mb: 3 }}>
        <CardContent>
          <Typography variant="h6" gutterBottom>
            Individual Models
          </Typography>
          {modelStatus.models ? (
            Object.entries(modelStatus.models).map(([modelName, modelInfo]) => 
              renderModelCard(modelName, modelInfo)
            )
          ) : (
            <Typography color="text.secondary">No models available</Typography>
          )}
        </CardContent>
      </Card>

      {/* Performance Metrics */}
      {renderPerformanceMetrics()}

      {/* Insights */}
      {insights.insights && (
        <Card sx={{ mb: 3 }}>
          <CardContent>
            <Typography variant="h6" gutterBottom>
              Model Insights & Recommendations
            </Typography>
            {insights.insights.recommendations?.map((rec, index) => (
              <Alert key={index} severity="info" sx={{ mb: 1 }}>
                {rec}
              </Alert>
            ))}
          </CardContent>
        </Card>
      )}

      {/* Prediction Dialog */}
      {renderPredictionDialog()}
    </Box>
  );
};

export default AdvancedMLPanel;
