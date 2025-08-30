"""
Authentication routes for login, register, logout, and password management
"""

from fastapi import APIRouter, HTTPException, Depends, Request, status
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from typing import Optional, Dict, Any
import logging
from datetime import datetime, timedelta

from .database import get_db
from .models import User, UserSession, AuditLog
from .utils import (
    hash_password, verify_password, generate_access_token, generate_refresh_token,
    generate_session_token, validate_email_address, validate_password_strength,
    generate_secure_token, sanitize_input
)
from .middleware import rate_limit, log_audit_event
from .rate_limiter import rate_limiter

logger = logging.getLogger(__name__)

# Create router
router = APIRouter(prefix="/auth", tags=["authentication"])

# Security scheme
security = HTTPBearer()

# Pydantic models for request/response
class UserRegister(BaseModel):
    email: EmailStr
    password: str
    first_name: str
    last_name: str
    role: str = "client"

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int
    user: Dict[str, Any]

class PasswordResetRequest(BaseModel):
    email: EmailStr

class PasswordReset(BaseModel):
    token: str
    new_password: str

class PasswordChange(BaseModel):
    current_password: str
    new_password: str

class UserProfile(BaseModel):
    id: int
    email: str
    first_name: str
    last_name: str
    role: str
    is_active: bool
    email_verified: bool
    created_at: Optional[datetime] = None

@router.post("/register", response_model=TokenResponse)
async def register(
    user_data: UserRegister,
    request: Request,
    db: Session = Depends(get_db)
):
    """
    Register a new user
    """
    try:
        # Rate limiting
        client_ip = request.client.host
        if not rate_limiter.is_ip_allowed(client_ip, request.headers.get("user-agent", "")):
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Too many registration attempts. Please try again later."
            )
        
        # Validate email
        if not validate_email_address(user_data.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid email address"
            )
        
        # Check if user already exists
        existing_user = db.query(User).filter(User.email == user_data.email).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        # Validate password strength
        password_validation = validate_password_strength(user_data.password)
        if not password_validation["is_valid"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Password validation failed: {'; '.join(password_validation['errors'])}"
            )
        
        # Validate role
        valid_roles = ["agent", "employee", "admin"]
        if user_data.role not in valid_roles:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid role. Must be one of: {', '.join(valid_roles)}"
            )
        
        # Sanitize input
        first_name = sanitize_input(user_data.first_name)
        last_name = sanitize_input(user_data.last_name)
        
        # Create new user
        hashed_password = hash_password(user_data.password)
        new_user = User(
            email=user_data.email.lower(),
            password_hash=hashed_password,
            first_name=first_name,
            last_name=last_name,
            role=user_data.role,
            is_active=True,
            email_verified=False,  # Will be verified via email
            created_at=datetime.utcnow()
        )
        
        db.add(new_user)
        db.flush()  # Get the user ID
        
        # Generate tokens
        access_token = generate_access_token(new_user.id, new_user.email, new_user.role)
        refresh_token = generate_refresh_token(new_user.id)
        session_token = generate_session_token()
        
        # Create user session
        session = UserSession(
            user_id=new_user.id,
            session_token=access_token,
            refresh_token=refresh_token,
            ip_address=client_ip,
            user_agent=request.headers.get("user-agent"),
            expires_at=datetime.utcnow() + timedelta(minutes=30),  # 30 minutes
            created_at=datetime.utcnow()
        )
        
        db.add(session)
        db.commit()
        
        # Log audit event
        audit_log = AuditLog(
            user_id=new_user.id,
            event_type="user_registration",
            event_data=f"User registered with role: {new_user.role}",
            ip_address=client_ip,
            user_agent=request.headers.get("user-agent"),
            success=True
        )
        db.add(audit_log)
        db.commit()
        
        # Return response
        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            expires_in=30 * 60,  # 30 minutes in seconds
            user={
                "id": new_user.id,
                "email": new_user.email,
                "first_name": new_user.first_name,
                "last_name": new_user.last_name,
                "role": new_user.role,
                "is_active": new_user.is_active,
                "email_verified": new_user.email_verified
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Registration error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Registration failed"
        )

