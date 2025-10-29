#!/usr/bin/env python3
"""
Detailed test for users router to identify the specific function causing FastAPI error
"""
import sys
import traceback
from fastapi import FastAPI

def test_individual_endpoints():
    """Test each endpoint individually to isolate the problematic one"""
    
    # Import the router
    try:
        from app.api.v1.users import router
        print("✓ Users router imported successfully")
    except Exception as e:
        print(f"✗ Failed to import users router: {e}")
        traceback.print_exc()
        return
    
    # Create a test app and try to include the router
    app = FastAPI()
    
    try:
        app.include_router(router)
        print("✓ Users router included successfully")
    except Exception as e:
        print(f"✗ Failed to include users router: {e}")
        traceback.print_exc()
        return
    
    # Try to access the routes to trigger the error
    try:
        routes = app.routes
        print(f"✓ Found {len(routes)} routes")
        
        for route in routes:
            if hasattr(route, 'path') and hasattr(route, 'methods'):
                print(f"  - {route.methods} {route.path}")
                
    except Exception as e:
        print(f"✗ Error accessing routes: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    test_individual_endpoints()