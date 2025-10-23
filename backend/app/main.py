"""
Main FastAPI application for LemonNPie Backend API
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from contextlib import asynccontextmanager
import structlog
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from app.core.config import settings
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
        docs_url="/docs" if settings.DEBUG else None,
        redoc_url="/redoc" if settings.DEBUG else None,
        lifespan=lifespan,
    )
    
    # Add security middleware (order matters)
    app.add_middleware(SecurityMiddleware)
    app.add_middleware(InputValidationMiddleware)
    app.add_middleware(AuthMiddleware)
    app.add_middleware(
        RoleBasedAccessMiddleware, 
        route_permissions=create_role_permissions_map()
    )
    app.add_middleware(LoggingMiddleware)
    
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
    
    # Health check endpoint
    @app.get("/health")
    async def health_check():
        """Health check endpoint"""
        return {
            "status": "healthy",
            "service": settings.APP_NAME,
            "version": settings.APP_VERSION,
        }
    
    # Root endpoint
    @app.get("/")
    async def root():
        """Root endpoint"""
        return {
            "message": "Welcome to LemonNPie Backend API",
            "version": settings.APP_VERSION,
            "docs": "/docs" if settings.DEBUG else "Documentation not available in production",
        }
    
    return app


# Create the application instance
app = create_app()