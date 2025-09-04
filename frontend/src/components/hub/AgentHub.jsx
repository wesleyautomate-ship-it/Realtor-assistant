import React, { useState, useEffect } from 'react';
import {
  Box,
  Grid,
  Paper,
  Typography,
  useTheme,
  useMediaQuery,
  Fade,
  Grow,
} from '@mui/material';
import {
  Dashboard as DashboardIcon,
  Chat as ChatIcon,
  Home as HomeIcon,
  People as PeopleIcon,
  Analytics as AnalyticsIcon,
} from '@mui/icons-material';

// Import new AI Copilot components
import TodaysAgendaPanel from './TodaysAgendaPanel';
import ReadyForReviewPanel from './ReadyForReviewPanel';

// Import new hub components (we'll create these next)
import GlobalCommandBar from '../GlobalCommandBar';
import TaskQueue from './TaskQueue';
import AIInsightsPanel from './AIInsightsPanel';
import ContentHub from './ContentHub';
import MobileNavigation from './MobileNavigation';
import RealTimeNotifications from './RealTimeNotifications';

const AgentHub = () => {
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('md'));
  const isTablet = useMediaQuery(theme.breakpoints.down('lg'));

  const [activeSection, setActiveSection] = useState('hub');
  const [commandBarOpen, setCommandBarOpen] = useState(false);

  // Mock data for development - will be replaced with real API calls
  const [userStats, setUserStats] = useState({
    totalLeads: 24,
    activeProperties: 12,
    pendingTasks: 5,
    completedToday: 8,
  });

  useEffect(() => {
    // TODO: Fetch real user statistics and insights
    console.log('AgentHub mounted - fetching user data...');
  }, []);

  // Global keyboard shortcut for Command Bar (Ctrl+K or Cmd+K)
  useEffect(() => {
    const handleKeyDown = (event) => {
      if ((event.ctrlKey || event.metaKey) && event.key === 'k') {
        event.preventDefault();
        setCommandBarOpen(true);
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, []);

  // Handle command execution
  const handleCommandExecuted = (result) => {
    console.log('Command executed:', result);
    // TODO: Handle command results (e.g., show notifications, navigate, etc.)
    setCommandBarOpen(false);
  };

  // Desktop Layout: Three-column design
  const renderDesktopLayout = () => (
    <Box sx={{ height: '100vh', display: 'flex', overflow: 'hidden' }}>
      {/* Left Column: Smart Navigation & AI Command Center */}
      <Box
        sx={{
          width: 280,
          bgcolor: 'background.paper',
          borderRight: `1px solid ${theme.palette.divider}`,
          display: 'flex',
          flexDirection: 'column',
          p: 2,
        }}
      >
        {/* Logo and Brand */}
        <Box sx={{ textAlign: 'center', mb: 3 }}>
          <Typography variant="h5" sx={{ fontWeight: 700, color: 'primary.main' }}>
            Dubai RAG
          </Typography>
        </Box>

        {/* AI Command Button - The Star of the Show */}
        <Paper
          elevation={3}
          sx={{
            p: 2,
            mb: 3,
            background: 'linear-gradient(135deg, #1976d2 0%, #42a5f5 100%)',
            color: 'white',
            cursor: 'pointer',
            transition: 'all 0.3s ease',
            '&:hover': {
              transform: 'translateY(-2px)',
              boxShadow: theme.shadows[8],
            },
          }}
          onClick={() => setCommandBarOpen(true)}
        >
          <Box sx={{ textAlign: 'center' }}>
            <Typography variant="h6" sx={{ fontWeight: 600, mb: 1 }}>
              ⭐ AI COMMAND
            </Typography>
            <Typography variant="body2" sx={{ opacity: 0.9 }}>
              Your AI Copilot awaits
            </Typography>
            <Typography variant="caption" sx={{ opacity: 0.8, fontSize: '0.7rem' }}>
              Press Ctrl+K anytime
            </Typography>
          </Box>
        </Paper>

        {/* Navigation Menu */}
        <Box sx={{ flex: 1 }}>
          <Typography variant="subtitle2" sx={{ color: 'text.secondary', mb: 1 }}>
            Navigation
          </Typography>
          {[
            { id: 'hub', label: 'Hub', icon: DashboardIcon, active: true },
            { id: 'chat', label: 'Chat', icon: ChatIcon },
            { id: 'properties', label: 'Properties', icon: HomeIcon },
            { id: 'clients', label: 'Clients', icon: PeopleIcon },
            { id: 'analytics', label: 'Analytics', icon: AnalyticsIcon },
          ].map((item) => (
            <Box
              key={item.id}
              sx={{
                display: 'flex',
                alignItems: 'center',
                p: 1.5,
                mb: 0.5,
                borderRadius: 1,
                cursor: 'pointer',
                bgcolor: item.active ? 'primary.light' : 'transparent',
                color: item.active ? 'primary.contrastText' : 'text.primary',
                '&:hover': {
                  bgcolor: item.active ? 'primary.main' : 'action.hover',
                },
                transition: 'all 0.2s ease',
              }}
              onClick={() => setActiveSection(item.id)}
            >
              <item.icon sx={{ mr: 2, fontSize: 20 }} />
              <Typography variant="body2" sx={{ fontWeight: item.active ? 600 : 400 }}>
                {item.label}
              </Typography>
            </Box>
          ))}
        </Box>

        {/* User Profile */}
        <Box sx={{ p: 2, borderTop: `1px solid ${theme.palette.divider}` }}>
          <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
            <Box
              sx={{
                width: 40,
                height: 40,
                borderRadius: '50%',
                bgcolor: 'primary.main',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                color: 'white',
                fontWeight: 600,
                mr: 2,
              }}
            >
              W
            </Box>
            <Box>
              <Typography variant="body2" sx={{ fontWeight: 600 }}>
                Wesley Agent
              </Typography>
              <Typography variant="caption" sx={{ color: 'primary.main' }}>
                [Agent]
              </Typography>
            </Box>
          </Box>
        </Box>
      </Box>

      {/* Center Column: Today's Mission Control */}
      <Box
        sx={{
          flex: 1,
          display: 'flex',
          flexDirection: 'column',
          overflow: 'hidden',
        }}
      >
        {/* Header */}
        <Box
          sx={{
            p: 3,
            borderBottom: `1px solid ${theme.palette.divider}`,
            bgcolor: 'background.default',
          }}
        >
          <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', mb: 2 }}>
            <Box>
              <Typography variant="h4" sx={{ fontWeight: 700, mb: 1 }}>
                🎯 Today's Mission
              </Typography>
              <Typography variant="body1" sx={{ color: 'text.secondary' }}>
                Welcome back, Agent! Here's your proactive dashboard.
              </Typography>
            </Box>
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
              <RealTimeNotifications />
            </Box>
          </Box>
        </Box>

        {/* Content Area */}
        <Box sx={{ flex: 1, overflow: 'auto', p: 3 }}>
          <Grid container spacing={3}>
            {/* Today's Agenda Widget */}
            <Grid item xs={12} lg={6}>
              <Grow in timeout={300}>
                <Paper elevation={2} sx={{ height: '100%', minHeight: 400 }}>
                  <TodaysAgendaPanel />
                </Paper>
              </Grow>
            </Grid>

            {/* Active Tasks Widget */}
            <Grid item xs={12} lg={6}>
              <Grow in timeout={400}>
                <Paper elevation={2} sx={{ height: '100%', minHeight: 400 }}>
                  <ReadyForReviewPanel />
                </Paper>
              </Grow>
            </Grid>

            {/* AI Insights Panel */}
            <Grid item xs={12}>
              <Grow in timeout={500}>
                <Paper elevation={2}>
                  <AIInsightsPanel />
                </Paper>
              </Grow>
            </Grid>
          </Grid>
        </Box>
      </Box>

      {/* Right Column: Live Task & Content Hub */}
      <Box
        sx={{
          width: 350,
          bgcolor: 'background.paper',
          borderLeft: `1px solid ${theme.palette.divider}`,
          display: 'flex',
          flexDirection: 'column',
          overflow: 'hidden',
        }}
      >
        {/* Header */}
        <Box
          sx={{
            p: 2,
            borderBottom: `1px solid ${theme.palette.divider}`,
            bgcolor: 'background.default',
          }}
        >
          <Typography variant="h6" sx={{ fontWeight: 600 }}>
            ⚡ Live Tasks & Results
          </Typography>
        </Box>

        {/* Content */}
        <Box sx={{ flex: 1, overflow: 'auto', p: 2 }}>
          <ContentHub />
        </Box>
      </Box>
    </Box>
  );

  // Mobile Layout: Single-column with bottom navigation
  const renderMobileLayout = () => (
    <Box sx={{ height: '100vh', display: 'flex', flexDirection: 'column' }}>
      {/* Header */}
      <Box
        sx={{
          p: 2,
          borderBottom: `1px solid ${theme.palette.divider}`,
          bgcolor: 'background.default',
        }}
      >
        <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', mb: 2 }}>
          <Box>
            <Typography variant="h5" sx={{ fontWeight: 700, mb: 1 }}>
              🎯 Agent Hub
            </Typography>
            <Typography variant="body2" sx={{ color: 'text.secondary' }}>
              Welcome back, Wesley!
            </Typography>
          </Box>
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
            <RealTimeNotifications />
          </Box>
        </Box>
      </Box>

      {/* Main Content Area */}
      <Box sx={{ flex: 1, overflow: 'auto', p: 2 }}>
        <Grid container spacing={2}>
          {/* Today's Agenda */}
          <Grid item xs={12}>
            <Paper elevation={2}>
              <TodaysAgendaPanel />
            </Paper>
          </Grid>

          {/* Active Tasks */}
          <Grid item xs={12}>
            <Paper elevation={2}>
              <ReadyForReviewPanel />
            </Paper>
          </Grid>

          {/* AI Insights */}
          <Grid item xs={12}>
            <Paper elevation={2}>
              <AIInsightsPanel />
            </Paper>
          </Grid>

          {/* Content Hub */}
          <Grid item xs={12}>
            <Paper elevation={2}>
              <ContentHub />
            </Paper>
          </Grid>
        </Grid>
      </Box>

      {/* Bottom Navigation */}
      <MobileNavigation activeSection={activeSection} onSectionChange={setActiveSection} />
    </Box>
  );

  return (
    <Box sx={{ height: '100vh', bgcolor: 'background.default' }}>
      {isMobile ? renderMobileLayout() : renderDesktopLayout()}
      
      {/* Global Command Bar - AI Copilot Interface */}
      <GlobalCommandBar 
        open={commandBarOpen} 
        onClose={() => setCommandBarOpen(false)} 
        onCommandExecuted={handleCommandExecuted}
      />

      {/* Floating Keyboard Shortcut Hint */}
      <Box
        sx={{
          position: 'fixed',
          bottom: 20,
          right: 20,
          zIndex: theme.zIndex.fab,
          display: { xs: 'none', md: 'block' }, // Only show on desktop
        }}
      >
        <Paper
          elevation={3}
          sx={{
            p: 1.5,
            borderRadius: 2,
            backgroundColor: 'background.paper',
            border: `1px solid ${theme.palette.divider}`,
            cursor: 'pointer',
            '&:hover': {
              backgroundColor: 'action.hover',
            },
          }}
          onClick={() => setCommandBarOpen(true)}
        >
          <Typography variant="caption" sx={{ color: 'text.secondary', fontSize: '0.7rem' }}>
            ⌨️ Ctrl+K
          </Typography>
        </Paper>
      </Box>
    </Box>
  );
};

export default AgentHub;
