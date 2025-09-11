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
const AdminDashboard = React.lazy(() => import('./pages/AdminDashboard'));
const RoleBasedDashboard = React.lazy(() => import('./components/RoleBasedDashboard'));
const BrokerageDashboard = React.lazy(() => import('./pages/BrokerageDashboard'));
const AIAssistant = React.lazy(() => import('./pages/AIAssistant'));
const DeveloperDashboard = React.lazy(() => import('./pages/DeveloperDashboard'));
const Hub = React.lazy(() => import('./pages/Hub'));
const Compose = React.lazy(() => import('./pages/Compose'));
const RequestDetail = React.lazy(() => import('./pages/RequestDetail'));
const Chat = React.lazy(() => import('./pages/Chat'));
const Properties = React.lazy(() => import('./pages/Properties'));
const ProfilePage = React.lazy(() => import('./pages/ProfilePage'));
const SettingsPage = React.lazy(() => import('./pages/SettingsPage'));
const AdminFiles = React.lazy(() => import('./pages/AdminFiles'));
const TeamManagement = React.lazy(() => import('./components/team/TeamManagement'));

// New pages for mobile-first design
const Contacts = React.lazy(() => import('./pages/Contacts'));
const Documents = React.lazy(() => import('./pages/Documents'));
const Reports = React.lazy(() => import('./pages/Reports'));

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
          {/* Default route - redirect to dashboard */}
          <Route index element={<Navigate to="/dashboard" replace />} />
          
          {/* Main Dashboard - Role-based routing */}
          <Route 
            path="dashboard" 
            element={
              <ErrorBoundary>
                <Suspense fallback={<PageLoader />}>
                  <RoleBasedDashboard />
                </Suspense>
              </ErrorBoundary>
            } 
          />
          
          {/* Contacts/People Management */}
          <Route 
            path="contacts" 
            element={
              <ErrorBoundary>
                <Suspense fallback={<PageLoader />}>
                  <Contacts />
                </Suspense>
              </ErrorBoundary>
            } 
          />
          
          {/* Chat Interface */}
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
          
          {/* Documents Management */}
          <Route 
            path="documents" 
            element={
              <ErrorBoundary>
                <Suspense fallback={<PageLoader />}>
                  <Documents />
                </Suspense>
              </ErrorBoundary>
            } 
          />
          
          {/* Reports & Analytics */}
          <Route 
            path="reports" 
            element={
              <ErrorBoundary>
                <Suspense fallback={<PageLoader />}>
                  <Reports />
                </Suspense>
              </ErrorBoundary>
            } 
          />
          
          {/* Hub/List - AI Teams and Requests */}
          <Route 
            path="hub" 
            element={
              <ErrorBoundary>
                <Suspense fallback={<PageLoader />}>
                  <Hub />
                </Suspense>
              </ErrorBoundary>
            } 
          />
          
          {/* Additional existing routes */}
          <Route 
            path="compose" 
            element={
              <ErrorBoundary>
                <Suspense fallback={<PageLoader />}>
                  <Compose />
                </Suspense>
              </ErrorBoundary>
            } 
          />
          <Route 
            path="requests/:id" 
            element={
              <ErrorBoundary>
                <Suspense fallback={<PageLoader />}>
                  <RequestDetail />
                </Suspense>
              </ErrorBoundary>
            } 
          />
          <Route 
            path="brokerage-dashboard" 
            element={
              <ErrorBoundary>
                <Suspense fallback={<PageLoader />}>
                  <BrokerageDashboard />
                </Suspense>
              </ErrorBoundary>
            } 
          />
          <Route 
            path="ai-assistant" 
            element={
              <ErrorBoundary>
                <Suspense fallback={<PageLoader />}>
                  <AIAssistant />
                </Suspense>
              </ErrorBoundary>
            } 
          />
          <Route 
            path="developer-dashboard" 
            element={
              <ErrorBoundary>
                <Suspense fallback={<PageLoader />}>
                  <DeveloperDashboard />
                </Suspense>
              </ErrorBoundary>
            } 
          />
          <Route 
            path="team/management" 
            element={
              <ErrorBoundary>
                <Suspense fallback={<PageLoader />}>
                  <TeamManagement />
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
          <Route 
            path="profile" 
            element={
              <ErrorBoundary>
                <Suspense fallback={<PageLoader />}>
                  <ProfilePage />
                </Suspense>
              </ErrorBoundary>
            } 
          />
          <Route 
            path="settings" 
            element={
              <ErrorBoundary>
                <Suspense fallback={<PageLoader />}>
                  <SettingsPage />
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
      </ToastProvider>
    </ThemeProvider>
  );
};

export default App;