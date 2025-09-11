import React, { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Card,
  CardContent,
  Avatar,
  IconButton,
  TextField,
  InputAdornment,
  Chip,
  Stack,
  Grid,
  Paper,
  Button,
  useTheme,
  useMediaQuery,
} from '@mui/material';
import {
  Notifications as NotificationsIcon,
  Mic as MicIcon,
  Send as SendIcon,
  TrendingUp as TrendingUpIcon,
  Home as HomeIcon,
  People as PeopleIcon,
  Description as DescriptionIcon,
  CalendarToday as CalendarIcon,
  AttachMoney as MoneyIcon,
  Business as BusinessIcon,
} from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';
import { useAppContext } from '../context/AppContext';

const Dashboard = () => {
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('md'));
  const navigate = useNavigate();
  const { currentUser } = useAppContext();
  
  const [commandInput, setCommandInput] = useState('');
  const [followUpsCount] = useState(3);
  
  // Mock data - in real app, this would come from your backend
  const meetings = [
    { id: 1, title: "Call Mr. Khan - Palm Jumeirah", time: "2:00 PM" },
    { id: 2, title: "Follow-up with RERA inspector", time: "4:30 PM" },
  ];

  const recentlySold = [
    { id: 1, location: "Palm Jumeirah", type: "3BR", price: "AED 12M" },
    { id: 2, location: "Downtown Dubai", type: "2BR", price: "AED 3.5M" },
  ];

  const marketNews = [
    "Palm Jumeirah rental yields up 3% this week",
    "Dubai Marina sales up 15% MoM",
    "Expo City Dubai launches new district",
  ];

  const handleCommandSubmit = () => {
    if (commandInput.trim()) {
      // Navigate to chat with the command
      navigate('/chat', { 
        state: { prepopulatedPrompt: commandInput } 
      });
      setCommandInput('');
    }
  };

  const handleKeyPress = (event) => {
    if (event.key === 'Enter') {
      handleCommandSubmit();
    }
  };

  const getGreeting = () => {
    const hour = new Date().getHours();
    if (hour < 12) return 'Good Morning';
    if (hour < 17) return 'Good Afternoon';
    return 'Good Evening';
  };

  return (
    <Box sx={{ 
      height: '100vh', 
      bgcolor: '#1a1a2e', // Dark background like mockup
      overflow: 'hidden',
      display: 'flex', 
      flexDirection: 'column'
    }}>
      {/* Header Section - Ultra Compact */}
      <Box sx={{ 
        p: 1.5, 
        background: 'linear-gradient(135deg, #16213e 0%, #0f3460 100%)', // Darker blue gradient
        color: 'white',
        flexShrink: 0
      }}>
        <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', mb: 0.5 }}>
          <Avatar sx={{ bgcolor: 'rgba(255,255,255,0.2)', width: 28, height: 28 }}>
            {currentUser?.first_name?.charAt(0) || 'A'}
          </Avatar>
          <IconButton sx={{ color: 'white', p: 0.3 }}>
            <NotificationsIcon fontSize="small" />
          </IconButton>
        </Box>
        
        <Typography variant="h6" sx={{ fontWeight: 700, mb: 0.25, fontSize: '1.25rem' }}>
          {getGreeting()}, {currentUser?.first_name || 'Laura'}
        </Typography>
        <Typography variant="caption" sx={{ opacity: 0.9, fontSize: '0.75rem' }}>
          {followUpsCount} follow-ups pending today
        </Typography>
      </Box>

      {/* Main Content - Optimized for Single Screen */}
      <Box sx={{ 
        flex: 1, 
        p: 1, 
        overflow: 'hidden',
        display: 'flex',
        flexDirection: 'column'
      }}>
        <Grid container spacing={1} sx={{ height: '100%' }}>
          {/* Meetings Card */}
          <Grid item xs={12} sm={6} sx={{ height: '50%' }}>
            <Card sx={{ 
              borderRadius: 1.5, 
              bgcolor: '#2d2d44', // Dark card background
              border: '1px solid #3a3a5c',
              height: '100%',
              display: 'flex',
              flexDirection: 'column'
            }}>
              <CardContent sx={{ p: 1, flex: 1, display: 'flex', flexDirection: 'column' }}>
                <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                  <CalendarIcon sx={{ color: '#64b5f6', mr: 0.5, fontSize: '1rem' }} />
                  <Typography variant="subtitle2" sx={{ fontWeight: 600, color: 'white', fontSize: '0.85rem' }}>
                    Meetings
                  </Typography>
                </Box>
                <Stack spacing={0.5} sx={{ flex: 1 }}>
                  {meetings.map((meeting) => (
                    <Box key={meeting.id} sx={{ 
                      p: 0.75, 
                      bgcolor: '#3a3a5c', 
                      borderRadius: 1,
                      border: '1px solid #4a4a6c'
                    }}>
                      <Typography variant="body2" sx={{ fontWeight: 500, color: 'white', fontSize: '0.75rem', lineHeight: 1.2 }}>
                        {meeting.title}
                      </Typography>
                      <Typography variant="caption" sx={{ color: '#b0b0b0', fontSize: '0.65rem' }}>
                        {meeting.time}
                      </Typography>
                    </Box>
                  ))}
                </Stack>
              </CardContent>
            </Card>
          </Grid>

          {/* Recently Sold Card */}
          <Grid item xs={12} sm={6} sx={{ height: '50%' }}>
            <Card sx={{ 
              borderRadius: 1.5, 
              bgcolor: '#2d2d44', // Dark card background
              border: '1px solid #3a3a5c',
              height: '100%',
              display: 'flex',
              flexDirection: 'column'
            }}>
              <CardContent sx={{ p: 1, flex: 1, display: 'flex', flexDirection: 'column' }}>
                <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                  <MoneyIcon sx={{ color: '#4caf50', mr: 0.5, fontSize: '1rem' }} />
                  <Typography variant="subtitle2" sx={{ fontWeight: 600, color: 'white', fontSize: '0.85rem' }}>
                    Recently Sold
                  </Typography>
                </Box>
                <Stack spacing={0.5} sx={{ flex: 1 }}>
                  {recentlySold.map((sale) => (
                    <Box key={sale.id} sx={{ 
                      p: 0.75, 
                      bgcolor: '#3a3a5c', 
                      borderRadius: 1,
                      border: '1px solid #4a4a6c'
                    }}>
                      <Typography variant="body2" sx={{ fontWeight: 500, color: 'white', fontSize: '0.75rem', lineHeight: 1.2 }}>
                        {sale.location} - {sale.type}
                      </Typography>
                      <Typography variant="caption" sx={{ color: '#4caf50', fontWeight: 600, fontSize: '0.65rem' }}>
                        {sale.price}
                      </Typography>
                    </Box>
                  ))}
                </Stack>
              </CardContent>
            </Card>
          </Grid>

          {/* Market News Card - Full Width */}
          <Grid item xs={12} sx={{ height: '25%' }}>
            <Card sx={{ 
              borderRadius: 1.5, 
              bgcolor: '#2d2d44', // Dark card background
              border: '1px solid #3a3a5c',
              height: '100%',
              display: 'flex',
              flexDirection: 'column'
            }}>
              <CardContent sx={{ p: 1, flex: 1, display: 'flex', flexDirection: 'column' }}>
                <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                  <TrendingUpIcon sx={{ color: '#ff9800', mr: 0.5, fontSize: '1rem' }} />
                  <Typography variant="subtitle2" sx={{ fontWeight: 600, color: 'white', fontSize: '0.85rem' }}>
                    Market News
                  </Typography>
                </Box>
                <Stack spacing={0.5} sx={{ flex: 1 }}>
                  {marketNews.map((news, index) => (
                    <Box key={index} sx={{ 
                      display: 'flex', 
                      alignItems: 'center',
                      p: 0.75, 
                      bgcolor: '#3a3a5c', 
                      borderRadius: 1,
                      border: '1px solid #4a4a6c'
                    }}>
                      <Box sx={{ 
                        width: 3, 
                        height: 3, 
                        borderRadius: '50%', 
                        bgcolor: '#ff9800', 
                        mr: 1 
                      }} />
                      <Typography variant="body2" sx={{ color: 'white', fontSize: '0.75rem', lineHeight: 1.2 }}>
                        {news}
                      </Typography>
                    </Box>
                  ))}
                </Stack>
              </CardContent>
            </Card>
          </Grid>

          {/* Smart Follow-up Engine Card */}
          <Grid item xs={12} sm={6} sx={{ height: '25%' }}>
            <Card sx={{ 
              borderRadius: 1.5, 
              background: 'linear-gradient(135deg, #7b1fa2 0%, #c2185b 100%)', // Darker purple gradient
              color: 'white',
              height: '100%',
              display: 'flex',
              flexDirection: 'column'
            }}>
              <CardContent sx={{ p: 1, flex: 1, display: 'flex', flexDirection: 'column', justifyContent: 'space-between' }}>
                <Box>
                  <Typography variant="subtitle2" sx={{ fontWeight: 600, mb: 0.25, fontSize: '0.85rem' }}>
                    Smart Follow-up Engine
                  </Typography>
                  <Typography variant="caption" sx={{ opacity: 0.9, fontSize: '0.7rem' }}>
                    5 leads awaiting response
                  </Typography>
                </Box>
                <Button
                  variant="contained"
                  size="small"
                  sx={{
                    bgcolor: 'rgba(255,255,255,0.2)',
                    color: 'white',
                    fontSize: '0.7rem',
                    py: 0.25,
                    px: 1,
                    '&:hover': {
                      bgcolor: 'rgba(255,255,255,0.3)',
                    },
                    borderRadius: 1,
                  }}
                  onClick={() => navigate('/contacts')}
                >
                  View Leads
                </Button>
              </CardContent>
            </Card>
          </Grid>

          {/* Command Center Card */}
          <Grid item xs={12} sm={6} sx={{ height: '25%' }}>
            <Card sx={{ 
              borderRadius: 1.5, 
              background: 'linear-gradient(135deg, #1565c0 0%, #1976d2 100%)', // Darker blue gradient
              color: 'white',
              height: '100%',
              display: 'flex',
              flexDirection: 'column'
            }}>
              <CardContent sx={{ p: 1, flex: 1, display: 'flex', flexDirection: 'column', justifyContent: 'space-between' }}>
                <Box>
                  <Typography variant="subtitle2" sx={{ fontWeight: 600, mb: 0.25, fontSize: '0.85rem' }}>
                    Command Center
                  </Typography>
                  <Typography variant="caption" sx={{ opacity: 0.9, fontSize: '0.65rem', lineHeight: 1.2 }}>
                    Type or speak commands, have full conversations, and let the system handle follow-ups.
      </Typography>
                </Box>
                <TextField
                  fullWidth
                  size="small"
                  placeholder="Ask anything..."
                  value={commandInput}
                  onChange={(e) => setCommandInput(e.target.value)}
                  onKeyPress={handleKeyPress}
                  sx={{
                    '& .MuiOutlinedInput-root': {
                      bgcolor: 'rgba(255,255,255,0.1)',
                      borderRadius: 1,
                      '& fieldset': {
                        borderColor: 'rgba(255,255,255,0.3)',
                      },
                      '&:hover fieldset': {
                        borderColor: 'rgba(255,255,255,0.5)',
                      },
                      '&.Mui-focused fieldset': {
                        borderColor: 'rgba(255,255,255,0.7)',
                      },
                    },
                    '& .MuiInputBase-input': {
                      color: 'white',
                      fontSize: '0.7rem',
                      py: 0.25,
                      '&::placeholder': {
                        color: 'rgba(255,255,255,0.7)',
                      },
                    },
                  }}
                  InputProps={{
                    endAdornment: (
                      <InputAdornment position="end">
                        <IconButton
                          onClick={handleCommandSubmit}
                          sx={{ color: 'white', p: 0.25 }}
                          disabled={!commandInput.trim()}
                          size="small"
                        >
                          <SendIcon fontSize="small" />
                        </IconButton>
                      </InputAdornment>
                    ),
                  }}
                />
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      </Box>
    </Box>
  );
};

export default Dashboard;