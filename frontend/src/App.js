import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import { CssBaseline, Box } from '@mui/material';
import './styles/design-system.css';

// Import authentication components
import { AuthProvider, useAuth } from './auth/AuthContext';
import LoginForm from './auth/LoginForm';
import RegisterForm from './auth/RegisterForm';
import ProtectedRoute from './auth/ProtectedRoute';

// Import existing components
import ModernChat from './components/ModernChat';
import ChatGPTStyleChat from './components/ChatGPTStyleChat';
import ModernPropertyManagement from './components/ModernPropertyManagement';
import EnhancedFileUpload from './components/EnhancedFileUpload';

// Import admin components
import AdminDashboard from './components/AdminDashboard';
import AdminDataManagement from './components/AdminDataManagement';
import AdminRAGMonitoring from './components/AdminRAGMonitoring';

const API_BASE_URL = 'http://localhost:8001';

// Create dark theme with gold accents
const theme = createTheme({
  palette: {
    mode: 'dark',
    primary: {
      main: '#D4AF37',
      light: '#E6C866',
      dark: '#B8860B',
      contrastText: '#0F172A',
    },
    secondary: {
      main: '#667eea',
      light: '#8b9dc3',
      dark: '#4a5bb8',
    },
    background: {
      default: '#0F172A',
      paper: '#1E293B',
    },
    surface: {
      main: '#334155',
    },
    text: {
      primary: '#ffffff',
      secondary: '#CBD5E1',
    },
    divider: 'rgba(212, 175, 55, 0.2)',
  },
  typography: {
    fontFamily: '"Inter", "Roboto", "Helvetica", "Arial", sans-serif',
    h1: {
      fontWeight: 700,
      background: 'linear-gradient(135deg, #D4AF37 0%, #E6C866 100%)',
      WebkitBackgroundClip: 'text',
      WebkitTextFillColor: 'transparent',
      backgroundClip: 'text',
    },
    h2: {
      fontWeight: 600,
      color: '#ffffff',
    },
    h3: {
      fontWeight: 600,
      color: '#ffffff',
    },
    h4: {
      fontWeight: 500,
      color: '#ffffff',
    },
    h5: {
      fontWeight: 500,
      color: '#ffffff',
    },
    h6: {
      fontWeight: 500,
      color: '#ffffff',
    },
  },
  components: {
    MuiButton: {
      styleOverrides: {
        root: {
          textTransform: 'none',
          borderRadius: 8,
          fontWeight: 600,
          transition: 'all 0.3s ease',
          '&:hover': {
            transform: 'translateY(-2px)',
          },
        },
        contained: {
          background: 'linear-gradient(135deg, #D4AF37 0%, #E6C866 100%)',
          color: '#0F172A',
          '&:hover': {
            background: 'linear-gradient(135deg, #E6C866 0%, #D4AF37 100%)',
            boxShadow: '0 8px 25px rgba(212, 175, 55, 0.3)',
          },
        },
        outlined: {
          borderColor: 'rgba(212, 175, 55, 0.3)',
          color: '#D4AF37',
          '&:hover': {
            background: 'rgba(212, 175, 55, 0.1)',
            borderColor: '#D4AF37',
          },
        },
      },
    },
  },
});

