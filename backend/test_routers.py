#!/usr/bin/env python3
"""
Test individual routers to isolate the FastAPI response field error
"""
import sys
import traceback
from fastapi import FastAPI

def test_router(router_module, router_name, description):
    """Test importing and adding a router to a FastAPI app"""
    try:
        print(f"Testing {description}...")
        
        # Create a minimal FastAPI app
        app = FastAPI()
        
        # Import the router
        module = __import__(router_module, fromlist=[router_name])
        router = getattr(module, router_name)
        
        # Try to include the router
        app.include_router(router, prefix="/api/v1")
        
        print(f"✓ {description} - SUCCESS")
        return True
    except Exception as e:
        print(f"✗ {description} - FAILED: {str(e)}")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("Testing individual routers to isolate FastAPI error...\n")
    
    # Test each router individually
    test_router("app.api.v1.auth", "router", "Auth Router")
    test_router("app.api.v1.users", "router", "Users Router")
    test_router("app.api.v1.movies", "router", "Movies Router")
    test_router("app.api.v1.reviews", "router", "Reviews Router")
    test_router("app.api.v1.uploads", "router", "Uploads Router")
    test_router("app.api.v1.admin", "router", "Admin Router")
    test_router("app.api.v1.notifications", "router", "Notifications Router")
    test_router("app.api.v1.analytics", "router", "Analytics Router")
    
    print("\nRouter testing complete!")