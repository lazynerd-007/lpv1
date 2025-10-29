#!/usr/bin/env python3
"""
Test the login endpoint specifically to verify it accepts POST requests
"""
import sys
import traceback
from fastapi import FastAPI
from fastapi.testclient import TestClient

def test_login_endpoint():
    """Test that the login endpoint accepts POST requests"""
    try:
        print("Testing login endpoint configuration...")
        
        # Create a minimal FastAPI app with just the auth router
        app = FastAPI()
        
        # Import and include the auth router
        from app.api.v1.auth import router as auth_router
        app.include_router(auth_router, prefix="/api/v1")
        
        print("✓ Auth router included successfully")
        
        # Create test client
        client = TestClient(app)
        
        # Check available routes
        routes = []
        for route in app.routes:
            if hasattr(route, 'methods') and hasattr(route, 'path'):
                if '/auth/login' in route.path:
                    routes.append(f"  - {route.methods} {route.path}")
        
        print("Available login routes:")
        for route in routes:
            print(route)
        
        # Test OPTIONS request (CORS preflight)
        try:
            response = client.options("/api/v1/auth/login")
            print(f"✓ OPTIONS /api/v1/auth/login: {response.status_code}")
        except Exception as e:
            print(f"  OPTIONS request failed: {e}")
        
        # Test POST request with invalid data (should get validation error, not 405)
        try:
            response = client.post("/api/v1/auth/login", json={})
            print(f"✓ POST /api/v1/auth/login (empty): {response.status_code}")
            if response.status_code == 405:
                print("  ✗ ERROR: Getting 405 Method Not Allowed - this indicates the route is not properly configured")
                return False
            else:
                print("  ✓ Route accepts POST requests (got validation error as expected)")
        except Exception as e:
            print(f"  POST request failed: {e}")
            return False
        
        # Test with proper structure but invalid credentials
        try:
            response = client.post("/api/v1/auth/login", json={
                "email": "test@example.com",
                "password": "wrongpassword"
            })
            print(f"✓ POST /api/v1/auth/login (invalid creds): {response.status_code}")
            if response.status_code == 405:
                print("  ✗ ERROR: Getting 405 Method Not Allowed")
                return False
        except Exception as e:
            print(f"  POST request with credentials failed: {e}")
        
        return True
        
    except Exception as e:
        print(f"✗ Login endpoint test failed: {e}")
        traceback.print_exc()
        return False

def main():
    """Test login endpoint"""
    success = test_login_endpoint()
    if success:
        print("\n✓ Login endpoint test passed - route accepts POST requests")
    else:
        print("\n✗ Login endpoint test failed - route configuration issue")
        sys.exit(1)

if __name__ == "__main__":
    main()