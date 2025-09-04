# Phase 3B: Frontend Components Implementation Plan

## Overview
Phase 3B focuses on implementing the frontend components for the Advanced In-Chat Experience, including the Contextual Side Panel and Rich Chat Components.

## New Components to Create

### 1. ContextualSidePanel.jsx
**Location**: `frontend/src/components/chat/ContextualSidePanel.jsx`
**Purpose**: Displays relevant context based on detected entities in the conversation
**Props**:
- `entities` (array): Detected entities from AI responses
- `conversationId` (string): Current conversation ID
- `onEntityClick` (function): Callback when entity is clicked
- `isVisible` (boolean): Whether panel should be visible

**Material-UI Components**:
- `Paper`, `Box`, `Typography`, `List`, `ListItem`, `ListItemText`
- `Chip`, `Avatar`, `Divider`, `Skeleton`
- `IconButton` for close/minimize

**Features**:
- Entity detection display
- Context fetching and caching
- Rich entity cards
- Loading states
- Error handling

### 2. PropertyCard.jsx
**Location**: `frontend/src/components/chat/PropertyCard.jsx`
**Purpose**: Rich display component for property information in chat
**Props**:
- `property` (object): Property data
- `compact` (boolean): Whether to show compact version
- `onClick` (function): Click handler

**Material-UI Components**:
- `Card`, `CardContent`, `CardMedia`, `CardActions`
- `Typography`, `Box`, `Chip`, `Rating`
- `Button`, `IconButton`

**Features**:
- Property image display
- Key details (price, beds, baths, sqft)
- Status indicators
- Action buttons

### 3. ContentPreviewCard.jsx
**Location**: `frontend/src/components/chat/ContentPreviewCard.jsx`
**Purpose**: Preview component for documents, reports, and other content
**Props**:
- `content` (object): Content metadata
- `type` (string): Content type (document, report, etc.)
- `onView` (function): View handler

**Material-UI Components**:
- `Card`, `CardContent`, `CardActions`
- `Typography`, `Box`, `Chip`
- `Button`, `IconButton`

**Features**:
- Content type icons
- Preview text
- Metadata display
- View/download actions

## Components to Modify

### 1. Chat.jsx
**Location**: `frontend/src/pages/Chat.jsx`
**Changes**:
- Implement two-panel layout (chat + side panel)
- Add entity detection integration
- Integrate rich chat components
- Add context fetching logic
- Update message rendering to use rich components

**New Features**:
- Split view layout
- Entity detection on AI responses
- Context side panel integration
- Rich message rendering
- Context caching

### 2. MainLayout.jsx
**Location**: `frontend/src/layouts/MainLayout.jsx`
**Changes**:
- Add context management state
- Integrate entity detection services
- Add context panel toggle

## API Layer Updates

### 1. api.js
**Location**: `frontend/src/utils/api.js`
**New Functions**:
- `detectEntities(message)`: POST to `/phase3/ai/detect-entities`
- `fetchEntityContext(entityType, entityId)`: GET `/phase3/context/{entityType}/{entityId}`
- `getPropertyDetails(propertyId)`: GET `/phase3/properties/{propertyId}/details`
- `getClientInfo(clientId)`: GET `/phase3/clients/{clientId}`
- `getMarketContext(location, propertyType)`: GET `/phase3/market/context`
- `batchFetchContext(entities)`: POST `/phase3/context/batch`

## Implementation Order

### Step 1: Create Rich Chat Components
1. Create `PropertyCard.jsx`
2. Create `ContentPreviewCard.jsx`
3. Test components with sample data

### Step 2: Create Contextual Side Panel
1. Create `ContextualSidePanel.jsx`
2. Implement entity display logic
3. Add context fetching integration
4. Add loading and error states

### Step 3: Update Chat.jsx
1. Implement two-panel layout
2. Add entity detection integration
3. Integrate rich chat components
4. Add context side panel

### Step 4: Update API Layer
1. Add new API functions to `api.js`
2. Implement error handling
3. Add request/response interceptors

### Step 5: Update MainLayout.jsx
1. Add context management state
2. Integrate entity detection
3. Add context panel controls

## Technical Considerations

### State Management
- Context data caching
- Entity detection state
- Side panel visibility state
- Loading states for context fetching

### Performance
- Debounced entity detection
- Context data caching with expiration
- Lazy loading of rich components
- Optimized re-renders

### Error Handling
- API error handling for context fetching
- Fallback to text-only display
- Graceful degradation for missing data

### Accessibility
- Keyboard navigation for side panel
- Screen reader support
- Focus management
- ARIA labels and descriptions

## Testing Strategy

### Unit Tests
- Component rendering tests
- Props validation tests
- Event handler tests

### Integration Tests
- API integration tests
- Context fetching tests
- Entity detection tests

### User Acceptance Tests
- Two-panel layout functionality
- Rich component display
- Context side panel interaction
- Performance testing

## Success Criteria

1. **Two-Panel Layout**: Chat.jsx successfully displays chat and context side panel
2. **Entity Detection**: AI responses trigger entity detection and context fetching
3. **Rich Components**: Property and content cards display properly in chat
4. **Context Side Panel**: Relevant context displays based on conversation entities
5. **Performance**: No significant performance degradation with new features
6. **Error Handling**: Graceful handling of API failures and missing data
7. **Accessibility**: All new components meet accessibility standards

## Dependencies

- Material-UI components
- React Router for navigation
- Axios for API calls
- Existing chat infrastructure
- Phase 3A backend services (already implemented)

## Timeline Estimate

- Step 1 (Rich Components): 2-3 hours
- Step 2 (Side Panel): 3-4 hours
- Step 3 (Chat Integration): 4-5 hours
- Step 4 (API Layer): 1-2 hours
- Step 5 (Layout Updates): 1-2 hours
- Testing and refinement: 2-3 hours

**Total Estimated Time**: 13-19 hours
