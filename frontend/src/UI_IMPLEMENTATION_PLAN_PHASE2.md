# Phase 2 Implementation Plan: Core Copilot UI & UX

## Overview
This document outlines the implementation plan for Phase 2 of the "Core Copilot UI & UX" roadmap, focusing on transforming the dashboard into a proactive "Mission Control" and implementing a global command bar for instant AI access.

## New Components

### 1. TodaysAgendaWidget.jsx
**Location:** `frontend/src/components/widgets/TodaysAgendaWidget.jsx`

**Props:**
- `onTaskSelect` (function): Callback when a task is selected
- `refreshInterval` (number, optional): Polling interval in milliseconds (default: 300000 - 5 minutes)

**Material-UI Components:**
- `Card`, `CardContent`, `CardHeader`
- `List`, `ListItem`, `ListItemText`, `ListItemIcon`
- `Button`, `Chip`, `Typography`
- `CircularProgress`, `Alert`
- `Divider`, `Stack`

**Functionality:**
- Fetches agent's daily tasks via `api.getAgenda()`
- Displays tasks in two sections: "Scheduled" and "Suggested"
- Each scheduled task has a "Prep with AI" button that navigates to chat with pre-populated prompt
- Auto-refreshes data at specified interval
- Error handling with user-friendly messages

### 2. ActiveTasksWidget.jsx
**Location:** `frontend/src/components/widgets/ActiveTasksWidget.jsx`

**Props:**
- `pollingInterval` (number, optional): Polling interval for task status (default: 5000 - 5 seconds)
- `maxTasks` (number, optional): Maximum number of tasks to display (default: 10)

**Material-UI Components:**
- `Card`, `CardContent`, `CardHeader`
- `List`, `ListItem`, `ListItemText`, `ListItemIcon`
- `LinearProgress`, `Chip`, `Typography`
- `Button`, `Link`
- `Stack`, `Box`

**Functionality:**
- Manages list of active task IDs in component state
- Implements polling mechanism using `setInterval` to check task status
- Displays task status with progress indicators
- Shows completion status with clickable result links
- Automatically removes completed tasks from active list
- Error handling for failed status checks

### 3. GlobalCommandBar.jsx
**Location:** `frontend/src/components/GlobalCommandBar.jsx`

**Props:**
- `open` (boolean): Controls modal visibility
- `onClose` (function): Callback when modal should close
- `onCommandExecuted` (function, optional): Callback after command execution

**Material-UI Components:**
- `Dialog`, `DialogContent`, `DialogTitle`
- `TextField`, `InputAdornment`
- `Button`, `IconButton`
- `Typography`, `Box`
- `Snackbar`, `Alert`

**Functionality:**
- Modal dialog with auto-focused text input
- Listens for global keyboard shortcut (Ctrl+K / Cmd+K)
- Executes commands via `api.sendMessage()`
- Provides feedback via notifications
- Auto-closes after command execution
- Error handling with user-friendly messages

## Modified Components

### 1. Dashboard.jsx
**Location:** `frontend/src/pages/Dashboard.jsx`

**Changes:**
- Replace current grid layout with modern widget-based grid using Material-UI `Grid` component
- Remove existing dashboard content and replace with widget container
- Import and render `TodaysAgendaWidget` and `ActiveTasksWidget`
- Implement responsive grid layout (2 columns on desktop, 1 column on mobile)
- Add loading states and error handling for widgets
- Maintain existing theme integration and styling patterns

### 2. MainLayout.jsx
**Location:** `frontend/src/layouts/MainLayout.jsx`

**Changes:**
- Import and integrate `GlobalCommandBar` component
- Add command bar button to header/app bar area
- Implement keyboard shortcut listener for global command access
- Add state management for command bar visibility
- Ensure command bar is mounted on all pages
- Maintain existing layout structure and responsive behavior

## API Layer Additions

### New Functions in api.js

#### 1. getAgenda()
**Endpoint:** `GET /users/me/agenda`
**Purpose:** Fetch agent's daily tasks and nurturing suggestions
**Returns:** Object containing scheduled and suggested tasks
**Error Handling:** Network errors, authentication errors, server errors

#### 2. getTaskStatus(taskId)
**Endpoint:** `GET /async/processing-status/${taskId}`
**Purpose:** Check status of asynchronous backend jobs
**Returns:** Object containing task status, progress, and result URL if completed
**Error Handling:** Task not found, processing errors, network errors

#### 3. sendGlobalCommand(message)
**Endpoint:** `POST /sessions/default/chat` or similar
**Purpose:** Execute commands from global command bar
**Returns:** Command execution result
**Error Handling:** Invalid commands, authentication errors, server errors

## Implementation Order

1. **Create API functions** in `api.js`
2. **Create widget components** (`TodaysAgendaWidget.jsx`, `ActiveTasksWidget.jsx`)
3. **Create GlobalCommandBar component**
4. **Modify Dashboard.jsx** to use new widget-based layout
5. **Update MainLayout.jsx** to integrate global command bar
6. **Test integration** and error handling
7. **Polish UI/UX** and responsive behavior

## Technical Considerations

### State Management
- Widgets will manage their own local state for data and loading states
- Global command bar state managed in MainLayout
- Use React hooks for polling and lifecycle management

### Error Handling
- Implement comprehensive error boundaries
- User-friendly error messages
- Graceful degradation when APIs are unavailable
- Retry mechanisms for failed requests

### Performance
- Implement proper cleanup for polling intervals
- Use React.memo for widget components if needed
- Optimize re-renders with proper dependency arrays

### Accessibility
- Keyboard navigation support
- Screen reader compatibility
- ARIA labels and descriptions
- Focus management for modal dialogs

### Responsive Design
- Mobile-first approach
- Adaptive grid layouts
- Touch-friendly interactions
- Optimized for different screen sizes

## Testing Strategy

1. **Unit Tests:** Test individual widget components
2. **Integration Tests:** Test API integration and error handling
3. **E2E Tests:** Test complete user workflows
4. **Accessibility Tests:** Ensure WCAG compliance
5. **Performance Tests:** Verify polling doesn't impact performance

## Success Criteria

- Dashboard displays proactive task information
- Global command bar responds to keyboard shortcuts
- Widgets update in real-time with backend data
- Error states are handled gracefully
- UI is responsive and accessible
- Performance remains optimal with polling
