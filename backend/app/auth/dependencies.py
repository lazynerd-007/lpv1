"""
Authentication dependencies for FastAPI endpoints
"""
from typing import Optional
from uuid import UUID

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.jwt_service import jwt_service
from app.db.database import get_db
from app.models.user import User
from app.models.enums import UserRole
from sqlalchemy import select


# HTTP Bearer token scheme
security = HTTPBearer()
optional_security = HTTPBearer(auto_error=False)


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db)
) -> User:
    """
    Dependency to get the current authenticated user
    """
    token = credentials.credentials
    
    # Verify token and extract user ID
    user_id = jwt_service.get_user_id_from_token(token)
    
    # Fetch user from database
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Inactive user",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return user


async def get_current_active_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """
    Dependency to get the current active user
    """
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    return current_user


async def get_optional_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(optional_security),
    db: AsyncSession = Depends(get_db)
) -> Optional[User]:
    """
    Dependency to optionally get the current user (for endpoints that work with or without auth)
    """
    if credentials is None:
        return None
    
    try:
        token = credentials.credentials
        user_id = jwt_service.get_user_id_from_token(token)
        
        result = await db.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()
        
        if user and user.is_active:
            return user
    except HTTPException:
        pass
    
    return None


def require_role(required_role: UserRole):
    """
    Dependency factory to require a specific user role
    """
    async def role_checker(current_user: User = Depends(get_current_user)) -> User:
        # Define role hierarchy
        role_hierarchy = {
            UserRole.USER: 0,
            UserRole.CRITIC: 1,
            UserRole.MODERATOR: 2,
            UserRole.ADMIN: 3
        }
        
        user_role_level = role_hierarchy.get(current_user.role, 0)
        required_role_level = role_hierarchy.get(required_role, 0)
        
        if user_role_level < required_role_level:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Insufficient permissions. Required role: {required_role.value}"
            )
        
        return current_user
    
    return role_checker


def require_roles(*allowed_roles: UserRole):
    """
    Dependency factory to require one of multiple roles
    """
    async def roles_checker(current_user: User = Depends(get_current_user)) -> User:
        if current_user.role not in allowed_roles:
            allowed_roles_str = ", ".join([role.value for role in allowed_roles])
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Insufficient permissions. Allowed roles: {allowed_roles_str}"
            )
        
        return current_user
    
    return roles_checker


# Common role dependencies
require_admin = require_role(UserRole.ADMIN)
require_moderator = require_role(UserRole.MODERATOR)
require_critic = require_role(UserRole.CRITIC)
require_moderator_or_admin = require_roles(UserRole.MODERATOR, UserRole.ADMIN)

# Convenience function for admin users
async def get_current_admin_user(current_user: User = Depends(require_admin)) -> User:
    """
    Get current user and ensure they have admin role
    """
    return current_user