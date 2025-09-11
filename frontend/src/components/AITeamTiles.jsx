import React from 'react';
import {
  Grid,
  Card,
  CardContent,
  Typography,
  Box,
  useTheme,
  useMediaQuery,
  Fade,
  Grow
} from '@mui/material';
import {
  Campaign as MarketingIcon,
  Analytics as AnalyticsIcon,
  Share as SocialIcon,
  Settings as StrategyIcon,
  Inventory as PackagesIcon,
  Handshake as TransactionsIcon
} from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';

const AITeamTiles = () => {
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('md'));
  const navigate = useNavigate();

  const aiTeams = [
    {
      id: 'marketing',
      name: 'Marketing',
      description: 'Reach the Right Audience',
      icon: MarketingIcon,
      color: '#E91E63',
      lightColor: '#FCE4EC',
      route: '/compose?team=marketing'
    },
    {
      id: 'analytics',
      name: 'Data & Analytics',
      description: 'Make Informed Decisions',
      icon: AnalyticsIcon,
      color: '#9C27B0',
      lightColor: '#F3E5F5',
      route: '/compose?team=analytics'
    },
    {
      id: 'social',
      name: 'Social Media',
      description: 'Amplify Your Presence',
      icon: SocialIcon,
      color: '#FF9800',
      lightColor: '#FFF3E0',
      route: '/compose?team=social'
    },
    {
      id: 'strategy',
      name: 'Strategy',
      description: 'Plan for Success',
      icon: StrategyIcon,
      color: '#4CAF50',
      lightColor: '#E8F5E8',
      route: '/compose?team=strategy'
    },
    {
      id: 'packages',
      name: 'Packages',
      description: 'Curated Business Bundles',
      icon: PackagesIcon,
      color: '#2E7D32',
      lightColor: '#E8F5E8',
      route: '/compose?team=packages'
    },
    {
      id: 'transactions',
      name: 'Transactions',
      description: 'Manage Workflow',
      icon: TransactionsIcon,
      color: '#673AB7',
      lightColor: '#EDE7F6',
      route: '/compose?team=transactions'
    }
  ];

  const handleTeamClick = (team) => {
    navigate(team.route);
  };

  return (
    <Box sx={{ mb: 4 }}>
      <Typography 
        variant="h5" 
        sx={{ 
          fontWeight: 600, 
          mb: 3, 
          color: 'text.primary',
          textAlign: isMobile ? 'center' : 'left'
        }}
      >
        Choose Your AI Team
      </Typography>
      
      <Grid container spacing={2}>
        {aiTeams.map((team, index) => {
          const IconComponent = team.icon;
          return (
            <Grid item xs={12} sm={6} md={4} key={team.id}>
              <Grow in timeout={300 + index * 100}>
                <Card
                  sx={{
                    height: '100%',
                    cursor: 'pointer',
                    transition: 'all 0.3s ease-in-out',
                    border: `2px solid transparent`,
                    '&:hover': {
                      transform: 'translateY(-4px)',
                      boxShadow: theme.shadows[8],
                      border: `2px solid ${team.color}`,
                    },
                    '&:active': {
                      transform: 'translateY(-2px)',
                    }
                  }}
                  onClick={() => handleTeamClick(team)}
                >
                  <CardContent sx={{ p: 3, textAlign: 'center' }}>
                    <Box
                      sx={{
                        width: 64,
                        height: 64,
                        borderRadius: '50%',
                        backgroundColor: team.lightColor,
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center',
                        mx: 'auto',
                        mb: 2,
                        transition: 'all 0.3s ease-in-out',
                        '&:hover': {
                          backgroundColor: team.color,
                          '& .MuiSvgIcon-root': {
                            color: 'white',
                          }
                        }
                      }}
                    >
                      <IconComponent
                        sx={{
                          fontSize: 32,
                          color: team.color,
                          transition: 'color 0.3s ease-in-out',
                        }}
                      />
                    </Box>
                    
                    <Typography
                      variant="h6"
                      sx={{
                        fontWeight: 600,
                        mb: 1,
                        color: 'text.primary',
                        fontSize: '1.1rem'
                      }}
                    >
                      {team.name}
                    </Typography>
                    
                    <Typography
                      variant="body2"
                      sx={{
                        color: 'text.secondary',
                        fontSize: '0.875rem',
                        lineHeight: 1.4
                      }}
                    >
                      {team.description}
                    </Typography>
                  </CardContent>
                </Card>
              </Grow>
            </Grid>
          );
        })}
      </Grid>
    </Box>
  );
};

export default AITeamTiles;
