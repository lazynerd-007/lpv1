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
            print(f"AUTH: Found bearer token: {token[:20]}...")
            try:
                # Verify token and extract user info
                payload = jwt_service.verify_token(token)
                request.state.user_id = payload.get("sub")
                request.state.user_role = payload.get("role")
                request.state.token_payload = payload
                print(f"AUTH: Token verified. User ID: {request.state.user_id}, Role: {request.state.user_role}")
            except Exception as e:
                # Token verification failed, but continue without authentication
                print(f"AUTH: Token verification failed: {e}")
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
        """Check if user has required role for the requested route"""
        print(f"MIDDLEWARE: Processing {request.method} {request.url.path}")
        path = request.url.path
        method = request.method.lower()
        
        # Check if route requires specific roles
        route_key = f"{request.method.lower()}:{request.url.path}"
        required_roles = self.route_permissions.get(route_key, [])
        
        import logging
        print(f"ROLE DEBUG: Route key: {route_key}")
        print(f"ROLE DEBUG: Required roles: {required_roles}")
        
        if required_roles:
            user_role = getattr(request.state, 'user_role', None)
            print(f"ROLE DEBUG: User role: {user_role}")
            print(f"ROLE DEBUG: User role in required roles: {user_role in required_roles if user_role else False}")
            if not user_role or user_role not in required_roles:
                print(f"ROLE DEBUG: Access denied - user role '{user_role}' not in required roles {required_roles}")
                raise HTTPException(
                    status_code=401,
                    detail="Authentication required"
                )
        
        response = await call_next(request)
        return response


def create_role_permissions_map() -> dict:
    """
    Create a mapping of routes to required roles
    """
    return {
        # Admin and Moderator routes (using uppercase to match JWT token format)
        "get:/api/v1/dashboard": ["MODERATOR", "ADMIN"],
        
        # Admin-only routes
        "get:/api/v1/admin/users": ["ADMIN"],
        "put:/api/v1/admin/users/{user_id}/role": ["ADMIN"],
        "post:/api/v1/admin/users/{user_id}/suspend": ["ADMIN"],
        "get:/api/v1/admin/analytics": ["ADMIN"],
        
        # Moderator and Admin routes
        "get:/api/v1/admin/reports": ["MODERATOR", "ADMIN"],
        "put:/api/v1/admin/reports/{report_id}/resolve": ["MODERATOR", "ADMIN"],
        "get:/api/v1/admin/moderation": ["MODERATOR", "ADMIN"],
        "post:/api/v1/admin/moderation/{content_id}": ["MODERATOR", "ADMIN"],
        
        # Critic, Moderator, and Admin routes (enhanced review features)
        "post:/api/v1/reviews/featured": ["CRITIC", "MODERATOR", "ADMIN"],
        
        # All authenticated users (examples)
        "post:/api/v1/reviews": ["USER", "CRITIC", "MODERATOR", "ADMIN"],
        "put:/api/v1/reviews/{review_id}": ["USER", "CRITIC", "MODERATOR", "ADMIN"],
        "delete:/api/v1/reviews/{review_id}": ["USER", "CRITIC", "MODERATOR", "ADMIN"],
    }