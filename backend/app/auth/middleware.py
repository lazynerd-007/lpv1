"""
Authentication and authorization middleware
"""
from typing import Optional, List
from fastapi import Request, HTTPException, status
from fastapi.security.utils import get_authorization_scheme_param
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

from app.auth.jwt_service import jwt_service
from app.models.enums import UserRole


class AuthMiddleware(BaseHTTPMiddleware):
    """
    Middleware for handling authentication and authorization
    """
    
    def __init__(self, app, protected_paths: Optional[List[str]] = None):
        super().__init__(app)
        self.protected_paths = protected_paths or []
    
    async def dispatch(self, request: Request, call_next):
        """
        Process request and add user context if authenticated
        """
        # Extract token from Authorization header
        authorization = request.headers.get("Authorization")
        scheme, token = get_authorization_scheme_param(authorization)
        
        # Add user context to request state
        request.state.user = None
        request.state.user_id = None
        request.state.user_role = None
        
        if scheme.lower() == "bearer" and token:
            try:
                # Verify token and extract user info
                payload = jwt_service.verify_token(token)
                request.state.user_id = payload.get("sub")
                request.state.user_role = payload.get("role")
                request.state.token_payload = payload
            except HTTPException:
                # Invalid token - continue without user context
                pass
        
        response = await call_next(request)
        return response


class RoleBasedAccessMiddleware(BaseHTTPMiddleware):
    """
    Middleware for role-based access control on specific routes
    """
    
    def __init__(self, app, route_permissions: Optional[dict] = None):
        super().__init__(app)
        # Route permissions mapping: {"/path": ["role1", "role2"]}
        self.route_permissions = route_permissions or {}
    
    async def dispatch(self, request: Request, call_next):
        """
        Check if user has required role for the requested route
        """
        path = request.url.path
        method = request.method.lower()
        
        # Check if this route requires specific roles
        route_key = f"{method}:{path}"
        required_roles = self.route_permissions.get(route_key)
        
        if required_roles:
            user_role = getattr(request.state, 'user_role', None)
            
            if not user_role:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Authentication required"
                )
            
            if user_role not in required_roles:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Insufficient permissions. Required roles: {', '.join(required_roles)}"
                )
        
        response = await call_next(request)
        return response


def create_role_permissions_map() -> dict:
    """
    Create a mapping of routes to required roles
    """
    return {
        # Admin-only routes
        "get:/api/v1/admin/dashboard": [UserRole.ADMIN.value],
        "get:/api/v1/admin/users": [UserRole.ADMIN.value],
        "put:/api/v1/admin/users/{user_id}/role": [UserRole.ADMIN.value],
        "post:/api/v1/admin/users/{user_id}/suspend": [UserRole.ADMIN.value],
        "get:/api/v1/admin/analytics": [UserRole.ADMIN.value],
        
        # Moderator and Admin routes
        "get:/api/v1/admin/reports": [UserRole.MODERATOR.value, UserRole.ADMIN.value],
        "put:/api/v1/admin/reports/{report_id}/resolve": [UserRole.MODERATOR.value, UserRole.ADMIN.value],
        "get:/api/v1/admin/moderation": [UserRole.MODERATOR.value, UserRole.ADMIN.value],
        "post:/api/v1/admin/moderation/{content_id}": [UserRole.MODERATOR.value, UserRole.ADMIN.value],
        
        # Critic, Moderator, and Admin routes (enhanced review features)
        "post:/api/v1/reviews/featured": [UserRole.CRITIC.value, UserRole.MODERATOR.value, UserRole.ADMIN.value],
        
        # All authenticated users (examples)
        "post:/api/v1/reviews": ["user", "critic", "moderator", "admin"],
        "put:/api/v1/reviews/{review_id}": ["user", "critic", "moderator", "admin"],
        "delete:/api/v1/reviews/{review_id}": ["user", "critic", "moderator", "admin"],
    }