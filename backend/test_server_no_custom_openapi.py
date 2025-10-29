#!/usr/bin/env python3
"""
Test server without custom OpenAPI function
"""
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import routers
from app.api.v1.auth import router as auth_router
from app.api.v1.movies import router as movies_router
from app.api.v1.reviews import router as reviews_router
from app.api.v1.users import router as users_router
from app.api.v1.uploads import router as uploads_router
from app.api.v1.admin import router as admin_router
from app.api.v1.notifications import router as notifications_router
from app.api.v1.analytics import router as analytics_router

def create_test_app():
    """Create test app without custom OpenAPI"""
    app = FastAPI(
        title="LemonNPie Test API",
        version="1.0.0",
        description="Test API without custom OpenAPI"
    )
    
    # Basic CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Include routers
    app.include_router(auth_router, prefix="/api/v1")
    app.include_router(movies_router, prefix="/api/v1")
    app.include_router(reviews_router, prefix="/api/v1")
    app.include_router(users_router, prefix="/api/v1")
    app.include_router(uploads_router, prefix="/api/v1")
    app.include_router(admin_router, prefix="/api/v1")
    app.include_router(notifications_router, prefix="/api/v1")
    app.include_router(analytics_router, prefix="/api/v1")
    
    @app.get("/health")
    async def health_check():
        return {"status": "ok"}
    
    return app

if __name__ == "__main__":
    print("🚀 Starting test server without custom OpenAPI...")
    app = create_test_app()
    
    # Print route info
    user_routes = [route for route in app.routes 
                  if hasattr(route, 'path') and '/users' in route.path]
    print(f"👥 User routes registered: {len(user_routes)}")
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8001,  # Different port to avoid conflict
        reload=False
    )