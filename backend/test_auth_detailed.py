#!/usr/bin/env python3
"""
Detailed test for auth router to identify problematic endpoint
"""
import sys
import traceback
from fastapi import FastAPI

def test_auth_router():
    """Test auth router by including it in a FastAPI app"""
    try:
        print("Testing Auth Router...")
        
        # Import the router
        from app.api.v1.auth import router as auth_router
        print("✓ Auth router imported successfully")
        
        # Create a test FastAPI app
        app = FastAPI()
        
        # Include the router
        app.include_router(auth_router, prefix="/api/v1")
        print("✓ Auth router included successfully")
        
        # Get all routes
        routes = []
        for route in app.routes:
            if hasattr(route, 'methods') and hasattr(route, 'path'):
                routes.append(f"  - {route.methods} {route.path}")
        
        print(f"✓ Found {len(routes)} routes")
        for route in routes:
            print(route)
            
        return True
        
    except Exception as e:
        print(f"✗ Auth Router - FAILED: {e}")
        traceback.print_exc()
        return False

def main():
    """Test auth router"""
    success = test_auth_router()
    
    if success:
        print("\n✓ Auth router test completed successfully!")
    else:
        print("\n✗ Auth router test failed!")

if __name__ == "__main__":
    main()