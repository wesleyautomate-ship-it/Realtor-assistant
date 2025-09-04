import React, { Suspense } from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import { AppProvider } from './context/AppContext';
import { CircularProgress, Box, ThemeProvider } from '@mui/material';
import { customTheme } from './theme/customTheme';
import { ToastProvider } from './components/common/ToastNotifications';
import ProtectedRoute from './components/ProtectedRoute';
import MainLayout from './layouts/MainLayout';
import LoginPage from './pages/LoginPage';
import ErrorBoundary from './components/ErrorBoundary';
import SessionWarning from './components/SessionWarning';

// Lazy load page components for better performance
const Dashboard = React.lazy(() => import('./pages/Dashboard'));
const AgentHub = React.lazy(() => import('./components/hub/AgentHub'));
const Chat = React.lazy(() => import('./pages/Chat'));
const Properties = React.lazy(() => import('./pages/Properties'));
const AdminFiles = React.lazy(() => import('./pages/AdminFiles'));

// Loading fallback component
const PageLoader = () => (
  <Box 
    sx={{ 
      display: 'flex', 
      justifyContent: 'center', 
      alignItems: 'center', 
      height: '100vh',
      backgroundColor: 'background.default'
    }}
  >
    <CircularProgress />
  </Box>
);

// Main App component
const App = () => {
  return (
    <ThemeProvider theme={customTheme}>
      <ToastProvider>
        <AppProvider>
          {/* Global Session Warning Component */}
          <SessionWarning />
          
          <Routes>
        {/* Public routes */}
        <Route path="/login" element={<LoginPage />} />
        
        {/* Protected routes */}
        <Route
          path="/"
          element={
            <ProtectedRoute>
              <ErrorBoundary>
                <MainLayout />
              </ErrorBoundary>
            </ProtectedRoute>
          }
        >
          <Route index element={<Navigate to="/hub" replace />} />
          <Route 
            path="hub" 
            element={
              <ErrorBoundary>
                <Suspense fallback={<PageLoader />}>
                  <AgentHub />
                </Suspense>
              </ErrorBoundary>
            } 
          />
          <Route 
            path="dashboard" 
            element={
              <ErrorBoundary>
                <Suspense fallback={<PageLoader />}>
                  <Dashboard />
                </Suspense>
              </ErrorBoundary>
            } 
          />
          <Route 
            path="chat" 
            element={
              <ErrorBoundary>
                <Suspense fallback={<PageLoader />}>
                  <Chat />
                </Suspense>
              </ErrorBoundary>
            } 
          />
          <Route 
            path="chat/:sessionId" 
            element={
              <ErrorBoundary>
                <Suspense fallback={<PageLoader />}>
                  <Chat />
                </Suspense>
              </ErrorBoundary>
            } 
          />
          <Route 
            path="properties" 
            element={
              <ErrorBoundary>
                <Suspense fallback={<PageLoader />}>
                  <Properties />
                </Suspense>
              </ErrorBoundary>
            } 
          />
          
          {/* Admin routes */}
          <Route path="admin">
            <Route 
              path="files" 
              element={
                <ErrorBoundary>
                  <Suspense fallback={<PageLoader />}>
                    <AdminFiles />
                  </Suspense>
                </ErrorBoundary>
              } 
            />
          </Route>
        </Route>

        {/* Catch all route */}
        <Route path="*" element={<Navigate to="/hub" replace />} />
      </Routes>
        </AppProvider>
      </ToastProvider>
    </ThemeProvider>
  );
};

export default App;
