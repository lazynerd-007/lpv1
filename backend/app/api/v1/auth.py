"""
Authentication API routes
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.auth.auth_service import auth_service
from app.auth.dependencies import get_current_user
from app.schemas.auth import (
    UserRegistration, 
    UserLogin, 
    TokenResponse, 
    TokenRefresh,
    PasswordResetRequest,
    PasswordReset,
    EmailVerification,
    AuthResponse,
    UserResponse
)
from app.models.user import User


router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=AuthResponse, status_code=status.HTTP_201_CREATED)
async def register(
    user_data: UserRegistration,
    db: AsyncSession = Depends(get_db)
):
    """
    Register a new user account
    
    - **email**: Valid email address (must be unique)
    - **password**: Strong password (min 8 chars, uppercase, lowercase, digit)
    - **name**: Full name (2-255 characters)
    - **bio**: Optional user biography
    - **location**: Optional user location
    
    Returns user information and authentication tokens.
    """
    return await auth_service.register_user(user_data, db)


@router.post("/login", response_model=AuthResponse)
async def login(
    login_data: UserLogin,
    db: AsyncSession = Depends(get_db)
):
    """
    Authenticate user and return access tokens
    
    - **email**: User's email address
    - **password**: User's password
    
    Returns user information and authentication tokens.
    Account will be locked after 5 failed attempts for 30 minutes.
    """
    return await auth_service.authenticate_user(login_data, db)


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(
    token_data: TokenRefresh,
    db: AsyncSession = Depends(get_db)
):
    """
    Refresh access token using refresh token
    
    - **refresh_token**: Valid refresh token
    
    Returns new access token with same refresh token.
    """
    return await auth_service.refresh_token(token_data.refresh_token, db)


@router.post("/logout")
async def logout(
    current_user: User = Depends(get_current_user)
):
    """
    Logout current user
    
    In a production system, this would invalidate the tokens.
    For now, clients should discard tokens locally.
    """
    return {"message": "Successfully logged out"}


@router.post("/forgot-password")
async def forgot_password(
    request_data: PasswordResetRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Request password reset
    
    - **email**: Email address to send reset link to
    
    Sends password reset email if account exists.
    """
    token = await auth_service.generate_password_reset_token(request_data.email, db)
    
    # In production, this would send an email and not return the token
    return {
        "message": "If the email exists, a password reset link has been sent",
        "token": token  # Remove this in production
    }


@router.post("/reset-password")
async def reset_password(
    reset_data: PasswordReset,
    db: AsyncSession = Depends(get_db)
):
    """
    Reset password using token
    
    - **token**: Password reset token from email
    - **new_password**: New strong password
    
    Resets user password if token is valid.
    """
    success = await auth_service.reset_password(
        reset_data.token, 
        reset_data.new_password, 
        db
    )
    
    if success:
        return {"message": "Password successfully reset"}
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired token"
        )


@router.get("/verify-email/{token}")
async def verify_email(
    token: str,
    db: AsyncSession = Depends(get_db)
):
    """
    Verify email address using token
    
    - **token**: Email verification token from registration email
    
    Marks user email as verified if token is valid.
    """
    success = await auth_service.verify_email(token, db)
    
    if success:
        return {"message": "Email successfully verified"}
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired token"
        )


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: User = Depends(get_current_user)
):
    """
    Get current user information
    
    Returns the authenticated user's profile information.
    """
    return UserResponse.from_orm(current_user)