"""
Main FastAPI application for LemonNPie Backend API
"""
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from contextlib import asynccontextmanager
import structlog
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
import os

from app.core.config import settings
from app.core.documentation import (
    get_custom_openapi,
    get_swagger_ui_parameters,
    get_redoc_parameters
)
from app.core.versioning import (
    APIVersionManager,
    VersionCompatibilityHandler,
    create_version_info_endpoint
)
from app.middleware.version_middleware import APIVersionMiddleware, ResponseTransformMiddleware
from app.core.logging import configure_logging, LoggingMiddleware, get_logger
from app.core.exceptions import (
    LemonPieException,
    lemonnpie_exception_handler,
    http_exception_handler,
    general_exception_handler,
)
from app.db.database import init_db, close_db
from app.cache.redis import init_redis, close_redis
from app.auth.cors import setup_cors
from app.auth.middleware import AuthMiddleware, RoleBasedAccessMiddleware, create_role_permissions_map
from app.auth.security import SecurityMiddleware, InputValidationMiddleware
from app.auth.rate_limiter import limiter
from app.api.v1.auth import router as auth_router
from app.api.v1.movies import router as movies_router
from app.api.v1.reviews import router as reviews_router
from app.api.v1.users import router as users_router
from app.api.v1.uploads import router as uploads_router
from app.api.v1.admin import router as admin_router
from app.api.v1.notifications import router as notifications_router
from app.api.v1.analytics import router as analytics_router
from app.websocket.endpoints import websocket_endpoint

# Configure logging
configure_logging()
logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    # Startup
    logger.info("Starting LemonNPie Backend API", version=settings.APP_VERSION)
    
    # Initialize database
    await init_db()
    logger.info("Database initialized")
    
    # Initialize Redis
    await init_redis()
    logger.info("Redis initialized")
    
    yield
    
    # Shutdown
    logger.info("Shutting down LemonNPie Backend API")
    
    # Close database connections
    await close_db()
    logger.info("Database connections closed")
    
    # Close Redis connections
    await close_redis()
    logger.info("Redis connections closed")


