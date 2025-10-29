#!/usr/bin/env python3
"""
Test main app without custom OpenAPI
"""
from fastapi import FastAPI
from app.api.v1.auth import router as auth_router
from app.api.v1.movies import router as movies_router
from app.api.v1.reviews import router as reviews_router
from app.api.v1.users import router as users_router
from app.api.v1.uploads import router as uploads_router
from app.api.v1.admin import router as admin_router
from app.api.v1.notifications import router as notifications_router
from app.api.v1.analytics import router as analytics_router

def create_test_app():
    """Create a test app similar to main but without custom OpenAPI"""
    app = FastAPI(title="Test App")
    
    try:
        # Include API routes in same order as main
        app.include_router(auth_router, prefix="/api/v1")
        app.include_router(movies_router, prefix="/api/v1")
        app.include_router(reviews_router, prefix="/api/v1")
        app.include_router(users_router, prefix="/api/v1")
        app.include_router(uploads_router, prefix="/api/v1")
        app.include_router(admin_router, prefix="/api/v1")
        app.include_router(notifications_router, prefix="/api/v1")
        app.include_router(analytics_router, prefix="/api/v1")
        
        print("✅ All routers included successfully")
        
        # Check total routes
        print(f"📊 App has {len(app.routes)} routes")
        
        # Check user routes specifically
        user_routes = [route for route in app.routes 
                      if hasattr(route, 'path') and '/users' in route.path]
        print(f"👥 User routes: {len(user_routes)}")
        
        return app
        
    except Exception as e:
        print(f"❌ Error creating test app: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    print("🔍 Testing main app configuration...")
    app = create_test_app()
    
    if app:
        print("\n🎉 Test app created successfully!")
        
        # Try to get OpenAPI schema (default FastAPI)
        try:
            openapi_schema = app.openapi()
            paths = openapi_schema.get("paths", {})
            user_paths = [path for path in paths.keys() if "users" in path]
            print(f"\n📚 OpenAPI paths with 'users': {len(user_paths)}")
            for path in sorted(user_paths):
                methods = list(paths[path].keys())
                print(f"  {path} - {methods}")
                
            # Check specifically for privacy settings
            privacy_paths = [path for path in paths.keys() if "privacy" in path]
            print(f"\n🔒 Privacy-related paths: {len(privacy_paths)}")
            for path in privacy_paths:
                methods = list(paths[path].keys())
                print(f"  {path} - {methods}")
                
        except Exception as e:
            print(f"❌ Error getting OpenAPI schema: {e}")
            import traceback
            traceback.print_exc()
    else:
        print("❌ Failed to create test app")