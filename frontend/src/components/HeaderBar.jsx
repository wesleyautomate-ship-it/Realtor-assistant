import React, { useState } from 'react';
import {
  AppBar,
  Toolbar,
  Typography,
  IconButton,
  Avatar,
  Menu,
  MenuItem,
  Box,
  Badge,
  useTheme,
  useMediaQuery,
  Button,
  TextField,
  InputAdornment,
  Chip
} from '@mui/material';
import {
  Notifications as NotificationsIcon,
  Search as SearchIcon,
  AccountCircle as AccountIcon,
  Settings as SettingsIcon,
  Logout as LogoutIcon,
  Business as BusinessIcon
} from '@mui/icons-material';
import { useAppContext } from '../context/AppContext';
import { useNavigate } from 'react-router-dom';

const HeaderBar = () => {
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('md'));
  const { currentUser, logout } = useAppContext();
  const navigate = useNavigate();
  
  const [anchorEl, setAnchorEl] = useState(null);
  const [searchOpen, setSearchOpen] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');

  const handleProfileMenuOpen = (event) => {
    setAnchorEl(event.currentTarget);
  };

  const handleProfileMenuClose = () => {
    setAnchorEl(null);
  };

  const handleLogout = () => {
    logout();
    navigate('/login');
    handleProfileMenuClose();
  };

  const handleSearch = (event) => {
    if (event.key === 'Enter' && searchQuery.trim()) {
      // Navigate to search results or trigger search
      console.log('Searching for:', searchQuery);
      setSearchQuery('');
      setSearchOpen(false);
    }
  };

  const getGreeting = () => {
    const hour = new Date().getHours();
    if (hour < 12) return 'Good Morning';
    if (hour < 17) return 'Good Afternoon';
    return 'Good Evening';
  };

  const getActiveRequestsCount = () => {
    // This would come from context/state management
    return 3; // Mock data
  };

  return (
    <AppBar 
      position="static" 
      elevation={0}
      sx={{ 
        backgroundColor: 'background.paper',
        borderBottom: `1px solid ${theme.palette.divider}`,
        color: 'text.primary'
      }}
    >
      <Toolbar sx={{ justifyContent: 'space-between', py: 1 }}>
        {/* Left Section - Logo and Greeting */}
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
          <BusinessIcon sx={{ color: 'primary.main', fontSize: 28 }} />
          {!isMobile && (
            <Box>
              <Typography variant="h6" sx={{ fontWeight: 600, color: 'text.primary' }}>
                Dubai Real Estate AI
              </Typography>
              <Typography variant="body2" sx={{ color: 'text.secondary' }}>
                {getGreeting()}, {currentUser?.first_name || 'User'}
              </Typography>
            </Box>
          )}
        </Box>

        {/* Center Section - Search (Desktop) */}
        {!isMobile && (
          <Box sx={{ flex: 1, maxWidth: 400, mx: 4 }}>
            <TextField
              fullWidth
              size="small"
              placeholder="Search requests, properties, or ask AI..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              onKeyPress={handleSearch}
              InputProps={{
                startAdornment: (
                  <InputAdornment position="start">
                    <SearchIcon sx={{ color: 'text.secondary' }} />
                  </InputAdornment>
                ),
              }}
              sx={{
                '& .MuiOutlinedInput-root': {
                  backgroundColor: 'grey.50',
                  '&:hover': {
                    backgroundColor: 'grey.100',
                  },
                  '&.Mui-focused': {
                    backgroundColor: 'background.paper',
                  },
                },
              }}
            />
          </Box>
        )}

        {/* Right Section - Actions and Profile */}
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
          {/* Active Requests Badge */}
          <Chip
            label={`${getActiveRequestsCount()} Active`}
            color="primary"
            variant="outlined"
            size="small"
            sx={{ 
              fontWeight: 600,
              '& .MuiChip-label': {
                fontSize: '0.75rem'
              }
            }}
          />

          {/* Notifications */}
          <IconButton color="inherit" sx={{ color: 'text.secondary' }}>
            <Badge badgeContent={3} color="error">
              <NotificationsIcon />
            </Badge>
          </IconButton>

          {/* Mobile Search */}
          {isMobile && (
            <IconButton 
              color="inherit" 
              sx={{ color: 'text.secondary' }}
              onClick={() => setSearchOpen(!searchOpen)}
            >
              <SearchIcon />
            </IconButton>
          )}

          {/* Profile Menu */}
          <IconButton
            onClick={handleProfileMenuOpen}
            sx={{ 
              p: 0.5,
              '&:hover': {
                backgroundColor: 'grey.100',
                borderRadius: '50%'
              }
            }}
          >
            <Avatar
              sx={{ 
                width: 36, 
                height: 36,
                bgcolor: 'primary.main',
                fontSize: '0.875rem',
                fontWeight: 600
              }}
            >
              {currentUser?.first_name?.[0] || 'U'}
            </Avatar>
          </IconButton>

          <Menu
            anchorEl={anchorEl}
            open={Boolean(anchorEl)}
            onClose={handleProfileMenuClose}
            anchorOrigin={{
              vertical: 'bottom',
              horizontal: 'right',
            }}
            transformOrigin={{
              vertical: 'top',
              horizontal: 'right',
            }}
            PaperProps={{
              sx: {
                mt: 1,
                minWidth: 200,
                boxShadow: theme.shadows[8],
                borderRadius: 2,
              }
            }}
          >
            <MenuItem onClick={() => { navigate('/profile'); handleProfileMenuClose(); }}>
              <AccountIcon sx={{ mr: 2, fontSize: 20 }} />
              Profile
            </MenuItem>
            <MenuItem onClick={() => { navigate('/settings'); handleProfileMenuClose(); }}>
              <SettingsIcon sx={{ mr: 2, fontSize: 20 }} />
              Settings
            </MenuItem>
            <MenuItem onClick={handleLogout} sx={{ color: 'error.main' }}>
              <LogoutIcon sx={{ mr: 2, fontSize: 20 }} />
              Logout
            </MenuItem>
          </Menu>
        </Box>
      </Toolbar>

      {/* Mobile Search Bar */}
      {isMobile && searchOpen && (
        <Box sx={{ px: 2, pb: 2 }}>
          <TextField
            fullWidth
            size="small"
            placeholder="Search requests, properties, or ask AI..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            onKeyPress={handleSearch}
            autoFocus
            InputProps={{
              startAdornment: (
                <InputAdornment position="start">
                  <SearchIcon sx={{ color: 'text.secondary' }} />
                </InputAdornment>
              ),
            }}
            sx={{
              '& .MuiOutlinedInput-root': {
                backgroundColor: 'grey.50',
              },
            }}
          />
        </Box>
      )}
    </AppBar>
  );
};

export default HeaderBar;