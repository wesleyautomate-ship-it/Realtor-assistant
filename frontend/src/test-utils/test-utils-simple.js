import React from 'react';
import { render } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';

// Simple render function without complex providers
const SimpleProviders = ({ children }) => {
  return (
    <BrowserRouter>
      {children}
    </BrowserRouter>
  );
};

// Simple render function
const simpleRender = (ui, options) =>
  render(ui, { wrapper: SimpleProviders, ...options });

// Re-export everything
export * from '@testing-library/react';

// Override render method
export { simpleRender as render };

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

// Mock API functions
export const mockApi = {
  getAgenda: jest.fn().mockResolvedValue(mockAgenda),
  getTaskStatus: jest.fn().mockResolvedValue(mockTask),
  sendMessage: jest.fn().mockResolvedValue({ message: 'Test response' }),
};