@router.post("/login", response_model=TokenResponse)
async def login(
    user_data: UserLogin,
    request: Request,
    db: Session = Depends(get_db)
):
    """
    Login user
    """
    try:
        client_ip = request.client.host
        user_agent = request.headers.get("user-agent", "")
        
        # Check if IP is locked out
        if rate_limiter._is_ip_locked_out(client_ip):
            lockout_time = rate_limiter.get_lockout_time_remaining(client_ip)
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail=f"Account temporarily locked. Try again in {lockout_time} seconds."
            )
        
        # Rate limiting for login attempts
        if not rate_limiter.is_ip_allowed(client_ip, user_agent):  # Rate limiting
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Too many login attempts. Please try again later."
            )
        
        # Find user
        user = db.query(User).filter(User.email == user_data.email.lower()).first()
        if not user:
            # Record failed attempt
            rate_limiter.record_failed_login(client_ip)
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )
        
        # Check if user is active
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Account is disabled"
            )
        
        # Check if user is locked
        if user.is_locked:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Account is locked"
            )
        
        # Verify password
        if not verify_password(user_data.password, user.password_hash):
            # Record failed attempt
            rate_limiter.record_failed_login(client_ip)
            
            # Update user's failed login attempts
            user.failed_login_attempts += 1
            if user.failed_login_attempts >= 5:
                user.locked_until = datetime.utcnow() + timedelta(minutes=15)
            
            db.commit()
            
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )
        
        # Clear failed login attempts on successful login
        rate_limiter.record_successful_login(client_ip)
        user.failed_login_attempts = 0
        user.locked_until = None
        user.last_login = datetime.utcnow()
        
        # Generate tokens
        access_token = generate_access_token(user.id, user.email, user.role)
        refresh_token = generate_refresh_token(user.id)
        
        # Create or update session
        existing_session = db.query(UserSession).filter(
            UserSession.user_id == user.id,
            UserSession.is_active == True
        ).first()
        
        if existing_session:
            existing_session.is_active = False
        
        session = UserSession(
            user_id=user.id,
            session_token=access_token,
            refresh_token=refresh_token,
            ip_address=client_ip,
            user_agent=user_agent,
            expires_at=datetime.utcnow() + timedelta(minutes=30),
            created_at=datetime.utcnow()
        )
        
        db.add(session)
        db.commit()
        
        # Log audit event
        audit_log = AuditLog(
            user_id=user.id,
            event_type="user_login",
            event_data="User logged in successfully",
            ip_address=client_ip,
            user_agent=user_agent,
            success=True
        )
        db.add(audit_log)
        db.commit()
        
        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            expires_in=30 * 60,
            user={
                "id": user.id,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "role": user.role,
                "is_active": user.is_active,
                "email_verified": user.email_verified
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Login error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Login failed"
        )

@router.post("/logout")
async def logout(
    request: Request,
    db: Session = Depends(get_db)
):
    """
    Logout user (invalidate session)
    """
    try:
        # Get token from Authorization header
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authorization header"
            )
        
        token = auth_header.split(" ")[1]
        
        # Find and invalidate session
        session = db.query(UserSession).filter(
            UserSession.session_token == token,
            UserSession.is_active == True
        ).first()
        
        if session:
            session.is_active = False
            db.commit()
            
            # Log audit event
            audit_log = AuditLog(
                user_id=session.user_id,
                event_type="user_logout",
                event_data="User logged out",
                ip_address=request.client.host,
                user_agent=request.headers.get("user-agent"),
                success=True
            )
            db.add(audit_log)
            db.commit()
        
        return {"message": "Logged out successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Logout error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Logout failed"
        )

