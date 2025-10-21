"""
Custom exceptions for LemonNPie Backend API
"""
from typing import Any, Dict, Optional
from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from datetime import datetime
import structlog

logger = structlog.get_logger(__name__)


class LemonPieException(Exception):
    """Base exception for LemonNPie API"""
    
    def __init__(
        self, 
        message: str, 
        status_code: int = 500, 
        details: Optional[Dict[str, Any]] = None
    ):
        self.message = message
        self.status_code = status_code
        self.details = details or {}
        super().__init__(self.message)


class AuthenticationError(LemonPieException):
    """Authentication required"""
    
    def __init__(self, message: str = "Authentication required"):
        super().__init__(message, 401)


class AuthorizationError(LemonPieException):
    """Insufficient permissions"""
    
    def __init__(self, message: str = "Insufficient permissions"):
        super().__init__(message, 403)


class ValidationError(LemonPieException):
    """Validation error"""
    
    def __init__(self, message: str, details: Optional[Dict] = None):
        super().__init__(message, 422, details)


class NotFoundError(LemonPieException):
    """Resource not found"""
    
    def __init__(self, message: str = "Resource not found"):
        super().__init__(message, 404)


class ConflictError(LemonPieException):
    """Resource conflict"""
    
    def __init__(self, message: str = "Resource already exists"):
        super().__init__(message, 409)


class RateLimitError(LemonPieException):
    """Rate limit exceeded"""
    
    def __init__(self, message: str = "Rate limit exceeded"):
        super().__init__(message, 429)


async def lemonnpie_exception_handler(request: Request, exc: LemonPieException):
    """Handle custom LemonNPie exceptions"""
    
    logger.error(
        "LemonNPie exception occurred",
        error=exc.__class__.__name__,
        message=exc.message,
        status_code=exc.status_code,
        details=exc.details,
        path=request.url.path,
    )
    
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.__class__.__name__.lower().replace("error", ""),
            "message": exc.message,
            "details": exc.details,
            "timestamp": datetime.utcnow().isoformat(),
            "path": request.url.path,
        }
    )


async def http_exception_handler(request: Request, exc: HTTPException):
    """Handle FastAPI HTTP exceptions"""
    
    logger.error(
        "HTTP exception occurred",
        status_code=exc.status_code,
        detail=exc.detail,
        path=request.url.path,
    )
    
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": "http_error",
            "message": exc.detail,
            "details": {},
            "timestamp": datetime.utcnow().isoformat(),
            "path": request.url.path,
        }
    )


async def general_exception_handler(request: Request, exc: Exception):
    """Handle general exceptions"""
    
    logger.error(
        "Unexpected exception occurred",
        error=exc.__class__.__name__,
        message=str(exc),
        path=request.url.path,
        exc_info=True,
    )
    
    return JSONResponse(
        status_code=500,
        content={
            "error": "internal_server_error",
            "message": "An unexpected error occurred",
            "details": {},
            "timestamp": datetime.utcnow().isoformat(),
            "path": request.url.path,
        }
    )