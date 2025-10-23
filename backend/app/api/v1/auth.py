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


@router.post(
    "/register", 
    response_model=AuthResponse, 
    status_code=status.HTTP_201_CREATED,
    summary="Register new user account",
    description="Create a new user account with email verification",
    responses={
        201: {
            "description": "User successfully registered",
            "content": {
                "application/json": {
                    "example": {
                        "user": {
                            "id": "123e4567-e89b-12d3-a456-426614174000",
                            "email": "user@example.com",
                            "name": "John Doe",
                            "bio": "Movie enthusiast and Nollywood fan",
                            "location": "Lagos, Nigeria",
                            "role": "user",
                            "is_verified": False,
                            "created_at": "2024-01-01T00:00:00Z"
                        },
                        "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
                        "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
                        "token_type": "bearer",
                        "expires_in": 1800
                    }
                }
            }
        },
        400: {
            "description": "Validation error or email already exists",
            "content": {
                "application/json": {
                    "example": {
                        "error": "validation_error",
                        "message": "Email already registered",
                        "details": {"email": "This email is already in use"},
                        "timestamp": "2024-01-01T00:00:00Z",
                        "path": "/api/v1/auth/register"
                    }
                }
            }
        }
    }
)
async def register(
    user_data: UserRegistration,
    db: AsyncSession = Depends(get_db)
):
    """
    Register a new user account
    
    Creates a new user account with the provided information. The user will receive
    an email verification link to activate their account.
    
    **Password Requirements:**
    - Minimum 8 characters
    - At least one uppercase letter
    - At least one lowercase letter  
    - At least one digit
    - At least one special character
    
    **Email Requirements:**
    - Valid email format
    - Must be unique (not already registered)
    
    **Name Requirements:**
    - 2-255 characters
    - No special characters except spaces, hyphens, and apostrophes
    
    **Rate Limiting:** 5 requests per minute per IP address
    """
    return await auth_service.register_user(user_data, db)


@router.post(
    "/login", 
    response_model=AuthResponse,
    summary="Authenticate user",
    description="Login with email and password to receive authentication tokens",
    responses={
        200: {
            "description": "Successfully authenticated",
            "content": {
                "application/json": {
                    "example": {
                        "user": {
                            "id": "123e4567-e89b-12d3-a456-426614174000",
                            "email": "user@example.com",
                            "name": "John Doe",
                            "role": "user",
                            "is_verified": True
                        },
                        "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
                        "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
                        "token_type": "bearer",
                        "expires_in": 1800
                    }
                }
            }
        },
        401: {
            "description": "Invalid credentials",
            "content": {
                "application/json": {
                    "example": {
                        "error": "authentication_error",
                        "message": "Invalid email or password",
                        "timestamp": "2024-01-01T00:00:00Z",
                        "path": "/api/v1/auth/login"
                    }
                }
            }
        },
        423: {
            "description": "Account locked due to too many failed attempts",
            "content": {
                "application/json": {
                    "example": {
                        "error": "account_locked",
                        "message": "Account locked due to too many failed login attempts. Try again in 30 minutes.",
                        "details": {"locked_until": "2024-01-01T01:00:00Z"},
                        "timestamp": "2024-01-01T00:00:00Z",
                        "path": "/api/v1/auth/login"
                    }
                }
            }
        }
    }
)
async def login(
    login_data: UserLogin,
    db: AsyncSession = Depends(get_db)
):
    """
    Authenticate user and return access tokens
    
    Validates user credentials and returns JWT tokens for API access.
    
    **Security Features:**
    - Account lockout after 5 failed attempts (30 minutes)
    - Rate limiting: 10 requests per minute per IP
    - Secure password hashing with bcrypt
    - JWT tokens with configurable expiration
    
    **Token Information:**
    - **Access Token**: Used for API authentication (30 minutes default)
    - **Refresh Token**: Used to obtain new access tokens (7 days default)
    
    **Usage:**
    Include the access token in the Authorization header for subsequent requests:
    ```
    Authorization: Bearer <access_token>
    ```
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