@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(
    request: Request,
    db: Session = Depends(get_db)
):
    """
    Refresh access token using refresh token
    """
    try:
        # Get refresh token from request body
        body = await request.json()
        refresh_token = body.get("refresh_token")
        
        if not refresh_token:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Refresh token required"
            )
        
        # Verify refresh token
        from .utils import verify_jwt_token
        payload = verify_jwt_token(refresh_token)
        if not payload or payload.get("type") != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token"
            )
        
        user_id = int(payload.get("sub"))
        
        # Find user session
        session = db.query(UserSession).filter(
            UserSession.user_id == user_id,
            UserSession.refresh_token == refresh_token,
            UserSession.is_active == True
        ).first()
        
        if not session or session.is_expired:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired refresh token"
            )
        
        # Get user
        user = db.query(User).filter(User.id == user_id).first()
        if not user or not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found or inactive"
            )
        
        # Generate new tokens
        new_access_token = generate_access_token(user.id, user.email, user.role)
        new_refresh_token = generate_refresh_token(user.id)
        
        # Update session
        session.session_token = new_access_token
        session.refresh_token = new_refresh_token
        session.expires_at = datetime.utcnow() + timedelta(minutes=30)
        session.last_used = datetime.utcnow()
        
        db.commit()
        
        return TokenResponse(
            access_token=new_access_token,
            refresh_token=new_refresh_token,
            expires_in=30 * 60,
            user={
                "id": user.id,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "role": user.role,
                "is_active": user.is_active,
                "email_verified": user.email_verified
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Token refresh error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Token refresh failed"
        )

@router.post("/forgot-password")
async def forgot_password(
    password_data: PasswordResetRequest,
    request: Request,
    db: Session = Depends(get_db)
):
    """
    Request password reset
    """
    try:
        # Rate limiting
        client_ip = request.client.host
        if not rate_limiter.is_ip_allowed(client_ip, request.headers.get("user-agent", "")):  # Rate limiting
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Too many password reset requests. Please try again later."
            )
        
        # Find user
        user = db.query(User).filter(User.email == password_data.email.lower()).first()
        if not user:
            # Don't reveal if user exists or not
            return {"message": "If the email exists, a password reset link has been sent"}
        
        # Generate reset token
        reset_token = generate_secure_token(32)
        user.password_reset_token = reset_token
        user.password_reset_expires = datetime.utcnow() + timedelta(hours=1)
        
        db.commit()
        
        # TODO: Send email with reset link
        # For now, just log the token (in production, send email)
        logger.info(f"Password reset token for {user.email}: {reset_token}")
        
        # Log audit event
        audit_log = AuditLog(
            user_id=user.id,
            event_type="password_reset_requested",
            event_data="Password reset requested",
            ip_address=client_ip,
            user_agent=request.headers.get("user-agent"),
            success=True
        )
        db.add(audit_log)
        db.commit()
        
        return {"message": "If the email exists, a password reset link has been sent"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Forgot password error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Password reset request failed"
        )

@router.post("/reset-password")
async def reset_password(
    password_data: PasswordReset,
    request: Request,
    db: Session = Depends(get_db)
):
    """
    Reset password using token
    """
    try:
        # Find user with valid reset token
        user = db.query(User).filter(
            User.password_reset_token == password_data.token,
            User.password_reset_expires > datetime.utcnow()
        ).first()
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid or expired reset token"
            )
        
        # Validate new password
        password_validation = validate_password_strength(password_data.new_password)
        if not password_validation["is_valid"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Password validation failed: {'; '.join(password_validation['errors'])}"
            )
        
        # Update password
        user.password_hash = hash_password(password_data.new_password)
        user.password_reset_token = None
        user.password_reset_expires = None
        user.failed_login_attempts = 0
        user.locked_until = None
        
        # Invalidate all sessions
        db.query(UserSession).filter(UserSession.user_id == user.id).update({
            UserSession.is_active: False
        })
        
        db.commit()
        
        # Log audit event
        audit_log = AuditLog(
            user_id=user.id,
            event_type="password_reset_completed",
            event_data="Password reset completed",
            ip_address=request.client.host,
            user_agent=request.headers.get("user-agent"),
            success=True
        )
        db.add(audit_log)
        db.commit()
        
        return {"message": "Password reset successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Reset password error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Password reset failed"
        )

@router.get("/me", response_model=UserProfile)
async def get_current_user_profile(
    request: Request,
    db: Session = Depends(get_db)
):
    """
    Get current user profile
    """
    try:
        # Get token from Authorization header
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authorization header"
            )
        
        token = auth_header.split(" ")[1]
        
        # Verify token and get user
        from .utils import verify_jwt_token
        payload = verify_jwt_token(token)
        if not payload:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )
        
        user_id = int(payload.get("sub"))
        user = db.query(User).filter(User.id == user_id).first()
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found"
            )
        
        return UserProfile(
            id=user.id,
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
            role=user.role,
            is_active=user.is_active,
            email_verified=user.email_verified,
            created_at=user.created_at
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Get profile error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get user profile"
        )
