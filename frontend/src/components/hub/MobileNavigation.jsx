import React from 'react';
import {
  Box,
  BottomNavigation,
  BottomNavigationAction,
  Paper,
  useTheme,
  useMediaQuery,
} from '@mui/material';
import {
  Dashboard as DashboardIcon,
  Chat as ChatIcon,
  Home as HomeIcon,
  People as PeopleIcon,
  Assignment as AssignmentIcon,
} from '@mui/icons-material';

const MobileNavigation = ({ activeSection, onSectionChange }) => {
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('md'));

  const navigationItems = [
    {
      value: 'hub',
      label: 'Hub',
      icon: DashboardIcon,
      color: 'primary.main',
    },
    {
      value: 'chat',
      label: 'Chat',
      icon: ChatIcon,
      color: 'secondary.main',
    },
    {
      value: 'properties',
      label: 'Properties',
      icon: HomeIcon,
      color: 'success.main',
    },
    {
      value: 'clients',
      label: 'Clients',
      icon: PeopleIcon,
      color: 'info.main',
    },
    {
      value: 'tasks',
      label: 'Tasks',
      icon: AssignmentIcon,
      color: 'warning.main',
    },
  ];

  const handleChange = (event, newValue) => {
    onSectionChange(newValue);
  };

  if (!isMobile) {
    return null; // Only show on mobile
  }

  return (
    <Paper
      sx={{
        position: 'fixed',
        bottom: 0,
        left: 0,
        right: 0,
        zIndex: theme.zIndex.appBar,
        borderTop: `1px solid ${theme.palette.divider}`,
      }}
      elevation={8}
    >
      <BottomNavigation
        value={activeSection}
        onChange={handleChange}
        showLabels
        sx={{
          height: 70,
          '& .MuiBottomNavigationAction-root': {
            minWidth: 'auto',
            padding: '6px 12px 8px',
            '&.Mui-selected': {
              color: 'primary.main',
            },
          },
          '& .MuiBottomNavigationAction-label': {
            fontSize: '0.75rem',
            marginTop: '4px',
          },
        }}
      >
        {navigationItems.map((item) => (
          <BottomNavigationAction
            key={item.value}
            value={item.value}
            label={item.label}
            icon={
              <item.icon
                sx={{
                  fontSize: 24,
                  color: activeSection === item.value ? item.color : 'text.secondary',
                }}
              />
            }
            sx={{
              '&.Mui-selected': {
                '& .MuiBottomNavigationAction-label': {
                  color: item.color,
                  fontWeight: 600,
                },
              },
            }}
          />
        ))}
      </BottomNavigation>
    </Paper>
  );
};

export default MobileNavigation;
