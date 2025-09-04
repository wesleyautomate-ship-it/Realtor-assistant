# Authentication System Documentation

## Overview

The Dubai Real Estate RAG System now includes a comprehensive authentication and security system built with FastAPI, JWT tokens, and React. This system provides enterprise-grade security with role-based access control (RBAC), rate limiting, and audit logging.

## Features

### 🔐 **Security Features**
- **JWT Token Authentication** - Secure token-based authentication
- **Password Hashing** - bcrypt with 12 rounds for maximum security
- **Rate Limiting** - Prevents brute force attacks
- **Session Management** - Secure session tracking and invalidation
- **Role-Based Access Control** - Fine-grained permissions
- **Audit Logging** - Complete security event tracking
- **Input Validation** - XSS and injection protection
- **Security Headers** - Protection against common web vulnerabilities

### 👥 **User Roles**
- **Client** - Property buyers, sellers, and investors
- **Agent** - Real estate agents and brokers
- **Employee** - Company staff and employees
- **Admin** - System administrators and managers

### 🛡️ **Security Measures**
- Password strength validation
- Account lockout after failed attempts
- IP-based rate limiting
- Secure token refresh mechanism
- CSRF protection
- Input sanitization

## Backend Architecture

### Database Schema

```sql
-- Users table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    role VARCHAR(50) DEFAULT 'client',
    is_active BOOLEAN DEFAULT TRUE,
    email_verified BOOLEAN DEFAULT FALSE,
    email_verification_token VARCHAR(255) UNIQUE,
    password_reset_token VARCHAR(255) UNIQUE,
    password_reset_expires TIMESTAMP,
    last_login TIMESTAMP,
    failed_login_attempts INTEGER DEFAULT 0,
    locked_until TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- User sessions table
CREATE TABLE user_sessions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    session_token VARCHAR(255) UNIQUE NOT NULL,
    refresh_token VARCHAR(255) UNIQUE NOT NULL,
    ip_address VARCHAR(45),
    user_agent TEXT,
    expires_at TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_used TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE
);

-- Permissions table
CREATE TABLE permissions (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    description TEXT,
    resource VARCHAR(100) NOT NULL,
    action VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Roles table
CREATE TABLE roles (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    description TEXT,
    is_default BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Role permissions table
CREATE TABLE role_permissions (
    role_id INTEGER REFERENCES roles(id),
    permission_id INTEGER REFERENCES permissions(id),
    PRIMARY KEY (role_id, permission_id)
);

-- User roles table
CREATE TABLE user_roles (
    user_id INTEGER REFERENCES users(id),
    role_id INTEGER REFERENCES roles(id),
    PRIMARY KEY (user_id, role_id)
);

-- Audit logs table
CREATE TABLE audit_logs (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    event_type VARCHAR(100) NOT NULL,
    event_data TEXT,
    ip_address VARCHAR(45),
    user_agent TEXT,
    success BOOLEAN DEFAULT TRUE,
    error_message TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### API Endpoints

#### Authentication Endpoints

```http
POST /auth/register
POST /auth/login
POST /auth/logout
POST /auth/refresh
POST /auth/forgot-password
POST /auth/reset-password
GET /auth/me
```

#### Protected Endpoints

All existing endpoints are now protected and require authentication:

```http
GET /chat
POST /chat
GET /properties
POST /properties
GET /upload
POST /upload
```

### Middleware

The system includes several middleware components:

1. **Authentication Middleware** - Validates JWT tokens
2. **Role-Based Access Control** - Checks user permissions
3. **Rate Limiting** - Prevents abuse
4. **Security Headers** - Adds security headers to responses
5. **Audit Logging** - Logs security events

## Frontend Architecture

### Authentication Context

The frontend uses React Context for state management:

```javascript
const AuthContext = createContext();

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};
```

### Protected Routes

```javascript
import ProtectedRoute from './auth/ProtectedRoute';

// Basic protection
<ProtectedRoute>
  <Component />
</ProtectedRoute>

// Role-based protection
<ProtectedRoute requiredRoles={['admin']}>
  <AdminComponent />
