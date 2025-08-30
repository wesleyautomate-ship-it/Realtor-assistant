# 🚀 Quick Start Guide - Dubai RAG System Frontend

## 📋 Prerequisites

Before you begin, ensure you have the following installed:
- **Node.js** (v16 or higher)
- **npm** (v8 or higher)
- **Git**

## 🛠️ Installation

### 1. Clone the Repository
```bash
git clone <repository-url>
cd "RAG web app/frontend"
```

### 2. Install Dependencies
```bash
npm install
```

### 3. Environment Setup
Create a `.env` file in the frontend directory:
```bash
REACT_APP_API_URL=http://localhost:8001
REACT_APP_ENV=development
```

### 4. Start Development Server
```bash
npm start
```

The application will open at `http://localhost:3001`

## 🎯 Demo Login

For quick testing, use the demo login buttons:

### Agent Demo
- **Role**: Standard real estate agent
- **Access**: Dashboard, Properties, Chat
- **Features**: Property search, AI chat, file upload in chat

### Admin Demo
- **Role**: System administrator
- **Access**: All agent features + File Hub
- **Features**: System-wide file management, admin statistics

## 🧪 Testing the Application

### 1. Authentication Flow
- Click "Demo Agent" or "Demo Admin"
- Verify redirect to dashboard
- Check sidebar shows correct user info

### 2. Dashboard Features
- View daily briefing widget
- Check market update charts
- Test quick action buttons

### 3. Properties Hub
- Browse property listings
- Test filters (location, price, type)
- Switch between grid/list views
- Try favorite/unfavorite actions

### 4. Chat Interface
- Start a new conversation
- Send a message
- Upload a file (paperclip icon)
- View contextual help examples

### 5. Admin Features (Admin Demo)
- Access File Hub
- Upload a document
- View file statistics
- Test file management

## 🔧 Development Commands

```bash
npm start          # Start development server
npm run build      # Build for production
npm test           # Run tests
npm run eject      # Eject from Create React App
```

## 📁 Key Files to Explore

### Core Components
- `src/App.jsx` - Main application router
- `src/context/AppContext.jsx` - Global state management
- `src/layouts/MainLayout.jsx` - Application shell

### Pages
- `src/pages/LoginPage.jsx` - Authentication
- `src/pages/Dashboard.jsx` - Main dashboard
- `src/pages/Properties.jsx` - Property management
- `src/pages/Chat.jsx` - AI chat interface
- `src/pages/AdminFiles.jsx` - File management

### Utilities
- `src/utils/api.js` - API integration
- `src/components/ProtectedRoute.jsx` - Route protection
- `src/components/Sidebar.jsx` - Navigation

## 🔌 API Integration

### Backend Connection
The frontend connects to the backend API at `http://localhost:8001` by default.

### Key API Endpoints
- `/auth/login` - User authentication
- `/sessions` - Chat session management
- `/properties` - Property data
- `/admin/files` - File management
- `/market/overview` - Market data

### Mock Data
During development, the application uses mock data when API calls fail, ensuring the UI remains functional.

## 🎨 UI Components

### Material-UI Theme
The application uses a custom Material-UI theme with:
- **Primary Color**: Professional blue (#1976d2)
- **Secondary Color**: Dubai gold accent
- **Typography**: Roboto font family
- **Components**: Customized buttons, cards, and forms

### Responsive Design
- **Mobile**: Collapsible sidebar, touch-friendly
- **Tablet**: Adaptive layouts
- **Desktop**: Full sidebar, enhanced features

## 🐛 Troubleshooting

### Common Issues

#### 1. Port Already in Use
```bash
# Kill process on port 3001
npx kill-port 3001
# Or use a different port
PORT=3002 npm start
```

#### 2. API Connection Issues
- Verify backend is running on port 8001
- Check `.env` file configuration
- Application will use mock data if API is unavailable

#### 3. Build Errors
```bash
# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install
```

#### 4. ESLint Warnings
The application includes ESLint configuration. Warnings are shown in the terminal but don't prevent the app from running.

## 📱 Browser Testing

### Supported Browsers
- Chrome (recommended)
- Firefox
- Safari
- Edge

### Mobile Testing
- Use browser dev tools for mobile simulation
- Test touch interactions
- Verify responsive layouts

## 🚀 Production Build

### Build Process
```bash
npm run build
```

### Build Output
- Optimized production files in `build/` directory
- Minified JavaScript and CSS
- Static assets ready for deployment

### Deployment
The `build/` folder can be deployed to:
- Netlify
- Vercel
- AWS S3
- Any static hosting service

## 📚 Additional Resources

### Documentation
- `FRONTEND_DOCUMENTATION.md` - Comprehensive documentation
- `README.md` - Project overview
- Component comments for code-level documentation

### External Resources
- [React Documentation](https://reactjs.org/docs/)
- [Material-UI Documentation](https://mui.com/)
- [React Router Documentation](https://reactrouter.com/)

## 🤝 Contributing

### Code Standards
- Follow ESLint configuration
- Use functional components with hooks
- Implement proper error handling
- Add loading states for async operations

### Development Workflow
1. Create feature branch
2. Implement changes
3. Test thoroughly
4. Submit pull request

## 🎉 Getting Help

If you encounter issues:
1. Check the troubleshooting section
2. Review the comprehensive documentation
3. Check browser console for errors
4. Verify API connectivity

---

**Happy Coding! 🚀**

The Dubai RAG System frontend is designed to be developer-friendly and well-documented. Feel free to explore the codebase and contribute to its development.
