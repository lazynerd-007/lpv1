"""
Permission decorators and utilities for role-based access control
"""
from functools import wraps
from typing import List, Callable, Any
from fastapi import HTTPException, status

from app.models.enums import UserRole
from app.models.user import User


class PermissionChecker:
    """Utility class for checking user permissions"""
    
    @staticmethod
    def has_role(user: User, required_role: UserRole) -> bool:
        """Check if user has the required role or higher"""
        role_hierarchy = {
            UserRole.USER: 0,
            UserRole.CRITIC: 1,
            UserRole.MODERATOR: 2,
            UserRole.ADMIN: 3
        }
        
        user_level = role_hierarchy.get(user.role, 0)
        required_level = role_hierarchy.get(required_role, 0)
        
        return user_level >= required_level
    
    @staticmethod
    def has_any_role(user: User, allowed_roles: List[UserRole]) -> bool:
        """Check if user has any of the allowed roles"""
        return user.role in allowed_roles
    
    @staticmethod
    def can_modify_user(current_user: User, target_user: User) -> bool:
        """Check if current user can modify target user"""
        # Users can modify themselves
        if current_user.id == target_user.id:
            return True
        
        # Admins can modify anyone
        if current_user.role == UserRole.ADMIN:
            return True
        
        # Moderators can modify users and critics (but not other moderators or admins)
        if current_user.role == UserRole.MODERATOR:
            return target_user.role in [UserRole.USER, UserRole.CRITIC]
        
        return False
    
    @staticmethod
    def can_moderate_content(user: User) -> bool:
        """Check if user can moderate content"""
        return user.role in [UserRole.MODERATOR, UserRole.ADMIN]
    
    @staticmethod
    def can_access_admin_panel(user: User) -> bool:
        """Check if user can access admin panel"""
        return user.role in [UserRole.MODERATOR, UserRole.ADMIN]
    
    @staticmethod
    def can_manage_users(user: User) -> bool:
        """Check if user can manage other users"""
        return user.role == UserRole.ADMIN
    
    @staticmethod
    def can_write_featured_reviews(user: User) -> bool:
        """Check if user can write featured reviews"""
        return user.role in [UserRole.CRITIC, UserRole.MODERATOR, UserRole.ADMIN]


def require_permission(permission_func: Callable[[User], bool]):
    """
    Decorator to require a specific permission
    
    Args:
        permission_func: Function that takes a User and returns bool
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Extract current_user from kwargs (assumes it's passed as dependency)
            current_user = kwargs.get('current_user')
            if not current_user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Authentication required"
                )
            
            if not permission_func(current_user):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Insufficient permissions"
                )
            
            return await func(*args, **kwargs)
        return wrapper
    return decorator


def require_self_or_admin(target_user_id_param: str = "user_id"):
    """
    Decorator to require user to be accessing their own resource or be an admin
    
    Args:
        target_user_id_param: Name of the parameter containing the target user ID
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            current_user = kwargs.get('current_user')
            if not current_user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Authentication required"
                )
            
            target_user_id = kwargs.get(target_user_id_param)
            if not target_user_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Missing {target_user_id_param} parameter"
                )
            
            # Allow if user is accessing their own resource or is admin
            if str(current_user.id) != str(target_user_id) and current_user.role != UserRole.ADMIN:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Can only access your own resources"
                )
            
            return await func(*args, **kwargs)
        return wrapper
    return decorator


def require_content_ownership_or_moderator(content_user_id_param: str = "content_user_id"):
    """
    Decorator to require user to own the content or be a moderator/admin
    
    Args:
        content_user_id_param: Name of the parameter containing the content owner's user ID
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            current_user = kwargs.get('current_user')
            if not current_user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Authentication required"
                )
            
            content_user_id = kwargs.get(content_user_id_param)
            if not content_user_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Missing {content_user_id_param} parameter"
                )
            
            # Allow if user owns the content or is moderator/admin
            is_owner = str(current_user.id) == str(content_user_id)
            is_moderator = current_user.role in [UserRole.MODERATOR, UserRole.ADMIN]
            
            if not (is_owner or is_moderator):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Can only modify your own content or need moderator privileges"
                )
            
            return await func(*args, **kwargs)
        return wrapper
    return decorator


# Common permission decorators
require_admin = require_permission(lambda user: user.role == UserRole.ADMIN)
require_moderator = require_permission(lambda user: user.role in [UserRole.MODERATOR, UserRole.ADMIN])
require_critic = require_permission(lambda user: user.role in [UserRole.CRITIC, UserRole.MODERATOR, UserRole.ADMIN])
require_verified = require_permission(lambda user: user.is_verified)
require_active = require_permission(lambda user: user.is_active)