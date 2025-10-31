#!/usr/bin/env python3
"""
Test version of main server without Redis dependency
"""
import uvicorn
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

# Import the routers
from app.api.v1.auth import router as auth_router
from app.api.v1.movies import router as movies_router
from app.api.v1.reviews import router as reviews_router

# Import database initialization
from app.db.database import init_db, close_db, create_tables

# Import Redis initialization (use mock for testing)
from app.cache.mock_redis import init_mock_redis, close_mock_redis

# Import settings
from app.core.config import settings


@asynccontextmanager
async def test_lifespan(app: FastAPI):
    """Test application lifespan events with Redis and database"""
    # Startup
    print("Starting test server...")
    
    # Initialize database
    try:
        await init_db()
        print("Database initialized")
        
        # Create tables if they don't exist
        await create_tables()
        print("Database tables created/verified")
    except Exception as e:
        print(f"Database initialization failed: {e}")
        print("Continuing without database...")
    
    # Initialize Mock Redis
    try:
        await init_mock_redis()
        print("Mock Redis initialized")
    except Exception as e:
        print(f"Mock Redis initialization failed: {e}")
        print("Continuing without Redis...")
    
    yield
    
    # Shutdown
    print("Shutting down test server...")
    
    # Close Mock Redis connections
    try:
        await close_mock_redis()
        print("Mock Redis connections closed")
    except Exception as e:
        print(f"Mock Redis close failed: {e}")
    
    # Close database connections
    try:
        await close_db()
        print("Database connections closed")
    except Exception as e:
        print(f"Database close failed: {e}")


def create_test_app() -> FastAPI:
    """Create test FastAPI application without Redis"""
    
    app = FastAPI(
        title="Test LemonNPie API",
        version="1.0.0",
        description="Test Backend API for LemonNPie",
        lifespan=test_lifespan,
    )
    
    # Add CORS middleware with explicit configuration
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://localhost:5173",  # Frontend dev server
            "http://localhost:3000",  # Alternative frontend port
            "http://127.0.0.1:5173",
            "http://127.0.0.1:3000",
            "*"  # Allow all for testing
        ],
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
        allow_headers=["*"],
        expose_headers=["*"],
    )
    
    # Custom exception handlers to ensure CORS headers are always included
    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(request: Request, exc: StarletteHTTPException):
        response = JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail}
        )
        # Add CORS headers manually
        origin = request.headers.get("origin")
        if origin:
            response.headers["Access-Control-Allow-Origin"] = origin
        else:
            response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Credentials"] = "true"
        response.headers["Access-Control-Expose-Headers"] = "*"
        return response
    
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        # Convert errors to JSON serializable format
        errors = []
        for error in exc.errors():
            errors.append({
                "loc": error.get("loc", []),
                "msg": str(error.get("msg", "")),
                "type": str(error.get("type", ""))
            })
        
        response = JSONResponse(
            status_code=422,
            content={"detail": errors}
        )
        # Add CORS headers manually
        origin = request.headers.get("origin")
        if origin:
            response.headers["Access-Control-Allow-Origin"] = origin
        else:
            response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Credentials"] = "true"
        response.headers["Access-Control-Expose-Headers"] = "*"
        return response
    
    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception):
        response = JSONResponse(
            status_code=500,
            content={"detail": "Internal server error"}
        )
        # Add CORS headers manually
        origin = request.headers.get("origin")
        if origin:
            response.headers["Access-Control-Allow-Origin"] = origin
        else:
            response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Credentials"] = "true"
        response.headers["Access-Control-Expose-Headers"] = "*"
        return response
    
    # Include routers
    app.include_router(auth_router, prefix="/api/v1")
    app.include_router(movies_router, prefix="/api/v1/movies")
    app.include_router(reviews_router, prefix="/api/v1/reviews")
    
    # Test endpoint
    @app.get("/")
    async def root():
        return {"message": "Test LemonNPie API is running", "status": "ok"}
    
    @app.get("/health")
    async def health():
        return {"status": "healthy", "message": "Test server is running"}
    
    return app


if __name__ == "__main__":
    app = create_test_app()
    print("Starting test server on http://localhost:8000")
    print("Available endpoints:")
    print("- GET  /")
    print("- GET  /health")
    print("- POST /api/v1/auth/login")
    print("- GET  /api/v1/auth/me")
    print("- And all other auth, movies, and reviews endpoints...")
    uvicorn.run(app, host="0.0.0.0", port=8000)