const AuthWrapper = () => {
  const { isAuthenticated, loading, user } = useAuth();
  const [authMode, setAuthMode] = useState('login');
  const [selectedRole, setSelectedRole] = useState('agent');

  if (loading) {
    return (
      <Box
        sx={{
          display: 'flex',
          justifyContent: 'center',
          alignItems: 'center',
          minHeight: '100vh',
          background: 'linear-gradient(135deg, #0F172A 0%, #1E293B 50%, #334155 100%)',
          color: '#ffffff',
          fontSize: '1.2rem',
          fontWeight: '600'
        }}
      >
        <div style={{ 
          background: 'rgba(212, 175, 55, 0.1)', 
          padding: '20px 40px', 
          borderRadius: '12px',
          border: '1px solid rgba(212, 175, 55, 0.3)',
          color: '#D4AF37'
        }}>
          Loading...
        </div>
      </Box>
    );
  }

  // If user is authenticated, show main app
  if (isAuthenticated) {
    return <MainApp />;
  }

  // Show role selection and login
  return (
    <Box
      sx={{
        minHeight: '100vh',
        background: 'linear-gradient(135deg, #0F172A 0%, #1E293B 50%, #334155 100%)',
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        padding: 3
      }}
    >
      <Box
        sx={{
          maxWidth: 600,
          width: '100%',
          background: 'rgba(30, 41, 59, 0.9)',
          borderRadius: 3,
          padding: 4,
          border: '1px solid rgba(212, 175, 55, 0.2)',
          boxShadow: '0 8px 32px rgba(0, 0, 0, 0.3)'
        }}
      >
        <h1 style={{ 
          textAlign: 'center', 
          marginBottom: 3,
          background: 'linear-gradient(135deg, #D4AF37 0%, #E6C866 100%)',
          WebkitBackgroundClip: 'text',
          WebkitTextFillColor: 'transparent',
          backgroundClip: 'text'
        }}>
          Dubai Real Estate RAG System
        </h1>
        
        <h2 style={{ textAlign: 'center', marginBottom: 4, color: '#ffffff' }}>
          Professional Access Only
        </h2>

        {/* Role Selection */}
        <Box sx={{ mb: 4 }}>
          <h3 style={{ color: '#D4AF37', marginBottom: 2 }}>Select Your Role:</h3>
          <Box sx={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: 2 }}>
            {Object.entries({
              agent: { name: 'Agent', icon: '🏠', description: 'Real estate agents and brokers' },
              employee: { name: 'Employee', icon: '👨‍💼', description: 'Company staff and employees' },
              admin: { name: 'Admin', icon: '⚙️', description: 'System administrators and managers' }
            }).map(([role, info]) => (
              <Box
                key={role}
                onClick={() => setSelectedRole(role)}
                sx={{
                  p: 2,
                  border: selectedRole === role ? '2px solid #D4AF37' : '2px solid rgba(255, 255, 255, 0.1)',
                  borderRadius: 2,
                  cursor: 'pointer',
                  transition: 'all 0.3s ease',
                  background: selectedRole === role ? 'rgba(212, 175, 55, 0.1)' : 'rgba(255, 255, 255, 0.05)',
                  '&:hover': {
                    borderColor: '#D4AF37',
                    background: 'rgba(212, 175, 55, 0.1)'
                  }
                }}
              >
                <div style={{ fontSize: '2rem', textAlign: 'center', marginBottom: 1 }}>
                  {info.icon}
                </div>
                <h4 style={{ textAlign: 'center', color: '#ffffff', margin: '0 0 0.5rem 0' }}>
                  {info.name}
                </h4>
                <p style={{ textAlign: 'center', color: '#94A3B8', fontSize: '0.9rem', margin: 0 }}>
                  {info.description}
                </p>
              </Box>
            ))}
          </Box>
        </Box>

        {/* Login Required */}
        <Box sx={{ textAlign: 'center' }}>
          <h3 style={{ color: '#D4AF37', marginBottom: 2 }}>Login Required:</h3>
          <p style={{ color: '#94A3B8', marginBottom: 2 }}>
            {selectedRole === 'admin' ? 'Administrators must login for security.' :
             selectedRole === 'agent' ? 'Agents must login to access professional features.' :
             'Employees must login to access company resources.'}
          </p>
          <button
            onClick={() => setAuthMode('login')}
            style={{
              padding: '12px 24px',
              background: 'linear-gradient(135deg, #D4AF37 0%, #E6C866 100%)',
              color: '#0F172A',
              border: 'none',
              borderRadius: '8px',
              fontSize: '1rem',
              fontWeight: '600',
              cursor: 'pointer',
              transition: 'all 0.3s ease',
              boxShadow: '0 4px 15px rgba(212, 175, 55, 0.3)'
            }}
            onMouseOver={(e) => {
              e.target.style.transform = 'translateY(-2px)';
              e.target.style.boxShadow = '0 6px 20px rgba(212, 175, 55, 0.4)';
            }}
            onMouseOut={(e) => {
              e.target.style.transform = 'translateY(0)';
              e.target.style.boxShadow = '0 4px 15px rgba(212, 175, 55, 0.3)';
            }}
          >
            Login
          </button>
        </Box>
      </Box>

      {/* Show login/register forms */}
      {authMode === 'login' && (
        <Box sx={{ mt: 3, width: '100%', maxWidth: 400 }}>
          <LoginForm
            onSwitchToRegister={() => setAuthMode('register')}
            selectedRole={selectedRole}
          />
        </Box>
      )}

      {authMode === 'register' && (
        <Box sx={{ mt: 3, width: '100%', maxWidth: 400 }}>
          <RegisterForm
            onSwitchToLogin={() => setAuthMode('login')}
            selectedRole={selectedRole}
          />
        </Box>
      )}
    </Box>
  );
};