</ProtectedRoute>

// Convenience components
<AdminRoute>
  <AdminComponent />
</AdminRoute>

<AgentRoute>
  <AgentComponent />
</AgentRoute>
```

### Components

1. **LoginForm** - Modern login interface with validation
2. **RegisterForm** - User registration with password strength
3. **ProtectedRoute** - Route protection component
4. **AuthContext** - Authentication state management

## Setup Instructions

### 1. Environment Configuration

Create a `.env` file based on `env.example`:

```bash
# Copy example file
cp env.example .env

# Edit with your values
nano .env
```

### 2. Install Dependencies

```bash
# Backend
cd backend
pip install -r requirements.txt

# Frontend
cd frontend
npm install
```

### 3. Database Setup

```bash
# The database will be automatically initialized when you start the backend
# Default admin user will be created:
# Email: admin@dubai-estate.com
# Password: Admin123!
```

### 4. Start the Application

```bash
# Backend
cd backend
python main.py

# Frontend
cd frontend
npm start
```

## Usage

### 1. Registration

1. Navigate to the application
2. Click "Sign up"
3. Fill in your details
4. Choose your role (Client, Agent, Employee)
5. Create a strong password
6. Submit the form

### 2. Login

1. Enter your email and password
2. Click "Sign In"
3. You'll be redirected to the dashboard

### 3. Role-Based Access

- **Clients** can view properties and chat
- **Agents** can manage properties and view clients
- **Employees** can manage all data
- **Admins** have full system access

### 4. Password Reset

1. Click "Forgot your password?"
2. Enter your email
3. Check your email for reset link
4. Create a new password

## Security Best Practices

### 1. Password Requirements

- Minimum 8 characters
- At least one uppercase letter
- At least one lowercase letter
- At least one number
- Special characters recommended

### 2. Rate Limiting

- 60 requests per minute per IP
- 5 login attempts before lockout
- 15-minute lockout period

### 3. Token Security

- Access tokens expire in 30 minutes
- Refresh tokens expire in 7 days
- Tokens are automatically refreshed

### 4. Session Management

- One active session per user
- Sessions expire after 30 minutes of inactivity
- Automatic logout on token expiration

## API Documentation

### Authentication Headers

All protected endpoints require the Authorization header:

```http
Authorization: Bearer <access_token>
```

### Error Responses

```json
{
  "detail": "Invalid or expired token"
}
```

### Success Responses

```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "token_type": "bearer",
  "expires_in": 1800,
  "user": {
    "id": 1,
    "email": "user@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "role": "client",
    "is_active": true,
    "email_verified": true
  }
}
```

## Troubleshooting

### Common Issues

1. **Database Connection Error**
   - Check DATABASE_URL in .env
   - Ensure PostgreSQL is running
   - Verify database exists

2. **JWT Token Errors**
   - Check JWT_SECRET_KEY in .env
   - Ensure tokens are not expired
   - Verify token format

3. **CORS Errors**
   - Check ALLOWED_ORIGINS in settings
   - Ensure frontend URL is included

4. **Rate Limiting**
   - Wait for lockout period to expire
   - Check IP address restrictions

### Debug Mode

Enable debug mode for development:

```bash
DEBUG=True
```

This will provide detailed error messages and logging.

## Production Deployment

### Security Checklist

- [ ] Change all default passwords
- [ ] Update JWT_SECRET_KEY
- [ ] Set DEBUG=False
- [ ] Configure HTTPS
- [ ] Set up proper CORS origins
- [ ] Enable rate limiting
- [ ] Configure audit logging
- [ ] Set up monitoring

### Environment Variables

```bash
ENVIRONMENT=production
DEBUG=False
JWT_SECRET_KEY=<strong-random-key>
DATABASE_URL=<production-database-url>
```

## Support

For issues or questions:

1. Check the logs in `logs/app.log`
2. Review audit logs in the database
3. Check browser console for frontend errors
4. Verify environment configuration

## Changelog

### Version 1.0.0
- Initial authentication system implementation
- JWT token authentication
- Role-based access control
- Rate limiting
- Audit logging
- Modern UI components
