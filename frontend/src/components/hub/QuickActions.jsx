import React from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  Button,
  Grid,
  useTheme,
  Stack,
} from '@mui/material';
import {
  Assessment as CMAAIcon,
  Home as ListingIcon,
  Message as FollowUpIcon,
  Search as SearchIcon,
  TrendingUp as MarketIcon,
  PersonAdd as LeadIcon,
} from '@mui/icons-material';

const QuickActions = ({ onActionClick }) => {
  const theme = useTheme();

  const actions = [
    {
      id: 'cma',
      title: 'Create CMA',
      description: 'Comparative Market Analysis',
      icon: <CMAAIcon />,
      color: 'primary',
    },
    {
      id: 'listing',
      title: 'New Listing',
      description: 'Add property listing',
      icon: <ListingIcon />,
      color: 'secondary',
    },
    {
      id: 'follow_up',
      title: 'Follow Up',
      description: 'Client follow-up template',
      icon: <FollowUpIcon />,
      color: 'success',
    },
    {
      id: 'search',
      title: 'Property Search',
      description: 'Find properties',
      icon: <SearchIcon />,
      color: 'info',
    },
    {
      id: 'market',
      title: 'Market Report',
      description: 'Generate market insights',
      icon: <MarketIcon />,
      color: 'warning',
    },
    {
      id: 'lead',
      title: 'Add Lead',
      description: 'New client lead',
      icon: <LeadIcon />,
      color: 'error',
    },
  ];

  const handleActionClick = (action) => {
    onActionClick?.(action);
  };

  return (
    <Card sx={{ borderRadius: 2, boxShadow: 2 }}>
      <CardContent>
        <Typography variant="h6" sx={{ fontWeight: 600, mb: 2 }}>
          Quick Actions
        </Typography>
        
        <Grid container spacing={2}>
          {actions.map((action) => (
            <Grid item xs={12} sm={6} md={4} key={action.id}>
              <Button
                fullWidth
                variant="outlined"
                startIcon={action.icon}
                onClick={() => handleActionClick(action)}
                sx={{
                  height: 80,
                  flexDirection: 'column',
                  alignItems: 'flex-start',
                  justifyContent: 'flex-start',
                  p: 2,
                  textAlign: 'left',
                  borderRadius: 2,
                  borderColor: `${action.color}.main`,
                  color: `${action.color}.main`,
                  '&:hover': {
                    backgroundColor: `${action.color}.light`,
                    borderColor: `${action.color}.dark`,
                    color: `${action.color}.dark`,
                  },
                }}
              >
                <Stack spacing={0.5} sx={{ width: '100%' }}>
                  <Typography variant="subtitle2" sx={{ fontWeight: 600 }}>
                    {action.title}
                  </Typography>
                  <Typography variant="caption" color="text.secondary">
                    {action.description}
                  </Typography>
                </Stack>
              </Button>
            </Grid>
          ))}
        </Grid>
      </CardContent>
    </Card>
  );
};

export default QuickActions;
