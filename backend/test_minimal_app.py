#!/usr/bin/env python3
"""
Minimal FastAPI app to test users router
"""
from fastapi import FastAPI
from app.api.v1.users import router as users_router

def create_minimal_app():
    """Create a minimal FastAPI app with just the users router"""
    app = FastAPI(title="Minimal Test App")
    
    try:
        app.include_router(users_router, prefix="/api/v1")
        print("✅ Users router included successfully")
        
        # Check routes
        print(f"📊 App has {len(app.routes)} routes")
        
        user_routes = [route for route in app.routes 
                      if hasattr(route, 'path') and '/users' in route.path]
        print(f"👥 User routes: {len(user_routes)}")
        
        for route in user_routes:
            if hasattr(route, 'path') and hasattr(route, 'methods'):
                print(f"  - {route.path} - {list(route.methods)}")
        
        return app
        
    except Exception as e:
        print(f"❌ Error including users router: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    print("🔍 Testing minimal FastAPI app with users router...")
    app = create_minimal_app()
    
    if app:
        print("\n🎉 Minimal app created successfully!")
        
        # Try to get OpenAPI schema
        try:
            openapi_schema = app.openapi()
            paths = openapi_schema.get("paths", {})
            user_paths = [path for path in paths.keys() if "users" in path]
            print(f"\n📚 OpenAPI paths with 'users': {len(user_paths)}")
            for path in sorted(user_paths):
                methods = list(paths[path].keys())
                print(f"  {path} - {methods}")
                
        except Exception as e:
            print(f"❌ Error getting OpenAPI schema: {e}")
            import traceback
            traceback.print_exc()
    else:
        print("❌ Failed to create minimal app")