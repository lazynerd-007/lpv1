"""
Authentication service for user registration, login, and password management
"""
from datetime import datetime, timedelta
from typing import Optional, Tuple
from uuid import UUID
import secrets
import hashlib

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from fastapi import HTTPException, status

from app.models.user import User
from app.models.enums import UserRole
from app.auth.jwt_service import jwt_service
from app.schemas.auth import UserRegistration, UserLogin, TokenResponse, AuthResponse, UserResponse
from app.core.config import settings


class AuthService:
    """Service for handling authentication operations"""
    
    def __init__(self):
        self.max_login_attempts = 5
        self.lockout_duration_minutes = 30
    
    async def register_user(
        self, 
        user_data: UserRegistration, 
        db: AsyncSession
    ) -> AuthResponse:
        """Register a new user"""
        
        # Check if user already exists
        result = await db.execute(
            select(User).where(User.email == user_data.email)
        )
        existing_user = result.scalar_one_or_none()
        
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User with this email already exists"
            )
        
        # Hash password
        password_hash = jwt_service.hash_password(user_data.password)
        
        # Create new user
        new_user = User(
            email=user_data.email,
            password_hash=password_hash,
            name=user_data.name,
            bio=user_data.bio,
            location=user_data.location,
            role=UserRole.USER,
            is_active=True,
            is_verified=False  # Email verification required
        )
        
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)
        
        # Generate tokens
        access_token = jwt_service.create_access_token(
            user_id=new_user.id,
            email=new_user.email,
            role=new_user.role
        )
        
        refresh_token = jwt_service.create_refresh_token(
            user_id=new_user.id,
            email=new_user.email
        )
        
        tokens = TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
        )
        
        user_response = UserResponse.from_orm(new_user)
        
        return AuthResponse(user=user_response, tokens=tokens)
    
    async def authenticate_user(
        self, 
        login_data: UserLogin, 
        db: AsyncSession
    ) -> AuthResponse:
        """Authenticate user and return tokens"""
        
        # Get user by email
        result = await db.execute(
            select(User).where(User.email == login_data.email)
        )
        user = result.scalar_one_or_none()
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )
        
        # Check if user is locked out
        if user.locked_until and user.locked_until > datetime.utcnow():
            remaining_time = user.locked_until - datetime.utcnow()
            raise HTTPException(
                status_code=status.HTTP_423_LOCKED,
                detail=f"Account locked. Try again in {remaining_time.seconds // 60} minutes"
            )
        
        # Verify password
        if not jwt_service.verify_password(login_data.password, user.password_hash):
            # Increment login attempts
            await self._handle_failed_login(user, db)
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )
        
        # Check if user is active
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Account is deactivated"
            )
        
        # Reset login attempts on successful login
        if user.login_attempts > 0:
            await db.execute(
                update(User)
                .where(User.id == user.id)
                .values(login_attempts=0, locked_until=None)
            )
            await db.commit()
        
        # Generate tokens
        access_token = jwt_service.create_access_token(
            user_id=user.id,
            email=user.email,
            role=user.role
        )
        
        refresh_token = jwt_service.create_refresh_token(
            user_id=user.id,
            email=user.email
        )
        
        tokens = TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
        )
        
        user_response = UserResponse.from_orm(user)
        
        return AuthResponse(user=user_response, tokens=tokens)
    
    async def refresh_token(
        self, 
        refresh_token: str, 
        db: AsyncSession
    ) -> TokenResponse:
        """Refresh access token using refresh token"""
        
        # Verify refresh token
        payload = jwt_service.verify_token(refresh_token)
        
        # Verify this is a refresh token
        token_type = payload.get("type")
        if token_type != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token type"
            )
        
        user_id_str = payload.get("sub")
        if not user_id_str:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token payload"
            )
        
        user_id = UUID(user_id_str)
        
        # Get user from database to ensure they're still active
        result = await db.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()
        
        if not user or not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found or inactive"
            )
        
        # Generate new access token
        access_token = jwt_service.create_access_token(
            user_id=user.id,
            email=user.email,
            role=user.role
        )
        
        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,  # Keep the same refresh token
            expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
        )
    
    async def generate_password_reset_token(
        self, 
        email: str, 
        db: AsyncSession
    ) -> str:
        """Generate password reset token"""
        
        # Check if user exists
        result = await db.execute(select(User).where(User.email == email))
        user = result.scalar_one_or_none()
        
        if not user:
            # Don't reveal if email exists or not for security
            raise HTTPException(
                status_code=status.HTTP_200_OK,
                detail="If the email exists, a password reset link has been sent"
            )
        
        # Generate secure token
        token = secrets.token_urlsafe(32)
        
        # In a real implementation, you would:
        # 1. Store the token in database with expiration
        # 2. Send email with reset link
        # For now, we'll return the token (in production, this would be sent via email)
        
        return token
    
    async def reset_password(
        self, 
        token: str, 
        new_password: str, 
        db: AsyncSession
    ) -> bool:
        """Reset user password using token"""
        
        # In a real implementation, you would:
        # 1. Verify token exists in database and is not expired
        # 2. Get associated user
        # 3. Update password
        # 4. Invalidate token
        
        # For now, we'll implement a basic version
        # This is a placeholder implementation
        
        raise HTTPException(
            status_code=status.HTTP_501_NOT_IMPLEMENTED,
            detail="Password reset functionality will be implemented with email service"
        )
    
    async def verify_email(
        self, 
        token: str, 
        db: AsyncSession
    ) -> bool:
        """Verify user email using token"""
        
        # In a real implementation, you would:
        # 1. Verify token exists in database and is not expired
        # 2. Get associated user
        # 3. Mark email as verified
        # 4. Invalidate token
        
        # For now, we'll implement a basic version
        # This is a placeholder implementation
        
        raise HTTPException(
            status_code=status.HTTP_501_NOT_IMPLEMENTED,
            detail="Email verification functionality will be implemented with email service"
        )
    
    async def _handle_failed_login(self, user: User, db: AsyncSession) -> None:
        """Handle failed login attempt"""
        
        new_attempts = user.login_attempts + 1
        locked_until = None
        
        if new_attempts >= self.max_login_attempts:
            locked_until = datetime.utcnow() + timedelta(minutes=self.lockout_duration_minutes)
        
        await db.execute(
            update(User)
            .where(User.id == user.id)
            .values(login_attempts=new_attempts, locked_until=locked_until)
        )
        await db.commit()


# Global instance
auth_service = AuthService()