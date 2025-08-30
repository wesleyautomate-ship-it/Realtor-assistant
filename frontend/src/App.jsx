import React, { Suspense } from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import { AppProvider } from './context/AppContext';
import { CircularProgress, Box } from '@mui/material';
import ProtectedRoute from './components/ProtectedRoute';
import MainLayout from './layouts/MainLayout';
import LoginPage from './pages/LoginPage';
import ErrorBoundary from './components/ErrorBoundary';

// Lazy load page components for better performance
const Dashboard = React.lazy(() => import('./pages/Dashboard'));
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
    <AppProvider>
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
          <Route index element={<Navigate to="/dashboard" replace />} />
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
        <Route path="*" element={<Navigate to="/dashboard" replace />} />
      </Routes>
    </AppProvider>
  );
};

export default App;