// Main application component (only shown when authenticated)
const MainApp = () => {
  const { user, logout } = useAuth();
  const [messages, setMessages] = useState([]);
  const [inputMessage, setInputMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [selectedRole, setSelectedRole] = useState(user?.role || 'agent');
  const [sessionId, setSessionId] = useState(null);
  const [conversationId, setConversationId] = useState(null);
  const [selectedFile, setSelectedFile] = useState(null);
  const [isUploading, setIsUploading] = useState(false);
  const [currentView, setCurrentView] = useState('chat');
  const [chatMode, setChatMode] = useState('modern');
  const [error, setError] = useState(null);
  const [isConnected, setIsConnected] = useState(true);
  const [properties, setProperties] = useState([]);
  const [isSaving, setIsSaving] = useState(false);
  const [sidebarOpen, setSidebarOpen] = useState(false);

  // Role definitions
  const roles = {
    agent: {
      name: 'Agent',
      icon: '🏠',
      description: 'Real estate agents and brokers',
      color: 'var(--success)'
    },
    employee: {
      name: 'Employee',
      icon: '👨‍💼',
      description: 'Company staff and employees',
      color: 'var(--warning)'
    },
    admin: {
      name: 'Admin',
      icon: '⚙️',
      description: 'System administrators and managers',
      color: 'var(--error)'
    }
  };

  // Check if user is admin
  const isAdmin = user?.role === 'admin';

  // Generate a unique session ID
  const generateSessionId = () => {
    return `session_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
  };

  // Load conversation from localStorage
  const loadConversation = (sessionId) => {
    const savedMessages = localStorage.getItem(`chatMessages_${sessionId}`);
    if (savedMessages) {
      try {
        setMessages(JSON.parse(savedMessages));
      } catch (error) {
        console.error('Error loading conversation:', error);
        setMessages([]);
      }
    } else {
      setMessages([]);
    }
  };

  // Handle sending messages
  const handleSendMessage = async (message) => {
    if (!message.trim()) return;

    const userMessage = {
      id: Date.now(),
      text: message,
      sender: 'user',
      timestamp: new Date().toISOString(),
      role: selectedRole
    };

    setMessages(prev => [...prev, userMessage]);
    setIsLoading(true);
    setError(null);

    try {
      const response = await fetch(`${API_BASE_URL}/chat-direct`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message: message,
          role: selectedRole,
          session_id: sessionId,
          conversation_id: conversationId
        }),
      });

      if (response.ok) {
        const data = await response.json();
        const aiMessage = {
          id: Date.now() + 1,
          text: data.response,
          sender: 'ai',
          timestamp: new Date().toISOString(),
          role: selectedRole,
          conversation_id: data.conversation_id
        };
        setMessages(prev => [...prev, aiMessage]);
        setConversationId(data.conversation_id);
      } else {
        throw new Error('Failed to get response');
      }
    } catch (error) {
      console.error('Error sending message:', error);
      setError('Failed to send message. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleFileUpload = async (file) => {
    if (!file) return;

    setIsUploading(true);
    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await fetch(`${API_BASE_URL}/upload-file`, {
        method: 'POST',
        body: formData,
      });

      if (response.ok) {
        const data = await response.json();
        console.log('File uploaded successfully:', data);
      } else {
        throw new Error('Upload failed');
      }
    } catch (error) {
      console.error('Error uploading file:', error);
      setError('Failed to upload file. Please try again.');
    } finally {
      setIsUploading(false);
    }
  };

  const loadSampleProperties = () => {
    const sampleProperties = [
      {
        id: 1,
        title: 'Luxury Villa in Dubai Marina',
        price: 2500000,
        location: 'Dubai Marina',
        bedrooms: 4,
        bathrooms: 5,
        area: 4500,
        status: 'For Sale'
      },
      {
        id: 2,
        title: 'Modern Apartment in Downtown',
        price: 1200000,
        location: 'Downtown Dubai',
        bedrooms: 2,
        bathrooms: 2,
        area: 1200,
        status: 'For Sale'
      }
    ];
    setProperties(sampleProperties);
  };

  useEffect(() => {
    const roleSessionKey = `chatSessionId_${selectedRole}`;
    const existingSessionId = localStorage.getItem(roleSessionKey);
    if (existingSessionId) {
      setSessionId(existingSessionId);
      loadConversation(existingSessionId);
    } else {
      const newSessionId = generateSessionId();
      setSessionId(newSessionId);
      localStorage.setItem(roleSessionKey, newSessionId);
      loadConversation(newSessionId);
    }
  }, [selectedRole]);

  useEffect(() => {
    loadSampleProperties();
  }, []);

  useEffect(() => {
    if (sessionId && messages.length > 0) {
      setIsSaving(true);
      localStorage.setItem(`chatMessages_${sessionId}`, JSON.stringify(messages));
      setTimeout(() => setIsSaving(false), 500);
    }
  }, [messages, sessionId]);

  return (
    <div className="app-container">
      {/* Mobile menu button */}
      <button
        className="md:hidden fixed top-4 left-4 z-50 p-2 bg-surface rounded-lg border border-border-primary"
        onClick={() => setSidebarOpen(!sidebarOpen)}
        style={{
          background: 'var(--bg-surface)',
          border: '1px solid var(--border-primary)',
          borderRadius: 'var(--radius-lg)',
          padding: 'var(--space-2)',
          position: 'fixed',
          top: 'var(--space-4)',
          left: 'var(--space-4)',
          zIndex: 'var(--z-fixed)',
          display: 'none'
        }}
      >
        <span className="text-xl">☰</span>
      </button>

      {/* Sidebar overlay for mobile */}
      <div 
        className={`sidebar-overlay ${sidebarOpen ? 'open' : ''}`}
        onClick={() => setSidebarOpen(false)}
      />

      {/* Sidebar */}
      <div className={`sidebar ${sidebarOpen ? 'open' : ''}`}>
        {/* Header */}
        <div className="sidebar-header">
          <div className="sidebar-logo">
            <div className="logo-icon">🏠</div>
            <div className="logo-text">Dubai AI Estate</div>
          </div>
          
          <div className="user-section">
            <div className="user-avatar">
              {user?.role === 'admin' ? '⚙️' : user?.role === 'agent' ? '🏠' : '👨‍💼'}
            </div>
            <div className="user-info">
              <div className="user-name">{user?.name || 'User'}</div>
              <div className="user-role">{user?.role || 'Agent'}</div>
            </div>
          </div>
        </div>

        {/* Role selection */}
        <div className="nav-section">
          <div className="nav-section-header">Role Selection</div>
          <div className="flex flex-col gap-2">
            {Object.entries(roles).map(([roleKey, role]) => (
              <button
                key={roleKey}
                onClick={() => setSelectedRole(roleKey)}
                className={`nav-button ${selectedRole === roleKey ? 'active' : ''}`}
              >
                <span>{role.icon}</span>
                <span>{role.name}</span>
              </button>
            ))}
          </div>
        </div>

        {/* Navigation */}
        <div className="nav-section">
          <div className="nav-section-header">Navigation</div>
          
          <button
            onClick={() => {
              setCurrentView('chat');
              setSidebarOpen(false);
            }}
            className={`nav-button ${currentView === 'chat' ? 'active' : ''}`}
          >
            <span>💬</span>
            <span>AI Chat</span>
          </button>
          
          {/* Chat Mode Toggle */}
          {currentView === 'chat' && (
            <div className="nav-section">
              <div className="nav-section-header">Chat Mode</div>
              <div className="flex flex-col gap-2">
                <button
                  onClick={() => setChatMode('modern')}
                  className={`nav-button ${chatMode === 'modern' ? 'active' : ''}`}
                  style={{ fontSize: '0.9rem' }}
                >
                  <span>💬</span>
                  <span>Modern Chat</span>
                </button>
                <button
                  onClick={() => setChatMode('chatgpt')}
                  className={`nav-button ${chatMode === 'chatgpt' ? 'active' : ''}`}
                  style={{ fontSize: '0.9rem' }}
                >
                  <span>🤖</span>
                  <span>ChatGPT Style</span>
                </button>
              </div>
            </div>
          )}
          
          <button
            onClick={() => {
              setCurrentView('properties');
              setSidebarOpen(false);
            }}
            className={`nav-button ${currentView === 'properties' ? 'active' : ''}`}
          >
            <span>🏠</span>
            <span>Properties</span>
          </button>
          
          <button
            onClick={() => {
              setCurrentView('upload');
              setSidebarOpen(false);
            }}
            className={`nav-button ${currentView === 'upload' ? 'active' : ''}`}
          >
            <span>📁</span>
            <span>File Upload</span>
          </button>

          {/* Admin-only navigation */}
          {isAdmin && (
            <>
              <button
                onClick={() => {
                  setCurrentView('admin-dashboard');
                  setSidebarOpen(false);
                }}
                className={`nav-button ${currentView === 'admin-dashboard' ? 'active' : ''}`}
              >
                <span>📊</span>
                <span>Admin Dashboard</span>
              </button>
              <button
                onClick={() => {
                  setCurrentView('admin-data');
                  setSidebarOpen(false);
                }}
                className={`nav-button ${currentView === 'admin-data' ? 'active' : ''}`}
              >
                <span>🗄️</span>
                <span>Data Management</span>
              </button>
              <button
                onClick={() => {
                  setCurrentView('admin-rag');
                  setSidebarOpen(false);
                }}
                className={`nav-button ${currentView === 'admin-rag' ? 'active' : ''}`}
              >
                <span>🤖</span>
                <span>RAG Monitoring</span>
              </button>
            </>
          )}
        </div>

        {/* Logout button */}
        <button
          onClick={logout}
          className="nav-button"
          style={{
            marginTop: 'auto',
            background: 'rgba(212, 175, 55, 0.1)',
            borderColor: 'rgba(212, 175, 55, 0.3)',
            color: 'var(--brand-gold)'
          }}
        >
          <span>🚪</span>
          <span>Logout</span>
        </button>
      </div>

      {/* Main content area */}
      <div className="main-content">
        <div className="content-container">
          {currentView === 'chat' && (
            <>
              {chatMode === 'modern' ? (
                <ModernChat
                  messages={messages}
                  onSendMessage={handleSendMessage}
                  isLoading={isLoading}
                  selectedRole={selectedRole}
                  onRoleChange={setSelectedRole}
                  roles={roles}
                  onClearChat={() => {
                    setMessages([]);
                    setError(null);
                  }}
                  isSaving={isSaving}
                  sessionId={sessionId}
                />
              ) : (
                <ChatGPTStyleChat />
              )}
            </>
          )}
          {currentView === 'properties' && (
            <ModernPropertyManagement
              properties={properties}
              onPropertyUpdate={(updatedProperties) => setProperties(updatedProperties)}
            />
          )}
          {currentView === 'upload' && (
            <EnhancedFileUpload
              onFileUpload={handleFileUpload}
              isUploading={isUploading}
            />
          )}
          {currentView === 'admin-dashboard' && isAdmin && (
            <AdminDashboard />
          )}
          {currentView === 'admin-data' && isAdmin && (
            <AdminDataManagement />
          )}
          {currentView === 'admin-rag' && isAdmin && (
            <AdminRAGMonitoring />
          )}
        </div>
      </div>

      {/* Error display */}
      {error && (
        <div className="error-message">
          {error}
          <button
            onClick={() => setError(null)}
            className="bg-none border-none text-white ml-3 cursor-pointer"
          >
            ×
          </button>
        </div>
      )}
    </div>
  );
};

// Main App component with routing
function App() {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <AuthProvider>
        <Router>
          <Routes>
            <Route path="/" element={<AuthWrapper />} />
            <Route path="/login" element={<AuthWrapper />} />
            <Route path="/register" element={<AuthWrapper />} />
            <Route path="/dashboard" element={
              <ProtectedRoute>
                <MainApp />
              </ProtectedRoute>
            } />
            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </Router>
      </AuthProvider>
    </ThemeProvider>
  );
}

export default App;
