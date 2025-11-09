"""
API Version middleware for LemonNPie Backend API
"""
from fastapi import Request, Response, HTTPException, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from datetime import datetime
import logging

from app.core.versioning import APIVersionManager, VersionCompatibilityHandler


logger = logging.getLogger(__name__)


class APIVersionMiddleware(BaseHTTPMiddleware):
    """
    Middleware to handle API versioning and compatibility
    """
    
    def __init__(self, app, enable_version_validation: bool = True):
        super().__init__(app)
        self.enable_version_validation = enable_version_validation
    
    async def dispatch(self, request: Request, call_next):
        """Process request with version handling"""
        
        # Skip version handling for non-API routes
        if not request.url.path.startswith('/api/'):
            return await call_next(request)
        
        # Skip version handling for system endpoints
        system_endpoints = ['/api/info', '/api/versions', '/api/migration-guides']
        if any(request.url.path.startswith(endpoint) for endpoint in system_endpoints):
            return await call_next(request)
        
        try:
            # Extract API version from request
            api_version = APIVersionManager.get_version_from_request(request)
            
            # Validate version if enabled
            if self.enable_version_validation and not APIVersionManager.validate_version(api_version):
                return self._create_version_error_response(request, api_version)
            
            # Add version to request state
            request.state.api_version = api_version
            
            # Get version info for headers
            version_info = APIVersionManager.get_version_info(api_version)
            
            # Log version usage for analytics
            logger.info(
                f"API request",
                extra={
                    "api_version": api_version.value if hasattr(api_version, 'value') else str(api_version),
                    "endpoint": request.url.path,
                    "method": request.method,
                    "user_agent": request.headers.get("user-agent", ""),
                    "ip_address": request.client.host if request.client else "unknown"
                }
            )
            
            # Process the request
            response = await call_next(request)
            
            # Add version headers to response
            self._add_version_headers(response, api_version, version_info)
            
            return response
            
        except Exception as e:
            logger.error(f"Error in version middleware: {str(e)}", exc_info=True)
            # Continue processing without version handling on error
            return await call_next(request)
    
    def _create_version_error_response(self, request: Request, api_version) -> JSONResponse:
        """Create error response for unsupported version"""
        supported_versions = [v.value for v in APIVersionManager.VERSIONS.keys()]
        
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "error": "unsupported_api_version",
                "message": f"API version '{api_version}' is not supported",
                "details": {
                    "requested_version": api_version.value if hasattr(api_version, 'value') else str(api_version),
                    "supported_versions": supported_versions,
                    "current_version": APIVersionManager.DEFAULT_VERSION.value,
                    "version_info_endpoint": "/api/versions"
                },
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "path": request.url.path
            },
            headers={
                "X-Supported-API-Versions": ", ".join(supported_versions),
                "X-Current-API-Version": APIVersionManager.DEFAULT_VERSION.value
            }
        )
    
    def _add_version_headers(self, response: Response, api_version, version_info: dict):
        """Add version-related headers to response"""
        # Basic version headers
        response.headers["X-API-Version"] = api_version.value if hasattr(api_version, 'value') else str(api_version)
        response.headers["X-API-Version-Status"] = version_info["status"].value if hasattr(version_info["status"], 'value') else str(version_info["status"])
        
        # Add deprecation headers if applicable
        if version_info["status"].value == "deprecated":
            response.headers["Deprecation"] = "true"
            response.headers["Warning"] = f'299 - "API version {api_version.value} is deprecated"'
            
            if version_info.get("sunset_date"):
                response.headers["Sunset"] = version_info["sunset_date"]
        
        # Add supported versions header
        supported_versions = [v.value for v in APIVersionManager.VERSIONS.keys()]
        response.headers["X-Supported-API-Versions"] = ", ".join(supported_versions)
        
        # Add links to version information
        response.headers["Link"] = (
            f'</api/versions>; rel="version-info", '
            f'</api/migration-guides>; rel="migration-guides"'
        )


class ResponseTransformMiddleware(BaseHTTPMiddleware):
    """
    Middleware to transform responses for backward compatibility
    """
    
    async def dispatch(self, request: Request, call_next):
        """Transform response based on API version"""
        
        # Process the request
        response = await call_next(request)
        
        # Skip transformation for non-API routes or non-JSON responses
        if (not request.url.path.startswith('/api/') or 
            not response.headers.get("content-type", "").startswith("application/json")):
            return response
        
        # Get API version from request state
        api_version = getattr(request.state, 'api_version', APIVersionManager.DEFAULT_VERSION)
        
        # Transform response if needed (for future version compatibility)
        # Currently v1 is the only version, so no transformation needed
        
        return response


def create_version_middleware(enable_validation: bool = True) -> APIVersionMiddleware:
    """
    Factory function to create version middleware with configuration
    """
    return APIVersionMiddleware(None, enable_validation)