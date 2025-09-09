# Development Authentication Guide

## Overview

This guide explains the development authentication bypass system implemented to streamline development workflows while maintaining security in production environments.

## Standard Practices for Development Login Bypass

### 1. Environment-Based Authentication

The system uses environment variables to determine when authentication bypass is available:

```bash
# Development mode (authentication bypass enabled)
ENVIRONMENT=development
DEBUG=true

# Production mode (authentication bypass disabled)
ENVIRONMENT=production
DEBUG=false
```

### 2. Development Authentication Features

#### Backend Features

- **Development Login Endpoint**: `/auth/dev-login`
- **Development Users Endpoint**: `/auth/dev-users`
- **Environment Detection**: Automatic detection of development mode
- **JWT Token Generation**: Valid JWT tokens for development users

#### Frontend Features

- **Auto-Login**: Automatic login in development mode
- **Development Login Panel**: UI component for quick role switching
- **Development Banner**: Visual indicator when in development mode
- **Role Selection**: Easy switching between admin, agent, and employee roles

### 3. Available Development Users

| Role | Email | Permissions |
|------|-------|-------------|
| Admin | admin@dubai-estate.com | Full system access |
| Agent | agent@dubai-estate.com | Agent-level permissions |
| Employee | employee@dubai-estate.com | Employee-level permissions |

## Usage Instructions

### Backend Development

#### 1. Development Login Endpoint

```python
# POST /auth/dev-login
{
  "role": "agent"  # or "admin", "employee"
}

# Response
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "refresh_token": "dev-refresh-agent",
  "expires_in": 1800,
  "user": {
    "id": 2,
    "email": "agent@dubai-estate.com",
    "first_name": "Development",
    "last_name": "Agent",
    "role": "agent",
    "is_active": true,
    "email_verified": true
  }
}
```

#### 2. Environment Detection

```python
from backend.auth.dev_auth_bypass import is_development_mode

if is_development_mode():
    # Development-only code here
    pass
```

#### 3. Development User Creation

```python
from backend.auth.dev_auth_bypass import get_dev_user, create_dev_token

# Get development user data
dev_user = get_dev_user("admin")

# Create development token
token = create_dev_token("agent")
```

### Frontend Development

#### 1. Auto-Login Configuration

```javascript
import { setDevAutoLogin, AUTO_LOGIN_CONFIG } from '../config/development';

// Enable auto-login with default role
setDevAutoLogin(true, 'agent', true);

// Check if auto-login is enabled
if (AUTO_LOGIN_CONFIG.enabled) {
  // Auto-login will happen automatically
}
```

#### 2. Manual Development Login

```javascript
import { performDevLogin } from '../config/development';

// Perform development login
const loginData = await performDevLogin('admin');
console.log('Logged in as:', loginData.user);
```

#### 3. Development Utilities

```javascript
import { devUtils, isDevelopment } from '../config/development';

// Check if in development mode
if (isDevelopment()) {
  // Development-only code
  devUtils.log('Development mode active');
  devUtils.showDevBanner();
}
```

## Security Considerations

### Production Safety

1. **Environment Checks**: All development features check environment before activation
2. **Production Blocking**: Development endpoints return 403 in production
3. **Token Validation**: Development tokens are marked with `dev_mode: true`
4. **Audit Logging**: All development logins are logged for security

### Best Practices

1. **Never Commit Production Credentials**: Use environment variables
2. **Test Production Builds**: Ensure development features are disabled
3. **Monitor Logs**: Watch for development login attempts in production
4. **Regular Security Reviews**: Audit development bypass code

## Configuration

### Environment Variables

```bash
# Required for development mode
ENVIRONMENT=development
DEBUG=true

# Optional development settings
DEV_AUTO_LOGIN=true
DEV_DEFAULT_ROLE=agent
```

### Frontend Configuration

```javascript
// In your .env file
REACT_APP_ENVIRONMENT=development
REACT_APP_API_URL=http://localhost:8001
```

## Troubleshooting

### Common Issues

1. **Development Login Not Working**
   - Check `ENVIRONMENT=development` in backend
   - Verify `NODE_ENV=development` in frontend
   - Ensure backend is running on correct port

2. **Auto-Login Not Triggering**
   - Check localStorage for `dev-auto-login=true`
   - Verify development mode detection
   - Check browser console for errors

3. **Production Build Issues**
   - Ensure `NODE_ENV=production` for builds
   - Verify development code is tree-shaken
   - Test production build locally

### Debug Commands

```bash
# Check environment variables
echo $ENVIRONMENT
echo $DEBUG

# Check frontend environment
console.log(process.env.NODE_ENV)
console.log(process.env.REACT_APP_ENVIRONMENT)

# Check development mode
import { isDevelopment } from './config/development';
console.log('Development mode:', isDevelopment());
```

## Migration to Production

### Pre-Production Checklist

- [ ] Set `ENVIRONMENT=production`
- [ ] Set `DEBUG=false`
- [ ] Remove development endpoints from production builds
- [ ] Test authentication flow without bypass
- [ ] Verify security headers and CORS settings
- [ ] Run security audit

### Production Deployment

```bash
# Production environment variables
ENVIRONMENT=production
DEBUG=false
SECRET_KEY=your-secure-production-key
DATABASE_URL=your-production-database-url
```

## API Reference

### Development Endpoints

#### POST /auth/dev-login
Development-only login endpoint.

**Request:**
```json
{
  "role": "agent"
}
```

**Response:**
```json
{
  "access_token": "string",
  "refresh_token": "string", 
  "expires_in": 1800,
  "user": {
    "id": 2,
    "email": "agent@dubai-estate.com",
    "first_name": "Development",
    "last_name": "Agent",
    "role": "agent",
    "is_active": true,
    "email_verified": true
  }
}
```

#### GET /auth/dev-users
Get available development user roles.

**Response:**
```json
{
  "available_roles": ["admin", "agent", "employee"],
  "description": "Development users for testing different permission levels"
}
```

### Frontend Functions

#### `performDevLogin(role)`
Perform development login with specified role.

#### `setDevAutoLogin(enabled, role, remember)`
Configure development auto-login preferences.

#### `isDevelopment()`
Check if running in development mode.

#### `devUtils.log(message, data)`
Log development information.

## Conclusion

This development authentication bypass system provides a secure and efficient way to bypass login during development while maintaining production security. Always ensure proper environment configuration and never use development features in production environments.
