import React from 'react';
import { render } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import { ThemeProvider } from '@mui/material/styles';
import { AppProvider } from '../context/AppContext';
import { ToastProvider } from '../components/common/ToastNotifications';
import customTheme from '../theme/customTheme';

// Custom render function that includes all necessary providers
const AllTheProviders = ({ children }) => {
  return (
    <BrowserRouter>
      <ThemeProvider theme={customTheme}>
        <ToastProvider>
          <AppProvider>
            {children}
          </AppProvider>
        </ToastProvider>
      </ThemeProvider>
    </BrowserRouter>
  );
};

// Custom render function
const customRender = (ui, options) =>
  render(ui, { wrapper: AllTheProviders, ...options });

// Re-export everything
export * from '@testing-library/react';

// Override render method
export { customRender as render };

// Mock data for testing
export const mockUser = {
  id: 1,
  email: 'test@example.com',
  first_name: 'Test',
  last_name: 'User',
  role: 'agent',
  is_active: true,
  email_verified: true,
};

export const mockAgenda = {
  date: '2025-09-02',
  scheduled_follow_ups: [
    {
      lead_id: 1,
      lead_name: 'John Doe',
      lead_email: 'john@example.com',
      scheduled_time: '2025-09-02T14:00:00',
      nurture_status: 'Active',
      type: 'scheduled_follow_up',
    },
  ],
  leads_needing_attention: [
    {
      lead_id: 2,
      lead_name: 'Jane Smith',
      lead_email: 'jane@example.com',
      last_contacted: '2025-08-28T10:00:00',
      nurture_status: 'Follow Up',
      type: 'needs_attention',
    },
  ],
  notifications: [
    {
      id: 1,
      notification_type: 'follow_up',
      title: 'Follow Up Reminder',
      message: 'John Doe needs follow up',
      related_lead_id: 1,
      priority: 'high',
      created_at: '2025-09-02T09:00:00',
    },
  ],
  summary: {
    total_follow_ups: 1,
    leads_needing_attention: 1,
    unread_notifications: 1,
  },
};

export const mockTask = {
  task_id: 'test-task-id',
  status: 'completed',
  progress: 1.0,
  created_at: '2025-09-02T10:00:00',
  started_at: '2025-09-02T10:00:01',
  completed_at: '2025-09-02T10:00:05',
  result: {
    analysis: 'Test analysis result',
    recommendations: ['Test recommendation 1', 'Test recommendation 2'],
  },
  error_message: null,
};

export const mockProperty = {
  id: 1,
  address: '123 Test Street, Dubai',
  price: 2500000,
  bedrooms: 3,
  bathrooms: 2.5,
  square_feet: 2000,
  property_type: 'Apartment',
  description: 'Beautiful test property in Dubai',
  listing_status: 'active',
  agent_id: 1,
  created_at: '2025-09-01T00:00:00',
  updated_at: '2025-09-01T00:00:00',
};

export const mockClient = {
  id: 1,
  name: 'Test Client',
  email: 'client@example.com',
  phone: '+971501234567',
  budget_min: 2000000,
  budget_max: 3000000,
  preferred_location: 'Dubai Marina',
  requirements: '3+ bedrooms, waterfront view',
  created_at: '2025-09-01T00:00:00',
  updated_at: '2025-09-01T00:00:00',
};

// Mock API responses
export const mockApiResponses = {
  agenda: mockAgenda,
  task: mockTask,
  property: mockProperty,
  client: mockClient,
  health: { status: 'healthy', timestamp: '2025-09-02T10:00:00' },
};

// Mock API functions
export const mockApi = {
  getAgenda: jest.fn().mockResolvedValue(mockAgenda),
  getTaskStatus: jest.fn().mockResolvedValue(mockTask),
  getPropertyDetails: jest.fn().mockResolvedValue(mockProperty),
  getClientInfo: jest.fn().mockResolvedValue(mockClient),
  sendMessage: jest.fn().mockResolvedValue({ message: 'Test response' }),
  detectEntities: jest.fn().mockResolvedValue([
    { type: 'property', id: '1', confidence: 0.95 },
    { type: 'client', id: '1', confidence: 0.88 },
  ]),
};

// Mock context values
export const mockAppContext = {
  user: mockUser,
  isAuthenticated: true,
  isLoading: false,
  error: null,
  login: jest.fn(),
  logout: jest.fn(),
  register: jest.fn(),
  clearError: jest.fn(),
};

// Mock toast functions
export const mockToast = {
  show: jest.fn(),
  hide: jest.fn(),
  update: jest.fn(),
};

// Helper function to wait for async operations
export const waitFor = (callback, { timeout = 1000 } = {}) => {
  return new Promise((resolve, reject) => {
    const startTime = Date.now();
    
    const check = () => {
      try {
        callback();
        resolve();
      } catch (error) {
        if (Date.now() - startTime > timeout) {
          reject(error);
        } else {
          setTimeout(check, 10);
        }
      }
    };
    
    check();
  });
};

// Helper function to mock window resize
export const mockWindowResize = (width, height) => {
  Object.defineProperty(window, 'innerWidth', {
    writable: true,
    configurable: true,
    value: width,
  });
  Object.defineProperty(window, 'innerHeight', {
    writable: true,
    configurable: true,
    value: height,
  });
  window.dispatchEvent(new Event('resize'));
};

// Helper function to mock scroll position
export const mockScrollPosition = (scrollY) => {
  Object.defineProperty(window, 'scrollY', {
    writable: true,
    configurable: true,
    value: scrollY,
  });
  window.dispatchEvent(new Event('scroll'));
};
