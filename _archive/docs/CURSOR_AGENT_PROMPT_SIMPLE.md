# 🔐 CURSOR AGENT: Implement Phase 1 Authentication & Security

You are a senior full-stack developer agent. Implement a complete authentication and security system for this Dubai Real Estate RAG Chat System.

## 🎯 MISSION
The current system has NO authentication - all endpoints are public. Implement enterprise-grade authentication and security as Phase 1 of production readiness.

## 📋 CURRENT PROJECT
- Backend: FastAPI + PostgreSQL + ChromaDB + Google Gemini AI
- Frontend: React + Material-UI
- Status: No authentication exists - all endpoints public

## 🚀 IMPLEMENTATION TASKS

### STEP 1: Create Authentication Backend (Priority 1)
Create these files in `backend/auth/`:

1. **`backend/auth/models.py`** - User, UserSession, Role, Permission models
2. **`backend/auth/utils.py`** - Password hashing (bcrypt), JWT tokens, validation
3. **`backend/auth/middleware.py`** - JWT auth, RBAC, rate limiting middleware
4. **`backend/auth/routes.py`** - Login, register, logout, refresh endpoints
5. **`backend/security/validators.py`** - Input validation, XSS protection
6. **`backend/security/rate_limiter.py`** - Rate limiting, IP blocking
7. **`backend/security/audit.py`** - Audit logging, security events

### STEP 2: Create Authentication Frontend (Priority 1)
Create these files in `frontend/src/auth/`:

1. **`frontend/src/auth/AuthContext.jsx`** - React auth context, token management
2. **`frontend/src/auth/LoginForm.jsx`** - Material-UI login form
3. **`frontend/src/auth/RegisterForm.jsx`** - Registration form with validation
4. **`frontend/src/auth/ProtectedRoute.jsx`** - Route protection component

### STEP 3: Update Existing Files (Priority 1)
1. **`backend/main.py`** - Add auth middleware, protect endpoints
2. **`backend/config/settings.py`** - Add JWT, security settings
3. **`frontend/src/App.js`** - Integrate auth context, protected routes
4. **`backend/requirements.txt`** - Add: bcrypt, PyJWT, email-validator, slowapi
5. **`frontend/package.json`** - Add: react-router-dom

### STEP 4: Database Schema (Priority 1)
Create migration for these tables:
- users (id, email, password_hash, role, is_active, created_at)
- user_sessions (id, user_id, session_token, refresh_token, expires_at)
- roles (id, name, description)
- permissions (id, name, description)
- role_permissions (role_id, permission_id)
- user_roles (user_id, role_id)

## 🔧 TECHNICAL REQUIREMENTS

### Dependencies to Add
```bash
# Backend
bcrypt==4.0.1
PyJWT==2.8.0
email-validator==2.0.0
slowapi==0.1.9

# Frontend
react-router-dom
```

### Environment Variables (.env)
```bash
JWT_SECRET_KEY=your-super-secret-jwt-key-change-in-production
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30
JWT_REFRESH_TOKEN_EXPIRE_DAYS=7
BCRYPT_ROUNDS=12
RATE_LIMIT_REQUESTS_PER_MINUTE=60
RATE_LIMIT_LOGIN_ATTEMPTS=5
```

## 🎯 API ENDPOINTS TO CREATE
- POST /auth/register - User registration
- POST /auth/login - User login with JWT
- POST /auth/logout - User logout
- POST /auth/refresh - Token refresh
- POST /auth/forgot-password - Password reset request
- POST /auth/reset-password - Password reset

## 🔒 SECURITY REQUIREMENTS
- bcrypt password hashing (12 rounds)
- JWT tokens with proper expiration
- Rate limiting on auth endpoints
- Input validation and sanitization
- Security headers (CORS, XSS protection)
- Role-based access control (client, agent, admin)
- Audit logging for security events

## 📊 SUCCESS CRITERIA
- [ ] All existing endpoints are protected
- [ ] Users can register and login
- [ ] JWT tokens work correctly
- [ ] Role-based access control functions
- [ ] Rate limiting prevents abuse
- [ ] Frontend auth flow works
- [ ] No security vulnerabilities

## 🚨 CRITICAL INSTRUCTIONS
1. **Start with database schema and models**
2. **Implement security first - never compromise**
3. **Test each component before moving to next**
4. **Add comprehensive error handling**
5. **Follow existing code patterns**
6. **Document everything clearly**

**BEGIN IMMEDIATELY: Start with database schema and work systematically through each component. Report progress after each major milestone.**
