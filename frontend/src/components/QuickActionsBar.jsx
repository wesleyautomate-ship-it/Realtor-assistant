import React from 'react';
import {
  Box,
  Button,
  Stack,
  useTheme,
  useMediaQuery,
  Typography,
  Fade
} from '@mui/material';
import {
  Assessment as CMAAIcon,
  Description as ReportIcon,
  Share as SocialIcon,
  Event as ScheduleIcon,
  Add as AddIcon
} from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';

const QuickActionsBar = () => {
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('md'));
  const navigate = useNavigate();

  const quickActions = [
    {
      id: 'cma',
      label: 'Create CMA',
      icon: CMAAIcon,
      color: '#4CAF50',
      action: () => navigate('/compose?team=analytics&template=cma')
    },
    {
      id: 'report',
      label: 'Generate Report',
      icon: ReportIcon,
      color: '#2196F3',
      action: () => navigate('/compose?team=analytics&template=market_report')
    },
    {
      id: 'social',
      label: 'Social Post',
      icon: SocialIcon,
      color: '#FF9800',
      action: () => navigate('/compose?team=social&template=instagram')
    },
    {
      id: 'schedule',
      label: 'Schedule Viewing',
      icon: ScheduleIcon,
      color: '#9C27B0',
      action: () => navigate('/compose?team=transactions&template=contract')
    }
  ];

  return (
    <Fade in timeout={600}>
      <Box sx={{ mb: 4 }}>
        <Typography 
          variant="h6" 
          sx={{ 
            fontWeight: 600, 
            mb: 2, 
            color: 'text.primary',
            textAlign: isMobile ? 'center' : 'left'
          }}
        >
          Quick Actions
        </Typography>
        
        <Stack 
          direction={isMobile ? 'column' : 'row'} 
          spacing={2}
          sx={{ 
            justifyContent: isMobile ? 'center' : 'flex-start',
            alignItems: 'center'
          }}
        >
          {quickActions.map((action, index) => {
            const IconComponent = action.icon;
            return (
              <Button
                key={action.id}
                variant="outlined"
                startIcon={<IconComponent />}
                onClick={action.action}
                sx={{
                  borderColor: action.color,
                  color: action.color,
                  fontWeight: 600,
                  px: 3,
                  py: 1.5,
                  borderRadius: 2,
                  transition: 'all 0.3s ease-in-out',
                  '&:hover': {
                    backgroundColor: action.color,
                    color: 'white',
                    transform: 'translateY(-2px)',
                    boxShadow: theme.shadows[4],
                    borderColor: action.color,
                  },
                  minWidth: isMobile ? '100%' : 'auto'
                }}
              >
                {action.label}
              </Button>
            );
          })}
          
          {/* Create New Button */}
          <Button
            variant="contained"
            startIcon={<AddIcon />}
            onClick={() => navigate('/compose')}
            sx={{
              backgroundColor: theme.palette.primary.main,
              color: 'white',
              fontWeight: 600,
              px: 3,
              py: 1.5,
              borderRadius: 2,
              transition: 'all 0.3s ease-in-out',
              '&:hover': {
                backgroundColor: theme.palette.primary.dark,
                transform: 'translateY(-2px)',
                boxShadow: theme.shadows[6],
              },
              minWidth: isMobile ? '100%' : 'auto'
            }}
          >
            Create New
          </Button>
        </Stack>
      </Box>
    </Fade>
  );
};

export default QuickActionsBar;
