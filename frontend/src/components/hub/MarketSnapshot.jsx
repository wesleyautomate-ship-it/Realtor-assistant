import React, { useState, useEffect } from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  Grid,
  Chip,
  useTheme,
  LinearProgress,
  Stack,
  IconButton,
  Tooltip,
} from '@mui/material';
import {
  TrendingUp as TrendingUpIcon,
  TrendingDown as TrendingDownIcon,
  LocationOn as LocationIcon,
  AttachMoney as MoneyIcon,
  Home as HomeIcon,
  Refresh as RefreshIcon,
  AutoAwesome as AIIcon,
} from '@mui/icons-material';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip as RechartsTooltip, ResponsiveContainer, BarChart, Bar } from 'recharts';

const MarketSnapshot = () => {
  const theme = useTheme();
  const [marketData, setMarketData] = useState(null);
  const [isLoading, setIsLoading] = useState(true);

  // Mock data for development - will be replaced with real API calls
  useEffect(() => {
    const loadMarketData = async () => {
      setIsLoading(true);
      
      // Simulate API call
      setTimeout(() => {
        setMarketData({
          averagePrice: 1250, // AED per sq ft
          priceChange: 5.2, // percentage
          trendingAreas: [
            { name: 'Dubai Marina', price: 1450, change: 8.5, trend: 'up' },
            { name: 'Downtown Dubai', price: 1650, change: 3.2, trend: 'up' },
            { name: 'Palm Jumeirah', price: 2200, change: -1.2, trend: 'down' },
            { name: 'JBR', price: 1350, change: 6.8, trend: 'up' },
          ],
          priceHistory: [
            { month: 'Jan', price: 1200 },
            { month: 'Feb', price: 1220 },
            { month: 'Mar', price: 1180 },
            { month: 'Apr', price: 1250 },
            { month: 'May', price: 1280 },
            { month: 'Jun', price: 1250 },
          ],
          aiSummary: "Dubai's real estate market shows strong growth with a 5.2% increase in average prices. Dubai Marina and JBR are leading with 8.5% and 6.8% growth respectively. The market is showing resilience with consistent demand for waterfront properties.",
          marketInsights: [
            { label: 'Market Activity', value: 87, color: 'success' },
            { label: 'Investment Potential', value: 92, color: 'primary' },
            { label: 'Price Stability', value: 78, color: 'warning' },
          ]
        });
        setIsLoading(false);
      }, 1000);
    };

    loadMarketData();
  }, []);

  const handleRefresh = () => {
    // TODO: Implement refresh functionality
    console.log('Refreshing market data...');
  };

  if (isLoading) {
    return (
      <Card sx={{ borderRadius: 3, boxShadow: 3 }}>
        <CardContent>
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 2 }}>
            <TrendingUpIcon color="primary" />
            <Typography variant="h6" sx={{ fontWeight: 600 }}>
              Market Snapshot
            </Typography>
          </Box>
          <LinearProgress />
        </CardContent>
      </Card>
    );
  }

  return (
    <Card sx={{ borderRadius: 3, boxShadow: 3 }}>
      <CardContent>
        <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', mb: 3 }}>
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
            <TrendingUpIcon color="primary" />
            <Typography variant="h6" sx={{ fontWeight: 600 }}>
              Dubai Market Snapshot
            </Typography>
          </Box>
          <Tooltip title="Refresh Data">
            <IconButton onClick={handleRefresh} size="small">
              <RefreshIcon />
            </IconButton>
          </Tooltip>
        </Box>

        {/* Key Metrics */}
        <Grid container spacing={3} sx={{ mb: 3 }}>
          <Grid item xs={12} md={4}>
            <Box sx={{ textAlign: 'center', p: 2, borderRadius: 2, backgroundColor: 'primary.light' }}>
              <MoneyIcon sx={{ fontSize: 32, color: 'primary.main', mb: 1 }} />
              <Typography variant="h4" sx={{ fontWeight: 700, color: 'primary.main' }}>
                AED {marketData.averagePrice}
              </Typography>
              <Typography variant="body2" color="text.secondary">
                Average Price/sq ft
              </Typography>
              <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: 0.5, mt: 1 }}>
                {marketData.priceChange > 0 ? (
                  <TrendingUpIcon sx={{ color: 'success.main', fontSize: 16 }} />
                ) : (
                  <TrendingDownIcon sx={{ color: 'error.main', fontSize: 16 }} />
                )}
                <Typography 
                  variant="body2" 
                  sx={{ 
                    color: marketData.priceChange > 0 ? 'success.main' : 'error.main',
                    fontWeight: 600 
                  }}
                >
                  {marketData.priceChange > 0 ? '+' : ''}{marketData.priceChange}%
                </Typography>
              </Box>
            </Box>
          </Grid>

          <Grid item xs={12} md={8}>
            <Box sx={{ height: 200 }}>
              <ResponsiveContainer width="100%" height="100%">
                <LineChart data={marketData.priceHistory}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="month" />
                  <YAxis />
                  <RechartsTooltip 
                    formatter={(value) => [`AED ${value}`, 'Price/sq ft']}
                    labelStyle={{ color: theme.palette.text.primary }}
                  />
                  <Line 
                    type="monotone" 
                    dataKey="price" 
                    stroke={theme.palette.primary.main} 
                    strokeWidth={3}
                    dot={{ fill: theme.palette.primary.main, strokeWidth: 2, r: 4 }}
                  />
                </LineChart>
              </ResponsiveContainer>
            </Box>
          </Grid>
        </Grid>

        {/* Trending Areas */}
        <Box sx={{ mb: 3 }}>
          <Typography variant="subtitle1" sx={{ fontWeight: 600, mb: 2, display: 'flex', alignItems: 'center', gap: 1 }}>
            <LocationIcon color="primary" />
            Trending Areas
          </Typography>
          <Grid container spacing={2}>
            {marketData.trendingAreas.map((area, index) => (
              <Grid item xs={12} sm={6} key={index}>
                <Box
                  sx={{
                    p: 2,
                    borderRadius: 2,
                    border: '1px solid',
                    borderColor: 'divider',
                    '&:hover': {
                      borderColor: 'primary.main',
                      backgroundColor: 'action.hover',
                    },
                  }}
                >
                  <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', mb: 1 }}>
                    <Typography variant="subtitle2" sx={{ fontWeight: 600 }}>
                      {area.name}
                    </Typography>
                    <Chip
                      icon={area.trend === 'up' ? <TrendingUpIcon /> : <TrendingDownIcon />}
                      label={`${area.change > 0 ? '+' : ''}${area.change}%`}
                      size="small"
                      color={area.trend === 'up' ? 'success' : 'error'}
                    />
                  </Box>
                  <Typography variant="h6" sx={{ fontWeight: 600, color: 'primary.main' }}>
                    AED {area.price}/sq ft
                  </Typography>
                </Box>
              </Grid>
            ))}
          </Grid>
        </Box>

        {/* Market Insights */}
        <Box sx={{ mb: 3 }}>
          <Typography variant="subtitle1" sx={{ fontWeight: 600, mb: 2 }}>
            Market Insights
          </Typography>
          <Grid container spacing={2}>
            {marketData.marketInsights.map((insight, index) => (
              <Grid item xs={12} sm={4} key={index}>
                <Box>
                  <Typography variant="body2" color="text.secondary" sx={{ mb: 1 }}>
                    {insight.label}
                  </Typography>
                  <LinearProgress
                    variant="determinate"
                    value={insight.value}
                    color={insight.color}
                    sx={{ height: 8, borderRadius: 4 }}
                  />
                  <Typography variant="body2" sx={{ mt: 0.5, fontWeight: 600 }}>
                    {insight.value}%
                  </Typography>
                </Box>
              </Grid>
            ))}
          </Grid>
        </Box>

        {/* AI Summary */}
        <Box
          sx={{
            p: 2,
            borderRadius: 2,
            backgroundColor: 'primary.light',
            border: '1px solid',
            borderColor: 'primary.main',
          }}
        >
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 1 }}>
            <AIIcon sx={{ color: 'primary.main' }} />
            <Typography variant="subtitle2" sx={{ fontWeight: 600, color: 'primary.main' }}>
              AI Market Analysis
            </Typography>
          </Box>
          <Typography variant="body2" color="text.secondary">
            {marketData.aiSummary}
          </Typography>
        </Box>
      </CardContent>
    </Card>
  );
};

export default MarketSnapshot;
