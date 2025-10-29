#!/usr/bin/env python3
"""
Test reviews router in isolation
"""
import sys
import traceback
from fastapi import FastAPI

def test_reviews_only():
    """Test reviews router alone"""
    try:
        print("Testing Reviews router alone...")
        
        # Create a test FastAPI app
        app = FastAPI()
        
        # Import and add reviews router
        from app.api.v1.reviews import router as reviews_router
        app.include_router(reviews_router, prefix="/api/v1")
        print("✓ Reviews router works alone")
        
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
        print(f"✗ Reviews router failed: {e}")
        traceback.print_exc()
        return False

def main():
    """Test reviews router"""
    test_reviews_only()

if __name__ == "__main__":
    main()