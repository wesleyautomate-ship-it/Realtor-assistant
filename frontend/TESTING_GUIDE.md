# 🧪 Frontend Testing Guide

## Overview

This guide covers the comprehensive testing setup for the Dubai Real Estate RAG Frontend application. We use Jest as our test runner and React Testing Library for component testing.

## 🚀 Quick Start

### Run All Tests
```bash
npm run test
```

### Run Tests in Watch Mode
```bash
npm run test:watch
```

### Run Tests with Coverage
```bash
npm run test:coverage
```

### Run Tests for CI/CD
```bash
npm run test:ci
```

## 📁 Test Structure

```
src/
├── components/
│   ├── hub/
│   │   ├── __tests__/           # Test files for hub components
│   │   │   ├── AgentHub.test.jsx
│   │   │   ├── SmartCommandBar.test.jsx
│   │   │   └── TaskQueue.test.jsx
│   │   ├── AgentHub.jsx
│   │   ├── SmartCommandBar.jsx
│   │   └── TaskQueue.jsx
│   └── ...
├── test-utils/                   # Test utilities and helpers
│   └── test-utils.js
├── mocks/                        # Mock files for static assets
│   └── fileMock.js
├── setupTests.js                 # Jest setup configuration
└── ...
```

## 🛠️ Testing Tools

### Core Testing Libraries
- **Jest**: Test runner and assertion library
- **React Testing Library**: Component testing utilities
- **@testing-library/jest-dom**: Custom Jest matchers for DOM testing
- **@testing-library/user-event**: User interaction simulation

### Configuration Files
- **jest.config.js**: Jest configuration
- **setupTests.js**: Global test setup and mocks
- **package.json**: Test scripts and Jest configuration

## 📝 Writing Tests

### Test File Naming Convention
- Test files should be named `ComponentName.test.jsx` or `ComponentName.spec.jsx`
- Place test files in `__tests__` directories alongside the components they test

### Test Structure
```jsx
import React from 'react';
import { render, screen, fireEvent, waitFor } from '../test-utils/test-utils';
import ComponentName from '../ComponentName';

describe('ComponentName Component', () => {
  beforeEach(() => {
    // Setup before each test
    jest.clearAllMocks();
  });

  describe('Rendering', () => {
    it('renders correctly', () => {
      render(<ComponentName />);
      expect(screen.getByText(/Expected Text/i)).toBeInTheDocument();
    });
  });

  describe('User Interactions', () => {
    it('handles user input', async () => {
      render(<ComponentName />);
      const input = screen.getByPlaceholderText(/Enter text/i);
      fireEvent.change(input, { target: { value: 'test' } });
      expect(input.value).toBe('test');
    });
  });

  describe('API Integration', () => {
    it('fetches data on mount', async () => {
      render(<ComponentName />);
      await waitFor(() => {
        expect(screen.getByText(/Loaded Data/i)).toBeInTheDocument();
      });
    });
  });
});
```

### Testing Patterns

#### 1. Component Rendering
```jsx
it('renders without crashing', () => {
  render(<ComponentName />);
  expect(screen.getByTestId('component-root')).toBeInTheDocument();
});
```

#### 2. User Interactions
```jsx
it('responds to user clicks', () => {
  render(<ComponentName />);
  const button = screen.getByRole('button', { name: /Click me/i });
  fireEvent.click(button);
  expect(screen.getByText(/Clicked!/i)).toBeInTheDocument();
});
```

#### 3. Async Operations
```jsx
it('loads data asynchronously', async () => {
  render(<ComponentName />);
  await waitFor(() => {
    expect(screen.getByText(/Data loaded/i)).toBeInTheDocument();
  });
});
```

#### 4. Error Handling
```jsx
it('displays error message on API failure', async () => {
  mockApi.getData.mockRejectedValueOnce(new Error('API Error'));
  render(<ComponentName />);
  await waitFor(() => {
    expect(screen.getByText(/Error loading data/i)).toBeInTheDocument();
  });
});
```

## 🎭 Mocking

### API Mocking
```jsx
// Mock the API module
jest.mock('../../../utils/api', () => ({
  getData: mockApi.getData,
  postData: mockApi.postData,
}));
```

### Hook Mocking
```jsx
// Mock custom hooks
jest.mock('../../hooks/useCustomHook', () => ({
  useCustomHook: () => ({
    data: mockData,
    loading: false,
    error: null,
  }),
}));
```

### Component Mocking
```jsx
// Mock child components
jest.mock('../ChildComponent', () => {
  return function MockChildComponent(props) {
    return <div data-testid="mock-child">{props.children}</div>;
  };
});
```

