import React from 'react';
import { render, screen } from '../test-utils-simple';

// Simple test component
const TestComponent = () => <div>Hello Test World</div>;

describe('Test Utilities', () => {
  it('renders a simple component', () => {
    render(<TestComponent />);
    expect(screen.getByText('Hello Test World')).toBeInTheDocument();
  });

  it('provides mock data', () => {
    const { mockUser, mockAgenda, mockTask } = require('../test-utils-simple');
    
    expect(mockUser.email).toBe('test@example.com');
    expect(mockAgenda.date).toBe('2025-09-02');
    expect(mockTask.task_id).toBe('test-task-id');
  });

  it('provides mock API functions', () => {
    const { mockApi } = require('../test-utils-simple');
    
    expect(typeof mockApi.getAgenda).toBe('function');
    expect(typeof mockApi.getTaskStatus).toBe('function');
    expect(typeof mockApi.sendMessage).toBe('function');
  });
});
