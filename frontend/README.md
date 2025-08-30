# Dubai Real Estate RAG System - Frontend

This is the frontend application for the Dubai Real Estate RAG System, built with React and Material-UI.

## Features

- **Modern UI**: Clean, professional interface inspired by Gemini UI
- **Responsive Design**: Works seamlessly on desktop and mobile devices
- **Role-Based Access**: Different interfaces for agents and admins
- **Real-time Chat**: AI-powered conversation interface
- **Property Management**: Browse and search real estate listings
- **File Management**: Document upload and processing (admin only)

## Technology Stack

- **React 18**: Modern React with hooks and functional components
- **Material-UI**: Professional UI components and theming
- **React Router**: Client-side routing
- **Axios**: HTTP client for API communication
- **Date-fns**: Date formatting utilities

## Getting Started

### Prerequisites

- Node.js 16+ 
- npm or yarn

### Installation

1. Install dependencies:
```bash
npm install
```

2. Start the development server:
```bash
npm start
```

The application will be available at `http://localhost:3000`.

### Building for Production

```bash
npm run build
```

## Project Structure

```
src/
├── components/          # Reusable UI components
│   └── Sidebar.jsx     # Main navigation sidebar
├── context/            # React context for state management
│   └── AppContext.jsx  # Global application state
├── layouts/            # Layout components
│   └── MainLayout.jsx  # Main application layout
├── pages/              # Page components
│   ├── Dashboard.jsx   # Dashboard page
│   ├── Chat.jsx        # Chat interface
│   ├── Properties.jsx  # Property listings
│   └── AdminFiles.jsx  # File management (admin)
├── utils/              # Utility functions
├── App.jsx             # Main application component
└── index.js            # Application entry point
```

## API Integration

The frontend communicates with the backend API at `http://localhost:8001`. Key endpoints:

- `/sessions` - Chat session management
- `/chat` - Chat functionality
- `/properties` - Property data
- `/ingest/upload` - File upload (admin)

## Development

### Adding New Pages

1. Create a new component in `src/pages/`
2. Add the route in `src/App.jsx`
3. Add navigation item in `src/components/Sidebar.jsx` if needed

### Styling

The application uses Material-UI's theming system. Custom styles can be added using:

- `sx` prop for component-specific styles
- Theme customization in `src/index.js`
- Custom CSS modules if needed

### State Management

Global state is managed through React Context in `src/context/AppContext.jsx`. This includes:

- User authentication
- Chat sessions
- Application settings
- Error handling

## Phase 1 Implementation

This is Phase 1 of the frontend rebuild, focusing on:

✅ **Application Shell**: Main layout and navigation structure
✅ **Smart Sidebar**: Gemini-inspired collapsible sidebar
✅ **Routing**: Client-side routing with React Router
✅ **Global State**: Context-based state management
✅ **Role-Based UI**: Different interfaces for agents and admins
✅ **Responsive Design**: Mobile and desktop support

## Next Steps (Phase 2)

- Chat functionality implementation
- Property search and filtering
- File upload and management
- Real-time updates
- Advanced analytics dashboard

## Contributing

1. Follow the existing code style
2. Use Material-UI components when possible
3. Test on both desktop and mobile
4. Update documentation for new features

## License

This project is part of the Dubai Real Estate RAG System.