## 🔍 Testing Utilities

### Custom Render Function
```jsx
import { render } from '../test-utils/test-utils';

// This automatically wraps components with all necessary providers
render(<ComponentName />);
```

### Mock Data
```jsx
import { mockUser, mockAgenda, mockTask } from '../test-utils/test-utils';

// Use predefined mock data in tests
render(<ComponentName user={mockUser} />);
```

### Helper Functions
```jsx
import { waitFor, mockWindowResize, mockScrollPosition } from '../test-utils/test-utils';

// Wait for async operations
await waitFor(() => {
  expect(screen.getByText(/Expected/i)).toBeInTheDocument();
});

// Mock window events
mockWindowResize(1024, 768);
mockScrollPosition(100);
```

## 📊 Coverage Requirements

### Coverage Thresholds
- **Branches**: 70%
- **Functions**: 70%
- **Lines**: 70%
- **Statements**: 70%

### Running Coverage
```bash
npm run test:coverage
```

Coverage reports are generated in the `coverage/` directory and include:
- HTML coverage report
- LCOV coverage data
- Console summary

## 🚨 Common Testing Issues

### 1. Component Not Rendering
- Check if all required providers are included in the test wrapper
- Verify that the component doesn't have any runtime errors
- Check console for error messages

### 2. Async Test Failures
- Use `waitFor()` for async operations
- Ensure proper cleanup in `afterEach` blocks
- Mock timers when testing timeouts

### 3. Mock Not Working
- Verify mock placement (before imports)
- Check mock function signatures
- Ensure mocks are properly reset between tests

### 4. Provider Context Issues
- Use the custom `render` function from test-utils
- Check if all required context providers are included
- Verify context values are properly mocked

## 🎯 Best Practices

### 1. Test Behavior, Not Implementation
```jsx
// ❌ Don't test implementation details
expect(component.state.isLoading).toBe(true);

// ✅ Test user-visible behavior
expect(screen.getByText(/Loading.../i)).toBeInTheDocument();
```

### 2. Use Semantic Queries
```jsx
// ❌ Avoid testing by test ID when possible
screen.getByTestId('submit-button');

// ✅ Use semantic queries
screen.getByRole('button', { name: /Submit/i });
screen.getByLabelText(/Email address/i);
screen.getByPlaceholderText(/Enter email/i);
```

### 3. Test User Workflows
```jsx
it('allows user to complete full workflow', async () => {
  render(<ComponentName />);
  
  // Fill form
  fireEvent.change(screen.getByLabelText(/Name/i), { target: { value: 'John' } });
  fireEvent.change(screen.getByLabelText(/Email/i), { target: { value: 'john@example.com' } });
  
  // Submit form
  fireEvent.click(screen.getByRole('button', { name: /Submit/i }));
  
  // Verify success
  await waitFor(() => {
    expect(screen.getByText(/Success!/i)).toBeInTheDocument();
  });
});
```

### 4. Keep Tests Focused
```jsx
// ❌ Don't test multiple concerns in one test
it('renders, handles input, and submits form', () => {
  // Too many assertions
});

// ✅ Test one concern per test
it('renders form fields', () => {
  // Test rendering
});

it('handles user input', () => {
  // Test input handling
});

it('submits form successfully', () => {
  // Test form submission
});
```

## 🔧 Debugging Tests

### Verbose Output
```bash
npm run test -- --verbose
```

### Debug Mode
```bash
npm run test:debug
```

### Watch Mode with Console
```bash
npm run test:watch
```

### Isolated Test
```bash
npm test -- --testNamePattern="ComponentName Component"
```

## 📚 Additional Resources

- [Jest Documentation](https://jestjs.io/docs/getting-started)
- [React Testing Library Documentation](https://testing-library.com/docs/react-testing-library/intro/)
- [Testing Best Practices](https://kentcdodds.com/blog/common-mistakes-with-react-testing-library)
- [Jest Cheat Sheet](https://github.com/sapegin/jest-cheat-sheet)

## 🎉 Test Examples

See the following test files for comprehensive examples:
- `src/components/hub/__tests__/AgentHub.test.jsx`
- `src/components/hub/__tests__/SmartCommandBar.test.jsx`
- `src/components/hub/__tests__/TaskQueue.test.jsx`

These tests demonstrate:
- Component rendering tests
- User interaction testing
- API integration testing
- Error handling
- Accessibility testing
- Performance testing
- Mock usage patterns
