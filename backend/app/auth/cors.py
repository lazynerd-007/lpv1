"""
CORS configuration for LemonNPie Backend API
"""
from typing import List
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI

from app.core.config import settings


def setup_cors(app: FastAPI) -> None:
    """
    Configure CORS middleware for the FastAPI application
    """
    
    # Development origins (should be configured via environment variables)
    allowed_origins = settings.ALLOWED_ORIGINS
    
    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=allowed_origins,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],
        allow_headers=[
            "Accept",
            "Accept-Language",
            "Content-Language",
            "Content-Type",
            "Authorization",
            "X-Requested-With",
            "X-CSRF-Token",
            "Cache-Control",
            "Pragma",
        ],
        expose_headers=[
            "X-RateLimit-Limit",
            "X-RateLimit-Remaining", 
            "X-RateLimit-Reset",
            "Retry-After",
        ],
        max_age=86400,  # 24 hours
    )


def get_cors_origins() -> List[str]:
    """
    Get allowed CORS origins based on environment
    """
    if settings.DEBUG:
        # Development origins
        return [
            "http://localhost:3000",
            "http://localhost:5173",
            "http://localhost:8080",
            "http://127.0.0.1:3000",
            "http://127.0.0.1:5173",
            "http://127.0.0.1:8080",
        ]
    else:
        # Production origins (should be configured via environment variables)
        return settings.ALLOWED_ORIGINS


def validate_origin(origin: str) -> bool:
    """
    Validate if an origin is allowed
    """
    allowed_origins = get_cors_origins()
    
    # Allow exact matches
    if origin in allowed_origins:
        return True
    
    # Allow subdomain matches for production domains
    if not settings.DEBUG:
        for allowed_origin in allowed_origins:
            if allowed_origin.startswith("https://") and origin.endswith(allowed_origin[8:]):
                return True
    
    return False