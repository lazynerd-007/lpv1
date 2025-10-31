#!/usr/bin/env python3
"""
Test version of main app with proper database initialization
"""
import asyncio
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import database functions
from app.db.database import init_db, create_tables

# Import all the routers
from app.api.v1.auth import router as auth_router
from app.api.v1.users import router as users_router
from app.api.v1.movies import router as movies_router
from app.api.v1.reviews import router as reviews_router
from app.api.v1.admin import router as admin_router
from app.api.v1.analytics import router as analytics_router

def create_app():
    """Create FastAPI application with proper database initialization."""
    app = FastAPI(
        title="LemonNPie API - Test Version",
        description="Movie review and social platform API - Test with DB",
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc"
    )
    
    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:3000", "http://127.0.0.1:3000", "http://localhost:5173", "http://127.0.0.1:5173"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Include all routers
    app.include_router(auth_router, prefix="/api/v1/auth", tags=["Authentication"])
    app.include_router(users_router, prefix="/api/v1/users", tags=["Users"])
    app.include_router(movies_router, prefix="/api/v1/movies", tags=["Movies"])
    app.include_router(reviews_router, prefix="/api/v1/reviews", tags=["Reviews"])
    app.include_router(admin_router, prefix="/api/v1/admin", tags=["Admin"])
    app.include_router(analytics_router, prefix="/api/v1/analytics", tags=["Analytics"])
    
    @app.get("/health")
    async def health_check():
        """Health check endpoint."""
        return {"status": "healthy", "message": "API is running"}
    
    return app

async def startup():
    """Initialize database and create tables."""
    print("🔧 Initializing database...")
    await init_db()
    print("📊 Creating database tables...")
    await create_tables()
    print("✅ Database initialization complete!")

if __name__ == "__main__":
    # Initialize database first
    asyncio.run(startup())
    
    app = create_app()
    
    # Print route information
    print(f"🚀 Total routes: {len(app.routes)}")
    
    # Count user routes
    user_routes = [route for route in app.routes if hasattr(route, 'path') and '/users' in route.path]
    print(f"👤 User routes: {len(user_routes)}")
    
    for route in user_routes:
        if hasattr(route, 'methods'):
            print(f"  {route.path} - {list(route.methods)}")
    
    print("🌟 Starting server on http://0.0.0.0:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000)