def create_app() -> FastAPI:
    """Create and configure FastAPI application"""
    
    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        description="Backend API for LemonNPie Nollywood movie review platform",
        docs_url=None,  # We'll create custom docs
        redoc_url=None,  # We'll create custom redoc
        openapi_url="/openapi.json",
        lifespan=lifespan,
    )
    
    # Set up templates
    templates = Jinja2Templates(directory="app/templates")
    
    # Custom OpenAPI schema - TEMPORARILY DISABLED due to route registration issue
    # app.openapi = lambda: get_custom_openapi(app)
    
    # Add security middleware (order matters)
    app.add_middleware(SecurityMiddleware)
    app.add_middleware(InputValidationMiddleware)
    app.add_middleware(AuthMiddleware)
    app.add_middleware(
        RoleBasedAccessMiddleware, 
        route_permissions=create_role_permissions_map()
    )
    app.add_middleware(LoggingMiddleware)
    
    # Add version middleware
    app.add_middleware(APIVersionMiddleware, enable_version_validation=True)
    app.add_middleware(ResponseTransformMiddleware)
    
    # Setup CORS
    setup_cors(app)
    
    # Trusted host middleware (security)
    if not settings.DEBUG:
        app.add_middleware(
            TrustedHostMiddleware,
            allowed_hosts=["localhost", "127.0.0.1", "*.lemonnpie.com"]
        )
    
    # Rate limiting
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
    
    # Exception handlers
    app.add_exception_handler(LemonPieException, lemonnpie_exception_handler)
    app.add_exception_handler(HTTPException, http_exception_handler)
    app.add_exception_handler(Exception, general_exception_handler)
    
    # Include API routes
    app.include_router(auth_router, prefix="/api/v1")
    app.include_router(movies_router, prefix="/api/v1")
    app.include_router(reviews_router, prefix="/api/v1")
    app.include_router(users_router, prefix="/api/v1")
    app.include_router(uploads_router, prefix="/api/v1")
    app.include_router(admin_router, prefix="/api/v1")
    app.include_router(notifications_router, prefix="/api/v1")
    app.include_router(analytics_router, prefix="/api/v1")
    
    # WebSocket endpoint for real-time notifications
    app.websocket("/ws/notifications")(websocket_endpoint)
    
    # Health check endpoint
    @app.get("/health")
    async def health_check():
        """Health check endpoint"""
        return {
            "status": "healthy",
            "service": settings.APP_NAME,
            "version": settings.APP_VERSION,
        }
    
    # Custom documentation endpoints
    @app.get("/docs", response_class=HTMLResponse, include_in_schema=False)
    async def custom_swagger_ui_html(request: Request):
        """Custom Swagger UI documentation"""
        return templates.TemplateResponse("swagger_ui.html", {
            "request": request,
            "title": f"{settings.APP_NAME} - API Documentation",
            "openapi_url": "/openapi.json",
            "api_version": settings.APP_VERSION,
            "environment": "Development" if settings.DEBUG else "Production"
        })
    
    @app.get("/redoc", response_class=HTMLResponse, include_in_schema=False)
    async def custom_redoc_html(request: Request):
        """Custom ReDoc documentation"""
        return templates.TemplateResponse("redoc.html", {
            "request": request,
            "title": f"{settings.APP_NAME} - API Documentation",
            "openapi_url": "/openapi.json",
            "api_version": settings.APP_VERSION,
            "environment": "Development" if settings.DEBUG else "Production"
        })
    
    # API Info endpoint
    @app.get("/api/info", tags=["System"])
    async def api_info():
        """
        Get API information and status
        
        Returns comprehensive information about the API including:
        - Version information
        - Available endpoints
        - System status
        - Documentation links
        """
        return {
            "name": settings.APP_NAME,
            "version": settings.APP_VERSION,
            "description": "Backend API for LemonNPie Nollywood movie review platform",
            "environment": "development" if settings.DEBUG else "production",
            "documentation": {
                "swagger_ui": "/docs",
                "redoc": "/redoc",
                "openapi_schema": "/openapi.json"
            },
            "endpoints": {
                "authentication": "/api/v1/auth",
                "users": "/api/v1/users",
                "movies": "/api/v1/movies",
                "reviews": "/api/v1/reviews",
                "admin": "/api/v1/admin",
                "uploads": "/api/v1/uploads",
                "notifications": "/api/v1/notifications",
                "analytics": "/api/v1/analytics"
            },
            "websocket": {
                "notifications": "/ws/notifications"
            },
            "features": [
                "JWT Authentication",
                "Role-based Access Control",
                "Rate Limiting",
                "Full-text Search",
                "Real-time Notifications",
                "File Upload with Cloudinary",
                "Analytics Tracking",
                "Content Moderation"
            ],
            "status": "operational"
        }
    
    # API Versions endpoint
    @app.get("/api/versions", tags=["System"])
    async def get_api_versions():
        """
        Get API version information and migration guides
        
        Returns comprehensive information about:
        - All supported API versions
        - Version status and lifecycle
        - Migration guides between versions
        - Deprecation notices
        - Compatibility information
        """
        return create_version_info_endpoint()()
    
    # Migration guides endpoint
    @app.get("/api/migration-guides", tags=["System"])
    async def get_migration_guides():
        """
        Get API migration guides
        
        Returns detailed migration guides for upgrading between API versions,
        including:
        - Breaking changes and their impact
        - Step-by-step migration instructions
        - Code examples for common scenarios
        - Testing and rollback strategies
        """
        from app.docs.migration_guides import MigrationGuides
        
        return {
            "guides": MigrationGuides.get_all_guides(),
            "summary": MigrationGuides.get_guide_summary(),
            "support": {
                "documentation": "https://docs.lemonnpie.com/api/migration",
                "contact": "api-support@lemonnpie.com",
                "community": "https://community.lemonnpie.com/api"
            }
        }
    
    # Specific migration guide endpoint
    @app.get("/api/migration-guides/{from_version}/to/{to_version}", tags=["System"])
    async def get_specific_migration_guide(from_version: str, to_version: str):
        """
        Get specific migration guide between two versions
        
        Returns detailed migration guide for upgrading from one API version to another.
        """
        from app.docs.migration_guides import MigrationGuides
        
        guide = MigrationGuides.get_migration_guide(from_version, to_version)
        if not guide:
            raise HTTPException(
                status_code=404,
                detail=f"Migration guide from {from_version} to {to_version} not found"
            )
        
        return guide
    
    # Documentation index endpoint
    @app.get("/api/docs", tags=["System"])
    async def get_documentation_index():
        """
        Get comprehensive API documentation index
        
        Returns a structured overview of all available documentation,
        including guides, references, and support resources.
        """
        from app.docs.api_documentation import APIDocumentation
        
        return APIDocumentation.get_documentation_index()
    
    # Documentation search endpoint
    @app.get("/api/docs/search", tags=["System"])
    async def search_documentation(q: str):
        """
        Search through API documentation
        
        Search for specific topics, endpoints, or concepts in the documentation.
        """
        from app.docs.api_documentation import APIDocumentation
        
        if not q or len(q.strip()) < 2:
            raise HTTPException(
                status_code=400,
                detail="Search query must be at least 2 characters long"
            )
        
        results = APIDocumentation.search_documentation(q.strip())
        
        return {
            "query": q,
            "results": results,
            "total": len(results)
        }
    
    # Root endpoint
    @app.get("/")
    async def root():
        """
        Root endpoint - API welcome message
        
        Returns basic information about the API and links to documentation.
        """
        return {
            "message": "Welcome to LemonNPie Backend API 🍋🥧",
            "version": settings.APP_VERSION,
            "description": "Comprehensive RESTful API for Nollywood movie reviews and discovery",
            "documentation": {
                "interactive": "/docs",
                "static": "/redoc",
                "info": "/api/info"
            },
            "status": "operational",
            "environment": "development" if settings.DEBUG else "production"
        }
    
    return app


# Create the application instance
app = create_app()