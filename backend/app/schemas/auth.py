"""
Authentication schemas for LemonNPie Backend API
"""
from typing import Optional
from uuid import UUID
from datetime import datetime

from pydantic import BaseModel, EmailStr, Field, validator
from app.models.enums import UserRole


class UserRegistration(BaseModel):
    """Schema for user registration"""
    email: EmailStr = Field(
        ..., 
        description="Valid email address (must be unique)",
        example="john.doe@example.com"
    )
    password: str = Field(
        ..., 
        min_length=8, 
        max_length=100,
        description="Strong password with uppercase, lowercase, digit, and special character",
        example="SecurePass123!"
    )
    name: str = Field(
        ..., 
        min_length=2, 
        max_length=255,
        description="Full name (letters, spaces, hyphens, apostrophes only)",
        example="John Doe"
    )
    bio: Optional[str] = Field(
        None, 
        max_length=1000,
        description="Optional user biography or description",
        example="Movie enthusiast and Nollywood fan from Lagos"
    )
    location: Optional[str] = Field(
        None, 
        max_length=255,
        description="Optional user location",
        example="Lagos, Nigeria"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "email": "john.doe@example.com",
                "password": "SecurePass123!",
                "name": "John Doe",
                "bio": "Movie enthusiast and Nollywood fan",
                "location": "Lagos, Nigeria"
            }
        }
    
    @validator('password')
    def validate_password(cls, v):
        """Validate password strength"""
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        
        # Check for at least one uppercase, one lowercase, and one digit
        has_upper = any(c.isupper() for c in v)
        has_lower = any(c.islower() for c in v)
        has_digit = any(c.isdigit() for c in v)
        
        if not (has_upper and has_lower and has_digit):
            raise ValueError('Password must contain at least one uppercase letter, one lowercase letter, and one digit')
        
        return v
    
    @validator('name')
    def validate_name(cls, v):
        """Validate name format"""
        if not v.strip():
            raise ValueError('Name cannot be empty')
        
        # Check for valid characters (letters, spaces, hyphens, apostrophes)
        import re
        if not re.match(r"^[a-zA-Z\s\-']+$", v):
            raise ValueError('Name can only contain letters, spaces, hyphens, and apostrophes')
        
        return v.strip()


class UserLogin(BaseModel):
    """Schema for user login"""
    email: EmailStr = Field(
        ...,
        description="Registered email address",
        example="john.doe@example.com"
    )
    password: str = Field(
        ...,
        description="User password",
        example="SecurePass123!"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "email": "john.doe@example.com",
                "password": "SecurePass123!"
            }
        }


class TokenResponse(BaseModel):
    """Schema for token response"""
    access_token: str = Field(
        ...,
        description="JWT access token for API authentication",
        example="eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiYWRtaW4iOnRydWV9.TJVA95OrM7E2cBab30RMHrHDcEfxjoYZgeFONFh7HgQ"
    )
    refresh_token: str = Field(
        ...,
        description="JWT refresh token for obtaining new access tokens",
        example="eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiYWRtaW4iOnRydWV9.TJVA95OrM7E2cBab30RMHrHDcEfxjoYZgeFONFh7HgQ"
    )
    token_type: str = Field(
        default="bearer",
        description="Token type (always 'bearer')",
        example="bearer"
    )
    expires_in: int = Field(
        ...,
        description="Access token expiration time in seconds",
        example=1800
    )
    
    class Config:
        schema_extra = {
            "example": {
                "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
                "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
                "token_type": "bearer",
                "expires_in": 1800
            }
        }


class TokenRefresh(BaseModel):
    """Schema for token refresh"""
    refresh_token: str


class PasswordResetRequest(BaseModel):
    """Schema for password reset request"""
    email: EmailStr


class PasswordReset(BaseModel):
    """Schema for password reset"""
    token: str
    new_password: str = Field(..., min_length=8, max_length=100)
    
    @validator('new_password')
    def validate_password(cls, v):
        """Validate password strength"""
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        
        # Check for at least one uppercase, one lowercase, and one digit
        has_upper = any(c.isupper() for c in v)
        has_lower = any(c.islower() for c in v)
        has_digit = any(c.isdigit() for c in v)
        
        if not (has_upper and has_lower and has_digit):
            raise ValueError('Password must contain at least one uppercase letter, one lowercase letter, and one digit')
        
        return v


class EmailVerification(BaseModel):
    """Schema for email verification"""
    token: str


class UserResponse(BaseModel):
    """Schema for user response"""
    id: UUID
    email: EmailStr
    name: str
    bio: Optional[str] = None
    location: Optional[str] = None
    avatar_url: Optional[str] = None
    role: UserRole
    is_verified: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


class AuthResponse(BaseModel):
    """Schema for authentication response"""
    user: UserResponse = Field(
        ...,
        description="User information"
    )
    tokens: TokenResponse = Field(
        ...,
        description="Authentication tokens"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "user": {
                    "id": "123e4567-e89b-12d3-a456-426614174000",
                    "email": "john.doe@example.com",
                    "name": "John Doe",
                    "bio": "Movie enthusiast and Nollywood fan",
                    "location": "Lagos, Nigeria",
                    "avatar_url": None,
                    "role": "user",
                    "is_verified": False,
                    "created_at": "2024-01-01T00:00:00Z"
                },
                "tokens": {
                    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
                    "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
                    "token_type": "bearer",
                    "expires_in": 1800
                }
            }
        }